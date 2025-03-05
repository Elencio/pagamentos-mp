from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal

def seed_tipopagamentos():
    db: Session = SessionLocal()
    try:
        pix = db.query(models.TipoPagamento).filter(
            models.TipoPagamento.nome.ilike("PIX")
        ).first()
        if not pix:
            pix = models.TipoPagamento(nome="PIX")
            db.add(pix)

        boleto = db.query(models.TipoPagamento).filter(
            models.TipoPagamento.nome.ilike("Boleto")
        ).first()
        if not boleto:
            boleto = models.TipoPagamento(nome="Boleto")
            db.add(boleto)

        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def run_seed():
    seed_tipopagamentos()