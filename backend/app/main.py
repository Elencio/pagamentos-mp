import os
from fastapi import FastAPI
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from . import models


Base.metadata.create_all(bind=engine)

def seed_tipopagamentos():
    db: Session = SessionLocal()
    try:
        pix = db.query(models.TipoPagamento).filter(models.TipoPagamento.nome.ilike("PIX")).first()
        if not pix:
            pix = models.TipoPagamento(nome="PIX")
            db.add(pix)
        
        boleto = db.query(models.TipoPagamento).filter(models.TipoPagamento.nome.ilike("Boleto")).first()
        if not boleto:
            boleto = models.TipoPagamento(nome="Boleto")
            db.add(boleto)
        
        db.commit()
    finally:
        db.close()

seed_tipopagamentos()

app = FastAPI(title="API de Pagamentos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pagamento.router, prefix="/api", tags=["pagamentos"])

@app.get("/")
def root():
    return {"message": "API de Pagamentos funcionando!"}