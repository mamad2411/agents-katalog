# AGENTS.md — Codex Cloud Sandbox Instructions

> This file is read by GPT-5.1-Codex and GPT-5.2-Codex when running async tasks
> in the Codex cloud sandbox. It defines the project context, conventions, and
> guardrails for autonomous code generation.

## Project Overview

Full-stack web application with:
- **Backend**: Python 3.12+, FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Alembic
- **Frontend (primary)**: Vue 3 Composition API, TypeScript strict, Pinia, Vue Router 4, Vite
- **Frontend (secondary)**: React 18+, TypeScript, TanStack Query, Zustand
- **Database**: PostgreSQL 16
- **Containerization**: Docker + Docker Compose
- **Testing**: pytest + pytest-asyncio (backend), Vitest + Testing Library (frontend)

## Directory Structure

```
├── backend/
│   ├── app/
│   │   ├── api/v1/          # FastAPI route handlers
│   │   ├── core/            # Config, security, dependencies, exceptions
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── services/        # Business logic layer
│   │   ├── repositories/    # Data access layer
│   │   └── main.py          # App factory
│   ├── alembic/             # Database migrations
│   ├── tests/               # pytest test suite
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/             # API client + endpoint functions
│   │   ├── components/      # Reusable UI components
│   │   ├── composables/     # Vue composition functions
│   │   ├── pages/           # Route-level page components
│   │   ├── router/          # Vue Router config
│   │   ├── stores/          # Pinia stores
│   │   ├── types/           # Shared TypeScript interfaces
│   │   └── utils/           # Helper functions
│   ├── vite.config.ts
│   └── package.json
├── docker-compose.yml
└── .github/                 # Copilot agents, instructions, prompts
```

## Coding Conventions

### Python
- PEP 8 style, max line length 99
- Type hints on ALL function signatures
- `from __future__ import annotations` in every file
- Google-style docstrings on all public functions
- `async/await` for all I/O operations
- SQLAlchemy 2.0 `select()` style, never legacy `Query`
- Pydantic v2 `BaseModel` for all schemas
- `snake_case` for functions/variables, `PascalCase` for classes

### TypeScript / Vue
- `<script setup lang="ts">` exclusively — no Options API
- TypeScript strict mode, no `any`
- `defineProps<T>()` with generics for typed props
- Pinia setup stores (composition style)
- `camelCase` for functions/variables, `PascalCase` for components

### TypeScript / React
- Functional components with typed props
- TanStack Query for server state
- Custom hooks for reusable logic

## Security Rules (MANDATORY)

1. **No secrets in code** — use `os.environ` or `.env` files
2. **Parameterized queries only** — never f-string user input into SQL
3. **Validate all inputs** — Pydantic on backend, Zod on frontend
4. **Hash passwords** with `bcrypt` or `argon2`
5. **Short-lived JWTs** — 15 min access tokens, 7 day refresh
6. **Explicit CORS origins** — never `*` in production
7. **No `eval()`, `exec()`, or `shell=True`**
8. **No `v-html` or `dangerouslySetInnerHTML` with user data**

## Testing Requirements

- All new code must include tests
- pytest + pytest-asyncio for backend; Vitest + Testing Library for frontend
- Test happy path, error cases, edge cases, and security scenarios
- Run tests after implementation to verify correctness
- Target 80%+ coverage on business logic

## Git Conventions

- Branch naming: `feature/`, `fix/`, `refactor/`, `docs/`, `test/`
- Commit messages: conventional commits (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`)
- One logical change per commit
- Always run tests before committing

## What NOT To Do

- Never commit `.env` files, secrets, or credentials
- Never disable type checking or linting rules
- Never use `# type: ignore` without an explanatory comment
- Never leave `TODO` or `FIXME` comments without a linked issue
- Never use `print()` for logging — use `logging` module
- Never return raw dicts from API endpoints — always use response models
