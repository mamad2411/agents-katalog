# Windsurf Rules for FastAPI Boilerplate

## Project
Enterprise-grade Python FastAPI boilerplate with clean architecture.

## Stack
Python 3.12+, FastAPI, SQLAlchemy 2.x (async), Pydantic v2, PostgreSQL, Redis, Docker.

## Architecture Layers
1. API (src/api/) — HTTP endpoints, request parsing, response serialization
2. Services (src/services/) — Business logic, validation, orchestration
3. Repositories (src/repositories/) — Data access, SQL queries
4. Models (src/models/) — SQLAlchemy ORM definitions

## Rules
- All functions must have type annotations
- Use async/await for all I/O
- Use Pydantic v2 schemas for request/response
- Use repository pattern — no SQL in endpoints
- Use domain exceptions from src/core/exceptions.py
- Use structlog for logging, never print()
- Run `make lint` (ruff + mypy) and `make test` before committing
- Use `uv` as the package manager
