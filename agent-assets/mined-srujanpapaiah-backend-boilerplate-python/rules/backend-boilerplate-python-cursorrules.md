# Cursor Rules for FastAPI Boilerplate
# These rules guide the AI assistant in this codebase.

## Project Overview
This is an enterprise-grade Python FastAPI boilerplate following clean architecture.
Stack: Python 3.12+, FastAPI, SQLAlchemy 2.x (async), Alembic, Pydantic v2, PostgreSQL, Redis.

## Architecture
- `src/api/` — HTTP layer (routers, schemas, endpoint functions)
- `src/services/` — Business logic layer (orchestrates repositories)
- `src/repositories/` — Data access layer (DB queries only)
- `src/models/` — SQLAlchemy ORM models
- `src/core/` — Cross-cutting concerns (auth, middleware, logging, exceptions)
- `src/config/` — Application configuration via pydantic-settings
- `src/db/` — Database engine and session management
- `tests/` — Organized into unit/, integration/, e2e/

## Coding Standards

### Python
- Python 3.12+ — use modern syntax (type unions with `|`, `match` statements, etc.)
- All functions must have type annotations; use `from __future__ import annotations`
- Use `async/await` everywhere — no sync database calls
- Use Pydantic v2 models for all request/response schemas
- Follow the repository pattern — never put SQL in endpoints or services
- Use FastAPI's `Depends()` for dependency injection
- Prefer composition over inheritance

### Naming
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Schemas: `{Resource}{Action}` (e.g., `UserCreate`, `UserResponse`)

### Error Handling
- Raise domain exceptions from `src/core/exceptions.py` — never raw HTTPException
- All exceptions are caught by global handlers and serialized consistently
- Use structured logging via structlog — never `print()`

### Testing
- Every new feature needs tests — unit tests for services, integration tests for endpoints
- Use the fixtures in `tests/conftest.py` — `client`, `db_session`, `make_auth_headers`
- Test files mirror the source structure (e.g., `src/services/user.py` → `tests/unit/services/test_user_service.py`)
- Mark tests with `@pytest.mark.unit`, `@pytest.mark.integration`, or `@pytest.mark.e2e`

### Database
- Use Alembic for all schema changes — never modify the DB manually
- Create a new migration: `make migrate-create MSG="description"`
- Models inherit from `src/models/base.Base` which provides `id`, `created_at`, `updated_at`

### API Design
- All endpoints are versioned under `/api/v1/`
- Use consistent response envelopes: `APIResponse[T]` and `PaginatedResponse[T]`
- Protected endpoints use `CurrentUserId` dependency
- Use proper HTTP methods and status codes

### Dependencies
- Add dependencies via `uv add <package>` or edit pyproject.toml
- Dev dependencies go in `[project.optional-dependencies] dev`
- Run `uv sync` after changes

### Code Quality
- Lint: `make lint` (ruff + mypy)
- Format: `make format` (ruff format)
- Test: `make test`
- All checks must pass before committing
