---
description: Docker Compose and container development standards
globs:
  - "docker-compose*.yml"
  - "infrastructure/docker/**"
  - "**/Dockerfile*"
alwaysApply: false
---

# Docker

## Purpose

Keep local development aligned with production containers: reproducible infra, healthy dependencies, and safe host/Docker workflows on Windows/macOS/Linux.

## Required patterns

### Local stack

- Root `docker-compose.yml` is the canonical local orchestration.
- Infrastructure services: **PostgreSQL 16** and **Redis 7** with healthchecks before dependent apps start.
- App services (`api`, `web`) build from `infrastructure/docker/*.Dockerfile` with explicit `target: development` | `production`.

### Commands (root `package.json`)

| Script | Use |
|--------|-----|
| `pnpm docker:up` | Build and start full stack |
| `pnpm docker:down` | Stop services |
| `pnpm docker:clean` | Stop and remove volumes |
| `pnpm docker:logs` | Follow logs |

### Environment inside Compose

- Service env overrides use Docker network hostnames (`postgres`, `redis`, `api`) — not `localhost`.
- `api` service sets `DATABASE_URL`, `DIRECT_URL`, `REDIS_URL` for in-network access.
- `web` service sets `API_INTERNAL_URL=http://api:3001` for server-side fetches.

### Dockerfiles

- Base: `node:22-alpine`, pnpm via corepack — version pinned by `monorepo.mdc` (toolchain).
- **development** target: minimal COPY for layer cache; full repo mounted via volumes in compose.
- **production** target: `pnpm install --frozen-lockfile`, `pnpm db:generate`, app build, `CMD` runs compiled output (`node dist/main.js` for API).

### Host development alternative

- Postgres + Redis only: `docker compose up postgres redis -d`
- Apps via `pnpm dev` on host with `.env` pointing to `localhost:5432` and `localhost:6379`.

## Forbidden patterns

- Committing `.env` or secrets into images.
- Running `pnpm install` inside containers without understanding volume mounts on Windows (can corrupt host `node_modules`).
- Using both full Docker app services **and** host `pnpm dev` simultaneously without a healthy root `node_modules` from host `pnpm install`.
- Removing healthchecks to "speed up" startup — apps must `depends_on: condition: service_healthy`.
- Ad-hoc `latest` tags for Postgres/Redis in production deploy configs — pin major versions (16, 7).

## Implementation expectations

- After Docker-related permission errors on Windows (`EACCES`, missing `@nestjs/cli`): run recovery from `docs/workflows/development.md`:
  `pnpm docker:clean` → `pnpm clean:modules` → `pnpm install` → `pnpm build`
- Stale API build: delete `apps/api/dist` if `Cannot find module dist/main`.
- New system dependency (e.g. native module): update Dockerfile **and** document in `docs/workflows/development.md`.
- Volume `monolith_node_modules` shares node_modules across api/web in Compose — do not add per-app isolated node_modules volumes.

## Consistency expectations

- Local URLs match `.env.example`: web `3000`, API `3001`.
- Prisma generate runs after install in API container command chain (see compose `command` for `api`).

## Examples

**Good — healthcheck dependency**

```yaml
api:
  depends_on:
    postgres:
      condition: service_healthy
```

**Bad — hardcoded localhost in api service environment**

```yaml
DATABASE_URL: postgresql://...@localhost:5432/...  # inside api container use postgres hostname
```
