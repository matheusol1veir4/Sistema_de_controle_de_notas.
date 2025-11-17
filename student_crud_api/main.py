"""
Aplicação principal FastAPI.

Entry point da aplicação que configura e inicia o servidor FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.configuracoes import configuracoes
from app.config.database import criar_tabelas
from app.controller import aluno_controller, disciplina_controller, nota_controller


app = FastAPI(
    title=configuracoes.APP_NAME,
    version=configuracoes.APP_VERSION,
    description="API REST para gerenciamento de alunos, disciplinas e notas",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    aluno_controller.router,
    prefix=configuracoes.API_V1_PREFIX
)

app.include_router(
    disciplina_controller.router,
    prefix=configuracoes.API_V1_PREFIX
)

app.include_router(
    nota_controller.router,
    prefix=configuracoes.API_V1_PREFIX
)


@app.on_event("startup")
def inicializar_aplicacao():
    """
    Executado na inicialização da aplicação.
    
    Cria as tabelas no banco de dados se não existirem.
    """
    criar_tabelas()
    print(f"{configuracoes.APP_NAME} v{configuracoes.APP_VERSION} iniciado!")
    print("Documentação disponível em: http://localhost:8000/docs")


@app.get("/")
def raiz():
    """
    Endpoint raiz da API.
    
    Returns:
        dict: Informações básicas da API.
    """
    return {
        "aplicacao": configuracoes.APP_NAME,
        "versao": configuracoes.APP_VERSION,
        "documentacao": "/docs",
        "status": "online"
    }


@app.get("/health")
def verificar_saude():
    """
    Endpoint de health check.
    
    Returns:
        dict: Status da aplicação.
    """
    return {"status": "saudavel"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=configuracoes.DEBUG
    )
