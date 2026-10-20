# MLB StatBat — Claude Code Guide

## Project Overview

MLB StatBat is a natural language baseball stats query app.

- **Backend**: FastAPI (Python) + SQLAlchemy async + PostgreSQL
- **Frontend**: Next.js (TypeScript) — see `frontend/CLAUDE.md`
- **Data Pipeline**: Python scripts for ingesting batting stats
- **LLM**: Anthropic Claude (text-to-SQL) + OpenAI (fallback)

## Project Structure

```
mlb-statbat/
├── backend/          # FastAPI app
│   ├── app/
│   │   ├── main.py          # FastAPI entry point
│   │   ├── text_to_sql.py   # LLM-powered query generation
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── database.py      # Async DB session
│   │   └── config.py        # pydantic-settings config
│   └── requirements.txt
├── frontend/         # Next.js app
├── data_pipeline/    # Batting stats ingestion
└── docker-compose.yml
```

## Development Workflow

1. `/plan` — plan before writing code
2. `/tdd` — write tests first
3. `/python-review` — before committing Python changes
4. `/code-review` — before committing any changes
5. `/build-fix` — fix build/type errors
6. `/database-migration` — Alembic migrations

## Key Conventions

- Backend uses **async/await** throughout (asyncpg + SQLAlchemy async)
- All DB access through `AsyncSession` via dependency injection
- Pydantic models for request/response validation
- Environment variables via `pydantic-settings` (`app/config.py`)
- Never hardcode API keys — use `.env` (not committed)

## Environment Variables

```
DATABASE_URL=postgresql+asyncpg://...
ANTHROPIC_API_KEY=...
OPENAI_API_KEY=...
```

## Running Locally

```bash
docker compose up          # Start PostgreSQL + backend + frontend
cd backend && uvicorn app.main:app --reload   # Backend only
cd frontend && npm run dev                    # Frontend only
```

## Agents Available

| Agent | When to use |
|-------|-------------|
| `architect` | New features, system design decisions |
| `planner` | Complex implementation planning |
| `code-reviewer` | After any code change |
| `security-reviewer` | API endpoints, auth, user input handling |
| `database-reviewer` | SQL queries, schema changes, indexes |
| `migration-reviewer` | Alembic migration files |
| `tdd-guide` | Writing tests first |
