---
name: python-engineer
description: Architect production-grade Python services, async APIs with FastAPI, data engineering pipelines, and robust packages. Enforces static typing, Ruff linting, and modern packaging.
---

# Python Engineer Skill

## Purpose
Directs production-quality Python development, strict static type hints, async concurrency, and modern tooling.

## When to Use
- Developing web backends, microservices, or CLI tools in Python.
- Writing asynchronous services using FastAPI, asyncio, and Pydantic v2.
- Packaging libraries according to PEP 621 (`pyproject.toml`).

## Engineering Workflow
1. **Type Annotations**: Enforce strict typing on all function signatures; verify with `mypy --strict`.
2. **Quality & Formatting**: Use `ruff check --fix` and `ruff format`.
3. **Verification**:
   - `pytest -v --cov=. --cov-report=term-missing`

