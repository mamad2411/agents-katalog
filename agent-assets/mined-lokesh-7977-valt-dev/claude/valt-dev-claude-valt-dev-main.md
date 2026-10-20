# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

VALT: pnpm + Turborepo monorepo. `apps/web` (Next.js 15 App Router, React 19, TanStack Query, shadcn/ui on Tailwind v4) talks to `apps/api` (FastAPI, Python 3.11+, async SQLAlchemy 2 + Alembic + Postgres/pgvector, Gemini via `google-genai`). `packages/shared` holds the TS types mirroring the API contract. It is a generic multimodal AI shell (input → processing → result → recommended action) meant to be adapted to a problem statement by adding prompts/config, not by restructuring.

## Commands

Root (turbo fans out to both apps):

```bash
pnpm install && pnpm api:install   # api:install creates apps/api/.venv (Windows layout: .venv/Scripts/python), installs .[dev,ai]
pnpm dev                           # web :3000 + api :8000 (uvicorn must be the one in apps/api/.venv)
pnpm api:dev                       # API alone
pnpm lint                          # eslint (next lint) + ruff check src tests
pnpm typecheck                     # tsc --noEmit + mypy --strict src
pnpm test                          # pytest (web has no test suite)
pnpm build
pnpm db:up                         # Postgres 17 + pgvector via docker compose
pnpm db:migrate                    # alembic upgrade head
pnpm --filter @valt/api db:revision "msg"   # autogenerate migration — always review the output
```

Single API test (run from `apps/api`):

```bash
.venv/Scripts/python -m pytest tests/test_ai.py::test_name
.venv/Scripts/python -m pytest -k live tests/test_gemini.py   # live Gemini smoke test, needs GEMINI_API_KEY
```

Tests marked `@pytest.mark.db` are skipped unless `API_TEST_DATABASE_URL` points at a separate DB (e.g. `postgresql+psycopg://valt:valt@localhost:5432/valt_test`); the session fixture runs migrations down to base and back up, so it also proves downgrades work.

The API starts without a DB or Gemini key: DB endpoints return `503 database_unavailable`, AI endpoints `503 ai_unavailable`.

## Architecture

### Request path
- Browser → `/api/py/*` → Next rewrite (`apps/web/next.config.ts`) → `http://<API_INTERNAL_URL>/api/*`. Same origin, no CORS.
- Server components call `API_INTERNAL_URL` directly. Both paths go through `apps/web/src/lib/api.ts` — the only place allowed to call FastAPI (components never `fetch`). It unwraps the envelope, throws `ApiError(status, code, message, details, requestId)`, and parses SSE for `generateStream`.
- All API routes mount under `/api/v1` in `main.py`; `health` is also mounted unversioned at `/api/health` for infra probes.

### API layering (`apps/api/src/valt_api/`)
- `routers/` are HTTP only. `deps.py` provides `AIServiceDep`, `StorageDep`, `SettingsDep`; `db/session.py` provides `SessionDep`.
- Clients (Gemini model client, sessionmaker, storage) are built in `main.py` `lifespan` and stored on `app.state`. Tests swap them by assigning `app.state.*` (ASGITransport does not run lifespan) — see `tests/conftest.py` fixtures `client`, `ai_client` (with `FakeModelClient` from `tests/fakes.py`), `db_client` (per-test transaction rolled back).
- `services/ai/AIService` (`text`, `structured`, `json`, `stream`, `prepare`, `run`) sits over a `ModelClient` protocol; `services/gemini/` is the **only** module that imports the Gemini SDK and maps SDK errors to `ai_*` error codes (ADR 0014).
- `prompts/`: registry of `PromptTemplate`s (system, instruction with `{vars}`, Pydantic `output_model`, defaults). New domain tasks go in a new module that calls `register(...)` and is imported from `prompts/__init__.py`; they become available via `/process` and `/tasks` with no router change. Structured outputs retry once on schema mismatch.
- `services/storage/`: `FileStorage` protocol; local-disk impl (ephemeral per Cloud Run instance). `/upload` returns a `file_id` that other AI endpoints accept in `file_ids`.
- `db/`: models, repositories (repositories only `flush`; each write endpoint commits exactly once). `routers/items.py` is the reference CRUD pattern (keyset pagination, newest first, limit 1–100).
- `config.py`: all settings via pydantic-settings, `API_` prefix; Gemini key also accepted as `GEMINI_API_KEY` / `API_LLM_API_KEY`.

### Response contract (ADR 0013, `docs/api/conventions.md`)
- Success `{success: true, data, meta}` via `ok(...)`; errors `{success: false, error: {code, message, details, request_id}}`. Raise `AppError(status, code, message)` or a subclass in `core/errors.py` — handlers build the envelope. Clients branch on `code`, never `message`; messages never contain provider errors or echoed input.
- Every response carries `X-Request-ID`; logs include it.
- Streaming endpoints return SSE (`token`, `step`, `interrupt`, `done`, `error`), not the envelope — unless they fail before streaming starts.
- Pydantic models in `apps/api/src/valt_api/schemas.py` and `packages/shared/src/index.ts` are kept in sync **by hand**; change both together (`/sync-contract` skill).

### Web (`apps/web/src/`)
- `config/site.ts` (branding, nav) and `config/workflows.tsx` (a `WorkflowConfig`: copy, input modes/limits, a `run()` that calls `lib/api.ts`, and a `Result` component) drive the product. `<AiWorkflow config>` (`components/workflow/`) + `lib/workflow/use-ai-workflow.ts` is the engine; don't change it to add a workflow.
- Configs hold functions, so a page is a server component plus a small `"use client"` wrapper that renders `<AiWorkflow>`.
- `lib/errors.ts` maps backend error codes to user-facing copy/retryability; `lib/queries/ai.ts` holds TanStack Query keys and mutation hooks.
- `/kit` (dev only) shows every component; visual rules live in `design-system/valt/MASTER.md` (one blue accent, grayscale otherwise, 44px controls, 12px radius).
- Full adaptation guide: `docs/web/frontend-playbook.md`; backend counterpart: `docs/api/ai-backend.md`.

## Rules and gotchas

- Architectural decisions are recorded in `docs/adr/`. Adding a framework/infra dependency or deviating from an ADR needs a new ADR (`/adr` skill).
- AI extra (`langchain`, `langgraph`, `crewai`, `pgvector`) versions are pinned as a set (crewai caps pydantic); upgrade together. ADR 0006 guard rules: never run a Chroma server, never enable CrewAI `memory=True` or `knowledge_sources`; vectors live in pgvector.
- Windows: psycopg async can't use the Proactor loop — conftest forces `SelectorEventLoop`; do the same for any new async entrypoint that touches the DB.
- mypy runs in strict mode; ruff line length 100.
- `pnpm-workspace.yaml` overrides `next>postcss` for security advisories; drop only once on next@16+.
- Deploy: API to GCP Cloud Run (`pnpm gcp:deploy`, `infra/gcp/`, GitHub Actions `deploy-api.yml`) — see `/gcp-deploy` skill.
- `.claude/README.md` describes the agent/skill pipeline (`/prd` → `/tech-plan` → `/execute`, plans in `docs/plans/`, PRDs in `docs/product/`).
