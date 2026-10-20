---
applyTo: "**/*.py"
---

# Python Coding Standards

## Framework: FastAPI

- Use `APIRouter` for route grouping — never attach routes directly to `app`
- Define request/response models with Pydantic v2 `BaseModel`
- Use `Annotated[T, Depends(...)]` for dependency injection
- Return typed response models; never return raw dicts
- Set `status_code` on route decorators; use `Response` for custom headers
- Add OpenAPI metadata: `summary`, `description`, `tags`, `response_model`

## ORM: SQLAlchemy 2.0

- Use 2.0-style `select()` statements — never the legacy `Query` API
- Define models with `DeclarativeBase` and `Mapped[T]` type annotations
- Use `AsyncSession` for all database operations
- Relationships must have explicit `back_populates`
- Use `server_default` for database-level defaults; `default` for Python-level
- Always use `session.scalars()` or `session.execute()` — never `session.query()`

## Error Handling

- Raise `HTTPException` with appropriate status codes and `detail` messages
- Register custom exception handlers for domain errors in `app/core/exceptions.py`
- Never expose stack traces, internal paths, or raw SQL errors in responses
- Use structured error response schema: `{"detail": str, "code": str, "field": str | null}`

## Async Patterns

- All I/O operations must be `async` — database, HTTP, file system
- Use `asyncio.gather()` for concurrent independent operations
- Never use `time.sleep()` — use `asyncio.sleep()` if needed
- Background tasks via FastAPI `BackgroundTasks` or Celery for heavy work

## Imports & Style

- Use absolute imports from the project root
- Group: stdlib → third-party → local, separated by blank lines
- Use `from __future__ import annotations` for forward references
- Follow PEP 8; max line length 99 characters
- Use f-strings for string formatting; never `%` or `.format()`

## Project Structure

```
backend/
├── app/
│   ├── api/           # Route handlers (thin controllers)
│   │   └── v1/        # Versioned API routes
│   ├── core/          # Config, security, dependencies, exceptions
│   ├── models/        # SQLAlchemy ORM models
│   ├── schemas/       # Pydantic request/response schemas
│   ├── services/      # Business logic layer
│   ├── repositories/  # Data access layer (DB queries)
│   └── main.py        # FastAPI app factory
├── alembic/           # Database migrations
├── tests/
│   ├── api/           # API integration tests
│   ├── services/      # Service unit tests
│   └── conftest.py    # Shared fixtures
└── pyproject.toml
```

## Type Hints

- All function signatures must have complete type annotations
- Use `T | None` over `Optional[T]` (Python 3.10+ union syntax)
- Use `collections.abc` types: `Sequence`, `Mapping`, `Iterable` over concrete types
- Generic return types for repositories: `T | None` for single, `list[T]` for many
