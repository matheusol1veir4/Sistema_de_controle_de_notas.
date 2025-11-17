"""
Interface Gráfica Principal - Sistema de Cadastro de Alunos.

Desenvolvido com Tkinter seguindo princípios Clean Code.
Conecta-se à API FastAPI e permite exportação para TXT, CSV e JSON.
"""

import tkinter as tk
from tkinter import messagebox
import requests
from gerenciador_alunos import GerenciadorAlunos
from gerenciador_disciplinas import GerenciadorDisciplinas
from gerenciador_notas import GerenciadorNotas


class JanelaPrincipal:
    """
    Janela principal do sistema de cadastro.
    
    Gerencia a navegação entre as telas de Alunos, Disciplinas e Notas.
    Responsável por inicializar a interface e coordenar a abertura
    das janelas de gerenciamento.
    """
    
    def __init__(self):
        """
        Inicializa a janela principal.
        
        Configura a interface gráfica, verifica conexão com a API
        e prepara os componentes de navegação.
        """
        self.janela = tk.Tk()
        self.janela.title("Sistema de Cadastro de Alunos v1.0")
        self.janela.geometry("1000x650")
        self.janela.resizable(True, True)
        
        self.api_url = "http://localhost:8000/api/v1"
        
        self.verificar_conexao_api()
        self.configurar_interface()
    
    def verificar_conexao_api(self) -> bool:
        """
        Verifica se a API está acessível.
        
        Tenta conectar ao endpoint de health check da API.
        Exibe mensagem de erro caso a conexão falhe.
        
        Returns:
            bool: True se conectado com sucesso, False caso contrário.
        """
        try:
            resposta = requests.get("http://localhost:8000/health", timeout=2)
            if resposta.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            messagebox.showerror(
                "Erro de Conexão",
                "Não foi possível conectar à API.\n\n"
                "Certifique-se de que o servidor FastAPI está rodando:\n"
                "python3 main.py"
            )
        return False
    
    def configurar_interface(self):
        """
        Configura os componentes da interface principal.
        
        Cria e organiza os elementos visuais da janela principal,
        incluindo título, menu de navegação e área de informações.
        """
        frame_topo = tk.Frame(self.janela, bg="#2c3e50", height=80)
        frame_topo.pack(fill=tk.X)
        
        titulo = tk.Label(
            frame_topo,
            text="Sistema de Cadastro de Alunos",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        titulo.pack(pady=20)
        
        frame_menu = tk.Frame(self.janela, bg="#34495e", height=60)
        frame_menu.pack(fill=tk.X)
        
        btn_alunos = tk.Button(
            frame_menu,
            text="Alunos",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=15,
            height=2,
            cursor="hand2",
            command=self.abrir_gerenciador_alunos
        )
        btn_alunos.pack(side=tk.LEFT, padx=20, pady=10)
        
        btn_disciplinas = tk.Button(
            frame_menu,
            text="Disciplinas",
            font=("Arial", 12, "bold"),
            bg="#9b59b6",
            fg="white",
            width=15,
            height=2,
            cursor="hand2",
            command=self.abrir_gerenciador_disciplinas
        )
        btn_disciplinas.pack(side=tk.LEFT, padx=20, pady=10)
        
        btn_notas = tk.Button(
            frame_menu,
            text="Notas",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=15,
            height=2,
            cursor="hand2",
            command=self.abrir_gerenciador_notas
        )
        btn_notas.pack(side=tk.LEFT, padx=20, pady=10)
        
        frame_central = tk.Frame(self.janela, bg="white")
        frame_central.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        info_texto = tk.Label(
            frame_central,
            text="Bem-vindo ao Sistema de Cadastro de Alunos\n\n"
                 "Selecione uma opção no menu acima para começar:\n\n"
                 "• Alunos: Cadastrar e gerenciar alunos\n"
                 "• Disciplinas: Cadastrar e gerenciar disciplinas\n"
                 "• Notas: Lançar e gerenciar notas dos alunos\n\n"
                 "Todas as operações são salvas automaticamente no banco de dados\n"
                 "e podem ser exportadas para TXT, CSV ou JSON.",
            font=("Arial", 11),
            bg="white",
            justify=tk.LEFT
        )
        info_texto.pack(pady=50)
        
        frame_footer = tk.Frame(self.janela, bg="#ecf0f1", height=40)
        frame_footer.pack(side=tk.BOTTOM, fill=tk.X)
        
        footer_label = tk.Label(
            frame_footer,
            text="© 2025 - Sistema de Cadastro de Alunos | Desenvolvido com FastAPI + Tkinter",
            font=("Arial", 9),
            bg="#ecf0f1"
        )
        footer_label.pack(pady=10)
    
    def abrir_gerenciador_alunos(self):
        """
        Abre a janela de gerenciamento de alunos.
        
        Instancia e exibe a interface de gerenciamento de alunos,
        passando a URL base da API como parâmetro.
        """
        GerenciadorAlunos(self.api_url)
    
    def abrir_gerenciador_disciplinas(self):
        """
        Abre a janela de gerenciamento de disciplinas.
        
        Instancia e exibe a interface de gerenciamento de disciplinas,
        passando a URL base da API como parâmetro.
        """
        GerenciadorDisciplinas(self.api_url)
    
    def abrir_gerenciador_notas(self):
        """
        Abre a janela de gerenciamento de notas.
        
        Instancia e exibe a interface de gerenciamento de notas,
        passando a URL base da API como parâmetro.
        """
        GerenciadorNotas(self.api_url)
    
    def executar(self):
        """
        Inicia o loop principal da aplicação.
        
        Mantém a janela principal aberta e responsiva
        a eventos do usuário até que seja fechada.
        """
        self.janela.mainloop()


if __name__ == "__main__":
    app = JanelaPrincipal()
    app.executar()
