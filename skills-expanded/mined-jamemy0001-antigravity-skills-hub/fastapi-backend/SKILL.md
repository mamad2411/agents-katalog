---
name: fastapi-backend
description: High-performance asynchronous Python REST APIs with FastAPI, Pydantic v2 validation, Dependency Injection, SQLAlchemy 2.0 Async sessions, and Clean Architecture.
aliases:
  - fastapi
  - python-api
  - pydantic-v2
  - async-api
category: "01 - New Features & Business Logic"
tags:
  - agent-skill
  - fastapi
  - python
  - backend
  - api
  - stage-1
---

# FastAPI Backend & Clean Architecture

Production standards for building robust, high-performance asynchronous REST APIs in Python using FastAPI, Pydantic v2, and SQLAlchemy 2.0.

---

## Clean Architecture Layering

Organize FastAPI applications into distinct, decoupled layers:

```text
app/
├── api/          # Route handlers & controller endpoints
│   └── v1/
├── core/         # Settings (pydantic-settings), security, database engine
├── models/       # SQLAlchemy 2.0 ORM Declarative Models
├── schemas/      # Pydantic v2 Request & Response DTOs
├── repositories/ # Raw database query operations (CRUD)
├── services/     # Business logic & domain orchestration
└── main.py       # FastAPI application entry point & middleware
```

---

## Core Rules & Patterns

1. **Pydantic v2 Schema Separation**:
   - Always maintain separate DTO models: `ItemCreate`, `ItemUpdate`, `ItemResponse`.
   - Never expose raw ORM models directly in endpoints; use `model_config = ConfigDict(from_attributes=True)`.
2. **Explicit Dependency Injection (`Depends`)**:
   - Inject database sessions, authenticated users, and services via `Depends()`.
   - Use `AsyncSession` with async context managers for clean connection handling.
3. **Async DB Operations**:
   - Always use `await session.execute(select(...))` with SQLAlchemy 2.0 syntax.
   - Avoid synchronous blocking I/O calls inside `async def` route handlers.
4. **Global Typed Exception Handlers**:
   - Define custom domain exceptions (e.g. `EntityNotFoundException`) and handle them globally using `@app.exception_handler`.

---

## Standard Implementation Recipe

```python
# schemas/item.py
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class ItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# api/v1/endpoints/items.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.core.database import get_db
from app.schemas.item import ItemCreate, ItemResponse
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    payload: ItemCreate,
    session: AsyncSession = Depends(get_db)
) -> ItemResponse:
    service = ItemService(session)
    return await service.create_item(payload)

@router.get("/", response_model=list[ItemResponse])
async def list_items(
    skip: int = 0,
    limit: int = 50,
    session: AsyncSession = Depends(get_db)
) -> Sequence[ItemResponse]:
    service = ItemService(session)
    return await service.list_items(skip=skip, limit=limit)
```

---

## 🔗 Connected Skills (ทักษะที่เกี่ยวข้อง)
- [[Skills/backend-patterns/SKILL|backend-patterns]] — รูปแบบสถาปัตยกรรม Controller-Service-Repository
- [[Skills/api-design/SKILL|api-design]] — มาตรฐานการตั้งชื่อ Endpoints, Pagination และ Status Codes
- [[Skills/tdd-workflow/SKILL|tdd-workflow]] — การเขียนเทสต์ด้วย Pytest และ HTTPX AsyncClient
- [[Skills/database-migrations/SKILL|database-migrations]] — จัดการ Schema Migration ด้วย Alembic
- [[Skills/docker-and-compose/SKILL|docker-and-compose]] — บรรจุแอปพลิเคชันลงใน Docker Container

<!-- v1.1.0 synchronized: 2026-09-29 -->
