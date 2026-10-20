# Copilot Instructions — CLI Web Automatization

> **AI Primer:** Read this file completely before writing, editing, or scaffolding any code.
> Check `docs/FEATURES/` for feature specs and `docs/PRDs/` for product requirements.
> These files together are your complete project context.

---

## Project Overview

| Concern     | Technology                            |
| ----------- | ------------------------------------- |
| Backend API | Go (stdlib `net/http`) + PostgreSQL   |
| Frontend    | Next.js 16.2 App Router + TypeScript  |
| Database    | PostgreSQL 18 + sqlc (code-generated) |
| Auth        | Scaffolded — not yet implemented      |
| Deployment  | Docker Compose (local)                |
| CI/CD       | GitHub Actions                        |

---

## Repository Structure

```
.
├── .github/
│   ├── agents/                   ← agent definitions and instructions
│   ├── hooks/                    ← agent hooks
│   ├── prompts/                  ← agent prompts
│   └── skills/                   ← agent skills
├── docs/
│   ├── FEATURES/                 ← feature specs
│   ├── PRDs/                     ← product requirement documents
│   ├── TASKS/                    ← task boards and implementation plans
│   └── AGENTS.md                 ← agent docs guide
├── services/
│   ├── core/                     ← Go REST API
│   │   └── AGENTS.md             ← service-specific agent docs
│   └── web/                      ← Next.js frontend
│       └── AGENTS.md             ← service-specific agent docs
├── docker-compose.yml            ← PostgreSQL + core + web
└── AGENTS.md                     ← you are here
```

---

## Backend (`services/core`)

### Commands

```bash
cd services/core

make run          # run API locally
make build        # build binary → bin/core
make tidy         # go fmt + go mod tidy
make migrate/up   # apply pending migrations
make populate     # apply seed data
make reset        # drop + recreate + migrate + seed
make generate     # regenerate sqlc after SQL changes
make db/sync      # migrate/up + generate
```

---

## Frontend (`services/web`)

### Commands

```bash
cd services/web

bun install   # install dependencies
bun dev       # start dev server (port 3000)
bun build     # production build
bun lint      # Biome lint
bun format    # Biome format
```

## Local Development

Run the following command from the root directory to start the entire application locally:

```bash
# copy .env files
cp .env.example .env
cp services/core/.env.example services/core/.env
cp services/web/.env.example services/web/.env

# start services
docker-compose up -d --build

# run database migrations and generate sqlc code
cd services/core && make db/sync
```
