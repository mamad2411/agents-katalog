---
description: Python 开发规范，适用于 Python 3.10+ 项目
globs: ["**/*.py", "**/pyproject.toml", "**/requirements*.txt"]
alwaysApply: false
---

# Python 开发规范

## 基础规范

- 遵循 [PEP 8](https://peps.python.org/pep-0008/) 代码风格
- 使用 `ruff` 进行 lint 和格式化（替代 black + flake8 + isort）
- Python 版本要求：3.10+
- 使用类型注解（Type Hints），开启 `mypy` 静态检查

## 项目管理

- 使用 `uv` 或 `poetry` 管理依赖和虚拟环境
- 依赖定义在 `pyproject.toml` 中
- 区分开发依赖和生产依赖

```toml
# pyproject.toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.110.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.3.0",
    "mypy>=1.9.0",
]

[tool.ruff]
line-length = 120
target-version = "py310"

[tool.mypy]
python_version = "3.10"
strict = true
```

## 命名规范

- 模块和包：小写 + 下划线 `user_service.py`
- 类：PascalCase `class UserService`
- 函数/方法/变量：小写 + 下划线 `def get_user()`
- 常量：大写 + 下划线 `MAX_RETRIES = 3`
- 私有成员：单下划线前缀 `_internal_method()`
- 类型别名：PascalCase `UserId = NewType("UserId", str)`

## 类型注解

```python
from typing import TypeVar, Generic
from collections.abc import Sequence, Callable, AsyncGenerator

# 基础注解
def get_user(user_id: str) -> User | None:
    ...

# 泛型
T = TypeVar("T")

def first(items: Sequence[T]) -> T | None:
    return items[0] if items else None

# Python 3.10+ 联合类型简写
def process(value: int | str | None) -> str:
    match value:
        case int(n): return str(n)
        case str(s): return s
        case None: return ""

# TypedDict
from typing import TypedDict

class UserDict(TypedDict):
    id: str
    name: str
    email: str
```

## 数据验证：Pydantic

```python
from pydantic import BaseModel, Field, EmailStr, field_validator

class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    age: int = Field(ge=0, le=150)
    
    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name cannot be blank")
        return v.strip()

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    
    model_config = {"from_attributes": True}  # 支持 ORM 对象
```

## 错误处理

```python
# 自定义异常层次
class AppError(Exception):
    def __init__(self, message: str, code: str) -> None:
        super().__init__(message)
        self.code = code

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str) -> None:
        super().__init__(f"{resource} {id} not found", "NOT_FOUND")

class ValidationError(AppError):
    pass

# 使用具体异常而非裸 except
try:
    user = await user_repo.get(user_id)
except NotFoundError:
    raise HTTPException(status_code=404, detail="User not found")
except Exception as e:
    logger.exception("Unexpected error fetching user", extra={"user_id": user_id})
    raise
```

## 异步编程

```python
import asyncio
from asyncio import TaskGroup

# 使用 TaskGroup（Python 3.11+）并发执行任务
async def fetch_dashboard(user_id: str) -> Dashboard:
    async with TaskGroup() as tg:
        user_task = tg.create_task(fetch_user(user_id))
        orders_task = tg.create_task(fetch_orders(user_id))
        notifications_task = tg.create_task(fetch_notifications(user_id))

    return Dashboard(
        user=user_task.result(),
        orders=orders_task.result(),
        notifications=notifications_task.result(),
    )

# 异步上下文管理器
async def get_db_connection() -> AsyncGenerator[Connection, None]:
    async with pool.acquire() as conn:
        yield conn
```

## FastAPI 规范

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="My API", version="1.0.0")

# 依赖注入
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    user = await auth_service.verify_token(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return user

# 路由
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: CreateUserRequest,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
) -> UserResponse:
    user = await user_service.create(body, db)
    return UserResponse.model_validate(user)
```

## 测试规范

- 使用 `pytest` 作为测试框架
- 测试文件命名：`test_<module_name>.py`
- 测试函数命名：`test_<function>_<scenario>_<expected>`
- 使用 `pytest-asyncio` 测试异步代码
- 使用 `pytest-cov` 测量覆盖率

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user_valid_input_returns_201(
    client: AsyncClient,
    admin_token: str,
) -> None:
    response = await client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com", "age": 30},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert "id" in data

@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
```

## 日志规范

```python
import logging
import structlog  # 推荐使用结构化日志

logger = structlog.get_logger(__name__)

# 使用结构化日志
await logger.ainfo(
    "user_created",
    user_id=user.id,
    email=user.email,
)

await logger.aerror(
    "payment_failed",
    user_id=user_id,
    amount=amount,
    error=str(exc),
)
```

## 项目目录结构

```
project/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── main.py          # FastAPI 应用入口
│       ├── api/             # 路由层
│       │   └── v1/
│       ├── core/            # 核心配置
│       │   ├── config.py
│       │   └── security.py
│       ├── models/          # ORM 模型
│       ├── schemas/         # Pydantic 模型
│       ├── services/        # 业务逻辑
│       └── repositories/   # 数据访问层
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── README.md
```
