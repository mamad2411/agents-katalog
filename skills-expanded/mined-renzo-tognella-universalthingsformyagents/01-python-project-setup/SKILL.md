---
name: Python Project Setup & Structure
description: Configuração de projeto Python moderno com pyproject.toml, uv/pip, estrutura de diretórios para servidor MCP, e boas práticas de packaging.
---

# Python Project Setup & Structure

## Quando Usar

- Ao iniciar um novo projeto Python para o TheSearch
- Ao adicionar dependências ou reestruturar módulos
- Ao configurar ambientes de desenvolvimento

## Princípios

1. **pyproject.toml** é o padrão moderno — nunca use `setup.py` ou `requirements.txt` como fonte primária
2. **uv** é o gerenciador de pacotes preferido (10-100x mais rápido que pip)
3. **Python >= 3.11** obrigatório (union types `X | Y`, `StrEnum`, `tomllib`)
4. **Estrutura flat** — sem namespaces desnecessários

## Estrutura de Referência

```
memory-server/
├── server/           # Camada MCP (interface)
│   ├── __init__.py
│   ├── main.py       # Entry point
│   ├── tools.py      # Tools MCP
│   ├── resources.py  # Resources MCP
│   └── prompts.py    # Prompts MCP
├── models/           # Modelos Pydantic (contratos)
├── services/         # Lógica de negócio
├── scripts/          # Scripts utilitários (bootstrap, migrations)
├── tests/            # Testes (pytest)
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── pyproject.toml
├── .env.example
└── README.md
```

## Dependências Core

```toml
[project]
name = "memory-server"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "mcp[cli]>=1.26.0",
    "qdrant-client>=1.13,<1.15",
    "neo4j>=5.0",
    "pydantic>=2.0",
    "openai>=1.0",
    "instructor>=1.0",
    "httpx>=0.27",
    "python-dotenv>=1.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-asyncio>=0.23", "ruff>=0.3"]
```

## Comandos Essenciais

```bash
# Instalar com uv (preferido)
uv pip install -e ".[dev]"

# Instalar com pip (fallback)
pip install -e ".[dev]"

# Verificar versão Python
python --version  # >= 3.11

# Lint
ruff check .

# Formatar
ruff format .
```

## Variáveis de Ambiente

Sempre usar `.env` via `python-dotenv`. Nunca hardcodar credenciais:

```env
OPENAI_API_KEY=sk-...
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=memories
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=512
```

## Regras

- Todo módulo Python deve ter `__init__.py`
- Imports absolutos sempre (nunca `from ..services import`)
- Um arquivo por classe/conceito principal
- Nomes de arquivos em `snake_case`
- Nomes de classes em `PascalCase`
