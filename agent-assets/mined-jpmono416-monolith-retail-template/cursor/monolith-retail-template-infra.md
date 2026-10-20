---
description: CI/CD, Railway, Vercel, Supabase, and Upstash deployment standards
globs:
  - ".github/**"
  - "infrastructure/**"
  - "apps/web/vercel.json"
alwaysApply: false
---

# Infrastructure & deployment

## Purpose

Define how code moves from PR to production across GitHub Actions, Railway, Vercel, Supabase, and Upstash with environment parity. Toolchain pins (Node, pnpm) are owned by `monorepo.mdc`.

## Required patterns

### Deployment map

| Component | Platform | Config location |
|-----------|----------|-----------------|
| Web (Next.js) | Vercel | `apps/web/vercel.json`, Vercel project env |
| API (NestJS) | Railway | `infrastructure/railway/api.railway.toml` |
| PostgreSQL | Supabase (prod) / Docker (local) | `DATABASE_URL`, `DIRECT_URL` |
| Redis / BullMQ | Upstash (prod) / Docker (local) | `REDIS_URL`, `BULLMQ_PREFIX` |
| CI | GitHub Actions | `.github/workflows/ci.yml` |

### CI pipeline (PR gate)

Every PR and push to `main` must pass, in order:

1. `pnpm install --frozen-lockfile`
2. `pnpm db:generate`
3. `pnpm lint` → `pnpm typecheck` → `pnpm test` → `pnpm build`
4. Playwright E2E (`needs: quality`) on Chromium

CI provides Postgres 16 and Redis 7 service containers — tests must not assume external cloud services.

This is the single PR gate. Other rules (`agent-behaviour.mdc`, `testing.mdc`) reference it.

### Env-var registration (canonical checklist)

A new environment variable is a multi-surface change. All apply:

1. Add key + comment to `.env.example`.
2. Add to `apps/api/src/config/env.validation.ts` (validated, fail-fast).
3. Add to `apps/api/src/config/configuration.ts` typed factory.
4. Add to `docker-compose.yml` service env if needed in containers (`docker.mdc`).
5. Add to Railway / Vercel / Supabase / Upstash dashboards for affected environments.
6. If browser-exposed, prefix `NEXT_PUBLIC_` (see `naming.mdc`, `security.mdc`).

### Railway (API)

- Build: `infrastructure/docker/api.Dockerfile`, target `production`.
- Health check path: `/api/health`.
- Env vars set in Railway dashboard — never committed; mirror `.env.example`.

### Vercel (Web)

- Root directory: `apps/web` (monorepo setting).
- Production env: `NEXT_PUBLIC_APP_URL`, `NEXT_PUBLIC_API_URL` pointing to deployed API.
- Server-side API calls in production: `API_INTERNAL_URL` if using private networking; otherwise the public API URL.

### Supabase (database)

- `DATABASE_URL` — pooled connection for runtime (Prisma).
- `DIRECT_URL` — direct connection for migrations (`prisma migrate`).
- Run migrations from the deploy pipeline or a documented release step — never manually against prod without review.

### Upstash (Redis)

- `REDIS_URL` — TLS URL from Upstash for BullMQ/ioredis in production.
- Keep `BULLMQ_PREFIX` distinct per environment (`monolith`, `monolith-staging`, …) to avoid queue collisions.

## Forbidden patterns

- Storing production secrets in repo (`.env`, dashboard exports, terraform with plaintext secrets).
- Disabling CI checks to merge (`skip ci`, bypassing required checks).
- Deploying API without health check or without `pnpm db:generate` in build.
- Local Docker connection strings in Railway/Vercel production env.
- Divergent Node/pnpm versions between CI, Docker base images, and platform build images.

## Implementation expectations

- Infrastructure changes that affect deploy require updating `infrastructure/*/README.md` or `docs/workflows/`.
- Breaking API changes: coordinate web deploy or use backward-compatible responses.
- Turbo `build` outputs must remain correct in `turbo.json` for remote cache compatibility.

## Consistency expectations

- Branch protection on `main`: require CI green before merge.
- Production: `NODE_ENV=production`, `LOG_LEVEL=info` (or stricter).
- Staging uses separate Supabase/Upstash instances — never share prod DB/Redis.

## Examples

**Good — Railway healthcheck**

```toml
healthcheckPath = "/api/health"
```

**Good — CI service env**

```yaml
env:
  DATABASE_URL: postgresql://monolith:monolith@localhost:5432/monolith?schema=public
  REDIS_URL: redis://localhost:6379
```

**Bad — migration against pooled URL only**

```bash
DATABASE_URL="$POOLED_URL" pnpm db:migrate # use DIRECT_URL on Supabase
```
