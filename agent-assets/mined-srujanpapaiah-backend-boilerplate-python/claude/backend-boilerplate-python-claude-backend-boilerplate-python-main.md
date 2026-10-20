# CLAUDE.md — Instructions for Claude Code and Claude-based Agents

## Project Summary
Enterprise-grade FastAPI boilerplate with clean architecture (API → Service → Repository → Model).
Python 3.12+, async SQLAlchemy, Pydantic v2, JWT auth, structured logging, Docker, CI/CD.

## Common Commands
```bash
make dev          # Install all dependencies (including dev)
make run          # Start dev server with hot reload
make lint         # Ruff check + format check + mypy
make format       # Auto-fix lint issues and format code
make test         # Run all tests with coverage
make test-unit    # Run only unit tests
make migrate      # Apply database migrations
make migrate-create MSG="description"  # Create new migration
make docker-up    # Start Postgres + Redis + App via Docker
make clean        # Remove caches and build artifacts
```

## Architecture Rules
1. **Endpoints** (`src/api/`) only handle HTTP — parse request, call service, return response
2. **Services** (`src/services/`) contain business logic — validate rules, orchestrate repositories
3. **Repositories** (`src/repositories/`) handle data access — all SQL lives here
4. **Models** (`src/models/`) are SQLAlchemy ORM classes — always inherit from `Base`
5. **Schemas** (`src/api/v1/schemas/`) are Pydantic models — request/response DTOs

## Code Style
- Always add type annotations and use `from __future__ import annotations`
- Use `async/await` for all I/O operations
- Raise exceptions from `src/core/exceptions.py`, not `HTTPException`
- Use structlog for logging, never `print()`
- Use `Annotated[X, Depends()]` patterns for dependency injection
- Run `make lint` before committing — ruff + mypy must pass

## Testing
- Tests use in-memory SQLite via aiosqlite for speed
- Use fixtures from `tests/conftest.py`: `client`, `db_session`, `make_auth_headers`
- Use factories from `tests/factories/` to build test entities
- All tests must pass: `make test`

## Adding a New Feature
1. Create Pydantic schemas in `src/api/v1/schemas/`
2. Create/update the SQLAlchemy model in `src/models/`
3. Create a repository in `src/repositories/`
4. Create a service in `src/services/`
5. Create endpoint(s) in `src/api/v1/endpoints/`
6. Wire the router in `src/api/v1/router.py`
7. Create migration: `make migrate-create MSG="add feature"`
8. Write unit + integration tests
9. Run `make lint && make test`
