import os
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/mercadopago/webhook")
async def webhook_mercadopago(request: Request, db: Session = Depends(get_db)):

    payload = await request.json()

    pagamento_id = payload.get("id")
    novo_status = payload.get("status")
    status_detail = payload.get("status_detail")
    external_resource_url = payload.get("transaction_details", {}).get("external_resource_url")

    if not pagamento_id:
        raise HTTPException(status_code=400, detail="ID do pagamento não fornecido.")

    pagamento = db.query(models.Pagamento).filter(models.Pagamento.id == pagamento_id).first()
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado.")
    
    pagamento.status = novo_status
    if external_resource_url:
        pagamento.link_pagamento = external_resource_url

    db.commit()
    db.refresh(pagamento)

    return {
        "message": "Pagamento atualizado com sucesso.", 
        "pagamento": {
        "id": pagamento.id,
        "status": pagamento.status,
        "link_pagamento": pagamento.link_pagamento
    }}
