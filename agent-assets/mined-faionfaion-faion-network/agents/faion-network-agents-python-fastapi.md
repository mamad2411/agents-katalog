# FastAPI Standards

## Summary

**One-sentence:** Produces a production FastAPI app — @asynccontextmanager lifespan, Pydantic v2 Base/Create/Update/Response schemas, Annotated dependency aliases, async service functions, async SQLAlchemy 2 with flush+refresh, and Depends-based auth.

**One-paragraph:** Production-grade FastAPI: Pydantic v2 schemas define the API contract; separate `Base`, `Create`, `Update`, and `Response` schemas (Response uses `ConfigDict(from_attributes=True)`). `@asynccontextmanager` lifespan manages connection pools; never `@app.on_event` (deprecated). Annotated aliases (`DBSession = Annotated[AsyncSession, Depends(get_db)]`) eliminate boilerplate. Routers stay thin; service functions are `async def`, accept typed parameters, return ORM instances. After insert, `await db.flush(); await db.refresh(obj)` to get the generated ID without committing — commit happens in get_db on request success.

**Ефективно для:** new async REST APIs needing OpenAPI docs, microservices wanting high I/O concurrency, replacing sync Flask/DRF endpoints with async equivalents, services adopting Pydantic v2 + SQLAlchemy 2 async.

## Applies If (ALL must hold)

- Python >= 3.11.
- FastAPI >= 0.110 + Pydantic v2.
- async I/O is a real benefit (DB + HTTP clients).
- Team comfortable with `async/await` (or willing to learn).

## Skip If (ANY kills it)

- Existing Django + DRF service with complex ORM — DRF stays simpler.
- Simple CRUD with no async benefit — Flask/DRF easier to operate.
- GraphQL — different schema model.
- Team has zero async experience and timeline is tight — risk of subtle bugs.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| DB driver | string (asyncpg, aiomysql, motor) | infra ADR |
| Auth scheme | JWT / cookie | security ADR |
| Migration tool | alembic / piccolo | infra ADR |
| Settings management | pydantic-settings | config ADR |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[python]]` | Python ecosystem rules apply at the language level. |
| `[[python-poetry-setup]]` | Dep manager pin. |
| `[[error-handling]]` | RFC 7807 envelope for HTTP errors. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: lifespan, schema separation, Annotated aliases, async services return ORM, flush+refresh | ~700 |
| `content/01-project-structure.xml` | essential | Recommended directory layout (kept) | ~700 |
| `content/02-output-contract.xml` | essential | App shape + per-endpoint invariants | ~700 |
| `content/02-schemas-deps.xml` | essential | Schemas + Annotated deps (kept) | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: deprecated on_event, schema reuse, logic in router, sync DB call in async route | ~600 |
| `content/03-service-layer.xml` | essential | Service-function patterns (kept) | ~700 |
| `content/04-antipatterns.xml` | essential | Additional FastAPI-specific traps (kept) | ~600 |
| `content/04-procedure.xml` | medium | 6-step scaffold | ~800 |
| `content/06-decision-tree.xml` | essential | Root question on async REST API needing OpenAPI | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold main + lifespan | sonnet | Template. |
| Generate schemas | sonnet | DTO generation. |
| Migrate sync endpoint to async | opus | I/O reasoning. |
| Auth dependency wiring | sonnet | Pattern. |

## Templates

| File | Purpose |
|------|---------|
| `templates/main.py` | App + lifespan + router include scaffold. |
| `templates/schemas.py` | Base/Create/Update/Response schema skeletons. |
| `templates/dependencies.py` | Annotated DBSession + CurrentUser aliases. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-fastapi.py` | Greps for @app.on_event, sync DB calls in async routes, schema reuse. | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[python]]` — Python language rules
- `[[error-handling]]` — RFC 7807 envelope
- `[[integration-testing]]` — async test session pattern

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: async-benefiting workload, team comfort with async, Pydantic v2 adoptable.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/main.py`

```python
"""
FastAPI application entry point.
Adjust imports, router includes, and middleware to your project structure.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import init_db, close_db
from app.routers import users  # add more routers here


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup, release on shutdown."""
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production API",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy", "version": "1.0.0"}
```

### `templates/schemas.py`

```python
"""
Pydantic v2 schema hierarchy for User resource.
Copy and adapt for other resources: rename User → YourResource.
"""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """Request schema for user creation. Includes password (not in response)."""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Request schema for partial update (PATCH). All fields optional."""
    email: EmailStr | None = None
    name: str | None = Field(None, min_length=1, max_length=100)


class UserResponse(UserBase):
    """Response schema. Excludes password. from_attributes for ORM serialization."""
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    is_active: bool
    created_at: datetime


class UserListResponse(BaseModel):
    """Paginated user list response."""
    items: list[UserResponse]
    total: int
    page: int
    size: int
    pages: int
```

### `templates/dependencies.py`

```python
"""
Shared FastAPI dependencies: DB session, current user, type aliases.
Import DBSession and CurrentUser in route functions instead of raw Depends().
"""
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.config import settings
from app.db.database import async_session
from app.models.user import User
from app.services import users as user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_db() -> AsyncSession:  # type: ignore[return]
    """Yields an async DB session; commits on success, rolls back on error."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret,
                             algorithms=[settings.jwt_algorithm])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await user_service.get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Inactive user")
    return current_user


# Use these aliases in route function signatures
DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_active_user)]
```
