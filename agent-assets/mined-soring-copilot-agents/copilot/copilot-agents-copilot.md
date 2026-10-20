# Project-Wide Copilot Instructions

## Architecture

Full-stack application with clear separation of concerns:

- **Backend**: Python 3.12+, FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Alembic
- **Frontend (primary)**: Vue 3 Composition API, TypeScript strict, Pinia, Vue Router 4, Vite
- **Frontend (secondary)**: React 18+, TypeScript, TanStack Query, Zustand
- **Database**: PostgreSQL 16
- **Containerization**: Docker + Docker Compose
- **Testing**: pytest + pytest-asyncio (backend), Vitest + Testing Library (frontend)

## Core Principles

1. **Type safety everywhere** — Python type hints, TypeScript strict mode, Pydantic models
2. **Layered architecture** — API routes → services → repositories → models (backend); pages → components → composables → stores (frontend)
3. **Async by default** — `async/await` in both Python and TypeScript
4. **Fail explicitly** — structured error responses, never swallow exceptions
5. **Immutable data flow** — props down, events up; no hidden mutations

## Security Baseline (Always Enforced)

- **No secrets in code** — use environment variables or vault references
- **Parameterized queries only** — never interpolate user input into SQL
- **Validate all inputs** — Pydantic models on backend, Zod/Valibot on frontend
- **Principle of least privilege** — minimal scopes, minimal permissions
- **Dependency hygiene** — pin versions, audit regularly, no unused packages

## Documentation Expectations

- All public functions: docstrings (Python) or JSDoc (TypeScript)
- All modules: brief header comment explaining purpose
- All API endpoints: OpenAPI description via FastAPI docstrings
- Complex logic: inline comments explaining *why*, not *what*

## Naming Conventions

- Python: `snake_case` for functions/variables, `PascalCase` for classes
- TypeScript: `camelCase` for functions/variables, `PascalCase` for types/components
- Files: `kebab-case` (frontend), `snake_case` (backend)
- Database: `snake_case` for tables/columns, singular table names (e.g., `user`, not `users`)
