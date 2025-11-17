"""
Gerenciador de Disciplinas - Interface Tkinter.

Permite listar, incluir, alterar, excluir e exportar disciplinas.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from datetime import datetime
import json
import csv


class GerenciadorDisciplinas:
    """
    Janela de gerenciamento de disciplinas.
    
    Implementa CRUD completo e exportação para TXT, CSV e JSON.
    Gerencia a interface gráfica para operações com disciplinas,
    incluindo validação de dados e tratamento de erros.
    """
    
    def __init__(self, api_url: str):
        """
        Inicializa o gerenciador de disciplinas.
        
        Args:
            api_url: URL base da API FastAPI.
        """
        self.api_url = api_url
        self.janela = tk.Toplevel()
        self.janela.title("Gerenciar Disciplinas")
        self.janela.geometry("1100x700")
        self.janela.resizable(True, True)
        
        self.disciplina_selecionada_id = None
        
        self.configurar_interface()
        self.carregar_disciplinas()
    
    def configurar_interface(self):
        """
        Configura os componentes da interface gráfica.
        
        Cria e organiza todos os elementos visuais da janela,
        incluindo formulário, botões de ação e tabela de listagem.
        """
        frame_topo = tk.Frame(self.janela, bg="#9b59b6", height=60)
        frame_topo.pack(fill=tk.X)
        
        titulo = tk.Label(
            frame_topo,
            text="Gerenciamento de Disciplinas",
            font=("Arial", 16, "bold"),
            bg="#9b59b6",
            fg="white"
        )
        titulo.pack(pady=15)
        
        frame_principal = tk.Frame(self.janela)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        frame_form = tk.LabelFrame(
            frame_principal,
            text="Dados da Disciplina",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )
        frame_form.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        self._criar_campos_formulario(frame_form)
        self._criar_botoes_acao(frame_form)
        self._criar_botoes_exportacao(frame_form)
        self._criar_tabela_listagem(frame_principal)
        
        frame_principal.grid_columnconfigure(0, weight=1)
        frame_principal.grid_columnconfigure(1, weight=2)
        frame_principal.grid_rowconfigure(0, weight=1)
    
    def _criar_campos_formulario(self, frame_form: tk.Frame):
        """
        Cria os campos do formulário de cadastro.
        
        Args:
            frame_form: Frame pai onde os campos serão criados.
        """
        tk.Label(frame_form, text="Código:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_codigo = tk.Entry(frame_form, width=30, font=("Arial", 10))
        self.entry_codigo.grid(row=0, column=1, pady=5)
        
        tk.Label(frame_form, text="Nome:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_nome = tk.Entry(frame_form, width=30, font=("Arial", 10))
        self.entry_nome.grid(row=1, column=1, pady=5)
        
        tk.Label(frame_form, text="Carga Horária:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_carga_horaria = tk.Entry(frame_form, width=30, font=("Arial", 10))
        self.entry_carga_horaria.grid(row=2, column=1, pady=5)
        tk.Label(frame_form, text="(em horas)", font=("Arial", 8), fg="gray").grid(row=3, column=1, sticky="w")
    
    def _criar_botoes_acao(self, frame_form: tk.Frame):
        """
        Cria os botões de ação do formulário.
        
        Args:
            frame_form: Frame pai onde os botões serão criados.
        """
        frame_botoes = tk.Frame(frame_form)
        frame_botoes.grid(row=4, column=0, columnspan=2, pady=20)
        
        botoes_config = [
            ("Incluir", "#27ae60", self.incluir_disciplina),
            ("Alterar", "#f39c12", self.alterar_disciplina),
            ("Excluir", "#e74c3c", self.excluir_disciplina),
            ("Limpar", "#95a5a6", self.limpar_campos)
        ]
        
        for texto, cor, comando in botoes_config:
            btn = tk.Button(
                frame_botoes,
                text=texto,
                bg=cor,
                fg="white",
                font=("Arial", 10, "bold"),
                width=12,
                cursor="hand2",
                command=comando
            )
            btn.pack(side=tk.LEFT, padx=5)
    
    def _criar_botoes_exportacao(self, frame_form: tk.Frame):
        """
        Cria os botões de exportação de dados.
        
        Args:
            frame_form: Frame pai onde os botões serão criados.
        """
        frame_export = tk.LabelFrame(frame_form, text="Exportar Dados", font=("Arial", 10, "bold"))
        frame_export.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
        
        formatos = [
            ("TXT", "#34495e"),
            ("CSV", "#16a085"),
            ("JSON", "#8e44ad")
        ]
        
        for formato, cor in formatos:
            btn = tk.Button(
                frame_export,
                text=formato,
                bg=cor,
                fg="white",
                width=10,
                command=lambda f=formato.lower(): self.exportar_disciplinas(f)
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def _criar_tabela_listagem(self, frame_principal: tk.Frame):
        """
        Cria a tabela de listagem de disciplinas.
        
        Args:
            frame_principal: Frame pai onde a tabela será criada.
        """
        frame_lista = tk.LabelFrame(
            frame_principal,
            text="Disciplinas Cadastradas",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        frame_lista.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        colunas = ("ID", "Código", "Nome", "Carga Horária")
        self.tree = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=20)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Código", text="Código")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Carga Horária", text="C.H.")
        
        self.tree.column("ID", width=0, stretch=False)
        self.tree.column("Código", width=100)
        self.tree.column("Nome", width=300)
        self.tree.column("Carga Horária", width=80)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.bind("<<TreeviewSelect>>", self.ao_selecionar_disciplina)
    
    def carregar_disciplinas(self):
        """
        Carrega a lista de disciplinas da API e exibe na treeview.
        
        Busca todas as disciplinas cadastradas e atualiza a tabela
        de listagem. Exibe mensagem de erro em caso de falha.
        """
        try:
            resposta = requests.get(f"{self.api_url}/disciplinas")
            resposta.raise_for_status()
            disciplinas = resposta.json()
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for disciplina in disciplinas:
                self.tree.insert("", tk.END, values=(
                    disciplina["id"],
                    disciplina["codigo"],
                    disciplina["nome"],
                    f"{disciplina['carga_horaria']}h"
                ))
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro ao carregar disciplinas: {str(erro)}")
    
    def _validar_carga_horaria(self, carga_horaria_str: str) -> int:
        """
        Valida e converte a carga horária para inteiro.
        
        Args:
            carga_horaria_str: String com a carga horária.
            
        Returns:
            int: Carga horária convertida.
            
        Raises:
            ValueError: Se a carga horária não for um número válido.
        """
        try:
            return int(carga_horaria_str)
        except ValueError:
            raise ValueError("Carga horária deve ser um número inteiro!")
    
    def incluir_disciplina(self):
        """
        Inclui uma nova disciplina via API.
        
        Coleta os dados do formulário, valida e envia para a API.
        Atualiza a lista após sucesso ou exibe mensagem de erro.
        """
        codigo = self.entry_codigo.get().strip()
        nome = self.entry_nome.get().strip()
        carga_horaria_str = self.entry_carga_horaria.get().strip()
        
        if not codigo or not nome or not carga_horaria_str:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        
        try:
            carga_horaria = self._validar_carga_horaria(carga_horaria_str)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return
        
        dados = {
            "codigo": codigo,
            "nome": nome,
            "carga_horaria": carga_horaria
        }
        
        try:
            resposta = requests.post(f"{self.api_url}/disciplinas", json=dados)
            resposta.raise_for_status()
            messagebox.showinfo("Sucesso", "Disciplina cadastrada com sucesso!")
            self.limpar_campos()
            self.carregar_disciplinas()
        except requests.exceptions.HTTPError as erro:
            detalhe = erro.response.json().get('detail', str(erro)) if erro.response else str(erro)
            messagebox.showerror("Erro", f"Erro ao cadastrar disciplina:\n{detalhe}")
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro de conexão: {str(erro)}")
    
    def alterar_disciplina(self):
        """
        Altera os dados de uma disciplina selecionada.
        
        Valida se há uma disciplina selecionada, coleta os dados do formulário
        e envia atualização para a API. Atualiza a lista após sucesso.
        """
        if not self.disciplina_selecionada_id:
            messagebox.showwarning("Atenção", "Selecione uma disciplina para alterar!")
            return
        
        nome = self.entry_nome.get().strip()
        carga_horaria_str = self.entry_carga_horaria.get().strip()
        
        if not nome or not carga_horaria_str:
            messagebox.showwarning("Atenção", "Nome e carga horária são obrigatórios!")
            return
        
        try:
            carga_horaria = self._validar_carga_horaria(carga_horaria_str)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return
        
        dados = {
            "nome": nome,
            "carga_horaria": carga_horaria
        }
        
        try:
            resposta = requests.put(f"{self.api_url}/disciplinas/{self.disciplina_selecionada_id}", json=dados)
            resposta.raise_for_status()
            messagebox.showinfo("Sucesso", "Disciplina alterada com sucesso!")
            self.limpar_campos()
            self.carregar_disciplinas()
        except requests.exceptions.HTTPError as erro:
            detalhe = erro.response.json().get('detail', str(erro)) if erro.response else str(erro)
            messagebox.showerror("Erro", f"Erro ao alterar disciplina:\n{detalhe}")
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro de conexão: {str(erro)}")
    
    def excluir_disciplina(self):
        """Exclui a disciplina selecionada."""
        if not self.disciplina_selecionada_id:
            messagebox.showwarning("Atenção", "Selecione uma disciplina para excluir!")
            return
        
        confirmar = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja realmente excluir a disciplina '{self.entry_nome.get()}'?"
        )
        
        if not confirmar:
            return
        
        try:
            resposta = requests.delete(f"{self.api_url}/disciplinas/{self.disciplina_selecionada_id}")
            resposta.raise_for_status()
            messagebox.showinfo("Sucesso", "Disciplina excluída com sucesso!")
            self.limpar_campos()
            self.carregar_disciplinas()
        
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro ao excluir disciplina: {str(erro)}")
    
    def ao_selecionar_disciplina(self, evento):
        """
        Preenche os campos do formulário ao selecionar uma disciplina na lista.
        
        Args:
            evento: Evento de seleção da treeview.
        """
        selecao = self.tree.selection()
        if not selecao:
            return
        
        item = self.tree.item(selecao[0])
        valores = item["values"]
        
        self.disciplina_selecionada_id = valores[0]
        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, valores[1])
        self.entry_codigo.config(state="disabled")
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, valores[2])
        self.entry_carga_horaria.delete(0, tk.END)
        self.entry_carga_horaria.insert(0, valores[3].replace('h', ''))
    
    def limpar_campos(self):
        """Limpa todos os campos do formulário."""
        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.config(state="normal")
        self.entry_nome.delete(0, tk.END)
        self.entry_carga_horaria.delete(0, tk.END)
        self.disciplina_selecionada_id = None
    
    def exportar_disciplinas(self, formato: str):
        """
        Exporta a lista de disciplinas para arquivo.
        
        Busca as disciplinas da API e permite salvar em diferentes formatos.
        
        Args:
            formato: Formato do arquivo (txt, csv ou json).
        """
        try:
            resposta = requests.get(f"{self.api_url}/disciplinas")
            resposta.raise_for_status()
            disciplinas = resposta.json()
            
            if not disciplinas:
                messagebox.showwarning("Atenção", "Nenhuma disciplina para exportar!")
                return
            
            arquivo = filedialog.asksaveasfilename(
                defaultextension=f".{formato}",
                filetypes=[(formato.upper(), f"*.{formato}"), ("Todos os arquivos", "*.*")],
                initialfile=f"disciplinas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{formato}"
            )
            
            if not arquivo:
                return
            
            formatadores = {
                "txt": self._exportar_txt,
                "csv": self._exportar_csv,
                "json": self._exportar_json
            }
            
            formatador = formatadores.get(formato)
            if formatador:
                formatador(disciplinas, arquivo)
                messagebox.showinfo("Sucesso", f"Disciplinas exportadas para {arquivo}")
            else:
                messagebox.showerror("Erro", f"Formato {formato} não suportado!")
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(erro)}")
    
    def _exportar_txt(self, disciplinas: list, arquivo: str):
        """Exporta disciplinas para formato TXT."""
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("LISTA DE DISCIPLINAS\n")
            f.write("=" * 80 + "\n\n")
            
            for disciplina in disciplinas:
                f.write(f"ID: {disciplina['id']}\n")
                f.write(f"Código: {disciplina['codigo']}\n")
                f.write(f"Nome: {disciplina['nome']}\n")
                f.write(f"Carga Horária: {disciplina['carga_horaria']} horas\n")
                f.write("-" * 80 + "\n")
    
    def _exportar_csv(self, disciplinas: list, arquivo: str):
        """Exporta disciplinas para formato CSV."""
        with open(arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'codigo', 'nome', 'carga_horaria'])
            writer.writeheader()
            writer.writerows(disciplinas)
    
    def _exportar_json(self, disciplinas: list, arquivo: str):
        """Exporta disciplinas para formato JSON."""
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(disciplinas, f, ensure_ascii=False, indent=2)
