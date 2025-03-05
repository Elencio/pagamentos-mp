import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import pagamento
from .seed import run_seed


Base.metadata.create_all(bind=engine)

run_seed()

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