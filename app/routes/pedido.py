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

# Rota para criar um pedido
@router.post("/", response_model=schemas.PedidoOut)
def create_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    db_pedido = models.Pedido(
        cliente_id=pedido.cliente_id,
        data_pedido=pedido.data_pedido,
        status=pedido.status,
        total=pedido.total
    )
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

# Rota para listar todos os pedidos
@router.get("/", response_model=list[schemas.PedidoOut])
def get_pedidos(db: Session = Depends(get_db)):
    pedidos = db.query(models.Pedido).all()
    return pedidos

# Rota para obter um pedido por ID
@router.get("/{pedido_id}", response_model=schemas.PedidoOut)
def get_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

# Rota para atualizar um pedido
@router.put("/{pedido_id}", response_model=schemas.PedidoOut)
def update_pedido(pedido_id: int, pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    db_pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    db_pedido.cliente_id = pedido.cliente_id
    db_pedido.data_pedido = pedido.data_pedido
    db_pedido.status = pedido.status
    db_pedido.total = pedido.total
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

# Rota para deletar um pedido
@router.delete("/{pedido_id}", response_model=schemas.PedidoOut)
def delete_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    db.delete(db_pedido)
    db.commit()
    return db_pedido
