"""
Modelo de domínio: Nota.

Define a entidade Nota e suas validações.
Segue o princípio SRP: representa apenas a entidade Nota.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.config.database import Base


class NotaModel(Base):
    """
    Modelo ORM da entidade Nota.
    
    Representa a tabela 'notas' no banco de dados, estabelecendo
    relacionamento entre alunos e disciplinas.
    """
    
    __tablename__ = "notas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aluno_id = Column(UUID(as_uuid=True), ForeignKey("alunos.id"), nullable=False)
    disciplina_id = Column(UUID(as_uuid=True), ForeignKey("disciplinas.id"), nullable=False)
    valor = Column(Float, nullable=False)
    semestre = Column(String(10), nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    aluno = relationship("AlunoModel", back_populates="notas")
    disciplina = relationship("DisciplinaModel", back_populates="notas")


class NotaCriar(BaseModel):
    """
    Schema para criação de uma nova nota.
    
    Valida os dados de entrada ao criar uma nota.
    """
    
    aluno_id: uuid.UUID = Field(..., description="ID do aluno")
    disciplina_id: uuid.UUID = Field(..., description="ID da disciplina")
    valor: float = Field(..., ge=0.0, le=10.0, description="Valor da nota (0.0 a 10.0)")
    semestre: str = Field(..., min_length=5, max_length=10, description="Semestre (ex: 2024.1)")
    
    @field_validator('valor')
    @classmethod
    def validar_nota(cls, valor: float) -> float:
        """
        Valida se a nota está no intervalo permitido.
        
        Args:
            valor: Valor da nota a ser validada.
            
        Returns:
            float: Valor validado.
            
        Raises:
            ValueError: Se a nota estiver fora do intervalo 0.0 a 10.0.
        """
        if not 0.0 <= valor <= 10.0:
            raise ValueError("A nota deve estar entre 0.0 e 10.0")
        return round(valor, 2)


class NotaAtualizar(BaseModel):
    """
    Schema para atualização de uma nota.
    
    Permite atualização parcial dos campos.
    """
    
    valor: Optional[float] = Field(None, ge=0.0, le=10.0)
    semestre: Optional[str] = Field(None, min_length=5, max_length=10)
    
    @field_validator('valor')
    @classmethod
    def validar_nota(cls, valor: Optional[float]) -> Optional[float]:
        """Valida o valor da nota se fornecido."""
        if valor is not None and not 0.0 <= valor <= 10.0:
            raise ValueError("A nota deve estar entre 0.0 e 10.0")
        return round(valor, 2) if valor is not None else None


class NotaResposta(BaseModel):
    """
    Schema de resposta com dados da nota.
    
    Representa a nota retornada pela API.
    """
    
    id: uuid.UUID
    aluno_id: uuid.UUID
    disciplina_id: uuid.UUID
    valor: float
    semestre: str
    criado_em: datetime
    atualizado_em: datetime
    
    class Config:
        """Configuração do Pydantic."""
        from_attributes = True
