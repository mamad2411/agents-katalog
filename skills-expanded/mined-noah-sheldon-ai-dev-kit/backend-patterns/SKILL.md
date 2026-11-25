---
name: backend-patterns
description: FastAPI architecture patterns including system design, dependency injection, error handling, background tasks, WebSocket, testing, middleware, database integration, and OpenAPI design.
origin: AI Dev Kit
---

# Backend Patterns — FastAPI

Production-grade FastAPI patterns for Python backends: system design with OOP layering,
dependency injection, error contracts, background processing, real-time WebSocket, async
database integration, and comprehensive testing.

## When to Use

- Building or refactoring a FastAPI service from scratch or adding endpoints to an existing app.
- Designing layered architecture with entities, services, repositories, and domain events.
- Implementing dependency injection, middleware pipelines, or custom error handlers.
- Adding background task processing (celery, RQ, or FastAPI BackgroundTasks).
- Creating real-time WebSocket endpoints with connection lifecycle management.
- Integrating SQLAlchemy async ORM with Alembic migration workflows.
- Designing OpenAPI-compliant APIs with envelopes, versioning, and reusable schemas.
- Writing comprehensive async tests with TestClient and fixture patterns.

## Core Concepts

### 1. System Design & OOP Layering

Adopt a clean layered architecture that separates concerns across four tiers:

```
┌─────────────────────────────────────────────┐
│  Presentation Layer (FastAPI routers)        │
│  - Route handlers, request/response models   │
│  - Dependency injection wiring              │
├─────────────────────────────────────────────┤
│  Service Layer (business logic)              │
│  - Use cases, orchestration, domain events  │
│  - No direct HTTP or DB code                │
├─────────────────────────────────────────────┤
│  Repository Layer (data access)              │
│  - CRUD operations, query builders           │
│  - Returns domain entities, not ORM objects  │
├─────────────────────────────────────────────┤
│  Domain Layer (entities, value objects)      │
│  - Pure Python, no framework dependencies    │
│  - Domain events, invariants, value objects  │
└─────────────────────────────────────────────┘
```

**Domain Entities** — Pure Python dataclasses or Pydantic models with no framework coupling:

```python
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class User:
    id: UUID = field(default_factory=uuid4)
    email: str = ""
    name: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def deactivate(self) -> None:
        if not self.is_active:
            raise ValueError("User is already inactive")
        self.is_active = False
        self.updated_at = datetime.utcnow()
```

**Domain Events** — Lightweight event objects published by services:

```python
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DomainEvent:
    occurred_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class UserCreated(DomainEvent):
    user_id: UUID
    email: str


@dataclass
class UserDeactivated(DomainEvent):
    user_id: UUID
```

**Repository Interface** — Abstract contract for data access:

```python
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.entities import User


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def update(self, user: User) -> User: ...

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 50) -> list[User]: ...
```

**Service Layer** — Orchestrates use cases, publishes domain events:

```python
from typing import Protocol
from uuid import UUID

from app.domain.entities import User
from app.domain.events import UserCreated, UserDeactivated
from app.repositories import UserRepository


class EventPublisher(Protocol):
    async def publish(self, event: DomainEvent) -> None: ...


class UserService:
    def __init__(
        self,
        repo: UserRepository,
        publisher: EventPublisher,
    ) -> None:
        self.repo = repo
        self.publisher = publisher

    async def create_user(self, email: str, name: str) -> User:
        existing = await self.repo.get_by_email(email)
        if existing:
            raise DuplicateResourceError(f"User with email {email} already exists")

        user = User(email=email, name=name)
        user = await self.repo.create(user)
        await self.publisher.publish(UserCreated(user_id=user.id, email=user.email))
        return user

    async def deactivate_user(self, user_id: UUID) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundError(f"User {user_id} not found")

        user.deactivate()
        user = await self.repo.update(user)
        await self.publisher.publish(UserDeactivated(user_id=user.id))
        return user
```

### 2. FastAPI App Structure

Organize the application with routers, dependencies, middleware, and lifespan:

```
app/
├── __init__.py
├── main.py                # create_app(), lifespan, middleware wiring
├── config.py              # pydantic-settings BaseSettings
├── dependencies.py        # reusable Depends() providers
├── middleware.py           # custom middleware factories
├── exceptions.py          # custom exceptions + exception handlers
├── domain/
│   ├── entities.py
│   ├── events.py
│   └── errors.py
├── repositories/
│   ├── base.py            # Abstract base repository
│   └── user_repository.py
├── services/
│   ├── user_service.py
│   └── event_publisher.py
├── routers/
│   ├── users.py
│   └── health.py
├── schemas/
│   ├── user.py            # Pydantic request/response models
│   └── common.py          # Envelope, pagination, error schemas
├── database.py            # async engine, session factory
└── middleware/
    ├── auth.py
    ├── cors.py
    └── rate_limit.py
```

**Application Factory with Lifespan:**

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import Settings
from app.database import init_db, close_db
from app.exceptions import register_exception_handlers
from app.middleware.cors import setup_cors
from app.middleware.rate_limit import RateLimitMiddleware
from app.routers import users, health


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup: initialize database, warm caches
    await init_db()
    yield
    # Shutdown: close connections, flush buffers
    await close_db()


def create_app(settings: Settings | None = None) -> FastAPI:
    app = FastAPI(
        title="AI Dev Kit API",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        openapi_url="/openapi.json",
    )

    # Middleware
    setup_cors(app, origins=settings.allowed_origins if settings else [])
    app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

    # Exception handlers
    register_exception_handlers(app)

    # Routers
    app.include_router(users.router, prefix="/api/v1")
    app.include_router(health.router, prefix="/api/v1")

    return app
```

### 3. Pydantic v2 Models

Use Pydantic v2's `BaseModel`, `Field`, `field_validator`, and `model_config`:

```python
from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
    ConfigDict,
)


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=150)
    password: str = Field(..., min_length=8, max_length=128)

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "examples": [
                {
                    "email": "user @example.com",
                    "name": "Jane Doe",
                    "password": "s3cur3P@ss!",
                }
            ]
        },
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name must not be blank")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

### 4. Dependency Injection

Use `Depends()` for reusable, composable providers:

```python
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory
from app.domain.entities import User
from app.repositories.user_repository import SQLAlchemyUserRepository
from app.services.user_service import UserService
from app.services.event_publisher import RedisEventPublisher

# --- Database session ---
async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# --- Repository ---
def get_user_repo(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session)

# --- Service ---
def get_user_service(
    repo: Annotated[SQLAlchemyUserRepository, Depends(get_user_repo)],
) -> UserService:
    publisher = RedisEventPublisher()
    return UserService(repo=repo, publisher=publisher)

# --- Auth ---
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # decode JWT, look up user, raise if invalid
    user = await authenticate_token(token, service)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return user

# Type aliases for ergonomic injection
DBSession = Annotated[AsyncSession, Depends(get_db_session)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
CurrentUser = Annotated[User, Depends(get_current_user)]
```

### 5. Error Handling

Define a unified error contract with custom exceptions and handlers:

```python
# app/exceptions.py
from __future__ import annotations

from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class AppError(Exception):
    """Base application error with HTTP status and user-safe detail."""

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    detail: str = "Internal server error"
    extra: dict[str, Any] | None = None


class ResourceNotFoundError(AppError):
    status_code = HTTPStatus.NOT_FOUND
    detail = "Resource not found"


class DuplicateResourceError(AppError):
    status_code = HTTPStatus.CONFLICT
    detail = "Resource already exists"


class UnauthorizedError(AppError):
    status_code = HTTPStatus.UNAUTHORIZED
    detail = "Authentication required"


class ValidationError(AppError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    detail = "Validation failed"


class ErrorEnvelope(BaseModel):
    success: bool = False
    error: dict[str, Any]


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.status_code,
                    "message": exc.detail,
                    **(exc.extra or {}),
                },
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_error(request: Request, exc: Exception) -> JSONResponse:
        # Log stack trace in production; never leak internals to client
        app.logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {"code": 500, "message": "Internal server error"},
            },
        )
```

**Error Contract in Schemas:**

```python
# app/schemas/common.py
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")


class PaginationMeta(BaseModel):
    total: int
    page: int
    page_size: int
    pages: int


class APIEnvelope(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[dict[str, Any]] = None
    pagination: Optional[PaginationMeta] = None
```

### 6. Background Tasks

**FastAPI BackgroundTasks (lightweight):**

```python
from fastapi import BackgroundTasks, Depends
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService


@router.post("/users", response_model=APIEnvelope[UserResponse], status_code=201)
async def create_user(
    payload: UserCreate,
    bg: BackgroundTasks,
    service: UserServiceDep,
) -> APIEnvelope[UserResponse]:
    user = await service.create_user(email=payload.email, name=payload.name)
    bg.add_task(send_welcome_email, user.email, user.name)
    return APIEnvelope(success=True, data=UserResponse.model_validate(user))


def send_welcome_email(email: str, name: str) -> None:
    """Runs after the response is returned — non-blocking."""
    ...
```

**Celery Integration (heavy/long-running tasks):**

```python
# app/worker/celery_app.py
from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    worker_prefetch_multiplier=1,
)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def generate_report(self, user_id: str, params: dict) -> dict:
    try:
        # Long-running report generation
        result = build_report(user_id, params)
        return result
    except Exception as exc:
        self.retry(exc=exc)
```

### 7. WebSocket — Real-Time Endpoints

```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import asyncio
import json

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections with room-based grouping."""

    def __init__(self) -> None:
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str) -> None:
        await websocket.accept()
        self.active_connections.setdefault(room, set()).add(websocket)

    def disconnect(self, websocket: WebSocket, room: str) -> None:
        self.active_connections.get(room, set()).discard(websocket)
        if not self.active_connections.get(room):
            self.active_connections.pop(room, None)

    async def broadcast(self, room: str, message: dict) -> None:
        disconnected = set()
        for ws in self.active_connections.get(room, set()):
            try:
                await ws.send_json(message)
            except Exception:
                disconnected.add(ws)
        for ws in disconnected:
            self.disconnect(ws, room)


manager = ConnectionManager()


@router.websocket("/ws/{room}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, room: str, client_id: str) -> None:
    await manager.connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            # Echo to room or process
            await manager.broadcast(
                room,
                {"type": "message", "client_id": client_id, "data": payload},
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
        await manager.broadcast(room, {"type": "disconnect", "client_id": client_id})
```

### 8. Testing

**TestClient with Async Patterns:**

```python
# tests/conftest.py
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import create_app
from app.config import Settings
from app.database import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def engine():
    eng = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await eng.dispose()


@pytest.fixture
async def db_session(engine):
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session):
    settings = Settings(database_url=TEST_DATABASE_URL)
    app = create_app(settings)
    # Override dependency for test isolation
    app.dependency_overrides[get_db_session] = lambda: db_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# tests/test_users.py
import pytest


@pytest.mark.anyio
async def test_create_user_returns_envelope(client: AsyncClient) -> None:
    payload = {
        "email": "test @example.com",
        "name": "Test User",
        "password": "Str0ngP@ss!",
    }
    resp = await client.post("/api/v1/users", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["email"] == "test @example.com"
    assert "error" not in (body["error"] or {})


@pytest.mark.anyio
async def test_create_duplicate_user_returns_409(client: AsyncClient) -> None:
    payload = {
        "email": "dup @example.com",
        "name": "Dup",
        "password": "Str0ngP@ss!",
    }
    await client.post("/api/v1/users", json=payload)
    resp = await client.post("/api/v1/users", json=payload)
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == 409
```

### 9. Middleware

**CORS:**

```python
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app, origins: list[str]) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
        max_age=600,
    )
```

**Authentication Middleware:**

```python
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse
import jwt


class AuthMiddleware(BaseHTTPMiddleware):
    PUBLIC_PATHS = {"/api/v1/health", "/docs", "/openapi.json"}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if request.url.path in self.PUBLIC_PATHS:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"error": "Missing token"})

        token = auth_header.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
            request.state.user_id = payload["sub"]
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"error": "Token expired"})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"error": "Invalid token"})

        return await call_next(request)
```

**Rate Limiting:**

```python
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.rpm = requests_per_minute
        self.buckets: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request, call_next):
        ip = request.client.host
        now = time.time()
        # Prune old entries
        self.buckets[ip] = [t for t in self.buckets[ip] if now - t < 60]
        if len(self.buckets[ip]) >= self.rpm:
            return JSONResponse(status_code=429, content={"error": "Rate limited"})
        self.buckets[ip].append(now)
        return await call_next(request)
```

### 10. Database Integration

**SQLAlchemy Async Setup:**

```python
# app/database.py
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = settings.database_url  # e.g., postgresql+asyncpg://user:pass@host/db

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.debug,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_db() -> None:
    # Optionally run migrations here or rely on Alembic external
    async with engine.begin() as conn:
        # In dev: await conn.run_sync(Base.metadata.create_all)
        pass  # Alembic handles DDL in production


async def close_db() -> None:
    await engine.dispose()
```

**Alembic Migrations:**

```bash
# Initialize
alembic init -t async migrations

# Generate migration after model changes
alembic revision --autogenerate -m "add users table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### 11. OpenAPI & API Design

**Envelope Pattern (consistent responses):**

```json
// Success
{
  "success": true,
  "data": { "id": "uuid", "email": "user @example.com" },
  "error": null,
  "pagination": { "total": 1, "page": 1, "page_size": 20, "pages": 1 }
}

// Error
{
  "success": false,
  "error": {
    "code": 422,
    "message": "Validation failed",
    "details": [{ "field": "email", "reason": "Invalid email format" }]
  }
}
```

**API Versioning:**

```python
# Prefix-based versioning
app.include_router(v1_users_router, prefix="/api/v1")
app.include_router(v2_users_router, prefix="/api/v2")
```

**Schema Reuse with `json_schema_extra`:**

```python
class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    meta: PaginationMeta

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "items": [{"id": "uuid", "name": "Example"}],
                "meta": {"total": 1, "page": 1, "page_size": 20, "pages": 1},
            }]
        }
    )
```

## Anti-Patterns

- **Fat route handlers** — business logic in routers; move to service layer.
- **ORM objects leaking to API** — always map to Pydantic response schemas.
- **Synchronous DB calls in async routes** — use `AsyncSession` everywhere.
- **Global mutable state** — no shared dicts for caches or connections; use proper DI.
- **N+1 queries** — eager-load relationships; use `selectinload` / `joinedload`.
- **Hardcoded secrets or URLs** — use `pydantic-settings` with environment variables.
- **Catching `Exception` broadly** — catch specific errors; let unexpected ones bubble.
- **Missing transaction boundaries** — always commit/rollback in dependency lifecycle.
- **Returning raw Pydantic validation errors** — wrap in the unified error envelope.
- **Blocking BackgroundTasks with heavy work** — offload to Celery for anything >100ms.

## Best Practices

1. **Always use the envelope pattern** — `{success, data, error, pagination}` for every endpoint.
2. **Type all dependencies** — use `Annotated[T, Depends(provider)]` aliases.
3. **Pydantic v2 `model_config`** — prefer declarative config over class-level attributes.
4. **Async from the start** — use `create_async_engine`, `AsyncSession`, `asyncpg`.
5. **Service layer is the boundary** — routers call services, services call repositories.
6. **Domain events for side effects** — email, notifications, analytics via event publisher.
7. **Alembic for all schema changes** — never `create_all` in production.
8. **Test the error envelope contract** — assert structure on every error response.
9. **Rate limit public endpoints** — protect against abuse with sliding window counters.
10. **OpenAPI docs as living contract** — keep `json_schema_extra` examples up to date.
11. **Use `anyio` for async tests** — `@pytest.mark.anyio` or `asyncio` mode.
12. **Override dependencies in tests** — `app.dependency_overrides[provider] = mock_fn`.
13. **Health endpoint always public** — no auth required, returns DB connectivity status.
14. **Log correlation IDs** — propagate `X-Request-ID` through middleware into all logs.
15. **Paginate every list endpoint** — enforce max page size, return total count.

## Related Skills

- `python-patterns` — Pandas, NumPy, SQLAlchemy 2.0, data validation, performance
- `python-testing` — Pytest, FastAPI test patterns, Hypothesis, coverage
- `api-design` — API contract design, versioning, error semantics
- `security-review` — Auth patterns, input validation, secret management
- `docker-patterns` — Containerization of FastAPI services
- `observability-telemetry` — OpenTelemetry instrumentation, logging, tracing
- `hexagonal-architecture` — Ports and adapters pattern reference
