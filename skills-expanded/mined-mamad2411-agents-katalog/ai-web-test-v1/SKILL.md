# AI Web Test v1 — Agent Entry (Router)

> **Why this file is short:** One giant instruction file dilutes attention, creates conflicting rules, goes stale, and wastes tokens. This is a **router only** — see [Lecture 04 — Split Instructions Across Files](https://github.com/walkinglabs/learn-harness-engineering/blob/main/docs/en/lectures/lecture-04-why-one-giant-instruction-file-fails/index.md). Put detailed patterns in `.cursor/rules/*.mdc` or topic docs; never bloat this file.

## How Agents Should Use This

1. **Start here** — project identity, quick start, hard constraints.
2. **Route on demand** — open only the topic docs the current task needs (table below).
3. **Scoped rules** — glob-matched `.cursor/rules/*.mdc` apply when editing matching paths; index at `docs/CODEMAPS/cursor-rules.md`.
4. **Do not duplicate** — if content lives in a codemap or `.mdc`, link to it; do not copy it here.

## Project Overview

Self-hosted AI web testing platform: FastAPI backend, React/Vite frontend, three-tier browser execution (Playwright → Hybrid observe → Stagehand act). Integrates with ReqIQ (requirements) and Hermes (multi-agent orchestration).

## Quick Start

```bash
# Backend (activate venv before any Python command)
cd backend && .\venv\Scripts\activate
pip install -r requirements.txt && playwright install chromium
python start_server.py                    # http://127.0.0.1:8000

# Frontend (separate terminal)
cd frontend && npm install && npm run dev # http://localhost:5173
```

Verify: `http://127.0.0.1:8000/api/v1/docs` · Default login: `admin@aiwebtest.com` / `admin123`

```bash
cd backend && python -m pytest tests/unit/ -q   # backend tests
cd frontend && npm run test                    # frontend tests
```

---

## Hard Constraints (non-negotiable)

1. **Execution dispatch** — All step runs go through `ExecutionService` → `ThreeTierExecutionService`. Never call tier executors from endpoints.
2. **Lazy tiers** — Stagehand T2/T3 init only after Tier 1 failure (ADR-002-1).
3. **Backend layering** — Endpoints → services → CRUD. No business logic or raw SQL in routers.
4. **Database** — SQLAlchemy only (`backend/app/models/`, `crud/`, `migrations/`). No Prisma, no inline DDL in endpoints.
5. **Frontend API** — HTTP calls live in `frontend/src/services/`, not inline in page components.
6. **Python env** — Activate `backend/venv` before running Python or pytest.
7. **Scope** — Surgical diffs only; do not refactor unrelated code or expand scope without request.
8. **Commits** — Do not commit unless the user explicitly asks.
9. **Archive** — Do not treat `documentation/archive/` as current architecture.
10. **Deprecated rules** — Ignore `.cursor/rules/clerk-setup-refactoring-maintenance.mdc` and `file-folder-component-creation.mdc` (Clerk/Next.js; this repo uses JWT + Vite).
11. **OpenAPI contract** — AI Web Test: live `http://127.0.0.1:8000/api/v1/openapi.json`. ReqIQ: `docs/openapi/reqiq-api-v1.yaml`.
12. **Integration URLs** — Use configured hostnames/LAN IPs for Hermes/ReqIQ in production; `127.0.0.1` is local to each machine only.

---

## Topic Docs (read on demand)

| When | Read |
| --- | --- |
| Any task — repo map, ADRs, entry points | `docs/CODEMAPS/INDEX.md` |
| Orientation, ReqIQ/Hermes flows, commands | `docs/AGENTS.md` |
| Backend routers, services, agents | `docs/CODEMAPS/backend.md` |
| React pages, features, routing | `docs/CODEMAPS/frontend.md` |
| Three-tier execution, xpath cache, guards | `docs/CODEMAPS/execution-engine.md` + `documentation/ADR-002-test-execution-engine.md` |
| SQLAlchemy models, migrations | `docs/CODEMAPS/database.md` |
| ReqIQ proxy, Hermes, Stagehand, CORS | `docs/CODEMAPS/integrations.md` |
| Agent workflow architecture | `documentation/ADR-004-agent-workflow.md` |
| Cursor rules index (`.mdc` globs) | `docs/CODEMAPS/cursor-rules.md` |
| ReqIQ ↔ AI Web Test handoff | `docs/AI-Web-Test-Developer-Handoff.md` |
| External integrator API | `docs/ReqIQ-API-Integration-Guide.md` |
| ReqIQ OpenAPI folder guide | `docs/openapi/README.md` |
| Hermes multi-agent profiles / workflow | `docs/Hermes_QA_MultiAgent_Profiles_v3.md`, `docs/Hermes_QA_Autonomous_Workflow_v5.md` |
| Writing ADRs or updating docs | `documentation/` (active only, not `archive/`) |
| Full setup, Phase 3 agent testing | `README.md` |
| Git commit messages | `.cursor/rules/commit-messages.mdc` |
| Task Master workflow | `.cursor/rules/dev_workflow.mdc` |

## Cursor Rules

Glob-scoped rules live in `.cursor/rules/*.mdc`. **Full index:** `docs/CODEMAPS/cursor-rules.md` — do not duplicate rule bodies here.

---

## Before Adding New Rules

| Put it here when… | Put it elsewhere when… |
| --- | --- |
| Non-negotiable, repo-wide constraint every agent must see | Pattern applies to one layer or path → `.cursor/rules/*.mdc` with globs |
| | Architecture map, module layout → `docs/CODEMAPS/*.md` |
| | Integration flows, Hermes/ReqIQ detail → `docs/AGENTS.md` or handoff docs |
| | ADR-level decision → `documentation/ADR-*.md` |

Each rule needs: **source** (why), **applicability** (when), **expiry** (when to remove). See `.cursor/rules/self_improve.mdc`.

## End-of-Session Checklist

- [ ] Changes match hard constraints above
- [ ] Relevant topic doc / codemap updated if architecture changed
- [ ] No secrets committed (`.env`, credentials)
- [ ] Tests run for touched areas when feasible
