"""
Módulo de configuração do banco de dados.

Gerencia a conexão com o banco de dados usando SQLAlchemy.
Segue o princípio SRP: responsável apenas pela configuração do banco.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.config.configuracoes import configuracoes


engine = create_engine(
    configuracoes.DATABASE_URL,
    echo=configuracoes.DB_ECHO,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def obter_sessao_banco() -> Generator[Session, None, None]:
    """
    Dependency que fornece uma sessão do banco de dados.
    
    Yields:
        Session: Sessão do SQLAlchemy para operações no banco.
        
    Note:
        A sessão é fechada automaticamente após o uso.
    """
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()


def criar_tabelas() -> None:
    """
    Cria todas as tabelas no banco de dados.
    
    Note:
        Use Alembic para migrations em produção.
    """
    Base.metadata.create_all(bind=engine)
