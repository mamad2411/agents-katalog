---
name: python-typing
description: "When to activate: Python type hints, TypeVar, Generic, Protocol, TypedDict, Literal, typing extensions, mypy"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Python Typing Patterns

## Modern Type Hints (3.10+)
```python
from __future__ import annotations  # enables PEP 563 postponed evaluation

# Union: use | not Optional/Union
def find(id: int) -> User | None: ...

# Built-in generics (no need for List, Dict from typing)
def process(items: list[str]) -> dict[str, int]: ...

# Callable type
from collections.abc import Callable, Awaitable
Handler = Callable[[Request], Awaitable[Response]]

# TypeAlias (explicit)
from typing import TypeAlias
UserId: TypeAlias = int
JsonDict: TypeAlias = dict[str, "JsonValue"]
```

## TypeVar and Generics
```python
from typing import TypeVar, Generic
from collections.abc import Callable, Iterator

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)

class Repository(Generic[T]):
    async def get(self, id: int) -> T | None: ...
    async def list(self) -> list[T]: ...
    async def create(self, data: dict) -> T: ...

class UserRepository(Repository[User]):
    async def get(self, id: int) -> User | None:
        return await db.get(User, id)

# TypeVar with bound
Comparable = TypeVar("Comparable", bound="SupportsLT")

def minimum(items: list[Comparable]) -> Comparable:
    return min(items)
```

## Protocol (structural subtyping)
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    def to_dict(self) -> dict: ...
    
    @classmethod
    def from_dict(cls, data: dict) -> "Serializable": ...

# Any class with these methods satisfies the Protocol — no inheritance needed
class User:
    def to_dict(self) -> dict:
        return {"id": self.id, "email": self.email}
    
    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(id=data["id"], email=data["email"])

def serialize_all(items: list[Serializable]) -> list[dict]:
    return [item.to_dict() for item in items]
```

## TypedDict
```python
from typing import TypedDict, Required, NotRequired

class UserDict(TypedDict):
    id: Required[int]
    email: Required[str]
    name: Required[str]
    bio: NotRequired[str]  # optional key

class PaginatedResponse(TypedDict):
    data: list[UserDict]
    total: int
    page: int
    per_page: int
```

## Literal Types
```python
from typing import Literal, overload

Status = Literal["pending", "active", "cancelled"]
HttpMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]

def set_status(order: Order, status: Status) -> None: ...

@overload
def process(x: int) -> int: ...
@overload
def process(x: str) -> str: ...
def process(x: int | str) -> int | str:
    if isinstance(x, int):
        return x * 2
    return x.upper()
```

## Mypy Configuration
```toml
[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true
plugins = ["pydantic.mypy", "sqlalchemy.ext.mypy.plugin"]

# Per-module overrides
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```
