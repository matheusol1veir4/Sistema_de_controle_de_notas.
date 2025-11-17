"""
Gerenciador de Alunos - Interface Tkinter.

Permite listar, incluir, alterar, excluir e exportar alunos.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from datetime import datetime
import json
import csv


class GerenciadorAlunos:
    """
    Janela de gerenciamento de alunos.
    
    Implementa CRUD completo e exportação para TXT, CSV e JSON.
    Gerencia a interface gráfica para operações com alunos,
    incluindo validação de dados e tratamento de erros.
    """
    
    def __init__(self, api_url: str):
        """
        Inicializa o gerenciador de alunos.
        
        Args:
            api_url: URL base da API FastAPI para comunicação.
        """
        self.api_url = api_url
        self.janela = tk.Toplevel()
        self.janela.title("Gerenciar Alunos")
        self.janela.geometry("1200x700")
        self.janela.resizable(True, True)
        
        self.aluno_selecionado_id = None
        
        self.configurar_interface()
        self.carregar_alunos()
    
    def configurar_interface(self):
        """
        Configura os componentes da interface gráfica.
        
        Cria e organiza todos os elementos visuais da janela,
        incluindo formulário, botões de ação e tabela de listagem.
        """
        frame_topo = tk.Frame(self.janela, bg="#3498db", height=60)
        frame_topo.pack(fill=tk.X)
        
        titulo = tk.Label(
            frame_topo,
            text="Gerenciamento de Alunos",
            font=("Arial", 16, "bold"),
            bg="#3498db",
            fg="white"
        )
        titulo.pack(pady=15)
        
        frame_principal = tk.Frame(self.janela)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        frame_form = tk.LabelFrame(
            frame_principal,
            text="Dados do Aluno",
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
        tk.Label(frame_form, text="Nome:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nome = tk.Entry(frame_form, width=30, font=("Arial", 10))
        self.entry_nome.grid(row=0, column=1, pady=5)
        
        tk.Label(frame_form, text="Email:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_email = tk.Entry(frame_form, width=30, font=("Arial", 10))
        self.entry_email.grid(row=1, column=1, pady=5)
        
        tk.Label(frame_form, text="Matrícula:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_matricula = tk.Entry(frame_form, width=30, font=("Arial", 10))
        self.entry_matricula.grid(row=2, column=1, pady=5)
        
        tk.Label(frame_form, text="Data Nascimento:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.entry_data_nasc = tk.Entry(frame_form, width=30, font=("Arial", 10))
        self.entry_data_nasc.grid(row=3, column=1, pady=5)
        tk.Label(frame_form, text="(AAAA-MM-DD)", font=("Arial", 8), fg="gray").grid(row=4, column=1, sticky="w")
    
    def _criar_botoes_acao(self, frame_form: tk.Frame):
        """
        Cria os botões de ação do formulário.
        
        Args:
            frame_form: Frame pai onde os botões serão criados.
        """
        frame_botoes = tk.Frame(frame_form)
        frame_botoes.grid(row=5, column=0, columnspan=2, pady=20)
        
        btn_incluir = tk.Button(
            frame_botoes,
            text="Incluir",
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2",
            command=self.incluir_aluno
        )
        btn_incluir.pack(side=tk.LEFT, padx=5)
        
        btn_alterar = tk.Button(
            frame_botoes,
            text="Alterar",
            bg="#f39c12",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2",
            command=self.alterar_aluno
        )
        btn_alterar.pack(side=tk.LEFT, padx=5)
        
        btn_excluir = tk.Button(
            frame_botoes,
            text="Excluir",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2",
            command=self.excluir_aluno
        )
        btn_excluir.pack(side=tk.LEFT, padx=5)
        
        btn_limpar = tk.Button(
            frame_botoes,
            text="Limpar",
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2",
            command=self.limpar_campos
        )
        btn_limpar.pack(side=tk.LEFT, padx=5)
    
    def _criar_botoes_exportacao(self, frame_form: tk.Frame):
        """
        Cria os botões de exportação de dados.
        
        Args:
            frame_form: Frame pai onde os botões serão criados.
        """
        frame_export = tk.LabelFrame(frame_form, text="Exportar Dados", font=("Arial", 10, "bold"))
        frame_export.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")
        
        btn_export_txt = tk.Button(
            frame_export,
            text="TXT",
            bg="#34495e",
            fg="white",
            width=10,
            command=lambda: self.exportar_alunos("txt")
        )
        btn_export_txt.pack(side=tk.LEFT, padx=5, pady=5)
        
        btn_export_csv = tk.Button(
            frame_export,
            text="CSV",
            bg="#16a085",
            fg="white",
            width=10,
            command=lambda: self.exportar_alunos("csv")
        )
        btn_export_csv.pack(side=tk.LEFT, padx=5, pady=5)
        
        btn_export_json = tk.Button(
            frame_export,
            text="JSON",
            bg="#8e44ad",
            fg="white",
            width=10,
            command=lambda: self.exportar_alunos("json")
        )
        btn_export_json.pack(side=tk.LEFT, padx=5, pady=5)
    
    def _criar_tabela_listagem(self, frame_principal: tk.Frame):
        """
        Cria a tabela de listagem de alunos.
        
        Args:
            frame_principal: Frame pai onde a tabela será criada.
        """
        frame_lista = tk.LabelFrame(
            frame_principal,
            text="Alunos Cadastrados",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        frame_lista.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        colunas = ("ID", "Nome", "Email", "Matrícula", "Data Nascimento")
        self.tree = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=20)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Matrícula", text="Matrícula")
        self.tree.heading("Data Nascimento", text="Data Nascimento")
        
        self.tree.column("ID", width=0, stretch=False)
        self.tree.column("Nome", width=180)
        self.tree.column("Email", width=180)
        self.tree.column("Matrícula", width=100)
        self.tree.column("Data Nascimento", width=120)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.bind("<<TreeviewSelect>>", self.ao_selecionar_aluno)
    
    def _normalizar_data(self, valor: str) -> str:
        """
        Converte a data digitada para o padrão ISO (YYYY-MM-DD) aceito pela API.
        
        Aceita entradas nos formatos:
        - YYYY-MM-DD (formato ISO)
        - DD/MM/YYYY (formato brasileiro)
        
        Args:
            valor: String com a data a ser normalizada.
            
        Returns:
            str: Data no formato YYYY-MM-DD.
            
        Raises:
            ValueError: Se a data fornecida não estiver em um formato válido.
        """
        if not valor:
            return ""
        
        texto = valor.strip()
        if not texto:
            return ""
        
        formatos = [
            ("%Y-%m-%d", "%Y-%m-%d"),
            ("%d/%m/%Y", "%Y-%m-%d")
        ]
        
        for formato_entrada, formato_saida in formatos:
            try:
                dt = datetime.strptime(texto, formato_entrada)
                return dt.strftime(formato_saida)
            except ValueError:
                continue
        
        raise ValueError("Data inválida. Use AAAA-MM-DD ou DD/MM/AAAA.")
    
    def _formatar_data_exibicao(self, data_iso: str) -> str:
        """
        Formata data ISO para exibição no formato brasileiro.
        
        Args:
            data_iso: Data no formato YYYY-MM-DD.
            
        Returns:
            str: Data formatada como DD/MM/YYYY ou string vazia se inválida.
        """
        if not data_iso:
            return ""
        
        try:
            dt = datetime.strptime(data_iso, "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        except (ValueError, TypeError):
            return data_iso
    
    def carregar_alunos(self):
        """
        Carrega a lista de alunos da API e exibe na treeview.
        
        Busca todos os alunos cadastrados e atualiza a tabela
        de listagem. Exibe mensagem de erro em caso de falha.
        """
        try:
            resposta = requests.get(f"{self.api_url}/alunos")
            resposta.raise_for_status()
            alunos = resposta.json()
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for aluno in alunos:
                data_formatada = self._formatar_data_exibicao(
                    aluno.get("data_nascimento", "")
                )
                
                self.tree.insert("", tk.END, values=(
                    aluno["id"],
                    aluno["nome"],
                    aluno["email"],
                    aluno["matricula"],
                    data_formatada
                ))
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro ao carregar alunos: {str(erro)}")
    
    def _validar_campos_obrigatorios(self, nome: str, email: str, matricula: str = None) -> bool:
        """
        Valida se os campos obrigatórios foram preenchidos.
        
        Args:
            nome: Nome do aluno.
            email: Email do aluno.
            matricula: Matrícula do aluno (opcional para validação).
            
        Returns:
            bool: True se todos os campos obrigatórios estão preenchidos.
        """
        campos_obrigatorios = [nome, email]
        if matricula is not None:
            campos_obrigatorios.append(matricula)
        
        return all(campos_obrigatorios)
    
    def _preparar_dados_aluno(self, nome: str, email: str, matricula: str = None, data_nasc: str = None) -> dict:
        """
        Prepara os dados do aluno para envio à API.
        
        Args:
            nome: Nome do aluno.
            email: Email do aluno.
            matricula: Matrícula do aluno (opcional).
            data_nasc: Data de nascimento (opcional).
            
        Returns:
            dict: Dicionário com os dados formatados.
            
        Raises:
            ValueError: Se a data fornecida for inválida.
        """
        data_normalizada = None
        if data_nasc:
            data_normalizada = self._normalizar_data(data_nasc)
        
        dados = {
            "nome": nome,
            "email": email,
            "data_nascimento": data_normalizada
        }
        
        if matricula is not None:
            dados["matricula"] = matricula
        
        return dados
    
    def incluir_aluno(self):
        """
        Inclui um novo aluno via API.
        
        Coleta os dados do formulário, valida e envia para a API.
        Atualiza a lista após sucesso ou exibe mensagem de erro.
        """
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        matricula = self.entry_matricula.get().strip()
        data_nasc = self.entry_data_nasc.get().strip()
        
        if not self._validar_campos_obrigatorios(nome, email, matricula):
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios!")
            return
        
        try:
            dados = self._preparar_dados_aluno(nome, email, matricula, data_nasc)
        except ValueError as e:
            messagebox.showwarning("Atenção", str(e))
            return
        
        try:
            resposta = requests.post(f"{self.api_url}/alunos", json=dados)
            resposta.raise_for_status()
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_alunos()
        except requests.exceptions.HTTPError as erro:
            detalhe = erro.response.json().get('detail', str(erro)) if erro.response else str(erro)
            messagebox.showerror("Erro", f"Erro ao cadastrar aluno:\n{detalhe}")
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro de conexão: {str(erro)}")
    
    def alterar_aluno(self):
        """
        Altera os dados de um aluno selecionado.
        
        Valida se há um aluno selecionado, coleta os dados do formulário
        e envia atualização para a API. Atualiza a lista após sucesso.
        """
        if not self.aluno_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um aluno para alterar!")
            return
        
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        data_nasc = self.entry_data_nasc.get().strip()
        
        if not self._validar_campos_obrigatorios(nome, email):
            messagebox.showwarning("Atenção", "Nome e email são obrigatórios!")
            return
        
        try:
            dados = self._preparar_dados_aluno(nome, email, data_nasc=data_nasc)
        except ValueError as e:
            messagebox.showwarning("Atenção", str(e))
            return
        
        try:
            resposta = requests.put(f"{self.api_url}/alunos/{self.aluno_selecionado_id}", json=dados)
            resposta.raise_for_status()
            messagebox.showinfo("Sucesso", "Aluno alterado com sucesso!")
            self.limpar_campos()
            self.carregar_alunos()
        except requests.exceptions.HTTPError as erro:
            detalhe = erro.response.json().get('detail', str(erro)) if erro.response else str(erro)
            messagebox.showerror("Erro", f"Erro ao alterar aluno:\n{detalhe}")
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro de conexão: {str(erro)}")
    
    def excluir_aluno(self):
        """
        Exclui o aluno selecionado.
        
        Solicita confirmação do usuário antes de excluir.
        Atualiza a lista após sucesso ou exibe mensagem de erro.
        """
        if not self.aluno_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um aluno para excluir!")
            return
        
        confirmar = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja realmente excluir o aluno '{self.entry_nome.get()}'?"
        )
        
        if not confirmar:
            return
        
        try:
            resposta = requests.delete(f"{self.api_url}/alunos/{self.aluno_selecionado_id}")
            resposta.raise_for_status()
            messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")
            self.limpar_campos()
            self.carregar_alunos()
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro ao excluir aluno: {str(erro)}")
    
    def ao_selecionar_aluno(self, evento):
        """
        Preenche os campos do formulário ao selecionar um aluno na lista.
        
        Args:
            evento: Evento de seleção da treeview.
        """
        selecao = self.tree.selection()
        if not selecao:
            return
        
        item = self.tree.item(selecao[0])
        valores = item["values"]
        
        self.aluno_selecionado_id = valores[0]
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, valores[1])
        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, valores[2])
        self.entry_matricula.delete(0, tk.END)
        self.entry_matricula.insert(0, valores[3])
        self.entry_matricula.config(state="disabled")
        
        self.entry_data_nasc.delete(0, tk.END)
        if len(valores) > 4 and valores[4]:
            self.entry_data_nasc.insert(0, valores[4])
    
    def limpar_campos(self):
        """
        Limpa todos os campos do formulário.
        
        Remove os valores dos campos de entrada e reabilita
        o campo de matrícula para novos cadastros.
        """
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_matricula.delete(0, tk.END)
        self.entry_matricula.config(state="normal")
        self.entry_data_nasc.delete(0, tk.END)
        self.aluno_selecionado_id = None
    
    def exportar_alunos(self, formato: str):
        """
        Exporta a lista de alunos para arquivo.
        
        Busca os alunos da API e permite salvar em diferentes formatos.
        
        Args:
            formato: Formato do arquivo (txt, csv ou json).
        """
        try:
            resposta = requests.get(f"{self.api_url}/alunos")
            resposta.raise_for_status()
            alunos = resposta.json()
            
            if not alunos:
                messagebox.showwarning("Atenção", "Nenhum aluno para exportar!")
                return
            
            arquivo = filedialog.asksaveasfilename(
                defaultextension=f".{formato}",
                filetypes=[(formato.upper(), f"*.{formato}"), ("Todos os arquivos", "*.*")],
                initialfile=f"alunos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{formato}"
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
                formatador(alunos, arquivo)
                messagebox.showinfo("Sucesso", f"Alunos exportados para {arquivo}")
            else:
                messagebox.showerror("Erro", f"Formato {formato} não suportado!")
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(erro)}")
    
    def _exportar_txt(self, alunos: list, arquivo: str):
        """
        Exporta alunos para formato TXT.
        
        Args:
            alunos: Lista de dicionários com dados dos alunos.
            arquivo: Caminho do arquivo onde será salvo.
        """
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("LISTA DE ALUNOS\n")
            f.write("=" * 80 + "\n\n")
            
            for aluno in alunos:
                f.write(f"ID: {aluno['id']}\n")
                f.write(f"Nome: {aluno['nome']}\n")
                f.write(f"Email: {aluno['email']}\n")
                f.write(f"Matrícula: {aluno['matricula']}\n")
                f.write(f"Data Nascimento: {aluno.get('data_nascimento', 'N/A')}\n")
                f.write("-" * 80 + "\n")
    
    def _exportar_csv(self, alunos: list, arquivo: str):
        """
        Exporta alunos para formato CSV.
        
        Args:
            alunos: Lista de dicionários com dados dos alunos.
            arquivo: Caminho do arquivo onde será salvo.
        """
        with open(arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'nome', 'email', 'matricula', 'data_nascimento'])
            writer.writeheader()
            writer.writerows(alunos)
    
    def _exportar_json(self, alunos: list, arquivo: str):
        """
        Exporta alunos para formato JSON.
        
        Args:
            alunos: Lista de dicionários com dados dos alunos.
            arquivo: Caminho do arquivo onde será salvo.
        """
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(alunos, f, ensure_ascii=False, indent=2)
