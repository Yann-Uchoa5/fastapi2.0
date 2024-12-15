from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import cliente, produto, pedido

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)


app = FastAPI()

# Configuração de CORS
origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas das diferentes entidades
app.include_router(cliente.router, tags=["Clientes"], prefix="/clientes")
app.include_router(produto.router, tags=["Produtos"], prefix="/produtos")
app.include_router(pedido.router, tags=["Pedidos"], prefix="/pedidos")

# Rota de verificação de saúde
@app.get("/")
def root():
    return {"message": "Consulte a documentação da API em http://127.0.0.1:8000/docs"}
