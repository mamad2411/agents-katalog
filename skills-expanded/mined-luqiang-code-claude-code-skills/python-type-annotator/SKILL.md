---
name: python-type-annotator
description: |
  Add missing type annotations to Python code. Generates mypy-compatible type hints
  for function signatures, variables, and class attributes.
  Triggers on "add types", "type annotate", "add type hints", "type this file".
metadata:
  type: tool
  version: "1.0.0"
  author: community
  tags: [python, type-hints, mypy, static-analysis]
triggers:
  - "add types"
  - "type annotate"
  - "add type hints"
  - "type this file"
  - "mypy"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Python Type Annotator

Add mypy-compatible type annotations to Python code.

## When to Use
- A Python file/module is missing type hints
- Preparing to enable mypy in CI
- User mentions "type hints", "type annotate", "mypy"

## When NOT to Use
- The project doesn't use Python 3.8+ (type syntax differs)
- Code that's intentionally dynamic (use `Any` sparingly instead)
- Third-party library stubs (use `types-*` packages)

## Workflow
1. Read the target file(s)
2. For each function without type hints:
   - Analyze usage to infer parameter types
   - Trace return statements to infer return type
   - Use `Optional[T]` for parameters with `None` default
   - Use `Union[T1, T2]` for parameters accepting multiple types
3. Add `from __future__ import annotations` if Python < 3.10
4. Add `from typing import ...` imports as needed
5. Run `mypy <file>` to verify annotations are correct
6. Fix any type errors found by mypy

## Annotation Rules
```python
# Functions — always annotate parameters AND return type
def process_items(items: list[dict[str, Any]], limit: int = 10) -> list[dict[str, Any]]:
    ...

# Use | for unions (Python 3.10+) instead of Union
def get_user(user_id: int) -> dict[str, Any] | None:
    ...

# Class methods — include self/cls (unannotated is fine for self)
class UserService:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def find_by_email(self, email: str) -> User | None:
        ...

# Use Protocol for duck-typed interfaces
from typing import Protocol

class HasName(Protocol):
    name: str

def greet(entity: HasName) -> str:
    return f"Hello, {entity.name}"
```

## Key Principles
- Prefer built-in generics: `list[X]` over `typing.List[X]` (Python 3.9+)
- Use `| None` over `Optional[X]` (Python 3.10+)
- `Any` is a last resort — prefer `object` or a Protocol
- Don't annotate `self` or `cls` parameters
- Run mypy after annotating — fix all errors before declaring done

## Notes
- Run `mypy --strict` for the strictest checking
- If the project has `pyproject.toml`, check for existing mypy config
- Don't change runtime behavior — only add annotations
- For large files, annotate one function at a time, running mypy between each
