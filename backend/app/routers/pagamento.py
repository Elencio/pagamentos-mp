import os
import requests
import uuid 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
from ..config import MERCADO_PAGO_TOKEN

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pagamentos")
def criar_pagamento(
    cliente_id: int,
    valor: float,
    tipo_pagamento: str,  
    db: Session = Depends(get_db)
):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        cliente = models.Cliente(
            id=cliente_id,
            nome="Cliente Teste",
            sobrenome="Zivane",
            email="teste@exemplo.com",
            cpf_cnpj="19119119100",  # para PIX, se necessário
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
        status="pendente"
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
    print("Payload para boleto:", body)
    
    url = "https://api.mercadopago.com/v1/payments"
    
    response = requests.post(url, json=body, headers=headers)
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
def listar_pagamentos(db: Session = Depends(get_db)):
    pagamentos = db.query(models.Pagamento).all()
    return {"pagamentos": pagamentos}

@router.get("/pagamentos/{pagamento_id}")
def obter_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    pagamento = db.query(models.Pagamento).filter(models.Pagamento.id == pagamento_id).first()
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado.")
    
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
