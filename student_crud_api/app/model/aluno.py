"""
Modelo de domínio: Aluno.

Define a entidade Aluno e suas validações.
Segue o princípio SRP: representa apenas a entidade Aluno.
"""

import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.config.database import Base


class AlunoModel(Base):
    """
    Modelo ORM da entidade Aluno.
    
    Representa a tabela 'alunos' no banco de dados com todos os campos
    necessários para cadastro de estudantes.
    """
    
    __tablename__ = "alunos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    matricula = Column(String(20), unique=True, nullable=False, index=True)
    data_nascimento = Column(Date, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    notas = relationship("NotaModel", back_populates="aluno", cascade="all, delete-orphan")


class AlunoCriar(BaseModel):
    """
    Schema/DTO para criação de um novo aluno.
    
    Valida os dados de entrada ao criar um aluno.
    """
    
    nome: str = Field(..., min_length=3, max_length=100, description="Nome completo do aluno")
    email: EmailStr = Field(..., description="Email válido do aluno")
    matricula: str = Field(..., min_length=5, max_length=20, description="Matrícula única do aluno")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento")


class AlunoAtualizar(BaseModel):
    """
    Schema/DTO para atualização de dados de um aluno.
    
    Todos os campos são opcionais para atualização parcial.
    """
    
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    data_nascimento: Optional[date] = None


class AlunoResposta(BaseModel):
    """
    Schema/DTO de resposta com dados do aluno.
    
    Representa o aluno retornado pela API.
    """
    
    id: uuid.UUID
    nome: str
    email: str
    matricula: str
    data_nascimento: Optional[date]
    criado_em: datetime
    atualizado_em: datetime
    
    class Config:
        """Configuração do Pydantic."""
        from_attributes = True
