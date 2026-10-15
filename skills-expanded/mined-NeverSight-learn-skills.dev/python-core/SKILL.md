---
name: python-core
description: "Guía principal de desarrollo Python (3.13/3.14). Cubre type hints modernas, async/await, uv (package manager), stdlib, free-threaded Python (3.14), template strings, Pydantic v2 para modelos, y fundamentos del ecosistema. Actívala para cualquier tarea Python: nuevas features, revisión de código, migraciones de versión. Las sub-skills del kit profundizan en dominios específicos."
---

# Python Core Development Guide

Guía canónica para desarrollo Python moderno. Python 3.14 es la versión estable (Oct 2025). Python 3.13 como LTS base.

## Versiones

| Versión | Lanzamiento | Fin de soporte | Novedades clave |
|---------|-------------|----------------|-----------------|
| Python 3.12 | Oct 2023 | Abr 2029 | `type` statement, f-string mejorado, perf profiler |
| Python 3.13 | Oct 2024 | Oct 2029 | Free-threaded (experimental), JIT compiler (Tier 2), `TaskGroup` estable |
| **Python 3.14** | **Oct 2025** | **Oct 2031** | **Free-threaded oficial**, **template strings**, deferred annotations |

- **Proyectos nuevos** → Python 3.14. Free-threaded y template strings valen la pena.
- **Producción conservadora** → Python 3.13 (último año de bugfixes).

---

## uv — Package manager (Rust, 10-100x pip)

```bash
# Instalar uv (reemplaza pip, pipx, poetry, pyenv)
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/macOS
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# Crear proyecto
uv init miapp
cd miapp

# Agregar dependencias
uv add fastapi uvicorn[standard] sqlalchemy pydantic
uv add --dev pytest pytest-asyncio httpx ruff

# Crear virtualenv automáticamente
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Ejecutar scripts
uv run python main.py
uv run pytest
uv run ruff check .

# Lock file (determinístico como poetry.lock)
uv lock
uv sync  # Instala exactamente lo del lock
```

---

## Type Hints modernas (Python 3.13+)

```python
# ✅ Type hints nativas sin imports (PEP 695, Python 3.12+)
type Point = tuple[float, float]
type OrderStatus = Literal["pending", "confirmed", "shipped"]

# ✅ Generics simplificados (Python 3.12+)
def first[T](items: list[T]) -> T | None:
    return items[0] if items else None

# ✅ Union con | (Python 3.10+)
def get_order(order_id: str) -> Order | None:
    ...

# ✅ TypedDict para diccionarios estructurados
from typing import TypedDict

class OrderDict(TypedDict):
    id: str
    customer_id: str
    status: OrderStatus
    total_amount: float

# ✅ Protocol para duck typing estructural
from typing import Protocol

class OrderRepository(Protocol):
    async def save(self, order: Order) -> Order: ...
    async def find_by_id(self, order_id: str) -> Order | None: ...

# ✅ Deferred annotations (Python 3.14 — default!)
# Ya no necesitas from __future__ import annotations
class Order:
    items: list[OrderItem]  # Forward reference funciona sin quotes ni future
```

---

## Pydantic v2 — Modelos y validación

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from uuid import UUID, uuid4

class OrderCreate(BaseModel):
    model_config = {"extra": "forbid"}  # Rechazar campos desconocidos

    customer_id: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0, le=9_999_999)
    currency: str = Field(default="MXN", pattern=r"^[A-Z]{3}$")
    notes: str | None = Field(default=None, max_length=500)

    @field_validator("customer_id")
    @classmethod
    def validate_customer_id(cls, v: str) -> str:
        return v.strip().upper()

class Order(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    order_number: int
    customer_id: str
    status: str = "pending"
    total_amount: float
    currency: str = "MXN"
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Serialización
order = Order(order_number=1001, customer_id="CUST-001", total_amount=150.00)
print(order.model_dump())        # → dict
print(order.model_dump_json())   # → JSON string

# Validación desde dict/JSON
data = {"customer_id": " cust-001 ", "amount": 150}
parsed = OrderCreate.model_validate(data)
print(parsed.customer_id)  # "CUST-001" (stripped + upper)
```

---

## Async/Await moderno

```python
import asyncio
from asyncio import TaskGroup

# ✅ TaskGroup (Python 3.11+, estable en 3.13)
async def fetch_orders(user_ids: list[str]) -> list[Order]:
    async with TaskGroup() as tg:
        tasks = [tg.create_task(fetch_user_orders(uid)) for uid in user_ids]

    # Si alguna tarea falla, todas se cancelan automáticamente
    return [task.result() for task in tasks]

# ✅ asyncio.timeout (Python 3.11+)
async def fetch_with_timeout(url: str, timeout: float = 5.0):
    async with asyncio.timeout(timeout):
        return await fetch(url)

# ✅ Queue.shutdown (Python 3.13+)
async def producer_consumer():
    queue: asyncio.Queue[int] = asyncio.Queue()
    # ... producir / consumir ...
    queue.shutdown()  # Cierra la queue, los consumidores salen limpiamente

# ✅ asyncio.to_thread (CPU-bound sin bloquear event loop)
async def process_data(data: bytes) -> Result:
    return await asyncio.to_thread(cpu_intensive_computation, data)
```

---

## Free-threaded Python (3.14, sin GIL)

```bash
# Instalar Python 3.14 con free-threading
uv python install 3.14 --install-free-threaded

# Ejecutar en modo free-threaded
uv run --free-threaded python -c "import sys; print(sys._is_gil_enabled())"
# → False (GIL deshabilitado)
```

```python
# Con free-threading, threading.Thread escala en multi-core
from threading import Thread

def cpu_task(start: int, end: int) -> int:
    total = 0
    for i in range(start, end):
        total += i * i
    return total

threads = [
    Thread(target=cpu_task, args=(i * 100_000, (i + 1) * 100_000))
    for i in range(4)
]
for t in threads:
    t.start()  # Ahora realmente corren en paralelo (sin GIL)
for t in threads:
    t.join()
```

---

## Convenciones de código

### Naming

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Módulos | `snake_case.py` | `order_service.py` |
| Clases | `PascalCase` | `OrderService`, `CreateOrderUseCase` |
| Funciones | `snake_case` | `create_order()`, `calculate_total()` |
| Variables | `snake_case` | `order_id`, `total_amount` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_RETRY_ATTEMPTS` |
| Métodos privados | `_snake_case` | `_build_query()` |

### Estructura de proyecto

```
miapp/
├── pyproject.toml
├── uv.lock
├── README.md
├── src/
│   └── miapp/
│       ├── __init__.py
│       ├── main.py                      # Entry point (FastAPI app)
│       ├── config.py                    # Pydantic Settings
│       ├── modules/
│       │   └── orders/
│       │       ├── __init__.py
│       │       ├── router.py            # FastAPI routes
│       │       ├── service.py           # Business logic
│       │       ├── repository.py        # Data access
│       │       ├── schemas.py           # Pydantic models
│       │       └── models.py            # SQLAlchemy models
│       ├── shared/
│       │   ├── database.py
│       │   ├── exceptions.py
│       │   └── deps.py                  # FastAPI dependencies
│       └── types.py
└── tests/
    ├── __init__.py
    └── modules/
        └── orders/
            ├── test_router.py
            ├── test_service.py
            └── test_repository.py
```

---

## Template strings (Python 3.14)

```python
# Template string literal (PEP tbd — Python 3.14)
from string.templatelib import Template

name = "World"
t = t"Hello {name}!"  # Template string — no evalúa name aún

# Renderizar después
result = t.format(name="Python")  # → "Hello Python!"
result = t.format(name="3.14")    # → "Hello 3.14!"

# Útil para SQL, HTML templates, prompts de LLM
query = t"SELECT * FROM orders WHERE customer_id = {cust_id}"
sql = query.format(cust_id="CUST-001")
```

---

## Reglas de oro

1. **`uv` para todo.** Reemplaza `pip`, `poetry`, `pyenv`, `virtualenv`.
2. **Pydantic v2 para modelos.** Validación y serialización en un solo lugar.
3. **Type hints en todo.** `mypy` o `pyright` en CI con `strict = true`.
4. **`ruff` para linting y formatting.** Reemplaza flake8, isort, black.
5. **`async/await` para I/O.** Base de datos, HTTP, archivos.
6. **`asyncio.TaskGroup` sobre `gather`.** Cancelación segura.
7. **Sin `except Exception: pass`.** Capturar lo específico.
8. **`dataclass` o Pydantic sobre dicts crudos.** Tipado y validación.
9. **Python 3.14 por defecto.** Free-threaded para CPU-bound si aplica.
10. **Un módulo = una responsabilidad.**

---

## Sub-skills del kit

> 📁 Cada sub-skill tiene su guía detallada en `./{nombre}/GUIDE.md`. Usa `read` para cargarla cuando el tema lo requiera.


| Skill | Cuándo cargarla |
|-------|-----------------|
| `python-fastapi` | FastAPI, Pydantic Settings, DI, middleware, OpenAPI |
| `python-performance` | asyncio, profiling, caching, free-threading |
| `python-security` | JWT, OAuth2, CORS, validación, secrets |
| `python-testing` | pytest 9.1, pytest-asyncio, Testcontainers, httpx |
| `python-database` | SQLAlchemy 2.0, Alembic, asyncpg, PostgreSQL + SQL Server |
| `python-ml` | NumPy, Pandas, LangChain, OpenAI, pgvector |
| `python-deployment` | Docker, Uvicorn, Celery, CI/CD, logging |

---

## Stack recomendado

| Propósito | Herramienta |
|-----------|-------------|
| Package manager | `uv` |
| Framework web | FastAPI |
| Validación | Pydantic v2 |
| ORM | SQLAlchemy 2.0 (async) |
| Migraciones | Alembic |
| Testing | pytest 9.1 + pytest-asyncio |
| Linting | ruff |
| Type checking | pyright o mypy |
| Task queue | Celery 5.6 |
| AI/ML | LangChain + OpenAI / NumPy + Pandas |
