"""
Serviço de negócio: Nota.

Contém toda a lógica de negócio relacionada a notas.
Segue os princípios SOLID: SRP, OCP e DIP.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from fastapi import HTTPException, status
from typing import List
import uuid
from app.model.nota import NotaModel, NotaCriar, NotaAtualizar
from app.service.aluno_service import AlunoService
from app.service.disciplina_service import DisciplinaService


class NotaService:
    """
    Serviço responsável pela lógica de negócio de notas.
    
    Gerencia todas as operações CRUD e regras de negócio relacionadas
    às notas dos alunos.
    """
    
    def __init__(self, sessao: Session):
        """
        Inicializa o serviço com uma sessão do banco de dados.
        
        Args:
            sessao: Sessão do SQLAlchemy para operações no banco.
        """
        self.sessao = sessao
        self.servico_aluno = AlunoService(sessao)
        self.servico_disciplina = DisciplinaService(sessao)
    
    def listar_todas(self, pular: int = 0, limite: int = 100) -> List[NotaModel]:
        """
        Lista todas as notas com paginação.
        
        Args:
            pular: Número de registros a pular (offset).
            limite: Número máximo de registros a retornar.
            
        Returns:
            List[NotaModel]: Lista de notas encontradas.
        """
        return self.sessao.query(NotaModel).offset(pular).limit(limite).all()
    
    def buscar_por_id(self, nota_id: uuid.UUID) -> NotaModel:
        """
        Busca uma nota pelo ID.
        
        Args:
            nota_id: UUID da nota.
            
        Returns:
            NotaModel: Nota encontrada.
            
        Raises:
            HTTPException: Se a nota não for encontrada.
        """
        nota = self.sessao.query(NotaModel).filter(NotaModel.id == nota_id).first()
        if not nota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nota com ID {nota_id} não encontrada"
            )
        return nota
    
    def listar_por_aluno(self, aluno_id: uuid.UUID) -> List[NotaModel]:
        """
        Lista todas as notas de um aluno específico.
        
        Args:
            aluno_id: UUID do aluno.
            
        Returns:
            List[NotaModel]: Lista de notas do aluno.
        """
        self.servico_aluno.buscar_por_id(aluno_id)
        
        return self.sessao.query(NotaModel).filter(
            NotaModel.aluno_id == aluno_id
        ).all()
    
    def listar_por_disciplina(self, disciplina_id: uuid.UUID) -> List[NotaModel]:
        """
        Lista todas as notas de uma disciplina específica.
        
        Args:
            disciplina_id: UUID da disciplina.
            
        Returns:
            List[NotaModel]: Lista de notas da disciplina.
        """
        self.servico_disciplina.buscar_por_id(disciplina_id)
        
        return self.sessao.query(NotaModel).filter(
            NotaModel.disciplina_id == disciplina_id
        ).all()
    
    def verificar_nota_duplicada(self, aluno_id: uuid.UUID, disciplina_id: uuid.UUID, 
                                 semestre: str, nota_id: uuid.UUID = None) -> bool:
        """
        Verifica se já existe uma nota para o aluno na disciplina no semestre.
        
        Args:
            aluno_id: UUID do aluno.
            disciplina_id: UUID da disciplina.
            semestre: Semestre da nota.
            nota_id: UUID da nota atual (para ignorar na atualização).
            
        Returns:
            bool: True se existe nota duplicada, False caso contrário.
        """
        query = self.sessao.query(NotaModel).filter(
            and_(
                NotaModel.aluno_id == aluno_id,
                NotaModel.disciplina_id == disciplina_id,
                NotaModel.semestre == semestre
            )
        )
        
        if nota_id:
            query = query.filter(NotaModel.id != nota_id)
        
        return query.first() is not None
    
    def criar(self, dados_nota: NotaCriar) -> NotaModel:
        """
        Cria uma nova nota no sistema.
        
        Args:
            dados_nota: Dados da nota a ser criada.
            
        Returns:
            NotaModel: Nota criada com sucesso.
            
        Raises:
            HTTPException: Se aluno/disciplina não existirem ou nota duplicada.
        """
        self.servico_aluno.buscar_por_id(dados_nota.aluno_id)
        self.servico_disciplina.buscar_por_id(dados_nota.disciplina_id)
        
        if self.verificar_nota_duplicada(
            dados_nota.aluno_id, 
            dados_nota.disciplina_id, 
            dados_nota.semestre
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe uma nota cadastrada para este aluno nesta disciplina no semestre {dados_nota.semestre}"
            )
        
        nova_nota = NotaModel(**dados_nota.model_dump())
        
        try:
            self.sessao.add(nova_nota)
            self.sessao.commit()
            self.sessao.refresh(nova_nota)
            return nova_nota
        except IntegrityError as erro:
            self.sessao.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao criar nota: {str(erro)}"
            )
    
    def atualizar(self, nota_id: uuid.UUID, dados_atualizacao: NotaAtualizar) -> NotaModel:
        """
        Atualiza os dados de uma nota existente.
        
        Args:
            nota_id: UUID da nota a ser atualizada.
            dados_atualizacao: Novos dados da nota.
            
        Returns:
            NotaModel: Nota atualizada.
            
        Raises:
            HTTPException: Se a nota não for encontrada.
        """
        nota = self.buscar_por_id(nota_id)
        
        dados_dict = dados_atualizacao.model_dump(exclude_unset=True)
        for campo, valor in dados_dict.items():
            setattr(nota, campo, valor)
        
        try:
            self.sessao.commit()
            self.sessao.refresh(nota)
            return nota
        except IntegrityError as erro:
            self.sessao.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao atualizar nota: {str(erro)}"
            )
    
    def excluir(self, nota_id: uuid.UUID) -> dict:
        """
        Exclui uma nota do sistema.
        
        Args:
            nota_id: UUID da nota a ser excluída.
            
        Returns:
            dict: Mensagem de confirmação.
            
        Raises:
            HTTPException: Se a nota não for encontrada.
        """
        nota = self.buscar_por_id(nota_id)
        
        try:
            self.sessao.delete(nota)
            self.sessao.commit()
            return {"mensagem": "Nota excluída com sucesso"}
        except Exception as erro:
            self.sessao.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao excluir nota: {str(erro)}"
            )
