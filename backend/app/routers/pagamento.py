# Modified payment router with authentication
import os
import requests
import uuid 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import SessionLocal
from pydantic import BaseModel
from .. import models
from ..config import MERCADO_PAGO_TOKEN, MERCADO_PAGO_URL
from ..auth import get_current_active_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PaymentUpdateRequest(BaseModel):
    transaction_amount: float

@router.post("/pagamentos")
def criar_pagamento(
    cliente_id: int,
    valor: float,
    tipo_pagamento: str,  
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)  
):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        cliente = models.Cliente(
            id=cliente_id,
            nome="Cliente Teste",
            sobrenome="Zivane",
            email="teste@exemplo.com",
            cpf_cnpj="19119119100",  
            endereco="Rua Teste, 123"
        )
        db.add(cliente)
        db.commit()
        db.refresh(cliente)

    tipo_reg = db.query(models.TipoPagamento).filter(models.TipoPagamento.nome.ilike(tipo_pagamento)).first()
    if not tipo_reg:
        raise HTTPException(status_code=400, detail="Tipo de pagamento inválido.")

    novo_pagamento = models.Pagamento(
        cliente_id=cliente_id,
        valor=valor,
        tipo_pagamento_id=tipo_reg.id,
        status="pendente",
        user_id=current_user.id  # Track which user created the payment
    )
    db.add(novo_pagamento)
    db.commit()
    db.refresh(novo_pagamento)

    idempotency_key = str(uuid.uuid4())
    headers = {
        "Authorization": f"Bearer {MERCADO_PAGO_TOKEN}",
        "Content-Type": "application/json",
        "X-Idempotency-Key": idempotency_key
    }
    body = {
        "transaction_amount": valor,
        "description": "Pagamento Teste",
        "payment_method_id": "pix" if tipo_pagamento.lower() == "pix" else "bolbradesco",
        "payer": {
            "email": cliente.email,
            "first_name": cliente.nome,
        }
    }
    
    if tipo_pagamento.lower() == "boleto":
        body["payer"]["last_name"] = "Zivane"
        body["payer"]["identification"] = {
            "type": "CPF", 
            "number": "19119119100"  
        }
        body["payer"]["address"] = {
            "zip_code": "88000000",
            "street_name": "Rua da Abobrinha",
            "street_number": "3039",
            "neighborhood": "Parque Patricios",
            "city": "Buenos Aires",
            "federal_unit": "BA"
        }
    
    response = requests.post(MERCADO_PAGO_URL, json=body, headers=headers)
    if response.status_code not in [200, 201]:
        novo_pagamento.status = "falhou"
        db.commit()
        raise HTTPException(status_code=400, detail=f"Erro ao criar pagamento: {response.text}")
    
    mp_data = response.json()
    novo_pagamento.metadados = mp_data
    novo_pagamento.link_pagamento = mp_data.get("transaction_details", {}).get("external_resource_url", None)
    db.commit()
    db.refresh(novo_pagamento)
    
    return {
        "message": "Pagamento criado com sucesso.",
        "pagamento": {
            "id": novo_pagamento.id,
            "status": novo_pagamento.status,
            "link_pagamento": novo_pagamento.link_pagamento,
            "metadados": novo_pagamento.metadados
        }
    }

@router.get("/pagamentos")
def listar_pagamentos(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user) 
):
    if current_user.is_admin:
        pagamentos = db.query(models.Pagamento).all()
    else:
        pagamentos = db.query(models.Pagamento).filter(models.Pagamento.user_id == current_user.id).all()
    return {"pagamentos": pagamentos}

@router.get("/pagamentos/{pagamento_id}")
def obter_pagamento(
    pagamento_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)  # Added authentication
):
    pagamento = db.query(models.Pagamento).filter(models.Pagamento.id == pagamento_id).first()
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado.")
    
    # Check if user has access to this payment
    if not current_user.is_admin and pagamento.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado a este pagamento.")
    
    tipo_nome = None
    if pagamento.tipo_pagamento:
        tipo_nome = pagamento.tipo_pagamento.nome

    return {
        "id": pagamento.id,
        "cliente_id": pagamento.cliente_id,
        "valor": pagamento.valor,
        "tipo_pagamento": tipo_nome or pagamento.tipo_pagamento_id,
        "status": pagamento.status,
        "link_pagamento": pagamento.link_pagamento,
        "metadados": pagamento.metadados,
    }


@router.put("/pagamentos/{pagamento_id}/quitar")
def atualizar_status_pagamento(
    pagamento_id: int,
    approval_data: PaymentUpdateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    pagamento = db.query(models.Pagamento).filter(models.Pagamento.id == pagamento_id).first()
    if not pagamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado.")
    
    if pagamento.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Apenas o usuário que criou o pagamento pode atualizá-lo.")
    
    new_status = "approved"
    
    url = f"{MERCADO_PAGO_URL}/{pagamento_id}"
    
    headers = {
        "Authorization": f"Bearer {MERCADO_PAGO_TOKEN}",
        "Content-Type": "application/json",
        "x-idempotency-key": str(uuid.uuid4())
    }
    
    body = {
        "status": new_status,
        "transaction_amount": approval_data.transaction_amount
    }
    
    response = requests.put(url, json=body, headers=headers)
    
    if response.status_code not in [200, 201]:
        pagamento.status = "falhou"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Erro ao atualizar pagamento no Mercado Pago: {response.text}"
        )
    

    pagamento.status = new_status
    db.commit()
    db.refresh(pagamento)
    
    return {
        "message": "Pagamento atualizado para approved com sucesso.",
        "pagamento": {
            "id": pagamento.id,
            "status": pagamento.status,
            "link_pagamento": pagamento.link_pagamento,
            "metadados": pagamento.metadados,
        }
    }