"""
Serviço de negócio: Aluno.

Contém toda a lógica de negócio relacionada a alunos.
Segue os princípios SOLID:
- SRP: Responsável apenas pela lógica de negócio de alunos
- OCP: Aberto para extensão, fechado para modificação
- DIP: Depende de abstrações (Session) não de implementações concretas
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
import uuid
from app.model.aluno import AlunoModel, AlunoCriar, AlunoAtualizar


class AlunoService:
    """
    Serviço responsável pela lógica de negócio de alunos.
    
    Gerencia todas as operações CRUD e regras de negócio relacionadas
    aos alunos do sistema.
    """
    
    def __init__(self, sessao: Session):
        """
        Inicializa o serviço com uma sessão do banco de dados.
        
        Args:
            sessao: Sessão do SQLAlchemy para operações no banco.
        """
        self.sessao = sessao
    
    def listar_todos(self, pular: int = 0, limite: int = 100) -> List[AlunoModel]:
        """
        Lista todos os alunos com paginação.
        
        Args:
            pular: Número de registros a pular (offset).
            limite: Número máximo de registros a retornar.
            
        Returns:
            List[AlunoModel]: Lista de alunos encontrados.
        """
        return self.sessao.query(AlunoModel).offset(pular).limit(limite).all()
    
    def buscar_por_id(self, aluno_id: uuid.UUID) -> AlunoModel:
        """
        Busca um aluno pelo ID.
        
        Args:
            aluno_id: UUID do aluno.
            
        Returns:
            AlunoModel: Aluno encontrado.
            
        Raises:
            HTTPException: Se o aluno não for encontrado.
        """
        aluno = self.sessao.query(AlunoModel).filter(AlunoModel.id == aluno_id).first()
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aluno com ID {aluno_id} não encontrado"
            )
        return aluno
    
    def buscar_por_matricula(self, matricula: str) -> Optional[AlunoModel]:
        """
        Busca um aluno pela matrícula.
        
        Args:
            matricula: Matrícula do aluno.
            
        Returns:
            Optional[AlunoModel]: Aluno encontrado ou None.
        """
        return self.sessao.query(AlunoModel).filter(AlunoModel.matricula == matricula).first()
    
    def buscar_por_email(self, email: str) -> Optional[AlunoModel]:
        """
        Busca um aluno pelo email.
        
        Args:
            email: Email do aluno.
            
        Returns:
            Optional[AlunoModel]: Aluno encontrado ou None.
        """
        return self.sessao.query(AlunoModel).filter(AlunoModel.email == email).first()
    
    def criar(self, dados_aluno: AlunoCriar) -> AlunoModel:
        """
        Cria um novo aluno no sistema.
        
        Args:
            dados_aluno: Dados do aluno a ser criado.
            
        Returns:
            AlunoModel: Aluno criado com sucesso.
            
        Raises:
            HTTPException: Se matrícula ou email já existirem.
        """
        if self.buscar_por_matricula(dados_aluno.matricula):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Matrícula {dados_aluno.matricula} já está cadastrada"
            )
        
        if self.buscar_por_email(dados_aluno.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {dados_aluno.email} já está cadastrado"
            )
        
        novo_aluno = AlunoModel(**dados_aluno.model_dump())
        
        try:
            self.sessao.add(novo_aluno)
            self.sessao.commit()
            self.sessao.refresh(novo_aluno)
            return novo_aluno
        except IntegrityError as erro:
            self.sessao.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao criar aluno: {str(erro)}"
            )
    
    def atualizar(self, aluno_id: uuid.UUID, dados_atualizacao: AlunoAtualizar) -> AlunoModel:
        """
        Atualiza os dados de um aluno existente.
        
        Args:
            aluno_id: UUID do aluno a ser atualizado.
            dados_atualizacao: Novos dados do aluno.
            
        Returns:
            AlunoModel: Aluno atualizado.
            
        Raises:
            HTTPException: Se o aluno não for encontrado ou email já existir.
        """
        aluno = self.buscar_por_id(aluno_id)
        
        if dados_atualizacao.email:
            aluno_existente = self.buscar_por_email(dados_atualizacao.email)
            if aluno_existente and aluno_existente.id != aluno_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email {dados_atualizacao.email} já está em uso"
                )
        
        dados_dict = dados_atualizacao.model_dump(exclude_unset=True)
        for campo, valor in dados_dict.items():
            setattr(aluno, campo, valor)
        
        try:
            self.sessao.commit()
            self.sessao.refresh(aluno)
            return aluno
        except IntegrityError as erro:
            self.sessao.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao atualizar aluno: {str(erro)}"
            )
    
    def excluir(self, aluno_id: uuid.UUID) -> dict:
        """
        Exclui um aluno do sistema.
        
        Args:
            aluno_id: UUID do aluno a ser excluído.
            
        Returns:
            dict: Mensagem de confirmação.
            
        Raises:
            HTTPException: Se o aluno não for encontrado.
        """
        aluno = self.buscar_por_id(aluno_id)
        
        try:
            self.sessao.delete(aluno)
            self.sessao.commit()
            return {"mensagem": f"Aluno {aluno.nome} excluído com sucesso"}
        except Exception as erro:
            self.sessao.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao excluir aluno: {str(erro)}"
            )
