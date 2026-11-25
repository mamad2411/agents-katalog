---
name: tpl-backend-python-fastapi
description: Template do pack (backend/02-python-fastapi.md). Orienta o agente em APIs, servicos e arquitetura backend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: backend/02-python-fastapi.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Python REST API (FastAPI)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `backend/02-python-fastapi.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12 | Runtime |
| FastAPI | 0.111+ | HTTP framework |
| SQLAlchemy | 2.0 async | ORM |
| asyncpg | 0.29+ | Async PostgreSQL driver |
| Alembic | 1.13+ | Database migrations |
| Pydantic | v2 | Request/response validation + settings |
| pytest | 8.x | Test runner |
| httpx | 0.27+ | Async HTTP client for tests |
| ruff | 0.4+ | Linting + formatting |
| mypy | 1.10+ | Static type checking |
| python-jose | 3.x | JWT tokens |
| passlib[bcrypt] | 1.7+ | Password hashing |

---

## PROJECT STRUCTURE

```
app/
├── core/
│   ├── config.py         # Pydantic BaseSettings — env vars
│   ├── security.py       # JWT creation/verification, password hashing
│   ├── database.py       # Async engine + session factory
│   └── exceptions.py     # Custom HTTP exceptions + handlers
├── modules/
│   └── users/
│       ├── router.py          # APIRouter, endpoints only
│       ├── service.py         # Business logic
│       ├── repository.py      # DB queries (SQLAlchemy)
│       ├── models.py          # SQLAlchemy ORM models
│       ├── schemas.py         # Pydantic request/response schemas
│       └── dependencies.py    # FastAPI Depends() factories
├── middlewares/
│   ├── logging.py        # Request/response logging
│   └── cors.py           # CORS config
├── tasks/
│   └── email.py          # Background tasks (send email, etc.)
├── migrations/
│   ├── env.py            # Alembic async env config
│   └── versions/         # Auto-generated migration files
└── main.py               # App factory, include_router, lifespan
alembic.ini
pyproject.toml
tests/
├── conftest.py           # Fixtures: async client, test DB, test user
├── unit/
│   └── users/
│       └── test_service.py
└── integration/
    └── users/
        └── test_router.py
```

---

## ARCHITECTURE RULES

- **Router → Service → Repository** — strict, no skipping layers
- Routers contain ONLY path declarations and dependency injection
- Services contain business logic — never import `Request` or `Response`
- Repositories contain ONLY SQLAlchemy queries — no `if/else` logic
- All endpoint functions are `async def`; synchronous endpoints use `run_in_executor`
- Models (SQLAlchemy) and Schemas (Pydantic) are SEPARATE — never expose ORM objects directly
- All schemas use `model_config = ConfigDict(from_attributes=True)` for ORM conversion

---

## DEPENDENCY INJECTION PATTERN

### Async Session Dependency

```python
# app/core/database.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### Current User Dependency

```python
# app/modules/users/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_access_token
from app.modules.users.repository import UserRepository
from app.modules.users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = decode_access_token(token)  # raises 401 if invalid
    user = await UserRepository(db).get_by_id(payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin required")
    return current_user
```

### OAuth2 Password Flow (Login endpoint)

```python
# app/modules/auth/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.modules.users.repository import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    repo = UserRepository(db)
    user = await repo.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return {
        "access_token": create_access_token({"sub": str(user.id), "role": user.role}),
        "refresh_token": create_refresh_token(str(user.id)),
        "token_type": "bearer",
    }
```

### Background Tasks

```python
# app/tasks/email.py
from fastapi import BackgroundTasks
import smtplib
from app.core.config import settings

def send_welcome_email(email: str, name: str) -> None:
    # This runs in a thread pool — do NOT use async here
    print(f"Sending welcome email to {email}")

# In router:
@router.post("/register", status_code=201)
async def register(
    body: UserCreateSchema,
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    user = await UserService(db).create(body)
    background_tasks.add_task(send_welcome_email, user.email, user.name)
    return user
```

---

## SETTINGS PATTERN

```python
# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

settings = Settings()
```

---

## ROUTING TABLE

| Trigger | Method | Route | Auth | Handler |
|---------|--------|-------|------|---------|
| Register | POST | `/api/v1/auth/register` | Public | auth.register |
| Login | POST | `/api/v1/auth/login` | Public (form) | auth.login |
| Refresh | POST | `/api/v1/auth/refresh` | Refresh token | auth.refresh |
| Get profile | GET | `/api/v1/users/me` | Bearer | users.me |
| Update profile | PATCH | `/api/v1/users/me` | Bearer | users.update_me |
| List all users | GET | `/api/v1/users` | Bearer + admin | users.list |
| Get user by ID | GET | `/api/v1/users/{id}` | Bearer + admin | users.get |
| Delete user | DELETE | `/api/v1/users/{id}` | Bearer + admin | users.delete |
| Health check | GET | `/health` | Public | health.check |

---

## QUALITY GATES

Before opening a PR, verify ALL of the following:

- [ ] `ruff check . && ruff format --check .` passes with zero issues
- [ ] `mypy app/` passes — no `type: ignore` without a comment explaining why
- [ ] `pytest -x --tb=short` passes with zero failures
- [ ] Coverage ≥ 80% for new service/repository code
- [ ] New Alembic migration generated for any model changes: `alembic revision --autogenerate`
- [ ] Migration tested: `alembic upgrade head && alembic downgrade -1`
- [ ] No synchronous DB calls inside `async def` functions — always `await`
- [ ] No ORM model instances returned directly from endpoints — always use Pydantic schemas
- [ ] All new endpoints have a type annotation for the response model
- [ ] Secrets not hardcoded — sourced from `Settings`

---

## FORBIDDEN

- **NEVER** use `session.execute(text("raw SQL"))` — use SQLAlchemy ORM expressions
- **NEVER** define `async def` route handlers that block on sync I/O without `run_in_executor`
- **NEVER** share a single `AsyncSession` across multiple requests
- **NEVER** return SQLAlchemy model objects directly — always serialize through Pydantic
- **NEVER** use `from __future__ import annotations` — it breaks Pydantic v2 at runtime
- **NEVER** commit secrets to git — use `.env` (gitignored) and `.env.example`
- **NEVER** use `Union[X, None]` — use `X | None` (Python 3.10+ syntax)
- **NEVER** put business logic in Pydantic validators — keep them in services
- **NEVER** use `global` variables for shared state — use dependency injection
- **NEVER** ignore mypy errors with blanket `# type: ignore` — fix the types
