# Crypto News Aggregator — Cursor Rules

## Project Context
This is an internal tool for the Social Media team of a crypto academy platform.
It aggregates news from crypto RSS sources, translates them to Persian with a custom tone,
applies branded image templates, and publishes to Telegram and Bale channels.

Target output: ~30 quality news posts per day.
Primary users: Social Media team (operators) + Admin (super user).

## Tech Stack (STRICT — do not suggest alternatives)
- Backend: Python 3.11+ with FastAPI
- DB: PostgreSQL 15+ with pgvector extension
- Queue: Celery + Redis
- LLM providers: OpenAI + Anthropic (configurable)
- Embedding: multilingual-e5-small (local, via sentence-transformers)
- Frontend: Jinja2 + HTMX + TailwindCSS (no SPA frameworks)
- Image: Pillow + CairoSVG
- Auth: FastAPI-Users with JWT
- Deploy: Docker Compose

## Code Conventions
- Python: PEP 8, type hints mandatory, async-first where IO is involved
- Use Pydantic v2 for all DTOs and settings
- SQLAlchemy 2.0 style (async) for DB
- All prompts live in `app/agents/prompts/` as .txt or .md files (not hardcoded in Python)
- All config from environment + database (NOT hardcoded)
- Error handling: custom exception classes per module
- Logging: structlog with JSON format in production

## Architecture Principles
1. **Layered architecture** — refer to docs/02-architecture.md
2. **State Machine driven** — every news item has a clear status (see docs/06)
3. **Modular agents** — each AI task is an isolated agent (see docs/04)
4. **Config-driven** — admin can change prompts, tones, sources without deploy
5. **Cost-aware** — every LLM call logs tokens and cost (see docs/08)

## File Structure Rules
- `app/` — main application code
  - `app/api/` — FastAPI routes
  - `app/agents/` — AI agents (translator, classifier)
  - `app/agents/prompts/` — prompt templates
  - `app/core/` — config, logging, exceptions
  - `app/db/` — models, migrations, session
  - `app/services/` — business logic
  - `app/workers/` — Celery tasks
  - `app/templates/` — Jinja2 templates
  - `app/static/` — CSS, JS (HTMX)
- `docs/` — all product documentation
- `tests/` — pytest tests mirroring app/ structure
- `alembic/` — DB migrations
- `assets/` — SVG templates, logos

## Before Writing Code
1. Read the relevant doc in `docs/` first
2. Check if there's an existing pattern in `app/services/`
3. Verify the state machine transition is valid (docs/06)
4. Ensure you're not hardcoding something that should be config

## Forbidden Patterns
- ❌ Hardcoded prompts inside Python code
- ❌ Hardcoded channel IDs or source URLs in code
- ❌ Direct LLM calls outside `app/agents/`
- ❌ Skipping state machine validation
- ❌ Synchronous DB calls in request handlers
- ❌ Missing cost logging on any LLM call
- ❌ UI in JavaScript frameworks (use HTMX only)

## When in Doubt
- Check `docs/11-development-roadmap.md` to see if the feature is in scope for current phase
- Ask the user rather than assuming requirements