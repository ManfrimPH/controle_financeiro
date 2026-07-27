# Controle Financeiro - Telegram Bot

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4479A1?logo=postgresql&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?logo=googlesheets&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

Bot Telegram para gestao de financas pessoais. Registre ganhos e gastos pelo chat e visualize no Google Sheets + Looker Studio.

---

## Comandos

| Comando | Descricao |
|---------|-----------|
| `/add` | Registrar ganho ou gasto (fluxo guiado) |
| `/del` | Remover o ultimo registro |
| `/list` | Mostrar ultimos 5 ganhos e 5 gastos |
| `/summary` | Resumo do mes atual por categoria |
| `/update` | Sincronizar dados com Google Sheets |
| `/cancel` | Cancelar operacao em andamento |

---

## Arquitetura

```
Telegram  -->  Bot (Python)  -->  PostgreSQL  -->  Google Sheets  -->  Looker Studio
                    |                   |
               Conversation        Connection Pool
               Manager             (Threaded)
```

## Estrutura do Projeto

```
controle_financeiro/
├── main.py              # Core do bot, handlers, menu de comandos
├── add.py               # Fluxo de adicao (gain + spent)
├── delete.py            # Fluxo de delecao
├── update.py            # Sincronizacao banco -> Google Sheets
├── data_base.py         # Camada de compatibilidade (dicts -> dataclasses)
├── db.py                # Connection pool + repositorios (tuplas)
├── models.py            # Dataclasses tipadas (GainEntry, SpentEntry)
├── validators.py        # Validacao de entrada (moeda, data, texto)
├── exceptions.py        # Excecoes estruturadas com mensagens amigaveis
├── conversation.py      # Gerenciador de conversas multi-usuario
├── commands.py          # Handlers de /list e /summary
├── Dockerfile           # Imagem do bot (python:3.12-slim)
├── docker-compose.yml   # Orquestracao (db + bot)
├── init.sql             # Schema automatico do banco
├── .env.example         # Template de variaveis de ambiente
├── requirements.txt     # Dependencias Python
├── credentials.json     # Service account Google Sheets (nao versionado)
├── .gitignore
├── .dockerignore
└── tests/
    ├── test_validators.py
    ├── test_conversation.py
    └── test_models.py
```

---

## Instalacao e Execucao

### Via Docker (recomendado)

```bash
git clone https://github.com/ManfrimPH/controle_financeiro.git
cd controle_financeiro

cp .env.example .env
# Edite .env com seu BOT_KEY, DB_PASSWORD e SPREADSHEET_ID

# Coloque seu credentials.json do Google Sheets na raiz

docker compose up -d
```

### Via Python direto

```bash
pip install -r requirements.txt
python main.py
```

### Executar testes

```bash
pytest tests/ -v
```

---

## Stack

- **Python 3.12** com pyTelegramBotAPI
- **PostgreSQL 16** (Docker, Alpine)
- **Google Sheets API v4** (service account)
- **Docker Compose** com healthcheck
- **GitHub Actions** (CI)

## Autor

Desenvolvido por **ManfrimPH**.
