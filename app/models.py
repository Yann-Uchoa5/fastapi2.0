from .database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, DateTime, func
from sqlalchemy.orm import relationship

# Modelo para Produto
class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)
    disponivel = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    pedidos = relationship("Pedido", back_populates="produto")  # Relacionamento com Pedido


# Modelo para Cliente
class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=True)
    endereco = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    pedidos = relationship("Pedido", back_populates="cliente")  # Relacionamento com Pedido


# Modelo para Pedido
class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    data_pedido = Column(DateTime, nullable=False, server_default=func.now())
    status = Column(String, nullable=False)
    total = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    cliente = relationship("Cliente", back_populates="pedidos")  # Relacionamento com Cliente
    produto = relationship("Produto", back_populates="pedidos")  # Relacionamento com Produto
