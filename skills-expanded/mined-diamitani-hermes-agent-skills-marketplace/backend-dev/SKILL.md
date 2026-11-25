---
name: backend-dev
description: "Use when building a backend, REST API, web service, or web app server. Python + FastAPI + SQLAlchemy + pytest. Bootstrap, data layer, routes, testing, deployment — full lifecycle."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [backend, fastapi, python, api, web, rest, sqlalchemy, pytest, deployment]
    related_skills: [Backend, test-driven-development, plan, vercel-deploy, database-operations]
---

# Backend Web Development Agent

## Overview

End-to-end backend development workflow for Python + FastAPI projects. Covers the full lifecycle: bootstrap a new project, build the data layer, wire up API routes, test everything, and deploy. Every phase produces working, testable code — no hand-waving.

This skill assumes Python 3.11+, uv as the package manager, FastAPI as the web framework, SQLAlchemy 2.0 async for the ORM, Pydantic v2 for validation, Alembic for migrations, and pytest + httpx for testing. For general backend engineering principles (error handling, timeouts, retries, caching, security), the `Backend` skill is always loaded alongside this one.

## When to Use

- "Build a backend for..." — new projects from scratch
- "Create a REST API that..." — API-first development
- "I need a web service for..." — service endpoints
- "Add a backend to my [frontend] app" — full-stack pairing
- "Set up a database + API for..." — data-backed services

**Don't use for:** frontend-only work, CLI tools, data science pipelines (use those dedicated skills), or microservices in other languages (adapt the patterns, but the exact commands won't apply).

## Phase 0: Plan First

Before writing a single line of code, create a plan. Use the `plan` skill to write a concrete, bite-sized implementation plan to `.hermes/plans/`. The plan should cover:

- Data models and relationships
- API endpoint inventory (what routes, what they return)
- File structure
- Testing strategy
- Deployment target (Vercel, Docker, bare metal)

A good plan prevents 80% of rework. If the project has 3+ models or 5+ endpoints, **planning is mandatory** before code.

## Phase 1: Project Bootstrap

### 1.1 Scaffold with uv

```bash
# Create project directory
mkdir my-backend && cd my-backend

# Initialize with uv
uv init --app

# Install core dependencies
uv add fastapi uvicorn[standard] sqlalchemy[asyncio] aiosqlite alembic pydantic pydantic-settings python-dotenv

# Install dev dependencies
uv add --dev pytest pytest-asyncio httpx pytest-cov
```

### 1.2 Standard Project Structure

```
my-backend/
├── pyproject.toml
├── .env                          # Secrets (gitignored)
├── .env.example                  # Template for teammates
├── alembic.ini                   # Alembic config
├── alembic/
│   ├── env.py
│   └── versions/                 # Migration files
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py               # FastAPI app factory + lifespan
│       ├── config.py             # Settings from env (pydantic-settings)
│       ├── database.py           # Async engine + session factory
│       ├── models/
│       │   ├── __init__.py
│       │   └── base.py           # SQLAlchemy declarative base
│       ├── schemas/              # Pydantic request/response schemas
│       │   └── __init__.py
│       ├── routers/              # API route modules
│       │   └── __init__.py
│       ├── services/             # Business logic (thin, orchestration)
│       │   └── __init__.py
│       └── dependencies.py       # FastAPI Depends() factories
└── tests/
    ├── __init__.py
    ├── conftest.py               # Shared fixtures (async client, test db)
    └── test_routers/
        └── __init__.py
```

### 1.3 Core Files (copy-paste templates)

**`src/app/config.py`** — environment-backed settings:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My Backend"
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./app.db"
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()
```

**`src/app/database.py`** — async engine + session:
```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from .config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
```

**`src/app/main.py`** — app factory:
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine
from .models.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}
```

### 1.4 Verify Bootstrap

```bash
uv run uvicorn src.app.main:app --reload
# Hit http://localhost:8000/health → {"status":"ok"}
# Hit http://localhost:8000/docs → OpenAPI docs load
```

**Check:** `/health` returns 200. `/docs` renders the Swagger UI. `app.db` file is created in the project root. Stop the server before proceeding.

## Phase 2: Data Layer

### 2.1 Define SQLAlchemy Models

Models go in `src/app/models/`. One file per domain entity, plus a `base.py`.

**`src/app/models/base.py`:**
```python
from sqlalchemy.orm import DeclarativeBase
import uuid
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

**Pattern for a domain model (`src/app/models/item.py`):**
```python
from sqlalchemy import Column, String, Text, Boolean, Float
from .base import Base, TimestampMixin

class Item(TimestampMixin, Base):
    __tablename__ = "items"

    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    is_active = Column(Boolean, default=True)
```

### 2.2 Define Pydantic Schemas

Schemas go in `src/app/schemas/`. One file per domain entity. Separate Create, Update, and Response schemas — never reuse the same schema for input and output.

**`src/app/schemas/item.py`:**
```python
import uuid
from datetime import datetime
from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    price: float = Field(..., ge=0)

class ItemUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    price: float | None = Field(None, ge=0)
    is_active: bool | None = None

class ItemResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    price: float
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

### 2.3 Set Up Alembic Migrations

```bash
# Initialize alembic (from project root)
uv run alembic init alembic

# Edit alembic/env.py — wire up async engine and Base metadata:
```

In `alembic/env.py`, replace the `target_metadata` and `run_migrations` sections:

```python
from src.app.models.base import Base
from src.app.config import settings
# Import ALL model modules so Base.metadata knows about them
import src.app.models.item  # noqa: F401 — required for autogenerate

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = settings.database_url
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    from sqlalchemy.ext.asyncio import create_async_engine
    connectable = create_async_engine(settings.database_url)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    import asyncio
    asyncio.run(run_async_migrations())
```

Also update `alembic.ini` — remove the `sqlalchemy.url` line (settings come from config.py).

```bash
# Generate initial migration
uv run alembic revision --autogenerate -m "initial"

# Apply migration
uv run alembic upgrade head
```

**Check:** `uv run alembic current` shows the head revision. `app.db` has the new tables.

## Phase 3: API Routes

### 3.1 Router Organization

One router file per resource in `src/app/routers/`. Each router is self-contained: it declares its prefix, tags, and all CRUD operations for that resource.

**Pattern (`src/app/routers/items.py`):**
```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models.item import Item
from ..schemas.item import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item_in: ItemCreate, db: AsyncSession = Depends(get_db)):
    item = Item(**item_in.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

@router.get("/", response_model=list[ItemResponse])
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    from sqlalchemy import select
    result = await db.execute(select(Item).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item_in: ItemUpdate, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    update_data = item_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    await db.delete(item)
    await db.commit()
```

### 3.2 Register Routers in main.py

```python
from .routers import items

app.include_router(items.router)
```

### 3.3 Error Handling Middleware

Add a global exception handler in `main.py` for unhandled errors:

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import logging
    logging.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
```

### 3.4 Verify Routes

```bash
uv run uvicorn src.app.main:app --reload

# In another terminal or via httpx:
# POST /items → 201
# GET /items → 200 + list
# GET /items/{id} → 200 | 404
# PATCH /items/{id} → 200 | 404
# DELETE /items/{id} → 204 | 404
```

**Check:** All 5 CRUD operations work end-to-end. OpenAPI docs at `/docs` show every endpoint with correct request/response schemas.

## Phase 4: Testing

### 4.1 Test Configuration

**`tests/conftest.py`** — shared fixtures:
```python
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.app.main import app
from src.app.database import get_db
from src.app.models.base import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_async_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with test_async_session() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
```

### 4.2 Test Pattern

Follow `test-driven-development` skill — RED-GREEN-REFACTOR. One test per behavior, clear names.

**`tests/test_routers/test_items.py`:**
```python
import pytest

@pytest.mark.asyncio
async def test_create_item_returns_201(client):
    response = await client.post("/items/", json={"name": "Widget", "price": 9.99})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Widget"
    assert data["price"] == 9.99
    assert "id" in data

@pytest.mark.asyncio
async def test_get_item_returns_404_for_missing(client):
    response = await client.get("/items/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_items_respects_pagination(client):
    # Create 3 items
    for i in range(3):
        await client.post("/items/", json={"name": f"Item {i}", "price": 1.0})
    response = await client.get("/items/?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
```

### 4.3 Run Tests

```bash
# All tests
uv run pytest tests/ -v

# With coverage
uv run pytest tests/ -v --cov=src/app --cov-report=term-missing

# Single test
uv run pytest tests/test_routers/test_items.py::test_create_item_returns_201 -v
```

**Check:** All tests pass. Coverage ≥ 80% on routers and services. No warnings.

## Phase 5: Deployment

### 5.1 Vercel (Python/FastAPI)

For Vercel deployment, add a `vercel.json` at the project root:

```json
{
  "builds": [{"src": "src/app/main.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "src/app/main.py"}]
}
```

Then deploy using the `vercel-deploy` skill:

```bash
vercel --prod
```

Set environment variables in the Vercel dashboard or via CLI:
```bash
vercel env add DATABASE_URL production
```

### 5.2 Docker

**`Dockerfile`:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install uv && uv sync --frozen --no-dev
COPY . .
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`docker-compose.yml`** (add when the project needs Postgres):
```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 5s
      retries: 5
```

### 5.3 Environment Management

Always provide a `.env.example`:
```
# Database
DATABASE_URL=sqlite+aiosqlite:///./app.db

# App
DEBUG=false
APP_NAME=My Backend
CORS_ORIGINS=["http://localhost:3000"]
```

**Check:** `.env` is in `.gitignore`. `.env.example` is committed. `vercel env` or Docker env vars match `.env.example` keys.

## Delegation Patterns

For multi-resource projects, dispatch subagents for parallel work:

```python
delegate_task(
    goal="Implement the Item model, schemas, router, and tests for CRUD operations",
    context="""
    Project: /path/to/my-backend
    Stack: FastAPI + SQLAlchemy async + SQLite + pytest

    Follow the backend-dev skill workflow:
    - Phase 2: Create models/items.py and schemas/item.py
    - Phase 3: Create routers/items.py with full CRUD
    - Phase 4: Write tests/test_routers/test_items.py with RED-GREEN-REFACTOR

    Test command: uv run pytest tests/ -v
    Dev server: uv run uvicorn src.app.main:app --reload
    """,
    toolsets=['terminal', 'file', 'web']
)
```

Run up to 3 model/router pairs in parallel as separate subagents. After all complete, run the full test suite to catch integration issues.

## Common Pitfalls

1. **Skipping the plan.** Projects with 3+ models or 5+ endpoints need a plan. Without one, you'll restructure mid-build. Loading `plan` skill is cheap insurance.

2. **Reusing schemas for input and output.** `ItemCreate` ≠ `ItemResponse`. Input schemas should never expose internal fields (id, created_at). Output schemas should never accept user-controlled fields. Separate them always.

3. **Forgetting to import models in `alembic/env.py`.** Alembic autogenerate can only see models that have been imported. If a migration is missing a table, check that the model module is imported in `env.py`.

4. **Synchronous database calls in async routes.** Use `AsyncSession`, `select()` from sqlalchemy (not `session.query()`), and `await` all database operations. A single sync call blocks the entire event loop.

5. **No pagination on list endpoints.** Every `GET /items/` must have `skip` + `limit`. Without it, a table with 100k rows returns them all and degrades the server.

6. **Skipping RED (watching the test fail).** TDD rule: if you didn't see it fail, you don't know it tests the right thing. Run `pytest tests/test_file.py::test_name -v` and confirm FAIL before writing code.

8. **Committing `.env`.** Secrets in version control are a security incident. `.env` must be in `.gitignore` from the first commit.

9. **No `.env.example`.** Teammates (and future you) need to know what environment variables exist without reading the source. Keep `.env.example` in sync with `config.py`.

10. **Unwrapped LLM API calls crash without an API key.** When your backend optionally calls an LLM (DeepSeek, OpenAI, etc.), every `.chat()` or `.completion()` call must be wrapped in try/except — not just the JSON parsing, but the HTTP call itself. The try block must encompass the entire invocation. Without this, missing or invalid API keys cause 500s instead of graceful fallback.

**Before (broken — 500 on missing key):**
```python
if self.client:
    response = self.client.chat(prompt)       # 💥 HTTP 401 → 500
    try:
        return json.loads(response)
    except Exception:
        pass
return fallback()
```

**After (fixed — graceful fallback):**
```python
if self.client:
    try:
        response = self.client.chat(prompt)   # caught by outer try
        return json.loads(response)
    except Exception:
        pass  # Fall back to simulated/default behavior
return fallback()
```

**Audit pattern:** grep for `client.chat(` across the codebase and verify each is inside a try block (not just the JSON parse after it):
```bash
grep -n "\.chat\(" src/ --include="*.py" 
# For each hit, check whether a try: block appears within the preceding 5 lines
```

## Verification Checklist

Before declaring the backend "done":

- [ ] `/health` returns 200
- [ ] `/docs` renders all endpoints with correct schemas
- [ ] All CRUD operations work end-to-end (create → read → update → delete)
- [ ] Pagination works (skip/limit respected)
- [ ] 404 for missing resources, 422 for invalid input, 201 for creates, 204 for deletes
- [ ] All tests pass (`uv run pytest tests/ -v`)
- [ ] Test coverage ≥ 80% on routers and services
- [ ] `.env` is gitignored, `.env.example` is committed
- [ ] Alembic migrations are generated and applied (`uv run alembic current` shows head)
- [ ] CORS is configured (not `allow_origins=["*"]` in production)
- [ ] No sync DB calls in async routes
- [ ] Deployment target is configured (vercel.json, Dockerfile, or equivalent)

## Project Structure Reference

Quick-reference for where things go:

| Concern | Location |
|---------|----------|
| App factory + lifespan | `src/app/main.py` |
| Settings (env vars) | `src/app/config.py` |
| DB engine + session | `src/app/database.py` |
| SQLAlchemy models | `src/app/models/<entity>.py` |
| Declarative base + mixins | `src/app/models/base.py` |
| Pydantic schemas | `src/app/schemas/<entity>.py` |
| API routes | `src/app/routers/<entity>.py` |
| Business logic | `src/app/services/<domain>.py` |
| Dependency injection | `src/app/dependencies.py` |
| Shared test fixtures | `tests/conftest.py` |
| Route tests | `tests/test_routers/test_<entity>.py` |
| Alembic config | `alembic.ini` + `alembic/env.py` |
| Deployment config | `vercel.json`, `Dockerfile`, `docker-compose.yml` |
