import os
from fastapi import FastAPI
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from . import models


Base.metadata.create_all(bind=engine)

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