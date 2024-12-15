from fastapi import APIRouter, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from app import models, schemas
from app.database import SessionLocal

router = APIRouter()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar um cliente
@router.post("/", response_model=schemas.ClienteOut)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = models.Cliente(
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone,
        endereco=cliente.endereco
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Rota para listar todos os clientes
@router.get("/", response_model=list[schemas.ClienteOut])
def get_clientes(db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).all()
    return clientes

# Rota para obter um cliente por ID
@router.get("/{cliente_id}", response_model=schemas.ClienteOut)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

# Rota para atualizar um cliente
@router.put("/{cliente_id}", response_model=schemas.ClienteOut)
def update_cliente(cliente_id: int, cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    db_cliente.nome = cliente.nome
    db_cliente.email = cliente.email
    db_cliente.telefone = cliente.telefone
    db_cliente.endereco = cliente.endereco
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Rota para deletar um cliente
@router.delete("/{cliente_id}", response_model=schemas.ClienteOut)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    db.delete(db_cliente)
    db.commit()
    return db_cliente
