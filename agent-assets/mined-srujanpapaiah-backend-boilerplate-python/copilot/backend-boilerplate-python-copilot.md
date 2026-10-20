# GitHub Copilot Instructions

## Context
This is a Python FastAPI backend boilerplate with clean architecture.
Tech stack: Python 3.12+, FastAPI, SQLAlchemy 2.x async, Pydantic v2, PostgreSQL, Redis.

## Code Generation Guidelines

### Always
- Add full type annotations to all functions and variables
- Use `from __future__ import annotations` at the top of every module
- Use `async def` for any function that performs I/O
- Follow the repository pattern — SQL in repositories, logic in services, HTTP in endpoints
- Use Pydantic v2 `model_validate()` and `model_dump()` methods
- Raise domain exceptions from `src/core/exceptions.py`
- Write docstrings for public classes and complex functions
- Use `Annotated[X, Depends(get_x)]` for FastAPI dependency injection; define type aliases like `DbSession = Annotated[AsyncSession, Depends(get_db_session)]`

### Never
- Use `print()` — use `structlog.get_logger()`
- Use sync database operations
- Put business logic in endpoint functions
- Use `HTTPException` directly — use domain exceptions
- Hardcode configuration values — use `Settings` from `src/config/`
- Write tests without proper pytest markers (`@pytest.mark.unit` etc.)

### Patterns
```python
# Dependency injection
from src.core.dependencies import DbSession, CurrentUserId

@router.get("/resource")
async def get_resource(user_id: CurrentUserId, session: DbSession):
    svc = ResourceService(session)
    return await svc.get(user_id)

# Response envelope
from src.api.v1.schemas.common import APIResponse
return APIResponse(data=schema.model_validate(obj))

# Error handling
from src.core.exceptions import NotFoundError
raise NotFoundError("Resource", resource_id)
```

### File Organization
- New schemas → `src/api/v1/schemas/<resource>.py`
- New endpoints → `src/api/v1/endpoints/<resource>.py`
- New services → `src/services/<resource>.py`
- New repositories → `src/repositories/<resource>.py`
- New models → `src/models/<resource>.py` (import in `__init__.py`)
- New tests → mirror the source path under `tests/`
