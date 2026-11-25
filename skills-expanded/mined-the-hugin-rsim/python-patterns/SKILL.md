---
name: python-patterns
description: Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications.
origin: ECC
group: domain
triggers:
  - "Python код"
  - "питоновский стиль"
  - "type hints"
  - "pyproject.toml"
output: "idiomatic Python code with type hints, proper error handling, and best practices"
calls: []
---

# Python Development Patterns

Idiomatic Python patterns and best practices for building robust, efficient, and maintainable applications.

## When to Activate

- Writing new Python code
- Reviewing Python code
- Refactoring existing Python code
- Designing Python packages/modules

## Core Principles

### 1. Readability Counts

```python
# Good: Clear and readable
def get_active_users(users: list[User]) -> list[User]:
    return [user for user in users if user.is_active]

# Bad: Clever but confusing
def get_active_users(u):
    return [x for x in u if x.a]
```

### 2. Explicit is Better Than Implicit

Avoid magic; be clear about what your code does.

### 3. EAFP — Easier to Ask Forgiveness Than Permission

```python
# Good: EAFP style
def get_value(dictionary: dict, key: str) -> Any:
    try:
        return dictionary[key]
    except KeyError:
        return default_value

# Bad: LBYL (Look Before You Leap)
def get_value(dictionary: dict, key: str) -> Any:
    if key in dictionary:
        return dictionary[key]
    return default_value
```

## Type Hints

### Modern Type Hints (Python 3.9+)

```python
# Python 3.9+ — use built-in types
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# TypeVar for generics
from typing import TypeVar
T = TypeVar('T')

def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

### Protocol-Based Duck Typing

```python
from typing import Protocol

class Renderable(Protocol):
    def render(self) -> str: ...

def render_all(items: list[Renderable]) -> str:
    return "\n".join(item.render() for item in items)
```

## Error Handling

### Specific Exception Handling

```python
# Good: specific + chained
def load_config(path: str) -> Config:
    try:
        with open(path) as f:
            return Config.from_json(f.read())
    except FileNotFoundError as e:
        raise ConfigError(f"Config file not found: {path}") from e
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in config: {path}") from e

# Bad: bare except / silent failure
try:
    ...
except:
    return None
```

### Custom Exception Hierarchy

```python
class AppError(Exception): pass
class ValidationError(AppError): pass
class NotFoundError(AppError): pass
```

## Context Managers

```python
# Prefer with for all resources
with open(path, 'r') as f:
    return f.read()

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    start = time.perf_counter()
    yield
    print(f"{name} took {time.perf_counter() - start:.4f}s")
```

## Data Classes

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    id: str
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def __post_init__(self):
        if "@" not in self.email:
            raise ValueError(f"Invalid email: {self.email}")
```

## Generators for Large Data

```python
# Good: lazy evaluation
def read_large_file(path: str) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            yield line.strip()

# Good: generator expression
total = sum(x * x for x in range(1_000_000))
```

## Concurrency

```python
import concurrent.futures

# I/O-bound: threads
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_url, urls))

# CPU-bound: processes
with concurrent.futures.ProcessPoolExecutor() as executor:
    results = list(executor.map(heavy_compute, datasets))

# Async for concurrent I/O
async def fetch_all(urls: list[str]) -> list[str]:
    tasks = [fetch_async(url) for url in urls]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

## Memory Optimization

```python
# __slots__ reduces memory
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

# join instead of concatenation
result = "".join(str(item) for item in items)  # O(n)
# not: result += str(item)                     # O(n²)
```

## Tooling

```bash
black .          # formatting
isort .          # import sorting
ruff check .     # linting
mypy .           # type checking
pytest           # testing
bandit -r .      # security scan
```

### pyproject.toml

```toml
[tool.black]
line-length = 88
target-version = ['py39']

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.9"
disallow_untyped_defs = true
warn_return_any = true
```

## Anti-Patterns

```python
# Bad: mutable default argument
def append_to(item, items=[]):     # mutates across calls!
    items.append(item)
# Good:
def append_to(item, items=None):
    if items is None: items = []
    items.append(item)

# Bad: type() check
if type(obj) == list: ...
# Good: isinstance
if isinstance(obj, list): ...

# Bad: None comparison
if value == None: ...
# Good:
if value is None: ...

# Bad: wildcard import
from os.path import *
# Good: explicit
from os.path import join, exists
```

## Quick Reference

| Idiom | Description |
|-------|-------------|
| EAFP | Try first, handle exceptions |
| Context managers | `with` for all resources |
| List comprehensions | Simple transformations |
| Generators | Lazy evaluation, large datasets |
| Type hints | Annotate all function signatures |
| Dataclasses | Data containers with auto methods |
| `__slots__` | Memory optimization |
| f-strings | String formatting (3.6+) |
| `pathlib.Path` | Path operations (3.4+) |
| `enumerate` | Index-element pairs in loops |
