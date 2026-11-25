---
name: backend-development
description: Use when building or structuring a Python backend on FastAPI + SQLAlchemy 2.0 (async) + Alembic + Pydantic v2. Provides the opinionated project layout, the standard kit (auth, async jobs, caching, storage, observability), and best practices.
---

# Backend Development

**Announce at start:** "I'm using claude-engineer:backend-development to build the FastAPI backend."

## The stack (defaults)
Python 3.12+ · **FastAPI** · **SQLAlchemy 2.0 async** (asyncpg) · **Alembic** · **Pydantic v2** +
pydantic-settings · **uv** (deps/venv) · **ruff** (lint+format) · **mypy** (types) · **pytest** (tests).
Domain-modular layout: `src/<domain>/{router,schemas,models,service,dependencies}.py`.

## The standard kit (scaffold these by default)
- **Auth & security** - OAuth2 password flow, JWT access + refresh, password hashing (argon2/bcrypt), rate limiting, CORS, security headers.
- **Async jobs & scheduling** - a task queue + scheduled jobs over Redis (see the reference for the recommended library and why).
- **Caching & object storage** - Redis cache patterns + an S3/MinIO storage abstraction.
- **Observability** - structured logging, Sentry, OpenTelemetry traces, `/health` + `/ready` endpoints.

## Non-negotiables
1. **Async all the way** - async engine + session-per-request dependency; no sync DB calls in request paths.
2. **Migrations are real** - every schema change ships an Alembic migration (async-compatible); never auto-create in prod paths.
3. **Typed & validated** - Pydantic v2 request/response models; **mypy clean** (hard gate).
4. **Tested** - pytest + pytest-asyncio + httpx AsyncClient against a real test DB; meet the coverage threshold.
5. **Config via pydantic-settings** - no secrets in code; env-driven; documented required vars.
6. **Services in Docker, app native** - connect to Postgres/Redis/MinIO/Mailpit on localhost (`claude-engineer:docker-dev-environment`); run uvicorn natively.

**Full detail:** read `references/fastapi-stack.md` (exact project structure, SQLAlchemy 2.0 patterns, async Alembic setup, the job-queue recommendation, auth, observability, the blessed-packages list, pyproject.toml) on demand.

## Red flags - STOP
- A sync DB driver or blocking I/O in an async endpoint.
- A model change without a matching Alembic migration.
- Secrets/config literals in source instead of pydantic-settings + env.
- Shipping an endpoint with no test.
