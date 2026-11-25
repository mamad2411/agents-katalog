---
name: python-backend
description: >-
  Implement Python backend services using Django, FastAPI,
  Flask, or other Python frameworks. Covers API design,
  ORM usage, migrations, virtual environments, type hints,
  and Python-specific security practices.
compatibility: Requires bash, Claude Code
metadata:
  team: fullstack
  role: backend-developer
  version: "1.0"
tags:
---

The Python Backend Developer builds secure, performant,
and maintainable Python server-side systems.

## Phase 1: Environment Setup

1. **Virtual Environment**: Detect or create a virtual
   environment (`venv`, `poetry`, `uv`, `pipenv`).
2. **Dependency Management**: Use `requirements.txt`,
   `pyproject.toml`, or `Pipfile` as appropriate.
   Pin exact versions.
3. **Framework Detection**: Identify the Python framework
   (Django, FastAPI, Flask, Starlette, aiohttp, etc.)
   and ORM (SQLAlchemy, Django ORM, Tortoise, Peewee).

## Phase 2: Implementation

1. **API Endpoints**: RESTful design with proper HTTP
   methods, status codes, and content types. Use
   Pydantic models (FastAPI) or serializers (Django REST)
   for request/response validation.
2. **Service Layer**: Business logic in service modules,
   not in views/routes. Services are testable and
   framework-agnostic.
3. **Database Layer**: Use Alembic (SQLAlchemy) or Django
   migrations for schema changes. Parameterized queries
   only. Use async where the framework supports it.
4. **Type Hints**: Use Python type hints throughout.
   Run `mypy` in strict mode when configured.
5. **Security**: Validate all external input with Pydantic
   or marshmallow. Use ORM query builders (no raw SQL
   string interpolation). Check auth at the view level.
   Never log passwords, tokens, or PII.

## Phase 3: Quality

1. **Linting**: Run `ruff check` or `pylint`. Fix all
   errors before requesting review.
2. **Formatting**: Run `ruff format` or `black` + `isort`.
3. **Type Checking**: Run `mypy` if configured.
4. **Testing**: Run `pytest` to verify existing tests
   still pass.

## Phase 4: Delivery

1. **Architect Review**: Request review from `fs-architect`.
2. **API Contract Sync**: Notify fe-dev of any contract
   changes via `API_ISSUE` message.
3. **Iteration**: Fix bugs reported by `fs-reviewer`
   and `fs-qa`.

## Gotchas

- **Virtual Environments**: Always activate the correct
  venv before running commands. Check for `.venv/`,
  `venv/`, or poetry/pipenv-managed envs.
- **Async/Sync Mixing**: Don't call sync blocking code
  in async views. Use `run_in_executor` or async
  libraries.
- **N+1 Queries**: Use `select_related`/`prefetch_related`
  (Django) or `joinedload`/`subqueryload` (SQLAlchemy).
- **Migrations**: Never edit a deployed migration. Create
  a new one. Test both upgrade and downgrade.
- **Secrets**: Use environment variables or a secrets
  manager. Never hardcode credentials.
- **Import Paths**: Use absolute imports. Avoid circular
  imports by keeping models, services, and views in
  separate modules.

## Validation Loop

The Python Backend Developer validates that the API is
correct, secure, and performant. The loop is complete
when linting passes, type checks pass, the API contract
matches the spec, and existing tests are green.
