---
name: python-conventions
description: Modern Python (3.11+) conventions — type discipline, pathlib, async patterns, structlog, ruff + mypy strict + pytest defaults. Use when writing or reviewing Python code.
license: MIT
---

# Python conventions

Modern Python (3.11+) defaults.

## Types

- Type hints required everywhere
- `from __future__ import annotations` at top
- Pydantic v2 for I/O, TypedDict for internal, Literal for string enums

## Stdlib

- pathlib.Path over os.path
- dataclasses over manual __init__
- subprocess.run over os.system
- f-strings except logging
- match for tagged unions

## Async

- async def end-to-end, httpx not requests
- TaskGroup for structured concurrency
- Never time.sleep in async

## Logging

- structlog or stdlib + structured extras
- No print() in libraries
- Lazy formatting

## Tooling

- ruff for lint + format
- mypy --strict
- pytest fixtures
- uv over pip

## Banned

- Bare except
- Mutable defaults
- `from foo import *`
- eval/exec on user input
- Stringly-typed returns

---

Full content + 15 worked examples at https://github.com/HermeticOrmus/python-conventions-skills.
