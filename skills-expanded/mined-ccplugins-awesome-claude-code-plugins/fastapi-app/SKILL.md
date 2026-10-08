---
name: fastapi-app
description: Bootstrap a new FastAPI backend with async SQLAlchemy 2.0, asyncpg, Alembic, Pydantic v2, and no deprecated APIs. Use when the user wants to start, scaffold, or set up a new FastAPI service, a Python REST API, an async backend, or asks to "create a new fastapi app" or "new python backend". Handles JWT auth, layered app structure, Docker + Postgres, and Vercel or container deploy.
---

# fastapi-app

Bootstrap a new FastAPI backend the way this owner builds them: async SQLAlchemy
2.0 with asyncpg, Alembic migrations, Pydantic v2 settings, a layered structure
(routers, services, models, schemas), JWT auth, and the house git and CI
workflow. Deployable to a container or Vercel.

First read the shared rules (they override anything you remember):
`../shared/house-rules.md`, `../shared/no-ai-attribution.md`,
`../shared/git-and-ci.md`, `../shared/docs-and-context.md`,
`../shared/hardening.md`, and (for public repos) `../shared/open-source-docs.md`.

## Step 0. Get the brief, then ask the variant questions (hard stop)

This is a hard stop. Do not run any scaffolding command until the user has
answered.

First, get the project brief: one paragraph on what the service does, its main
resources and endpoints, who calls it, and any hard constraints. If the user has
not given one, ask for it. The brief drives naming, the domain modules, and the
data model.

Then ask the variant questions. If a choice has multiple options, ask; do not
assume. Ask in one batch, then proceed.

1. Repo visibility: private, open-source, or private-plus-open-source.
2. Auth: JWT (python-jose or PyJWT), OAuth (Google), API-key, or none yet.
3. Database: Postgres via async SQLAlchemy + asyncpg (default), or none yet.
4. Dependency tooling: `uv` (default, fast) or `pip` + `requirements.txt`.
5. Admin UI: SQLAdmin, or none.
6. Deploy target: Docker container (default) or Vercel serverless.

If the user already answered some, do not re-ask.

## Step 1. Verify environment and current versions

- Check Python (`python3 --version`, want a current supported 3.x).
- Run `scripts/check-latest.sh` for current stable versions from PyPI. Pin those,
  not versions from memory (`../shared/house-rules.md` rule 2).
- Pull current FastAPI, SQLAlchemy 2.0, and Pydantic v2 docs via Context7 before
  writing code (`../shared/docs-and-context.md`). SQLAlchemy 2.0 async and
  Pydantic v2 both broke v1 patterns; do not write v1-era code from memory.

## Step 2. Scaffold the project

Create a virtualenv and the layout from `references/structure.md`. With `uv`:

```
uv init <name> && cd <name>
uv add fastapi "uvicorn[standard]" "sqlalchemy[asyncio]" asyncpg alembic \
       pydantic-settings python-jose[cryptography] httpx python-multipart
uv add --dev ruff pytest pytest-asyncio
```

With pip, install the same set and freeze into `requirements.txt`. Let the tool
resolve current versions; do not force numbers you remember.

## Step 3. Apply structure and conventions

- Layered app structure, async DB session, dependency-injected DB, settings, JWT
  auth: `references/structure.md`.
- Best practices, scalable domain-modular architecture, and nothing hardcoded:
  `references/best-practices.md`.
- Dependency set and version-boundary notes: `references/stack.md`.
- Production hardening (docs and schema disabled or gated in prod, generic error
  bodies, debug off, CORS locked): `../shared/hardening.md`.

## Step 4. Git, CI, docs, security

- Git branch model, conventional commits, auto-merge: `../shared/git-and-ci.md`.
- CI (ruff + pytest), Docker, migrations: `references/quality-gates.md`.
- Gitignore `.env*` and any service-account JSON. Provide `.env.example`.
  Settings load from env through `pydantic-settings`, never hardcoded.
- Add `docs/` and a README. For a public repo, ship the full open-source docs set
  per `../shared/open-source-docs.md` and run the open-source hard gate in
  `../shared/no-ai-attribution.md` before the first push.

## Step 5. Verify before declaring done

Run the gates in `references/quality-gates.md`: `ruff check`, `pytest`, the app
imports and starts, `/health` responds, and Alembic can generate a revision.
Report real results.
