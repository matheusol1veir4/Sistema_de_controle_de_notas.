"""
Serviço de negócio: Disciplina.

Contém toda a lógica de negócio relacionada a disciplinas.
Segue os princípios SOLID: SRP, OCP e DIP.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
import uuid
from app.model.disciplina import DisciplinaModel, DisciplinaCriar, DisciplinaAtualizar


class DisciplinaService:
    """
    Serviço responsável pela lógica de negócio de disciplinas.
    
    Gerencia todas as operações CRUD e regras de negócio relacionadas
    às disciplinas do sistema.
    """
    
    def __init__(self, sessao: Session):
        """
        Inicializa o serviço com uma sessão do banco de dados.
        
        Args:
            sessao: Sessão do SQLAlchemy para operações no banco.
        """
        self.sessao = sessao
    
    def listar_todas(self, pular: int = 0, limite: int = 100) -> List[DisciplinaModel]:
        """
        Lista todas as disciplinas com paginação.
        
        Args:
            pular: Número de registros a pular (offset).
            limite: Número máximo de registros a retornar.
            
        Returns:
            List[DisciplinaModel]: Lista de disciplinas encontradas.
        """
        stmt = select(DisciplinaModel).offset(pular).limit(limite)
        return list(self.sessao.scalars(stmt).all())
    
    def buscar_por_id(self, disciplina_id: uuid.UUID) -> DisciplinaModel:
        """
        Busca uma disciplina pelo ID.
        
        Args:
            disciplina_id: UUID da disciplina.
            
        Returns:
            DisciplinaModel: Disciplina encontrada.
            
        Raises:
            HTTPException: Se a disciplina não for encontrada.
        """
        stmt = select(DisciplinaModel).where(DisciplinaModel.id == disciplina_id)
        disciplina = self.sessao.scalar(stmt)
        
        if not disciplina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Disciplina com ID {disciplina_id} não encontrada"
            )
        return disciplina
    
    def buscar_por_codigo(self, codigo: str) -> Optional[DisciplinaModel]:
        """
        Busca uma disciplina pelo código.
        
        Args:
            codigo: Código da disciplina.
            
        Returns:
            Optional[DisciplinaModel]: Disciplina encontrada ou None.
        """
        stmt = select(DisciplinaModel).where(DisciplinaModel.codigo == codigo)
        return self.sessao.scalar(stmt)
    
    def criar(self, dados_disciplina: DisciplinaCriar) -> DisciplinaModel:
        """
        Cria uma nova disciplina no sistema.
        
        Args:
            dados_disciplina: Dados da disciplina a ser criada.
            
        Returns:
            DisciplinaModel: Disciplina criada com sucesso.
            
        Raises:
            HTTPException: Se o código já existir.
        """
        if self.buscar_por_codigo(dados_disciplina.codigo):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Código {dados_disciplina.codigo} já está cadastrado"
            )
        
        nova_disciplina = DisciplinaModel(**dados_disciplina.model_dump())
        
        try:
            self.sessao.add(nova_disciplina)
            self.sessao.commit()
            self.sessao.refresh(nova_disciplina)
            return nova_disciplina
        except IntegrityError as erro:
            self.sessao.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao criar disciplina: {str(erro)}"
            )
    
    def atualizar(self, disciplina_id: uuid.UUID, dados_atualizacao: DisciplinaAtualizar) -> DisciplinaModel:
        """
        Atualiza os dados de uma disciplina existente.
        
        Args:
            disciplina_id: UUID da disciplina a ser atualizada.
            dados_atualizacao: Novos dados da disciplina.
            
        Returns:
            DisciplinaModel: Disciplina atualizada.
            
        Raises:
            HTTPException: Se a disciplina não for encontrada.
        """
        disciplina = self.buscar_por_id(disciplina_id)
        
        dados_dict = dados_atualizacao.model_dump(exclude_unset=True)
        for campo, valor in dados_dict.items():
            setattr(disciplina, campo, valor)
        
        try:
            self.sessao.commit()
            self.sessao.refresh(disciplina)
            return disciplina
        except IntegrityError as erro:
            self.sessao.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao atualizar disciplina: {str(erro)}"
            )
    
    def excluir(self, disciplina_id: uuid.UUID) -> dict:
        """
        Exclui uma disciplina do sistema.
        
        Args:
            disciplina_id: UUID da disciplina a ser excluída.
            
        Returns:
            dict: Mensagem de confirmação.
            
        Raises:
            HTTPException: Se a disciplina não for encontrada.
        """
        disciplina = self.buscar_por_id(disciplina_id)
        
        try:
            self.sessao.delete(disciplina)
            self.sessao.commit()
            return {"mensagem": f"Disciplina {disciplina.nome} excluída com sucesso"}
        except Exception as erro:
            self.sessao.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao excluir disciplina: {str(erro)}"
            )
