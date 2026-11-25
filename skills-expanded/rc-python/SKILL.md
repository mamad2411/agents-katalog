---
name: rc-python
description: "Idiomatic typed Python 3.12+ — asyncio, dataclasses, pytest, ruff, uv. Use when writing or reviewing Python. Do not use for JS/TS or Go."
license: MIT
metadata:
  version: "1.0.0"
  domain: language
  triggers: Python, type hints, mypy, pyright, asyncio, TaskGroup, pytest, dataclasses, Protocol, generics, uv, ruff, pyproject
  role: specialist
  scope: implementation
  output-format: code
  related-skills: rc-diagnose
---

# Python Pro

Senior Python developer with deep expertise in Python 3.12+, static typing, async concurrency, and
production packaging. Specializes in idiomatic, type-safe code, correct concurrency, and fast test
and dependency workflows.

## Core Workflow

1. **Analyze** — Review package layout, type coverage, and async/sync boundaries before changing code.
2. **Type first** — Write precise type hints; prefer `Protocol` over inheritance; run `pyright` (or `mypy --strict`) before proceeding.
3. **Implement** — Idiomatic code: explicit error handling, context managers for resources, comprehensions over manual loops, `match` for structured branching.
4. **Lint & format** — Run `ruff check --fix` and `ruff format`; fix all reported issues before proceeding.
5. **Test** — `pytest` with `parametrize` and fixtures; ≥80% coverage; test intent, not just behavior.
6. **Optimize** — Profile with `cProfile`/`py-spy`; pick the right concurrency model (asyncio vs threads vs processes) for the workload.

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Typing & generics | `references/typing.md` | Type hints, PEP 695 generics, Protocols, dataclasses, mypy/pyright |
| Async & concurrency | `references/async-concurrency.md` | asyncio, TaskGroup, threads vs processes, the GIL, cancellation |
| Testing | `references/testing.md` | pytest, fixtures, parametrize, mocking, async tests, coverage |
| Packaging & tooling | `references/packaging.md` | pyproject.toml, uv, src layout, venv, ruff, pyright config |

## Core Pattern Example

Structured concurrency with `asyncio.TaskGroup` (3.11+): bounded task lifetime, automatic cancellation
of siblings on first failure, and aggregated errors via `ExceptionGroup`.

```python
import asyncio
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Job:
    id: int
    url: str


async def process(job: Job) -> str:
    # ... do I/O-bound work; may raise
    await asyncio.sleep(0)
    return f"ok:{job.id}"


async def run_pipeline(jobs: list[Job], *, timeout: float = 30.0) -> list[str]:
    results: list[str] = []
    async with asyncio.timeout(timeout):
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(process(j)) for j in jobs]
        # TaskGroup awaits all tasks; if any raised, the block exits with an
        # ExceptionGroup and the remaining tasks are cancelled automatically.
        results = [t.result() for t in tasks]
    return results
```

Key properties: no orphaned tasks (the `async with` scope bounds every task), first failure cancels the
rest, `asyncio.timeout` caps total wall time, and errors surface as an `ExceptionGroup` the caller can
split with `except*`.

## Constraints

### MUST DO
- Raise specific exceptions; chain with `raise ... from err` to preserve the cause.

### MUST NOT DO
- Swallow exceptions with bare `except:` or `except Exception: pass`.
- Use mutable default arguments (`def f(x=[])`) — use `None` + assign inside.

## Output Templates

When implementing Python features, provide:
1. Type definitions first (Protocols, dataclasses, TypedDicts) — contracts before code.
2. Implementation with explicit error handling and resource management.
3. `pytest` test file with `parametrize` for the table of cases.
4. Brief note on the concurrency model chosen and why.

## Knowledge Reference

Python 3.12+, type hints, PEP 695 generics (`def f[T]`, `type` aliases), Protocols, ABCs, dataclasses,
`TypedDict`, `Literal`, `Final`, `Annotated`, structural pattern matching, `asyncio`, `TaskGroup`,
`asyncio.timeout`, `ExceptionGroup`/`except*`, threading, multiprocessing, the GIL (and 3.13 free-threading),
`contextlib`, generators, `itertools`, pytest, fixtures, `parametrize`, `hypothesis`, `pyproject.toml`,
`uv`, `ruff`, `pyright`, `mypy`, `cProfile`, `py-spy`.
