# Python Type Hints

## Summary

**One-sentence:** Type hints + mypy/pyright + pydantic v2 — catch bugs at edit time, enable IDE autocomplete.

**One-paragraph:** Python type hints and static type checking with mypy, pyright, and Pydantic v2: catch bugs at development time, enable IDE autocomplete, document interfaces. Use built-in generics, X | None, PEP 695 type parameters; run strict mode at the boundary; validate IO with Pydantic.

**Ефективно для:** розробника, який вводить mypy/pyright strict у легасі-репо або проєктує API-границі — закриває петлю між сирими dict'ами і чітко типізованими контрактами.

## Applies If (ALL must hold)

- New code where IDE autocomplete and static analysis improve productivity.
- Teams where runtime type errors cause production bugs.
- Library code where types are the public API.
- Validating IO boundaries (HTTP, DB, queue) with Pydantic.

## Skip If (ANY kills it)

- One-off scripts under 50 lines.
- Notebooks for exploration.
- Hot loops where Pydantic validation overhead matters (use dataclasses instead).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Python 3.12+ interpreter | binary | uv install |
| mypy or pyright installed | package | uv add --dev mypy |
| pyproject.toml with [tool.mypy] | TOML | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-basics` | Built-in generics and X | None idioms. |
| `free/dev/python-developer/python-modern-2026` | PEP 695 type parameters. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: built-in generics, X | None, PEP 695 type params, strict at boundary, Pydantic for IO, unknown over Any. | ~1100 |
| `content/02-output-contract.xml` | essential | Shape: every public function typed; Pydantic schemas at IO boundary; no Any in new code. Forbidden: typing.List, Optional, Union; Any without #type: ignore[explicit-any] noqa. | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: Any everywhere, # type: ignore without reason, legacy typing imports, Pydantic for hot path, untyped public API. | ~800 |
| `content/04-procedure.xml` | medium | Steps: enable mypy strict → type public functions → add Pydantic at IO boundary → eliminate Any → run mypy in CI. | ~800 |
| `content/06-decision-tree.xml` | essential | Tree: IO boundary? → Pydantic. Internal data class? → dataclass. Generic algorithm? → PEP 695 type params. Unknown shape? → unknown not Any. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `annotate-module` | sonnet | Type signatures with judgement on generics. |
| `audit-any-leaks` | haiku | Grep Any usage and # type: ignore without reason. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pydantic-schema.py` | Pydantic v2 BaseModel with model_config and validators. |
| `templates/typed-service.py` | Service function fully typed with PEP 695 generics. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-type-hints.py` | Check no typing.List/Optional/Union imports, no bare Any in new code, Pydantic at IO boundary. | Pre-commit. |

## Related

- [[python-basics]]
- [[python-modern-2026]]
- [[python-code-quality]]
- [[python-fastapi]]

## Decision tree

The tree at content/06-decision-tree.xml routes between Pydantic, dataclass, NamedTuple, and PEP 695 generics based on whether the data crosses an IO boundary, needs validation, or is purely internal. Walk it whenever a new data shape appears.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pydantic-schema.py`

```python
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    name: str = Field(min_length=1, max_length=100)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
```

### `templates/typed-service.py`

```python
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Item:
    id: int
    name: str


def find_by_id[T](items: list[T], pred) -> T | None:
    for item in items:
        if pred(item):
            return item
    return None


def first_with_name(items: list[Item], name: str) -> Item | None:
    return find_by_id(items, lambda i: i.name == name)
```
