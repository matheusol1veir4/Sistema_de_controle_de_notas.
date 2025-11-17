"""
Controller: Aluno.

Define os endpoints REST para operações com alunos.
Segue o princípio SRP: responsável apenas pela camada de apresentação.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.config.database import obter_sessao_banco
from app.service.aluno_service import AlunoService
from app.model.aluno import AlunoCriar, AlunoAtualizar, AlunoResposta


router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"]
)


@router.get("/", response_model=List[AlunoResposta], status_code=status.HTTP_200_OK)
def listar_alunos(
    pular: int = 0,
    limite: int = 100,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Lista todos os alunos cadastrados com paginação.
    
    Args:
        pular: Número de registros a pular (padrão: 0).
        limite: Número máximo de registros (padrão: 100).
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        List[AlunoResposta]: Lista de alunos.
    """
    servico = AlunoService(sessao)
    return servico.listar_todos(pular=pular, limite=limite)


@router.get("/{aluno_id}", response_model=AlunoResposta, status_code=status.HTTP_200_OK)
def buscar_aluno(
    aluno_id: uuid.UUID,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Busca um aluno específico pelo ID.
    
    Args:
        aluno_id: UUID do aluno.
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        AlunoResposta: Dados do aluno encontrado.
    """
    servico = AlunoService(sessao)
    return servico.buscar_por_id(aluno_id)


@router.post("/", response_model=AlunoResposta, status_code=status.HTTP_201_CREATED)
def criar_aluno(
    dados_aluno: AlunoCriar,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Cria um novo aluno no sistema.
    
    Args:
        dados_aluno: Dados do aluno a ser criado.
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        AlunoResposta: Aluno criado com sucesso.
    """
    servico = AlunoService(sessao)
    return servico.criar(dados_aluno)


@router.put("/{aluno_id}", response_model=AlunoResposta, status_code=status.HTTP_200_OK)
def atualizar_aluno(
    aluno_id: uuid.UUID,
    dados_atualizacao: AlunoAtualizar,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Atualiza os dados de um aluno existente.
    
    Args:
        aluno_id: UUID do aluno a ser atualizado.
        dados_atualizacao: Novos dados do aluno.
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        AlunoResposta: Aluno atualizado.
    """
    servico = AlunoService(sessao)
    return servico.atualizar(aluno_id, dados_atualizacao)


@router.delete("/{aluno_id}", status_code=status.HTTP_200_OK)
def excluir_aluno(
    aluno_id: uuid.UUID,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Exclui um aluno do sistema.
    
    Args:
        aluno_id: UUID do aluno a ser excluído.
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        dict: Mensagem de confirmação.
    """
    servico = AlunoService(sessao)
    return servico.excluir(aluno_id)
