---
description: Project-wide Cursor rules for the FastAPI Boilerplate
globs: ["**/*.py"]
alwaysApply: true
---

# FastAPI Boilerplate — Cursor Project Rules

## Quick Reference
- **Language**: Python 3.12+ with full type annotations
- **Framework**: FastAPI with async SQLAlchemy 2.x
- **Config**: pydantic-settings (environment variables)
- **Linter**: ruff (replaces black, isort, flake8, bandit)
- **Type checker**: mypy (strict mode)
- **Tests**: pytest-asyncio with httpx.AsyncClient
- **Package manager**: uv

## When Writing New Code

### New Endpoint Checklist
1. Add Pydantic schemas in `src/api/v1/schemas/`
2. Add business logic in `src/services/`
3. Add data access in `src/repositories/`
4. Add the endpoint in `src/api/v1/endpoints/`
5. Wire the router in `src/api/v1/router.py`
6. Add unit tests in `tests/unit/`
7. Add integration tests in `tests/integration/api/`

### New Model Checklist
1. Create model in `src/models/` inheriting from `Base`
2. Import it in `src/models/__init__.py`
3. Run `make migrate-create MSG="add <table> table"`
4. Run `make migrate`

## Patterns to Follow
- Use `Annotated[X, Depends(...)]` for dependency injection type aliases
- Return Pydantic models from endpoints, not dicts
- Use `model_validate()` to convert ORM objects to schemas
- Use `model_dump(exclude_unset=True)` for partial updates
- Raise domain exceptions, never return error dicts manually

## Patterns to Avoid
- Do NOT use `print()` — use `structlog` logger
- Do NOT write raw SQL in endpoints — use repositories
- Do NOT use sync database drivers
- Do NOT hardcode configuration — use Settings
- Do NOT catch broad `Exception` in business logic without re-raising
