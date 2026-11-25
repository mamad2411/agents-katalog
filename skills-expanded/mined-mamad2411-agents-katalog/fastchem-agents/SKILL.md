# DOX framework

- DOX is highly performant AGENTS.md hierarchy installed here
- Agent must follow DOX instructions across any edits

## Core Contract

- AGENTS.md files are binding work contracts for their subtrees
- Work products, source materials, instructions, records, assets, and durable docs must stay understandable from the nearest applicable AGENTS.md plus every parent AGENTS.md above it

## Read Before Editing

1. Read the root AGENTS.md
2. Identify every file or folder you expect to touch
3. Walk from the repository root to each target path
4. Read every AGENTS.md found along each route
5. If a parent AGENTS.md lists a child AGENTS.md whose scope contains the path, read that child and continue from there
6. Use the nearest AGENTS.md as the local contract and parent docs for repo-wide rules
7. If docs conflict, the closer doc controls local work details, but no child doc may weaken DOX

Do not rely on memory. Re-read the applicable DOX chain in the current session before editing.

## Update After Editing

Every meaningful change requires a DOX pass before the task is done.

Update the closest owning AGENTS.md when a change affects:

- purpose, scope, ownership, or responsibilities
- durable structure, contracts, workflows, or operating rules
- required inputs, outputs, permissions, constraints, side effects, or artifacts
- user preferences about behavior, communication, process, organization, or quality
- AGENTS.md creation, deletion, move, rename, or index contents

Update parent docs when parent-level structure, ownership, workflow, or child index changes. Update child docs when parent changes alter local rules. Remove stale or contradictory text immediately. Small edits that do not change behavior or contracts may leave docs unchanged, but the DOX pass still must happen.

## Hierarchy

- Root AGENTS.md is the DOX rail: project-wide instructions, global preferences, durable workflow rules, and the top-level Child DOX Index
- Child AGENTS.md files own domain-specific instructions and their own Child DOX Index
- Each parent explains what its direct children cover and what stays owned by the parent
- The closer a doc is to the work, the more specific and practical it must be

## Child Doc Shape

- Create a child AGENTS.md when a folder becomes a durable boundary with its own purpose, rules, responsibilities, workflow, materials, or quality standards
- Work Guidance must reflect the current standards of the project or user instructions; if there are no specific standards or instructions yet, leave it empty
- Verification must reflect an existing check; if no verification framework exists yet, leave it empty and update it when one exists

Default section order:
- Purpose
- Ownership
- Local Contracts
- Work Guidance
- Verification
- Child DOX Index

## Style

- Keep docs concise, current, and operational
- Document stable contracts, not diary entries
- Put broad rules in parent docs and concrete details in child docs
- Prefer direct bullets with explicit names
- Do not duplicate rules across many files unless each scope needs a local version
- Delete stale notes instead of explaining history
- Trim obvious statements, repeated rules, misplaced detail, and warnings for risks that no longer exist

## Closeout

1. Re-check changed paths against the DOX chain
2. Update nearest owning docs and any affected parents or children
3. Refresh every affected Child DOX Index
4. Remove stale or contradictory text
5. Run existing verification when relevant
6. Report any docs intentionally left unchanged and why

---

# FastChem

## Purpose

FastChem is a fast-paced chemistry practice game: timed multiple-choice questions in single player, custom rooms, and ranked 1v1. Two deployable parts, one binary in production.

- `backend/` — Go 1.24 + Gin REST/WebSocket API, SQLite persistence. Also serves the built frontend.
- `frontend/` — Next.js 14 App Router, static-exported to `frontend/out/`.

## Ownership

Root-owned files:

- `README.md` — user-facing setup, API summary, Docker instructions
- `Dockerfile` — 3-stage build (frontend export → Go build with CGO → debian-slim runtime)
- `docker-compose.yml` — single `fastchem` service, `fastchem-data` volume at `/data`
- `run.sh` — local dev: builds the frontend, then runs the backend with `FRONTEND_DIR` set
- `.dockerignore`, `.gitignore`
- `AGENTS.md` (this DOX rail) and `CLAUDE.md`

## Local Contracts

- **One origin in production.** The Go server serves both `/api/*` and the static export, so the frontend calls the API with a relative base URL by default. Do not introduce a second runtime host without updating `Dockerfile`, `docker-compose.yml`, `run.sh`, and CORS defaults together.
- **Environment variables** are read only in `backend/internal/config/config.go`: `PORT`, `DB_PATH`, `JWT_SECRET`, `GIN_MODE`, `FRONTEND_DIR`, `ALLOWED_ORIGINS`. Adding one means updating that file, `Dockerfile`, `docker-compose.yml`, and `README.md`.
- **API shape is a cross-stack contract.** Go structs in `backend/internal/models/` and TypeScript interfaces in `frontend/src/types/index.ts` describe the same JSON. A change to either side is incomplete until the other matches — JSON tags are camelCase on both sides.
- **No secrets in the repo.** `JWT_SECRET` comes from the environment; the compose default `change-me-in-production` is a placeholder, not a value to rely on.
- **Do not commit build output or data:** `frontend/out/`, `frontend/.next/`, `frontend/node_modules/`, `logs/`, `*.db*`.

## Work Guidance

- Keep changes on the designated feature branch; never push to `main`.
- Match the surrounding style: Go uses `slog` for logging and standard `gofmt`; TypeScript/React uses function components, Tailwind utility classes, and the `@/*` path alias.
- Scoring, rating, and question-generation rules live in `backend/internal/services/`. The frontend displays results; it does not recompute authoritative scores.
- When adding a route, wire it in `backend/cmd/server/main.go` and add the matching client call in `frontend/src/lib/api.ts`.

## Verification

No CI exists in this repository, and Go tests cover only `backend/internal/services`. Run the checks that do exist:

```bash
cd backend  && go build ./... && go vet ./... && go test ./... -race
cd frontend && npm run lint && npm run build
```

`npm run build` is the real frontend gate — it type-checks and produces the static export the backend serves. Update this section if a test framework is ever added.

## User Preferences

- DOX is installed and must be followed for every edit in this repository.

## Child DOX Index

- `backend/AGENTS.md` — Go API server: routing, config, persistence, game logic
- `frontend/AGENTS.md` — Next.js static-export client: routes, UI, API client
