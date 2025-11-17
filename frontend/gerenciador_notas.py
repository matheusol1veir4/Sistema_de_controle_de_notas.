"""
Gerenciador de Notas - Interface Tkinter.

Permite listar, incluir, alterar, excluir e exportar notas.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from datetime import datetime
import json
import csv


class GerenciadorNotas:
    """
    Janela de gerenciamento de notas.
    
    Implementa CRUD completo e exportação para TXT, CSV e JSON.
    Gerencia a interface gráfica para operações com notas,
    incluindo validação de dados e tratamento de erros.
    """
    
    def __init__(self, api_url: str):
        """
        Inicializa o gerenciador de notas.
        
        Args:
            api_url: URL base da API FastAPI.
        """
        self.api_url = api_url
        self.janela = tk.Toplevel()
        self.janela.title("Gerenciar Notas")
        self.janela.geometry("1300x750")
        self.janela.resizable(True, True)
        
        self.nota_selecionada_id = None
        self.alunos = []
        self.disciplinas = []
        
        self.configurar_interface()
        self.carregar_alunos()
        self.carregar_disciplinas()
        self.carregar_notas()
    
    def configurar_interface(self):
        """
        Configura os componentes da interface gráfica.
        
        Cria e organiza todos os elementos visuais da janela,
        incluindo formulário, botões de ação e tabela de listagem.
        """
        frame_topo = tk.Frame(self.janela, bg="#e74c3c", height=60)
        frame_topo.pack(fill=tk.X)
        
        titulo = tk.Label(
            frame_topo,
            text="Gerenciamento de Notas",
            font=("Arial", 16, "bold"),
            bg="#e74c3c",
            fg="white"
        )
        titulo.pack(pady=15)
        
        frame_principal = tk.Frame(self.janela)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        frame_form = tk.LabelFrame(
            frame_principal,
            text="Dados da Nota",
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
        tk.Label(frame_form, text="Aluno:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.combo_aluno = ttk.Combobox(frame_form, width=28, font=("Arial", 10), state="readonly")
        self.combo_aluno.grid(row=0, column=1, pady=5)
        
        tk.Label(frame_form, text="Disciplina:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.combo_disciplina = ttk.Combobox(frame_form, width=28, font=("Arial", 10), state="readonly")
        self.combo_disciplina.grid(row=1, column=1, pady=5)
        
        tk.Label(frame_form, text="Valor (0-10):", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_valor = tk.Entry(frame_form, width=30, font=("Arial", 10))
        self.entry_valor.grid(row=2, column=1, pady=5)
        
        tk.Label(frame_form, text="Semestre:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.entry_semestre = tk.Entry(frame_form, width=30, font=("Arial", 10))
        self.entry_semestre.grid(row=3, column=1, pady=5)
        tk.Label(frame_form, text="(Ex: 2024.1)", font=("Arial", 8), fg="gray").grid(row=4, column=1, sticky="w")
    
    def _criar_botoes_acao(self, frame_form: tk.Frame):
        """
        Cria os botões de ação do formulário.
        
        Args:
            frame_form: Frame pai onde os botões serão criados.
        """
        frame_botoes = tk.Frame(frame_form)
        frame_botoes.grid(row=5, column=0, columnspan=2, pady=20)
        
        botoes_config = [
            ("Incluir", "#27ae60", self.incluir_nota),
            ("Alterar", "#f39c12", self.alterar_nota),
            ("Excluir", "#e74c3c", self.excluir_nota),
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
        frame_export.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")
        
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
                command=lambda f=formato.lower(): self.exportar_notas(f)
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def _criar_tabela_listagem(self, frame_principal: tk.Frame):
        """
        Cria a tabela de listagem de notas.
        
        Args:
            frame_principal: Frame pai onde a tabela será criada.
        """
        frame_lista = tk.LabelFrame(
            frame_principal,
            text="Notas Cadastradas",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        frame_lista.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        colunas = ("ID", "Aluno", "Disciplina", "Nota", "Semestre")
        self.tree = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=22)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Aluno", text="Aluno")
        self.tree.heading("Disciplina", text="Disciplina")
        self.tree.heading("Nota", text="Nota")
        self.tree.heading("Semestre", text="Semestre")
        
        self.tree.column("ID", width=0, stretch=False)
        self.tree.column("Aluno", width=200)
        self.tree.column("Disciplina", width=250)
        self.tree.column("Nota", width=80)
        self.tree.column("Semestre", width=100)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.bind("<<TreeviewSelect>>", self.ao_selecionar_nota)
    
    def carregar_alunos(self):
        """
        Carrega a lista de alunos da API.
        
        Busca todos os alunos cadastrados e preenche o combobox.
        Exibe mensagem de erro em caso de falha.
        """
        try:
            resposta = requests.get(f"{self.api_url}/alunos")
            resposta.raise_for_status()
            self.alunos = resposta.json()
            
            nomes = [f"{aluno['nome']} ({aluno['matricula']})" for aluno in self.alunos]
            self.combo_aluno['values'] = nomes
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro ao carregar alunos: {str(erro)}")
    
    def carregar_disciplinas(self):
        """
        Carrega a lista de disciplinas da API.
        
        Busca todas as disciplinas cadastradas e preenche o combobox.
        Exibe mensagem de erro em caso de falha.
        """
        try:
            resposta = requests.get(f"{self.api_url}/disciplinas")
            resposta.raise_for_status()
            self.disciplinas = resposta.json()
            
            nomes = [f"{disc['nome']} ({disc['codigo']})" for disc in self.disciplinas]
            self.combo_disciplina['values'] = nomes
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro ao carregar disciplinas: {str(erro)}")
    
    def carregar_notas(self):
        """
        Carrega a lista de notas da API e exibe na treeview.
        
        Busca todas as notas cadastradas e atualiza a tabela
        de listagem. Exibe mensagem de erro em caso de falha.
        """
        try:
            resposta = requests.get(f"{self.api_url}/notas")
            resposta.raise_for_status()
            notas = resposta.json()
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for nota in notas:
                nome_aluno = self.obter_nome_aluno(nota["aluno_id"])
                nome_disciplina = self.obter_nome_disciplina(nota["disciplina_id"])
                
                self.tree.insert("", tk.END, values=(
                    nota["id"],
                    nome_aluno,
                    nome_disciplina,
                    f"{nota['valor']:.1f}",
                    nota["semestre"]
                ))
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro ao carregar notas: {str(erro)}")
    
    def obter_nome_aluno(self, aluno_id: str) -> str:
        """
        Retorna o nome do aluno pelo ID.
        
        Args:
            aluno_id: ID do aluno a ser buscado.
            
        Returns:
            str: Nome do aluno ou "Desconhecido" se não encontrado.
        """
        for aluno in self.alunos:
            if aluno["id"] == aluno_id:
                return aluno["nome"]
        return "Desconhecido"
    
    def obter_nome_disciplina(self, disciplina_id: str) -> str:
        """
        Retorna o nome da disciplina pelo ID.
        
        Args:
            disciplina_id: ID da disciplina a ser buscada.
            
        Returns:
            str: Nome da disciplina ou "Desconhecida" se não encontrada.
        """
        for disc in self.disciplinas:
            if disc["id"] == disciplina_id:
                return disc["nome"]
        return "Desconhecida"
    
    def obter_id_aluno_selecionado(self) -> str:
        """
        Retorna o ID do aluno selecionado no combobox.
        
        Returns:
            str: ID do aluno selecionado ou None se nenhum estiver selecionado.
        """
        indice = self.combo_aluno.current()
        if indice >= 0:
            return self.alunos[indice]["id"]
        return None
    
    def obter_id_disciplina_selecionada(self) -> str:
        """
        Retorna o ID da disciplina selecionada no combobox.
        
        Returns:
            str: ID da disciplina selecionada ou None se nenhuma estiver selecionada.
        """
        indice = self.combo_disciplina.current()
        if indice >= 0:
            return self.disciplinas[indice]["id"]
        return None
    
    def _validar_valor_nota(self, valor_str: str) -> float:
        """
        Valida e converte o valor da nota para float.
        
        Args:
            valor_str: String com o valor da nota.
            
        Returns:
            float: Valor da nota convertido.
            
        Raises:
            ValueError: Se o valor não for um número válido ou estiver fora do intervalo.
        """
        try:
            valor = float(valor_str)
            if not 0 <= valor <= 10:
                raise ValueError("Nota deve estar entre 0 e 10")
            return valor
        except ValueError as e:
            if "could not convert" in str(e).lower():
                raise ValueError("Valor deve ser um número válido")
            raise
    
    def incluir_nota(self):
        """
        Inclui uma nova nota via API.
        
        Coleta os dados do formulário, valida e envia para a API.
        Atualiza a lista após sucesso ou exibe mensagem de erro.
        """
        aluno_id = self.obter_id_aluno_selecionado()
        disciplina_id = self.obter_id_disciplina_selecionada()
        valor_str = self.entry_valor.get().strip()
        semestre = self.entry_semestre.get().strip()
        
        if not aluno_id or not disciplina_id or not valor_str or not semestre:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        
        try:
            valor = self._validar_valor_nota(valor_str)
        except ValueError as e:
            messagebox.showerror("Erro", f"Valor inválido: {str(e)}")
            return
        
        dados = {
            "aluno_id": aluno_id,
            "disciplina_id": disciplina_id,
            "valor": valor,
            "semestre": semestre
        }
        
        try:
            resposta = requests.post(f"{self.api_url}/notas", json=dados)
            resposta.raise_for_status()
            messagebox.showinfo("Sucesso", "Nota cadastrada com sucesso!")
            self.limpar_campos()
            self.carregar_notas()
        except requests.exceptions.HTTPError as erro:
            detalhe = erro.response.json().get('detail', str(erro)) if erro.response else str(erro)
            messagebox.showerror("Erro", f"Erro ao cadastrar nota:\n{detalhe}")
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro de conexão: {str(erro)}")
    
    def alterar_nota(self):
        """
        Altera os dados de uma nota selecionada.
        
        Valida se há uma nota selecionada, coleta os dados do formulário
        e envia atualização para a API. Atualiza a lista após sucesso.
        """
        if not self.nota_selecionada_id:
            messagebox.showwarning("Atenção", "Selecione uma nota para alterar!")
            return
        
        valor_str = self.entry_valor.get().strip()
        semestre = self.entry_semestre.get().strip()
        
        if not valor_str or not semestre:
            messagebox.showwarning("Atenção", "Valor e semestre são obrigatórios!")
            return
        
        try:
            valor = self._validar_valor_nota(valor_str)
        except ValueError as e:
            messagebox.showerror("Erro", f"Valor inválido: {str(e)}")
            return
        
        dados = {
            "valor": valor,
            "semestre": semestre
        }
        
        try:
            resposta = requests.put(f"{self.api_url}/notas/{self.nota_selecionada_id}", json=dados)
            resposta.raise_for_status()
            messagebox.showinfo("Sucesso", "Nota alterada com sucesso!")
            self.limpar_campos()
            self.carregar_notas()
        except requests.exceptions.HTTPError as erro:
            detalhe = erro.response.json().get('detail', str(erro)) if erro.response else str(erro)
            messagebox.showerror("Erro", f"Erro ao alterar nota:\n{detalhe}")
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro de conexão: {str(erro)}")
    
    def excluir_nota(self):
        """Exclui a nota selecionada."""
        if not self.nota_selecionada_id:
            messagebox.showwarning("Atenção", "Selecione uma nota para excluir!")
            return
        
        confirmar = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja realmente excluir esta nota?"
        )
        
        if not confirmar:
            return
        
        try:
            resposta = requests.delete(f"{self.api_url}/notas/{self.nota_selecionada_id}")
            resposta.raise_for_status()
            messagebox.showinfo("Sucesso", "Nota excluída com sucesso!")
            self.limpar_campos()
            self.carregar_notas()
        
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro ao excluir nota: {str(erro)}")
    
    def ao_selecionar_nota(self, evento):
        """
        Preenche os campos do formulário ao selecionar uma nota na lista.
        
        Args:
            evento: Evento de seleção da treeview.
        """
        selecao = self.tree.selection()
        if not selecao:
            return
        
        item = self.tree.item(selecao[0])
        valores = item["values"]
        
        self.nota_selecionada_id = valores[0]
        
        self.combo_aluno.config(state="disabled")
        self.combo_disciplina.config(state="disabled")
        
        self.entry_valor.delete(0, tk.END)
        self.entry_valor.insert(0, valores[3])
        self.entry_semestre.delete(0, tk.END)
        self.entry_semestre.insert(0, valores[4])
    
    def limpar_campos(self):
        """Limpa todos os campos do formulário."""
        self.combo_aluno.set('')
        self.combo_aluno.config(state="readonly")
        self.combo_disciplina.set('')
        self.combo_disciplina.config(state="readonly")
        self.entry_valor.delete(0, tk.END)
        self.entry_semestre.delete(0, tk.END)
        self.nota_selecionada_id = None
    
    def exportar_notas(self, formato: str):
        """
        Exporta a lista de notas para arquivo.
        
        Busca as notas da API e permite salvar em diferentes formatos.
        
        Args:
            formato: Formato do arquivo (txt, csv ou json).
        """
        try:
            resposta = requests.get(f"{self.api_url}/notas")
            resposta.raise_for_status()
            notas = resposta.json()
            
            if not notas:
                messagebox.showwarning("Atenção", "Nenhuma nota para exportar!")
                return
            
            notas_completas = []
            for nota in notas:
                nota_completa = nota.copy()
                nota_completa['nome_aluno'] = self.obter_nome_aluno(nota['aluno_id'])
                nota_completa['nome_disciplina'] = self.obter_nome_disciplina(nota['disciplina_id'])
                notas_completas.append(nota_completa)
            
            arquivo = filedialog.asksaveasfilename(
                defaultextension=f".{formato}",
                filetypes=[(formato.upper(), f"*.{formato}"), ("Todos os arquivos", "*.*")],
                initialfile=f"notas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{formato}"
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
                formatador(notas_completas, arquivo)
                messagebox.showinfo("Sucesso", f"Notas exportadas para {arquivo}")
            else:
                messagebox.showerror("Erro", f"Formato {formato} não suportado!")
        except requests.exceptions.RequestException as erro:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(erro)}")
    
    def _exportar_txt(self, notas: list, arquivo: str):
        """Exporta notas para formato TXT."""
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("LISTA DE NOTAS\n")
            f.write("=" * 80 + "\n\n")
            
            for nota in notas:
                f.write(f"Aluno: {nota['nome_aluno']}\n")
                f.write(f"Disciplina: {nota['nome_disciplina']}\n")
                f.write(f"Nota: {nota['valor']:.1f}\n")
                f.write(f"Semestre: {nota['semestre']}\n")
                f.write("-" * 80 + "\n")
    
    def _exportar_csv(self, notas: list, arquivo: str):
        """Exporta notas para formato CSV."""
        with open(arquivo, 'w', newline='', encoding='utf-8') as f:
            campos = ['nome_aluno', 'nome_disciplina', 'valor', 'semestre']
            writer = csv.DictWriter(f, fieldnames=campos, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(notas)
    
    def _exportar_json(self, notas: list, arquivo: str):
        """Exporta notas para formato JSON."""
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(notas, f, ensure_ascii=False, indent=2)
