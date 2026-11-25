---
name: fastapi-skills
description: FastAPI framework patterns, best practices, and implementation guides
category: stacks/backend/fastapi
applies_to: fastapi
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# FastAPI Skills

Modern, fast Python web framework for building APIs.

## Sub-Skills

### Architecture
- [project-structure.md](architecture/project-structure.md) - Project structure patterns
- [dependency-injection.md](architecture/dependency-injection.md) - DI with Depends
- [routers.md](architecture/routers.md) - Router organization

### Database
- [sqlalchemy-patterns.md](database/sqlalchemy-patterns.md) - SQLAlchemy patterns
- [async-sqlalchemy.md](database/async-sqlalchemy.md) - Async SQLAlchemy
- [repository-pattern.md](database/repository-pattern.md) - Repository pattern
- [alembic-migrations.md](database/alembic-migrations.md) - Alembic migrations

### Security
- [jwt-auth.md](security/jwt-auth.md) - JWT authentication
- [oauth2.md](security/oauth2.md) - OAuth2 with FastAPI
- [api-keys.md](security/api-keys.md) - API key authentication

### Validation
- [pydantic-models.md](validation/pydantic-models.md) - Pydantic validation
- [custom-validators.md](validation/custom-validators.md) - Custom validators

### Error Handling
- [exception-handlers.md](error-handling/exception-handlers.md) - Exception handlers
- [error-responses.md](error-handling/error-responses.md) - Error response patterns

### Testing
- [pytest-testing.md](testing/pytest-testing.md) - Testing with pytest
- [test-client.md](testing/test-client.md) - TestClient patterns

### Performance
- [async-patterns.md](performance/async-patterns.md) - Async patterns
- [caching.md](performance/caching.md) - Caching strategies

## Detection
Auto-detected when project contains:
- `main.py` with FastAPI
- `fastapi` or `uvicorn` packages
- `from fastapi import` imports
