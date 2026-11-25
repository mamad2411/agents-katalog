# Competitor Scout agent guide

These instructions apply to the whole repository. Read the nearest nested `AGENTS.md` before changing files under `apps/backend` or `apps/web`; nested instructions add to or override this file for their subtree. Each `AGENTS.md` has a sibling `CLAUDE.md` that imports it — keep the pair together when adding a guide.

## Working style

- Implement small, well-scoped changes directly. Do not introduce formal specs, plans, TDD workflows, or subagents unless the user explicitly requests them.
- Preserve unrelated work in a dirty tree and keep changes within the requested scope.
- Do not create a git commit unless the user explicitly approves it.
- Prefer existing dependencies and patterns. Explain a new dependency before adding it.
- Update durable documentation when a change alters architecture, security boundaries, operational constraints, or design-system conventions.

## Repository map

| Path                         | Responsibility                                                       |
| ---------------------------- | -------------------------------------------------------------------- |
| `apps/backend`               | FastAPI API, PostgreSQL persistence, job worker, Scout agent runtime |
| `apps/web`                   | Next.js application, API client contracts, React UI                  |
| `docs/architecture`          | System, backend, and Scout runtime architecture                      |
| `docs/frontend`              | Frontend design-system guidance                                      |
| `docs/railway-deployment.md` | Production topology and operating procedure                          |
| `evals`                      | Offline evaluation datasets                                          |
| `.claude/skills`             | Tracked repository-specific agent workflows                          |

The root `README.md` is the human quick start. Keep operational agent rules here and explanatory design context under `docs/`.

This file owns the cross-cutting invariants and the verification matrix below. Nested guides and skills should link to them rather than restate them, so a rule has one place to change.

`docs/superpowers/` is gitignored local scratch space holding plans and specs from earlier sessions, and `.agents/` is machine-local harness wiring. Neither is current repository behavior.

## Cross-cutting invariants

- Normal development and CI must remain offline and must not make paid Otari calls. Hosted evaluations require explicit approval and the existing two-part paid-run gate.
- Preserve authentication, CSRF enforcement, user isolation, public-HTTPS/SSRF validation, secret redaction, and safe problem-details errors.
- Treat model output and fetched source content as untrusted. Validate scope and contracts before persistence or publication.
- Keep backend Pydantic response contracts and frontend Zod schemas synchronized.
- Add an Alembic migration for every database schema change; never rewrite a migration that may have reached a shared environment.
- The production worker remains a single replica until Otari concurrency is coordinated through a shared permit.

## Change boundaries

- Backend HTTP routes belong in `api/`, contracts in `schemas/`, reusable application behavior in `services/`, persistence in `models/`, background execution in `jobs/`, and model orchestration in `agents/`.
- Frontend route files in `src/app/` should compose views; reusable product components belong in `src/components/`, generic primitives in `src/components/ui/`, and API/Zod infrastructure in `src/lib/`.
- Do not expose raw ORM objects, provider responses, prompts, credentials, or sensitive task output through APIs or logs.
- Prefer semantic design tokens and documented UI patterns over new literal colors or duplicated class groups.

## Verification matrix

Run the smallest relevant checks during iteration and the complete affected suite before claiming completion.

| Scope                     | Commands                                                                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Backend                   | `cd apps/backend && uv run pytest && uv run ruff check src tests scripts && uv run ruff format --check src tests scripts` |
| Migration                 | Backend checks, then `uv run alembic upgrade head && uv run alembic check` against PostgreSQL                             |
| Frontend                  | `cd apps/web && pnpm format:check && pnpm test && pnpm lint && pnpm build`                                                |
| Browser smoke (on demand) | Frontend checks, then `cd apps/web && pnpm exec playwright install chromium && pnpm test:e2e`                             |
| Cross-stack contract      | Relevant backend integration tests plus frontend schema/API tests and build                                               |

Do not run `apps/backend/scripts/run_live_evals.py` without explicit approval.

## Repository skills

- Use `add-backend-endpoint` for FastAPI routes and cross-stack API contract changes.
- Use `add-ui-pattern` for reusable frontend components and interaction patterns.
- Use `update-repo-docs` when a change affects setup, architecture, runtime behavior, deployment, or design conventions.

Skill sources live in `.claude/skills/` and are the tracked copy. Harnesses that discover skills elsewhere may be pointed at them locally — for example relative symlinks under `.agents/skills/` for Codex — but that wiring is optional, machine-local, and must never be committed.
