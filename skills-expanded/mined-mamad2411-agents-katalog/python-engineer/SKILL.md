---
name: python-engineer
description: Build production Python applications — FastAPI/Flask backends, async processing, data engineering with pandas, scripting automation, CLI tools with Typer, testing with pytest, type hints, virtual environments, and package management. Use when building Python backends, data pipelines, scripts, or CLI tools.
---

# Python Engineering

## Project Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows
pip install fastapi uvicorn pydantic sqlalchemy alembic pytest httpx
```

### Project Structure
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + lifespan
│   ├── config.py             # Settings from env vars
│   ├── models/               # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/               # Pydantic schemas
│   │   └── user.py
│   ├── routes/                # API route handlers
│   │   └── users.py
│   ├── services/              # Business logic
│   │   └── user_service.py
│   ├── repositories/          # Database queries
│   │   └── user_repo.py
│   └── utils/                 # Helpers
│       └── auth.py
├── tests/
│   ├── conftest.py
│   └── test_users.py
├── alembic/
├── alembic.ini
├── pyproject.toml
├── requirements.txt
└── Dockerfile
```

## FastAPI Patterns

### Application Setup
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(title="My API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Route Handler
```python
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(prefix="/api/users", tags=["users"])

class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: str
    email: str
    name: str

    model_config = {"from_attributes": True}

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    existing = await user_service.get_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = await user_service.create(db, data)
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    user = await user_service.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Dependency Injection
```python
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    debug: bool = False

    model_config = {"env_file": ".env"}

@lru_cache
def get_settings() -> Settings:
    return Settings()

async def get_db():
    async with AsyncSession(engine) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

## Testing with pytest

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.anyio
async def test_create_user(client: AsyncClient):
    response = await client.post("/api/users/", json={
        "email": "test@example.com",
        "name": "Test User",
        "password": "SecurePass123",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"

@pytest.mark.anyio
async def test_duplicate_email_returns_409(client: AsyncClient):
    payload = {"email": "dup@test.com", "name": "User", "password": "SecurePass123"}
    await client.post("/api/users/", json=payload)
    response = await client.post("/api/users/", json=payload)
    assert response.status_code == 409
```

## CLI Tools (Typer)
```python
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="My CLI tool")
console = Console()

@app.command()
def greet(name: str, count: int = typer.Option(1, help="Number of greetings")):
    for _ in range(count):
        console.print(f"Hello, [bold magenta]{name}[/bold magenta]!")

@app.command()
def list_users():
    table = Table(title="Users")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="bold")
    table.add_column("Email")
    for user in get_users():
        table.add_row(user.id, user.name, user.email)
    console.print(table)

if __name__ == "__main__":
    app()
```

## Data Processing (pandas)
```python
import pandas as pd

def process_csv(input_path: str, output_path: str) -> None:
    df = pd.read_csv(input_path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df = df.dropna(subset=["email"])
    df["email"] = df["email"].str.lower().str.strip()
    df = df.drop_duplicates(subset=["email"], keep="last")
    df.to_csv(output_path, index=False)
```

## Best Practices
- Type hints on ALL function signatures
- Use `pydantic` for data validation — never validate manually
- Use `async` for I/O-bound operations
- Use `ruff` for linting and formatting
- Use `pyproject.toml` over `setup.py`
- Never use bare `except:` — always catch specific exceptions
- Use `pathlib.Path` over `os.path`
- Use `f-strings` — never `%` formatting or `.format()`
