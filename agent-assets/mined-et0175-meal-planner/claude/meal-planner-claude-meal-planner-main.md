# Meal Forge — Claude context

## Project overview
Meal Forge is a web app for meal planning, recipe management, and shopping lists.
Four Python microservices + one Next.js frontend, deployed on Railway + Vercel.

## Repository structure
```
backend/
  identity/    # Auth service: register, sign-in, password reset (CARD-001 ✓)
  catalog/     # Product catalog (CARD-003)
  planning/    # Meal planning (CARD-005)
  shopping/    # Shopping list (CARD-007)
  shared/
    auth_middleware.py  # HTTP auth pattern docs for non-identity services
frontend/      # Next.js 15 App Router (CARD-002, CARD-004, CARD-006, CARD-008)
docs/
  requirements/   # FRs, NFRs, user stories, test cases
  PLAN.md         # Implementation plan for the current module being built
meta/kanban/       # Kanban cards, board, dispatcher state
```

## Services and ports (local Docker Compose)
| Service | Port | Status |
|---------|------|--------|
| Identity | 8001 | ✓ implemented |
| Catalog | 8002 | stub |
| Planning | 8003 | stub |
| Shopping | 8004 | stub |
| Frontend | 3000 | stub |

## Running locally
```bash
docker compose up --build
```
Or run individual services:
```bash
cd backend/identity && uvicorn main:app --reload --port 8001
```

## Tech stack
- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0 async, asyncpg, Alembic, Pydantic v2, bcrypt
- **Frontend**: Next.js 15, TypeScript, Tailwind CSS v4, React 19
- **Databases**: PostgreSQL 16 (one per service)
- **Deployment**: Railway (backend), Vercel (frontend)

## Cross-service auth pattern
All protected endpoints on catalog/planning/shopping validate tokens by calling:
```
GET http://identity:8000/auth/session
Authorization: Bearer <token>
```
Returns `{account_id, email, role}` or 401. See `backend/shared/auth_middleware.py`.

## Adding a new service endpoint
1. Read the relevant CARD-XXX.md for architecture context
2. Read `backend/<service>/CLAUDE.md` for service-specific guidance
3. Check `docs/requirements/` for FRs and acceptance criteria
4. Implement → run `python3 -m pytest` → commit

## Deployment
- **Vercel**: connects to the `frontend/` directory; `vercel.json` at repo root
- **Railway**: each `backend/<service>/` has its own `Dockerfile` and `railway.toml`
- **Migrations**: `railway.toml` retries `alembic upgrade head` until DB is ready before starting uvicorn
- See `README.md` for full setup steps

## Each time you complete a kanban card (`done CARD-XXX`)
Write two files for the implemented module before committing the card closure:
1. `<module-path>/CLAUDE.md` — context for future Claude sessions: key decisions, file map, gotchas, test command
2. `<module-path>/README.md` — human docs: what it does, API, setup, env vars
Then commit both alongside the card status update.
