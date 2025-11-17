"""
Controller: Nota.

Define os endpoints REST para operações com notas.
Segue o princípio SRP: responsável apenas pela camada de apresentação.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.config.database import obter_sessao_banco
from app.service.nota_service import NotaService
from app.model.nota import NotaCriar, NotaAtualizar, NotaResposta


router = APIRouter(
    prefix="/notas",
    tags=["Notas"]
)


@router.get("/", response_model=List[NotaResposta], status_code=status.HTTP_200_OK)
def listar_notas(
    pular: int = 0,
    limite: int = 100,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Lista todas as notas cadastradas com paginação.
    
    Args:
        pular: Número de registros a pular (padrão: 0).
        limite: Número máximo de registros (padrão: 100).
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        List[NotaResposta]: Lista de notas.
    """
    servico = NotaService(sessao)
    return servico.listar_todas(pular=pular, limite=limite)


@router.get("/{nota_id}", response_model=NotaResposta, status_code=status.HTTP_200_OK)
def buscar_nota(
    nota_id: uuid.UUID,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Busca uma nota específica pelo ID.
    
    Args:
        nota_id: UUID da nota.
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        NotaResposta: Dados da nota encontrada.
    """
    servico = NotaService(sessao)
    return servico.buscar_por_id(nota_id)


@router.get("/aluno/{aluno_id}", response_model=List[NotaResposta], status_code=status.HTTP_200_OK)
def listar_notas_aluno(
    aluno_id: uuid.UUID,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Lista todas as notas de um aluno específico.
    
    Args:
        aluno_id: UUID do aluno.
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        List[NotaResposta]: Lista de notas do aluno.
    """
    servico = NotaService(sessao)
    return servico.listar_por_aluno(aluno_id)


@router.get("/disciplina/{disciplina_id}", response_model=List[NotaResposta], status_code=status.HTTP_200_OK)
def listar_notas_disciplina(
    disciplina_id: uuid.UUID,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Lista todas as notas de uma disciplina específica.
    
    Args:
        disciplina_id: UUID da disciplina.
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        List[NotaResposta]: Lista de notas da disciplina.
    """
    servico = NotaService(sessao)
    return servico.listar_por_disciplina(disciplina_id)


@router.post("/", response_model=NotaResposta, status_code=status.HTTP_201_CREATED)
def criar_nota(
    dados_nota: NotaCriar,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Cria uma nova nota no sistema.
    
    Args:
        dados_nota: Dados da nota a ser criada.
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        NotaResposta: Nota criada com sucesso.
    """
    servico = NotaService(sessao)
    return servico.criar(dados_nota)


@router.put("/{nota_id}", response_model=NotaResposta, status_code=status.HTTP_200_OK)
def atualizar_nota(
    nota_id: uuid.UUID,
    dados_atualizacao: NotaAtualizar,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Atualiza os dados de uma nota existente.
    
    Args:
        nota_id: UUID da nota a ser atualizada.
        dados_atualizacao: Novos dados da nota.
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        NotaResposta: Nota atualizada.
    """
    servico = NotaService(sessao)
    return servico.atualizar(nota_id, dados_atualizacao)


@router.delete("/{nota_id}", status_code=status.HTTP_200_OK)
def excluir_nota(
    nota_id: uuid.UUID,
    sessao: Session = Depends(obter_sessao_banco)
):
    """
    Exclui uma nota do sistema.
    
    Args:
        nota_id: UUID da nota a ser excluída.
        sessao: Sessão do banco de dados injetada.
        
    Returns:
        dict: Mensagem de confirmação.
    """
    servico = NotaService(sessao)
    return servico.excluir(nota_id)
