"""
Controller: Disciplina.

Define os endpoints REST para operações com disciplinas.
Segue o princípio SRP: responsável apenas pela camada de apresentação.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.config.database import obter_sessao_banco
from app.service.disciplina_service import DisciplinaService
from app.model.disciplina import DisciplinaCriar, DisciplinaAtualizar, DisciplinaResposta


router = APIRouter(
    prefix="/disciplinas",
    tags=["Disciplinas"]
)


@router.get("/", response_model=List[DisciplinaResposta], status_code=status.HTTP_200_OK)
def listar_disciplinas(
    pular: int = 0,
    limite: int = 100,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Lista todas as disciplinas cadastradas com paginação.
    
    Args:
        pular: Número de registros a pular (padrão: 0).
        limite: Número máximo de registros (padrão: 100).
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        List[DisciplinaResposta]: Lista de disciplinas.
    """
    servico = DisciplinaService(sessao)
    return servico.listar_todas(pular=pular, limite=limite)


@router.get("/{disciplina_id}", response_model=DisciplinaResposta, status_code=status.HTTP_200_OK)
def buscar_disciplina(
    disciplina_id: uuid.UUID,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Busca uma disciplina específica pelo ID.
    
    Args:
        disciplina_id: UUID da disciplina.
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        DisciplinaResposta: Dados da disciplina encontrada.
    """
    servico = DisciplinaService(sessao)
    return servico.buscar_por_id(disciplina_id)


@router.post("/", response_model=DisciplinaResposta, status_code=status.HTTP_201_CREATED)
def criar_disciplina(
    dados_disciplina: DisciplinaCriar,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Cria uma nova disciplina no sistema.
    
    Args:
        dados_disciplina: Dados da disciplina a ser criada.
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        DisciplinaResposta: Disciplina criada com sucesso.
    """
    servico = DisciplinaService(sessao)
    return servico.criar(dados_disciplina)


@router.put("/{disciplina_id}", response_model=DisciplinaResposta, status_code=status.HTTP_200_OK)
def atualizar_disciplina(
    disciplina_id: uuid.UUID,
    dados_atualizacao: DisciplinaAtualizar,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Atualiza os dados de uma disciplina existente.
    
    Args:
        disciplina_id: UUID da disciplina a ser atualizada.
        dados_atualizacao: Novos dados da disciplina.
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        DisciplinaResposta: Disciplina atualizada.
    """
    servico = DisciplinaService(sessao)
    return servico.atualizar(disciplina_id, dados_atualizacao)


@router.delete("/{disciplina_id}", status_code=status.HTTP_200_OK)
def excluir_disciplina(
    disciplina_id: uuid.UUID,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Exclui uma disciplina do sistema.
    
    Args:
        disciplina_id: UUID da disciplina a ser excluída.
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        dict: Mensagem de confirmação.
    """
    servico = DisciplinaService(sessao)
    return servico.excluir(disciplina_id)
