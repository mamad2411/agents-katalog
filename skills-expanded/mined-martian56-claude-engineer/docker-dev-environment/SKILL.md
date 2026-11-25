---
name: docker-dev-environment
description: Use when setting up local development services or running the project locally. Establishes the "stateful services in Docker, app runs native" pattern with Postgres, Redis, MinIO, and Mailpit.
---

# Docker Dev Environment

**Announce at start:** "I'm using claude-engineer:docker-dev-environment to run services in Docker and the app native."

## Iron Law
**Only stateful services run in Docker. The app (frontend + backend) runs NATIVELY** in its own shell.
Rationale: instant `uvicorn --reload` / `next dev` / `vite` HMR, real debuggers, and CI/toolchain parity -
Docker handles only the painful-to-install backing services.

## The baseline services (`docker-compose.yml`)
- **PostgreSQL** - primary DB (`localhost:5432`).
- **Redis** - cache, sessions, rate-limit, job broker (`localhost:6379`).
- **MinIO** - S3-compatible object storage (`localhost:9000` API / `9001` console) + a bucket-bootstrap step.
- **Mailpit** - email capture for signup/reset flows (`localhost:1025` SMTP / `8025` UI).
All with healthchecks and named volumes. The native app connects via `localhost` URLs in `.env`.

## The dev flow
1. `docker compose up -d` (services only).
2. Backend in shell A: `uv run uvicorn ...` (native).
3. Frontend in shell B: `pnpm dev` / `bun dev` / `vite` (native).

## Non-negotiables
1. Never containerize the app for local dev (the guard hook will remind you).
2. Healthchecks on every service; the app waits for healthy services.
3. Secrets/connection strings via `.env` (git-ignored), documented.

**Full detail (the complete compose file, MinIO bucket bootstrap, Mailpit SMTP config, connection settings):**
read `references/dev-services.md` on demand.

## Red flags - STOP
- `docker compose up` that builds/starts the app itself for local dev.
- Hardcoded service URLs instead of `.env`.
- A service with no healthcheck.
