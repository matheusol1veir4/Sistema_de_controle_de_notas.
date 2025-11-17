"""
Modelo de domínio: Disciplina.

Define a entidade Disciplina e suas validações.
Segue o princípio SRP: representa apenas a entidade Disciplina.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from typing import Optional
from app.config.database import Base


class DisciplinaModel(Base):
    """
    Modelo ORM da entidade Disciplina.
    
    Representa a tabela 'disciplinas' no banco de dados.
    """
    
    __tablename__ = "disciplinas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    nome = Column(String(100), nullable=False, index=True)
    carga_horaria = Column(Integer, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    notas = relationship("NotaModel", back_populates="disciplina", cascade="all, delete-orphan")


class DisciplinaCriar(BaseModel):
    """
    Schema para criação de uma nova disciplina.
    
    Valida os dados de entrada ao criar uma disciplina.
    """
    
    codigo: str = Field(..., min_length=3, max_length=20, description="Código único da disciplina")
    nome: str = Field(..., min_length=3, max_length=100, description="Nome da disciplina")
    carga_horaria: int = Field(..., gt=0, le=1000, description="Carga horária em horas")


class DisciplinaAtualizar(BaseModel):
    """
    Schema para atualização de dados de uma disciplina.
    
    Todos os campos são opcionais para atualização parcial.
    """
    
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    carga_horaria: Optional[int] = Field(None, gt=0, le=1000)


class DisciplinaResposta(BaseModel):
    """
    Schema de resposta com dados da disciplina.
    
    Representa a disciplina retornada pela API.
    """
    
    id: uuid.UUID
    codigo: str
    nome: str
    carga_horaria: int
    criado_em: datetime
    atualizado_em: datetime
    
    class Config:
        """Configuração do Pydantic."""
        from_attributes = True
