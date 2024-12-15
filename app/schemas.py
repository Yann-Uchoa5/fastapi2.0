from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: int

    class Config:
        from_attributes = True  

class ProdutoOut(ProdutoCreate):
    id: int

    class Config:
        from_attributes = True

class ProdutoUpdate(BaseModel):
    nome: Optional[str]
    descricao: Optional[str]
    preco: Optional[float]
    estoque: Optional[int]

    class Config:
        from_attributes = True


class ClienteCreate(BaseModel):
    nome: str
    email: str
    telefone: Optional[str] = None
    endereco: Optional[str] = None

    class Config:
        from_attributes = True  

class ClienteOut(ClienteCreate):
    id: int

    class Config:
        from_attributes = True

class ClienteUpdate(BaseModel):
    nome: Optional[str]
    email: Optional[str]
    telefone: Optional[str]

    class Config:
        from_attributes = True


class PedidoCreate(BaseModel):
    cliente_id: int
    data_pedido: datetime
    status: str
    total: float

    class Config:
        from_attributes = True  

class PedidoOut(PedidoCreate):
    id: int

    class Config:
        from_attributes = True

class PedidoUpdate(BaseModel):
    cliente_id: Optional[int]
    data_pedido: Optional[datetime]
    status: Optional[str]
    total: Optional[float]

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    detail: str
