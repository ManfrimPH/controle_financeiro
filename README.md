
# 💰 Controle Financeiro - Telegram Bot

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4479A1?style=flat&logo=postgresql&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=flat&logo=googlesheets&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)

Sistema para gestão de finanças pessoais que permite registrar gastos e ganhos via Telegram. O projeto utiliza **PostgreSQL** como storage principal e o **Google Sheets** como interface de visualização rápida e espelhamento para BI.

---

## 🚀 Arquitetura e Fluxo de Dados

1.  **Ingestão:** O usuário envia os dados através do Bot do Telegram.
2.  **Persistência:** O script `add.py` processa e insere as informações no PostgreSQL.
3.  **Manutenção:** O script `delete.py` permite a remoção atômica do último registro inserido no banco.
4.  **Sincronização (ETL):** O script `update.py` extrai os dados do banco e injeta-os no Google Sheets.
5.  **Visualização:** Dashboard no Looker Studio conectado à planilha (ou diretamente ao banco via túnel).

> ⚠️ **Nota Técnica:** O módulo `update.py` é uma ponte de sincronização para o Google Sheets. Se o sistema for implantado em um servidor com IP fixo/URL e os dados forem consumidos diretamente do PostgreSQL pelo BI, este módulo torna-se opcional.

---

## 📊 Dashboard (Template Copiável)

Você pode visualizar e utilizar o modelo de dashboard estruturado para este projeto no link abaixo:

👉 **[Acessar Template do Looker Studio](https://lookerstudio.google.com/u/0/reporting/620d918c-6088-4950-aa84-2ac594fe84c6/page/VoisF)**

**Como copiar para você:**
1. Abra o link acima.
2. No canto superior direito, clique nos três pontos (⋮) e selecione **"Fazer uma cópia"**.
3. Conecte a sua própria **Google Sheet** (gerada pelo bot) ou seu banco **PostgreSQL** como nova fonte de dados.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Banco de Dados:** PostgreSQL (Relacional)
* **Cloud API:** Google Sheets API v4 (gspread)
* **Infraestrutura:** Docker & Docker Compose
* **Interface:** Telegram Bot API

---

## 📋 Pré-requisitos

* [Git](https://git-scm.com/) e [Docker](https://www.docker.com/) instalados.
* Token de API do [@BotFather](https://t.me/botfather).
* Conta de Serviço (JSON) configurada no Google Cloud Console com acesso ao Sheets.

---

## 🔧 Instalação e Execução

### 1. Clonar o Repositório
```bash
git clone [https://github.com/ManfrimPH/controle_financeiro.git](https://github.com/ManfrimPH/controle_financeiro.git)
cd controle_financeiro
```

### 2. Configurar Credenciais
* Configure as variáveis de conexão (host, user, password) no arquivo `data_base.py`.
* Adicione o arquivo `credentials.json` na raiz do projeto.

### 3. Provisionar o Banco (Docker)
```bash
docker-compose up -d
```

### 4. Executar o Bot
```bash
# Instalação das dependências necessárias
pip install -r requirements.txt

# Inicialização do serviço
python main.py
```

---

## 📂 Estrutura do Projeto

| Arquivo | Descrição |
| :--- | :--- |
| `main.py` | Core do Bot: Gerencia comandos e interação com usuário. |
| `add.py` | Módulo de escrita (INSERT) no PostgreSQL. |
| `delete.py` | Módulo de rollback/deleção do último registro. |
| `update.py` | Job de sincronização Banco -> Google Sheets. |
| `data_base.py` | Camada de abstração de dados e drivers de conexão. |
| `*.sql` | Definição de Schema (DDL) para as tabelas de ganhos e gastos. |
| `docker-compose.yml` | Orquestração do ambiente de banco de dados. |
| `requirements.txt` | Lista de dependências do projeto. |

---

## 👤 Autor
Desenvolvido por **ManfrimPH**.
