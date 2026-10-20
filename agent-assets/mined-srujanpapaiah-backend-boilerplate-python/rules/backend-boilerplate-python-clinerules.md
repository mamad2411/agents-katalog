# Cline Rules for FastAPI Boilerplate

## Overview
Python 3.12+ FastAPI backend with clean architecture (API → Service → Repository → Model).

## Commands
- Install deps: `uv sync`
- Run dev server: `uv run uvicorn src.main:app --reload`
- Lint: `uv run ruff check src tests && uv run mypy src`
- Test: `uv run pytest`
- Format: `uv run ruff format src tests`

## Conventions
- Type annotate everything
- Use async/await for I/O
- Raise domain exceptions from src/core/exceptions.py
- Follow repository pattern
- Use Pydantic v2 for schemas
- Add tests for every feature
