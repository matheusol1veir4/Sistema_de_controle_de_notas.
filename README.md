📚 Sistema de Cadastro de Alunos
text
<div><img width="448" height="110" alt="image" src="https://github.com/user-attachments/assets/4febb8e5-750a-4e78-99e1-fab05a493d29" />
</div>
                                                        
  Sistema de Gerenciamento Acadêmico com Python
  
📋 Sobre o Projeto
Sistema completo de cadastro e gerenciamento de alunos, disciplinas e notas desenvolvido em Python, seguindo princípios SOLID e Clean Code. O projeto implementa uma arquitetura em camadas (MVC adaptado) com API REST (FastAPI) e interface gráfica desktop (Tkinter).

🎯 Funcionalidades Principais
✅ CRUD Completo de Alunos, Disciplinas e Notas

✅ Exportação de Dados para TXT, CSV e JSON

✅ Interface Gráfica intuitiva com Tkinter

✅ API REST documentada automaticamente (Swagger/OpenAPI)

✅ Validação de Dados automática com Pydantic

✅ Persistência em banco de dados relacional (PostgreSQL)

🏗️ Arquitetura do Sistema
Estrutura de Diretórios
text
<div><img width="592" height="611" alt="image" src="https://github.com/user-attachments/assets/fcb90ebd-bd4c-47ed-a2aa-c5d4fd9daa03" /></div>


Padrões de Arquitetura
Model-View-Controller (MVC) adaptado para FastAPI

Separation of Concerns: camadas independentes (config, model, service, controller)

Dependency Injection: gerenciamento de sessão do banco de dados

Repository Pattern: abstração de acesso a dados nos services

🚀 **Tecnologias Utilizadas**
**Backend:**

**Python 3.12+**

**FastAPI** - Framework web moderno e rápido

**SQLAlchemy 2.0** - ORM para mapeamento objeto-relacional

**Pydantic** - Validação de dados e schemas

**PostgreSQL 15** - Banco de dados relacional

**Uvicorn** - Servidor ASGI

**Frontend:**

**Tkinter** - Interface gráfica nativa do Python

**Requests** - Cliente HTTP para comunicação com a API

**DevOps:**
**Docker** - Containerização do PostgreSQL

**python-dotenv** - Gerenciamento de variáveis de ambiente

⚙️ Instalação e Configuração
Pré-requisitos
Python 3.12 ou superior

Docker e Docker Compose (opcional, para PostgreSQL)

Git

1. Clone o Repositório
bash
git clone https://github.com/seu-usuario/alunos-sistema.git
cd alunos-sistema
2. Configure o Banco de Dados
Opção A: Usando Docker (Recomendado)

bash
docker run --name postgres-student \
  -e POSTGRES_USER=aluno \
  -e POSTGRES_PASSWORD=senha123 \
  -e POSTGRES_DB=student_db \
  -p 5434:5432 \
  -d postgres:15
Opção B: PostgreSQL Local

Crie um banco de dados chamado student_db e ajuste as credenciais no arquivo .env.

3. Configurar Variáveis de Ambiente
Crie o arquivo .env dentro de student_crud_api/:

text
DATABASE_URL=postgresql://aluno:senha123@localhost:5434/student_db
DB_ECHO=True
DEBUG=True
APP_NAME=Sistema de Cadastro de Alunos
APP_VERSION=1.0.0
4. Instalar Dependências
Backend:

bash
cd student_crud_api
pip install -r requirements.txt
Frontend:

bash
# Tkinter geralmente já vem instalado com Python
# Se não estiver:
sudo apt-get install python3-tk  # Linux/Ubuntu
🎮 Como Executar
1. Iniciar o Backend (API)
bash
cd student_crud_api
python3 main.py
A API estará disponível em:

Aplicação: http://localhost:8000

Documentação Swagger: http://localhost:8000/docs

Health Check: http://localhost:8000/health

2. Iniciar o Frontend (Interface Gráfica)
Em outro terminal:

bash
cd frontend
python3 main_window.py
A interface gráfica será aberta automaticamente.

📖 Documentação da API
Endpoints Disponíveis
Alunos (/api/v1/alunos)
GET /api/v1/alunos - Listar todos os alunos (paginação disponível)

GET /api/v1/alunos/{id} - Buscar aluno por ID

POST /api/v1/alunos - Criar novo aluno

PUT /api/v1/alunos/{id} - Atualizar aluno

DELETE /api/v1/alunos/{id} - Excluir aluno

Disciplinas (/api/v1/disciplinas)
GET /api/v1/disciplinas - Listar todas as disciplinas

GET /api/v1/disciplinas/{id} - Buscar disciplina por ID

POST /api/v1/disciplinas - Criar nova disciplina

PUT /api/v1/disciplinas/{id} - Atualizar disciplina

DELETE /api/v1/disciplinas/{id} - Excluir disciplina

Notas (/api/v1/notas)
GET /api/v1/notas - Listar todas as notas

GET /api/v1/notas/{id} - Buscar nota por ID

GET /api/v1/notas/aluno/{aluno_id} - Listar notas de um aluno

GET /api/v1/notas/disciplina/{disciplina_id} - Listar notas de uma disciplina

POST /api/v1/notas - Lançar nova nota

PUT /api/v1/notas/{id} - Atualizar nota

DELETE /api/v1/notas/{id} - Excluir nota

Exemplo de Requisição
bash
# Criar um aluno
curl -X POST "http://localhost:8000/api/v1/alunos" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao.silva@email.com",
    "matricula": "2024001",
    "data_nascimento": "2000-05-15"
  }'
🖥️ Usando a Interface Gráfica
Tela Principal
A janela principal oferece três opções:

📚 Alunos - Gerenciar cadastro de alunos

📖 Disciplinas - Gerenciar disciplinas

📝 Notas - Lançar e consultar notas

Funcionalidades por Módulo
Gerenciador de Alunos:

Formulário para inclusão/alteração de dados

Lista completa de alunos cadastrados

Exportação para TXT, CSV ou JSON

Validação de email e matrícula única

Gerenciador de Disciplinas:

Cadastro de código, nome e carga horária

Validação de código único

Exportação de dados

Gerenciador de Notas:

Seleção de aluno e disciplina via combobox

Validação de nota (0 a 10)

Registro de semestre

Exportação de histórico

🗄️ Modelo de Dados
Diagrama Entidade-Relacionamento
text
<div><img width="579" height="220" alt="image" src="https://github.com/user-attachments/assets/628bca82-df55-467c-9469-dc74aee284de" /></div>

📦 Dependências do Projeto
text
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
requests==2.31.0
🧪 Testando a Aplicação
Teste Manual via Swagger
Acesse http://localhost:8000/docs

Clique em qualquer endpoint

Clique em "Try it out"

Preencha os dados e execute

Veja a resposta em tempo real

Teste via Frontend
Execute a interface gráfica

Clique em "📚 Alunos"

Preencha o formulário e clique "➕ Incluir"

Veja o aluno aparecer na lista à direita

Clique em "📄 TXT" para exportar

🛠️ Solução de Problemas
Erro: "ModuleNotFoundError: No module named 'tkinter'"
bash
# Linux/Ubuntu
sudo apt-get install python3-tk

# Verificar instalação
python3 -c "import tkinter; print('Tkinter OK!')"
Erro: "Não foi possível conectar à API"
Verifique se a API está rodando (python3 main.py)

Confirme que está na porta 8000

Teste: curl http://localhost:8000/health

Erro: "password authentication failed"
Verifique o arquivo .env

Confirme as credenciais do Docker:

bash
docker exec -it postgres-student psql -U aluno -d student_db
🤝 Contribuindo
Contribuições são bem-vindas! Para contribuir:

Fork o projeto

Crie uma branch para sua feature (git checkout -b feature/MinhaFeature)

Commit suas mudanças (git commit -m 'Adiciona MinhaFeature')

Push para a branch (git push origin feature/MinhaFeature)

Abra um Pull Request

📄 Licença
Este projeto foi desenvolvido para fins acadêmicos como trabalho da disciplina de Desenvolvimento Rápido em Python.

👤 Autor
Matheus Oliveira

GitHub:matheusol1veir4

Email: matheus.colvr@gmail.com

📞 Suporte
Para dúvidas ou problemas:

Entre em contato via email

🎓 Agradecimentos
Professores e colegas da disciplina

Comunidade Python Brasil

Documentação oficial do FastAPI e SQLAlchemy
