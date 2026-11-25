---
name: python-runtime
description: Python toolchain configuration and best practices. Use when setting up Ruff, pytest, mypy type hints, dependency management, virtual environments or Python project standards.
---

# Python Runtime

Skill para configurar y mantener toolchains Python modernos: Ruff (linting + formatting), pytest, type hints con mypy, gestión de dependencias, virtual environments y estándares de proyecto.

## Principios fundamentales

- Python 3.12+ como runtime mínimo.
- Ruff como linter y formatter unificado (reemplaza flake8, isort, black, pyflakes).
- pytest como test runner con plugins (pytest-cov, pytest-asyncio, hypothesis).
- Type hints obligatorios en funciones públicas. mypy o pyright para validación estática.
- Virtual environments siempre. Nunca instalar dependencias globalmente.

## Estructura de proyecto recomendada

```
proyecto/
├── src/
│   └── mi_paquete/
│       ├── __init__.py
│       ├── handlers/
│       ├── services/
│       ├── repositories/
│       ├── models/
│       └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## pyproject.toml recomendado

```toml
[project]
name = "mi-proyecto"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "aws-lambda-powertools[all]>=2.0.0",
    "pydantic>=2.0.0",
    "boto3>=1.34.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.4.0",
    "mypy>=1.10.0",
    "pytest>=8.0.0",
    "pytest-cov>=5.0.0",
    "pytest-asyncio>=0.23.0",
    "hypothesis>=6.100.0",
    "boto3-stubs[dynamodb,s3,sqs]",
    "moto[dynamodb,s3,sqs]>=5.0.0",
]

[tool.ruff]
target-version = "py312"
line-length = 120

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
    "TCH",  # flake8-type-checking
    "RUF",  # ruff-specific rules
]
ignore = ["E501"]  # line length handled by formatter

[tool.ruff.lint.isort]
known-first-party = ["mi_paquete"]

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow tests",
]
```

## Ruff: linting y formatting unificado

```bash
# Lint
ruff check .

# Lint con auto-fix
ruff check --fix .

# Format (reemplaza black)
ruff format .

# Check + format en CI
ruff check . && ruff format --check .
```

### Por qué Ruff sobre flake8/black/isort
- 10-100x más rápido que flake8 + black + isort combinados.
- Un solo binario, una sola configuración en `pyproject.toml`.
- Compatible con reglas de flake8, isort, pyupgrade, bugbear y más.
- Auto-fix para la mayoría de reglas.

## Type hints y mypy

### Patrones de tipado
```python
from typing import Any
from collections.abc import Sequence

# Funciones públicas: tipos explícitos siempre
def create_order(items: list[dict[str, Any]], customer_id: str) -> dict[str, str]:
    ...

# Variables locales: inferencia está bien
total = sum(item["price"] for item in items)  # mypy infiere float

# Optional explícito
def find_user(user_id: str) -> dict[str, Any] | None:
    ...

# TypedDict para estructuras conocidas
from typing import TypedDict

class OrderItem(TypedDict):
    name: str
    price: float
    quantity: int
```

## pytest: configuración y patrones

### Fixtures reutilizables
```python
# tests/conftest.py
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_dynamodb_table():
    table = MagicMock()
    table.query.return_value = {"Items": []}
    table.put_item.return_value = {}
    return table

@pytest.fixture
def order_service(mock_dynamodb_table):
    from mi_paquete.services.order import OrderService
    return OrderService(table=mock_dynamodb_table)
```

### Parametrize para múltiples casos
```python
@pytest.mark.parametrize("price,discount,expected", [
    (100.0, 0.1, 90.0),
    (100.0, 0.0, 100.0),
    (50.0, 0.5, 25.0),
    (0.01, 1.0, 0.0),
])
def test_apply_discount(price, discount, expected):
    assert apply_discount(price, discount) == pytest.approx(expected)
```

## Virtual environments

```bash
# Crear venv
python -m venv .venv

# Activar
source .venv/bin/activate

# Instalar dependencias
pip install -e ".[dev]"

# Freeze para reproducibilidad
pip freeze > requirements.txt
```

## Scripts de desarrollo (Makefile o scripts)

```makefile
.PHONY: lint format test typecheck all

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy src/

test:
	pytest tests/ -v --tb=short

test-cov:
	pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=80

all: lint typecheck test
```

## Anti-patrones a evitar

- ❌ No usar type hints en funciones públicas.
- ❌ `requirements.txt` sin versiones pinneadas.
- ❌ Instalar dependencias globalmente (sin venv).
- ❌ Usar `print()` para debugging en lugar de logging.
- ❌ Imports circulares entre módulos.
- ❌ `except Exception: pass` (silenciar errores).
- ❌ Mezclar lógica de negocio con I/O (dificulta testing).
- ❌ No tener `conftest.py` con fixtures compartidas.
- ❌ Tests sin assertions (solo ejecutan código sin verificar).
- ❌ Ignorar warnings de mypy/ruff.

## Checklist de proyecto Python

- [ ] Python 3.12+ como runtime.
- [ ] `pyproject.toml` con Ruff, mypy y pytest configurados.
- [ ] Virtual environment creado y `.venv` en `.gitignore`.
- [ ] Ruff como linter y formatter (reemplaza flake8/black/isort).
- [ ] mypy con `strict = true` para type checking.
- [ ] pytest con fixtures en `conftest.py`.
- [ ] Coverage mínimo 80% configurado.
- [ ] Type hints en todas las funciones públicas.
- [ ] Dependencias pinneadas en requirements.txt.
- [ ] Scripts de desarrollo (lint, format, test, typecheck).
