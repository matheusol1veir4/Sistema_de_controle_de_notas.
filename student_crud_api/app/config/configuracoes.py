"""
Módulo de configurações da aplicação.

Este módulo centraliza todas as configurações do sistema usando Pydantic Settings,
seguindo o princípio de Responsabilidade Única (SRP) do SOLID.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Configuracoes(BaseSettings):
    """
    Classe responsável por gerenciar as configurações da aplicação.
    
    Carrega variáveis de ambiente do arquivo .env e fornece valores padrão.
    Segue o princípio SRP: responsável apenas por configurações.
    """
    
    DATABASE_URL: str
    DB_ECHO: bool = False
    
    APP_NAME: str = "Sistema de Cadastro de Alunos"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        """Configurações do Pydantic."""
        env_file = ".env"
        case_sensitive = True


def obter_configuracoes() -> Configuracoes:
    """
    Retorna uma instância das configurações da aplicação.
    
    Returns:
        Configuracoes: Instância com todas as configurações carregadas.
    """
    return Configuracoes()


configuracoes = obter_configuracoes()
