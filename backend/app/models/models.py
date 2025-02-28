from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON, Enum
from sqlalchemy.orm import relationship
from .database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    sobrenome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    cpf_cnpj = Column(String, nullable=False)
    endereco = Column(String, nullable=True)

class TipoPagamento(Base):
    __tablename__ = "tipopagamentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)  

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    valor = Column(Float, nullable=False)
    tipo_pagamento_id = Column(Integer, ForeignKey("tipopagamentos.id"), nullable=False)
    status = Column(String, default="pendente")  
    link_pagamento = Column(String, nullable=True)
    metadados = Column(JSON, nullable=True)

  
    cliente = relationship("Cliente")
    tipo_pagamento = relationship("TipoPagamento")
