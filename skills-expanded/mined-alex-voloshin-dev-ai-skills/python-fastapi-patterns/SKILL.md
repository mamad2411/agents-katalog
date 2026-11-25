---
name: python-fastapi-patterns
description: Use this skill when designing or implementing Python backend code in FastAPI projects, reviewing Python pull requests, or onboarding new contributors to FastAPI conventions — a Python backend patterns knowledge base covering Python 3.12+, FastAPI layered architecture, Pydantic v2 schemas, SQLAlchemy 2.0 async ORM, Alembic migrations, async/await, dependency injection, pytest with httpx.AsyncClient, OAuth2/JWT security, ruff and mypy strict, structured logging and Prometheus metrics.
disable-model-invocation: true
---

# Python + FastAPI Patterns

Reference knowledge for Python 3.12+ backend services built on FastAPI. This skill is auto-loaded by the `python-engineer` agent and available to any other agent or skill that needs deep Python/FastAPI patterns — architects reviewing service designs, reviewers checking Python PRs, or DB engineers reviewing SQLAlchemy models.

## Project Architecture

Domain-driven module structure — each domain has its own package:

- `router.py` — path operations and HTTP layer only
- `schemas.py` — Pydantic request/response models
- `models.py` — SQLAlchemy ORM models
- `service.py` — business logic
- `dependencies.py` — FastAPI `Depends` callables
- `exceptions.py` — domain-specific exceptions
- `constants.py` — enums, error codes

Global modules: `main.py`, `database.py`, `config.py`, `exceptions.py`. Tests mirror source structure under `tests/<module_name>/`.

**Layering rule**: routers handle HTTP concerns only (path ops, status codes, response models). Business logic lives in the service layer. Repositories (or service-internal data accessors) own SQLAlchemy session use. Never pass raw dicts across layer boundaries.

**Configuration**: use `pydantic-settings` with `BaseSettings` for typed config, split per domain. Environment-specific files (`.env.dev`, `.env.prod`, `.env.test`) load via `env_file`. Externalize all secrets (`DATABASE_URL`, `REDIS_URL`, `JWT_SECRET`). Local dev uses `model_config = SettingsConfigDict(env_file=".env")`.

## Python Type System

- Enable `mypy --strict` — no implicit `Any`, no untyped defs
- Use modern syntax: `str | None` (not `Optional[str]`), `list[int]` (not `List[int]`)
- `TypeVar`, `Generic`, `Protocol` for reusable abstractions
- `TypeAlias` for complex types, `Literal` for constrained string values
- `@overload` for functions with different return types based on input
- Dataclasses for internal value objects; Pydantic models for external boundaries

## Pydantic v2

- Separate schemas per operation: `UserCreate`, `UserUpdate`, `UserResponse`, `UserInDB`
- Use `Field()` with `min_length`, `max_length`, `ge`, `le`, `pattern` for validation
- `model_config = ConfigDict(from_attributes=True)` for ORM compatibility
- Custom validators: `@field_validator` for field-level, `@model_validator` for cross-field
- Use `Annotated[type, Field(...)]` pattern for reusable field definitions
- Never use `model_validate` on untrusted data without an explicit schema

## SQLAlchemy 2.0 Async + Alembic

**ORM (2.0 style)**:

- Use `AsyncSession` with `async_sessionmaker` — never sync `Session` in FastAPI
- Declarative base with `MappedAsBase` and `Mapped[]` type annotations
- `mapped_column()` with explicit types: `Mapped[int]`, `Mapped[str | None]`
- Relationships: `relationship()` with `lazy="selectin"` or explicit `selectinload()` / `joinedload()`
- Always use the `select()` statement API — never the legacy `query()` API

**Database wiring**:

- Async engine: `create_async_engine(url, pool_size=20, max_overflow=10)`
- Session dependency via `Depends(get_async_session)` — yields a session, auto-closes
- Transaction management: service layer wraps operations in `async with session.begin()`
- N+1 prevention: `selectinload()` for collections, `joinedload()` for single relations
- Read-only queries: `execution_options(readonly=True)` where supported

**Alembic migrations**:

- Use the async engine in `env.py` via `sqlalchemy.ext.asyncio`
- Migration files live in `alembic/versions/`
- Auto-generate: `alembic revision --autogenerate -m "description"`
- Set `naming_convention` on `MetaData` for consistent constraint names
- Never edit or delete existing migrations. CI must run `alembic upgrade head` from an empty DB

## Dependency Injection

- Use `Depends()` for all cross-cutting concerns: auth, DB session, pagination, permissions
- Chain dependencies: `current_user = Depends(get_current_user)` → `admin_user = Depends(require_admin)`
- Dependencies are cached per-request — reuse the same DB session across a request
- Use `Annotated[type, Depends(dep)]` for clean, reusable dependency declarations
- Async dependencies for I/O operations; sync for pure computation

## REST API Design

**Conventions**:

- Resource-oriented: `/api/v1/users`, `/api/v1/users/{user_id}/orders`
- Use `APIRouter` with `prefix` and `tags` per domain module
- HTTP methods: GET (read), POST (create), PUT (full update), PATCH (partial), DELETE
- Status codes: 200, 201, 204, 400, 401, 403, 404, 409, 422, 500
- Pagination: `skip`/`limit` or cursor-based for large datasets. Return total count
- `response_model` on every endpoint — never return raw dicts or ORM objects

**Error handling**:

- Custom exception classes inheriting from a base `AppException`
- Global exception handler via `@app.exception_handler(AppException)`
- Consistent error response shape: `{"detail": str, "error_code": str, "status_code": int}`
- HTTP exceptions with explicit status codes — never raise a generic `HTTPException(500)`
- Log errors with a correlation ID (request ID middleware)

## Async Patterns

- `async def` for all I/O path operations — FastAPI runs sync defs in a threadpool (less efficient)
- `asyncio.gather()` for parallel independent I/O calls
- `run_in_threadpool()` from `starlette.concurrency` for unavoidable sync libraries
- CPU-bound work: offload to `ProcessPoolExecutor` or a task queue (Celery, ARQ)
- Never use `time.sleep()` in async context — use `asyncio.sleep()`
- Background tasks: `BackgroundTasks` for fire-and-forget; task queue for reliable processing

## Security

- **Authentication**: OAuth2 + JWT via `fastapi.security.OAuth2PasswordBearer`
- **Password hashing**: `passlib` with bcrypt, or `argon2-cffi` — never plaintext
- **CORS**: configure explicitly via `CORSMiddleware` — never `allow_origins=["*"]` in production
- **Rate limiting**: `slowapi` or custom middleware with a Redis backend
- **Input validation**: Pydantic handles request validation; sanitize HTML with `bleach` if rendering user content
- **SQL injection**: SQLAlchemy parameterizes queries by default — never use f-strings in queries
- **HTTPS**: enforce via reverse proxy; set `Secure`, `HttpOnly`, `SameSite` on cookies

For the full OWASP-aligned web checklist, see `owasp-coverage` skill.

## Testing with pytest

- **Framework**: `pytest` + `pytest-asyncio` + `httpx.AsyncClient`
- **Test client**: `async with AsyncClient(app=app, base_url="http://test") as client:`
- **DB fixtures**: override `get_async_session` with a test session (use transactions + rollback)
- **Factories**: `factory_boy` or manual fixtures for test data generation
- **Structure**: Arrange → Act → Assert. Use `parametrize` for input variations
- **Coverage**: `pytest-cov`, target ≥80% on service and router layers
- **What NOT to test**: framework internals, Pydantic validation (tested upstream), trivial CRUD

For broader test pyramid and coverage guidance, see `test-strategy` skill.

## Code Quality

- **Linting + formatting**: `ruff` (replaces flake8, isort, black) — single tool, fast
- **Type checking**: `mypy --strict` in CI — no commits with type errors
- **Pre-commit**: `ruff check`, `ruff format`, `mypy` as pre-commit hooks
- **Import sorting**: `ruff` with isort rules — stdlib → third-party → local
- **Docstrings**: Google style for public functions and classes. Routers auto-documented via OpenAPI

## Observability

- **Logging**: `structlog` or stdlib `logging` with a JSON formatter in production. Correlation IDs via middleware
- **Metrics**: `prometheus-fastapi-instrumentator` for automatic request metrics
- **Health check**: `/health` endpoint returning DB and Redis connectivity status
- **OpenAPI**: auto-generated docs at `/docs` (Swagger) and `/redoc`. Keep schemas accurate

## When this applies

| Workflow | Apply this knowledge |
|---|---|
| `Agent(python-engineer)` invocation | Auto-loaded via `skills:` frontmatter |
| `/develop` with a Python work-package | Spawned agent loads this knowledge |
| `/code-review` on Python PRs | Reviewer references these patterns |
| `/architecture-design` for a Python service | Architect references the layering, async, and DB patterns |
| `/bugfix` on Python services | Developer agent grounds the fix in these conventions |

## Integration

- **Consumed by**: `python-engineer` agent (primary), `software-engineer` (when reviewing Python code), `db-engineer` (when reviewing SQLAlchemy models)
- **Companion knowledge**: `context-engineering` (for Python agent harnesses), `owasp-coverage` (security section), `test-strategy` (pyramid and coverage targets)
- **External references**: FastAPI docs, Pydantic v2 docs, SQLAlchemy 2.0 docs, Alembic docs, ruff docs, mypy docs
