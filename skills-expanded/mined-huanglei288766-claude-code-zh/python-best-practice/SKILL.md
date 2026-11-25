---
name: python-best-practice
description: Python 开发最佳实践，涵盖项目结构、类型提示、异步编程、FastAPI/Django、pytest 测试模式
version: "1.0"
---

# Python 最佳实践

## 概述

本 Skill 指导 Python 项目的最佳实践，包括项目结构、类型提示、异步编程、错误处理、Web 框架、测试和包管理。

适用场景：
- 新建 Python 项目时确定目录结构和工具链
- FastAPI / Django 项目的架构设计
- 异步编程模式选择
- pytest 测试策略制定
- 类型系统设计与 Protocol 使用

---

## 项目结构

### src layout（推荐，适合发布为包）

```
my-project/
├── pyproject.toml          # 项目元数据和依赖（统一配置入口）
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py          # 入口文件
│       ├── config.py         # 配置管理
│       ├── domain/           # 领域层
│       │   ├── models.py
│       │   └── services.py
│       ├── api/              # 接口层
│       │   ├── routes.py
│       │   └── schemas.py    # Pydantic 模型
│       ├── infra/            # 基础设施层
│       │   ├── database.py
│       │   └── repositories.py
│       └── common/           # 通用工具
│           ├── exceptions.py
│           └── utils.py
├── tests/
│   ├── conftest.py           # 全局 fixture
│   ├── unit/
│   └── integration/
└── scripts/                  # 运维脚本
```

### flat layout（适合小型项目或微服务）

```
my-project/
├── pyproject.toml
├── my_project/
│   ├── __init__.py
│   ├── main.py
│   └── ...
└── tests/
```

**选择原则**：需要发布到 PyPI 或多包管理用 src layout；内部微服务用 flat layout。

---

## 类型提示

### 基础类型注解

```python
from typing import Optional
from collections.abc import Sequence

# 基础参数和返回值注解（Python 3.10+ 可用 | 替代 Optional）
def find_user(user_id: int) -> dict[str, str] | None:
    """根据用户 ID 查找用户，未找到返回 None"""
    ...

# 容器类型（Python 3.9+ 可直接用内置类型）
def process_items(items: list[str]) -> dict[str, int]:
    """处理条目列表，返回计数字典"""
    return {item: items.count(item) for item in set(items)}

# 复杂嵌套类型用 TypeAlias 提高可读性
type UserMap = dict[int, list[str]]  # Python 3.12+ type 语句
```

### Protocol（结构化子类型，鸭子类型的类型安全版）

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Repository(Protocol):
    """仓储协议 — 任何实现了这些方法的类都满足该协议"""

    def find_by_id(self, entity_id: int) -> dict | None: ...
    def save(self, entity: dict) -> None: ...
    def delete(self, entity_id: int) -> bool: ...


class MySQLUserRepository:
    """MySQL 用户仓储 — 无需显式继承 Repository"""

    def find_by_id(self, entity_id: int) -> dict | None:
        # 从 MySQL 查询
        ...

    def save(self, entity: dict) -> None:
        # 写入 MySQL
        ...

    def delete(self, entity_id: int) -> bool:
        # 从 MySQL 删除
        ...


def get_user(repo: Repository, user_id: int) -> dict | None:
    """依赖 Protocol 而非具体实现，方便测试和替换"""
    return repo.find_by_id(user_id)
```

### TypeVar 与泛型

```python
from typing import TypeVar, Generic

T = TypeVar("T")

class PageResult(Generic[T]):
    """通用分页结果"""

    def __init__(self, items: list[T], total: int, page: int, size: int) -> None:
        self.items = items
        self.total = total
        self.page = page
        self.size = size

    @property
    def total_pages(self) -> int:
        return (self.total + self.size - 1) // self.size

    def map(self, func: "Callable[[T], R]") -> "PageResult[R]":
        """转换分页中的每个元素"""
        return PageResult(
            items=[func(item) for item in self.items],
            total=self.total,
            page=self.page,
            size=self.size,
        )
```

---

## 异步编程

### asyncio 基础模式

```python
import asyncio
from collections.abc import Coroutine

async def fetch_user(user_id: int) -> dict:
    """模拟异步获取用户信息"""
    await asyncio.sleep(0.1)  # 模拟 IO 操作
    return {"id": user_id, "name": f"用户{user_id}"}

async def fetch_users_batch(user_ids: list[int]) -> list[dict]:
    """并发获取多个用户 — 使用 gather 并行执行"""
    tasks = [fetch_user(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    users = []
    for uid, result in zip(user_ids, results):
        if isinstance(result, Exception):
            # 记录错误，跳过失败的请求
            logger.error(f"获取用户 {uid} 失败: {result}")
        else:
            users.append(result)
    return users
```

### aiohttp 异步 HTTP 客户端

```python
import aiohttp
import asyncio

async def fetch_data(url: str, timeout: int = 10) -> dict:
    """异步 HTTP 请求，带超时和重试"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
                resp.raise_for_status()
                return await resp.json()
        except aiohttp.ClientError as e:
            raise ExternalServiceError(f"请求外部服务失败: {url}") from e

async def fetch_multiple(urls: list[str]) -> list[dict]:
    """并发请求多个 URL，用 Semaphore 控制并发数"""
    semaphore = asyncio.Semaphore(10)  # 最多 10 个并发请求

    async def _fetch(url: str) -> dict:
        async with semaphore:
            return await fetch_data(url)

    return await asyncio.gather(*[_fetch(url) for url in urls])
```

### 异步上下文管理器

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

@asynccontextmanager
async def get_db_connection() -> AsyncIterator["AsyncConnection"]:
    """异步数据库连接上下文管理器"""
    conn = await create_connection()
    try:
        yield conn
    except Exception:
        await conn.rollback()
        raise
    else:
        await conn.commit()
    finally:
        await conn.close()

# 使用
async def create_user(user_data: dict) -> int:
    async with get_db_connection() as conn:
        result = await conn.execute("INSERT INTO users ...", user_data)
        return result.lastrowid
```

---

## 错误处理

### 自定义异常层级

```python
class AppError(Exception):
    """应用异常基类"""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class BusinessError(AppError):
    """业务异常 — 可预期的业务规则违反"""

    def __init__(self, message: str, code: str = "BUSINESS_ERROR") -> None:
        super().__init__(message, code)


class NotFoundError(BusinessError):
    """资源不存在"""

    def __init__(self, resource: str, identifier: str | int) -> None:
        super().__init__(
            message=f"{resource} 不存在: {identifier}",
            code="NOT_FOUND",
        )


class DuplicateError(BusinessError):
    """资源重复"""

    def __init__(self, resource: str, field: str, value: str) -> None:
        super().__init__(
            message=f"{resource} 的 {field} 已存在: {value}",
            code="DUPLICATE",
        )


class ExternalServiceError(AppError):
    """外部服务调用异常"""

    def __init__(self, message: str, service_name: str = "") -> None:
        super().__init__(message, code="EXTERNAL_SERVICE_ERROR")
        self.service_name = service_name


class ValidationError(AppError):
    """参数校验异常"""

    def __init__(self, errors: list[dict]) -> None:
        super().__init__("参数校验失败", code="VALIDATION_ERROR")
        self.errors = errors
```

---

## FastAPI 最佳实践

### 项目结构与路由

```python
# api/routes/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/users", tags=["用户管理"])


class CreateUserRequest(BaseModel):
    """创建用户请求体"""
    username: str = Field(..., min_length=3, max_length=32, description="用户名")
    email: str = Field(..., pattern=r"^[\w.-]+@[\w.-]+\.\w+$", description="邮箱")
    password: str = Field(..., min_length=8, description="密码")

    model_config = {"json_schema_extra": {"examples": [
        {"username": "zhangsan", "email": "zhang@example.com", "password": "secure123"}
    ]}}


class UserResponse(BaseModel):
    """用户响应体"""
    id: int
    username: str
    email: str


class ApiResponse(BaseModel, Generic[T]):
    """统一响应格式"""
    code: int = 0
    message: str = "success"
    data: T | None = None


@router.post("", response_model=ApiResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    service: UserService = Depends(get_user_service),
) -> ApiResponse[UserResponse]:
    """创建用户"""
    user = await service.create_user(request)
    return ApiResponse(data=UserResponse.model_validate(user))


@router.get("/{user_id}", response_model=ApiResponse[UserResponse])
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> ApiResponse[UserResponse]:
    """获取用户详情"""
    user = await service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return ApiResponse(data=UserResponse.model_validate(user))
```

### 全局异常处理

```python
# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="示例服务", version="1.0.0")

@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError) -> JSONResponse:
    """业务异常统一处理"""
    return JSONResponse(
        status_code=400,
        content={"code": exc.code, "message": exc.message, "data": None},
    )

@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"code": exc.code, "message": exc.message, "data": None},
    )

@app.exception_handler(Exception)
async def global_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """未捕获异常兜底 — 记录日志但不暴露内部错误"""
    logger.exception(f"未处理异常: {request.method} {request.url}")
    return JSONResponse(
        status_code=500,
        content={"code": "INTERNAL_ERROR", "message": "服务器内部错误", "data": None},
    )
```

### 依赖注入

```python
# dependencies.py
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

@lru_cache
def get_settings() -> Settings:
    """缓存配置对象，避免重复加载"""
    return Settings()

async def get_db_session() -> AsyncIterator[AsyncSession]:
    """每个请求一个数据库 Session"""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

def get_user_service(session: AsyncSession = Depends(get_db_session)) -> UserService:
    """注入 UserService 及其依赖"""
    repo = SQLAlchemyUserRepository(session)
    return UserService(repo)
```

---

## Django 最佳实践

### 模型设计

```python
# models.py
from django.db import models
import uuid

class BaseModel(models.Model):
    """基础模型 — 所有模型继承此类"""
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        abstract = True

    def soft_delete(self) -> None:
        """软删除"""
        self.is_deleted = True
        self.save(update_fields=["is_deleted", "updated_at"])


class Order(BaseModel):
    """订单模型"""
    order_no = models.CharField(max_length=32, unique=True, verbose_name="订单号",
                                default=uuid.uuid4)
    user_id = models.BigIntegerField(db_index=True, verbose_name="用户ID")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="金额")
    status = models.SmallIntegerField(default=0, verbose_name="状态")

    class Meta:
        db_table = "orders"
        indexes = [
            models.Index(fields=["user_id", "status"], name="idx_user_status"),
        ]
```

---

## pytest 测试模式

### fixture 与参数化

```python
# conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """异步测试客户端"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def sample_user() -> dict:
    """测试用户数据"""
    return {"username": "testuser", "email": "test@example.com", "password": "secure123"}


# test_user.py
import pytest

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, sample_user: dict) -> None:
    """测试创建用户 — 正常流程"""
    resp = await client.post("/api/v1/users", json=sample_user)
    assert resp.status_code == 201
    data = resp.json()
    assert data["code"] == 0
    assert data["data"]["username"] == sample_user["username"]


@pytest.mark.asyncio
async def test_create_user_duplicate(client: AsyncClient, sample_user: dict) -> None:
    """测试创建用户 — 重复用户名应返回错误"""
    await client.post("/api/v1/users", json=sample_user)
    resp = await client.post("/api/v1/users", json=sample_user)
    assert resp.status_code == 400
    assert resp.json()["code"] == "DUPLICATE"


@pytest.mark.parametrize("field,value,expected_error", [
    ("username", "ab", "用户名长度不足"),
    ("email", "invalid", "邮箱格式错误"),
    ("password", "short", "密码长度不足"),
])
@pytest.mark.asyncio
async def test_create_user_validation(
    client: AsyncClient, sample_user: dict, field: str, value: str, expected_error: str,
) -> None:
    """测试创建用户 — 参数校验"""
    payload = {**sample_user, field: value}
    resp = await client.post("/api/v1/users", json=payload)
    assert resp.status_code == 422  # Pydantic 校验失败
```

### Mock 与依赖替换

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_get_user_from_external_service() -> None:
    """测试外部服务调用 — 使用 Mock 替换"""
    mock_response = {"id": 1, "name": "张三"}

    with patch("services.external.fetch_user", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = mock_response
        result = await user_service.get_external_user(1)
        assert result["name"] == "张三"
        mock_fetch.assert_called_once_with(1)
```

---

## 包管理

### poetry（成熟稳定）

```bash
# 初始化项目
poetry init
# 添加依赖
poetry add fastapi uvicorn[standard]
# 添加开发依赖
poetry add --group dev pytest pytest-asyncio ruff mypy
# 安装所有依赖
poetry install
# 运行命令
poetry run pytest
```

### uv（极速，推荐新项目）

```bash
# 初始化项目
uv init my-project
# 添加依赖
uv add fastapi uvicorn
# 添加开发依赖
uv add --dev pytest pytest-asyncio ruff mypy
# 同步依赖
uv sync
# 运行命令
uv run pytest
```

### pyproject.toml 配置示例

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"

[tool.ruff]
target-version = "py312"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "SIM", "RUF"]

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

---

## 编码规范速查

| 规则 | 说明 |
|------|------|
| 类型注解 | 所有公开函数必须有参数和返回值类型注解 |
| 不可变优先 | 使用 `tuple` 替代 `list`（数据不变时），`frozenset` 替代 `set` |
| dataclass | 数据类优先使用 `@dataclass(frozen=True)` 或 Pydantic `BaseModel` |
| 命名 | 模块/变量 snake_case，类 PascalCase，常量 UPPER_SNAKE |
| 文档字符串 | 公开类和函数必须有 docstring（Google 风格） |
| 格式化 | 使用 ruff format（替代 black），ruff check（替代 flake8 + isort） |
| 类型检查 | 使用 mypy --strict 或 pyright |
