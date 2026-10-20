---
name: railway-nestjs
description: >
  Reusable patterns for deploying NestJS applications on Railway.
  Invoke automatically when configuring Railway, writing a NestJS Dockerfile,
  implementing health checks, graceful shutdown, or automatic deploy via GitHub.
---

# Railway + NestJS

## Recommended service structure

```
Railway Project: <project-name>
├── api-production    ← branch main
└── api-staging       ← branch develop
```

Do not create Redis on Railway — use Upstash (serverless, cheaper for MVPs).

---

## `@fastify/*` plugin versions — mandatory compatibility

The `@fastify/*` plugins have major versions tied to the Fastify major version.
NestJS 10 uses **Fastify 4** internally. Installing plugins v12+/v7+/v9+ causes a crash on startup:
`FastifyError: fastify-plugin: @fastify/helmet - expected '5.x' fastify version, '4.x' is installed`

| Plugin | NestJS 10 (Fastify 4) | NestJS 11+ (Fastify 5) |
|---|---|---|
| `@fastify/helmet` | `^11.x` | `^13.x` |
| `@fastify/static` | `^6.x` | `^10.1.2`+ |
| `@fastify/multipart` | `^8.x` | `^10.x` |
| `@fastify/cors` | `^8.x` | `^10.x` |

The "NestJS 11+" versions above are the ones actually verified together in a real
NestJS 10 → 11 migration — not just the first major that's nominally Fastify-5-compatible. Picking an
earlier Fastify-5-compatible major (e.g. `@fastify/static@^7.x`) may still carry CVEs that
only got patched in a later minor/major — see skill `nestjs-fastify` for the full peer
dependency chain and the CVE this specifically closes.

**How to verify the Fastify version used by NestJS:**
```bash
node -e "console.log(require('@nestjs/platform-fastify').FastifyAdapter.name)"
cat node_modules/fastify/package.json | grep '"version"'
```

Before installing any `@fastify/*` plugin, confirm the Fastify major version in use.
Never use `^latest` for Fastify plugins — always pin to the correct major.

---

## NestJS Dockerfile for monorepo

```dockerfile
# apps/api/Dockerfile — build context: the repository root
# Node 24 LTS, the same major as CI. pnpm comes from corepack, which reads the exact version
# pinned in the root package.json "packageManager" field (e.g. "pnpm@10.x.y").
FROM node:24-alpine AS base
RUN corepack enable

FROM base AS builder
WORKDIR /repo
COPY . .
RUN pnpm install --frozen-lockfile
RUN pnpm --filter api build
# Self-contained production install of the api package (workspace deps included, no devDeps)
RUN pnpm --filter api deploy --prod /prod/api

FROM node:24-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder --chown=node:node /prod/api/package.json ./package.json
COPY --from=builder --chown=node:node /prod/api/node_modules ./node_modules
COPY --from=builder --chown=node:node /repo/apps/api/dist ./dist
USER node
EXPOSE 3000
# Liveness only (no dependency pings). The path includes the global prefix.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD wget -qO- "http://127.0.0.1:${PORT:-3000}/api/v1/health/live" > /dev/null || exit 1
CMD ["node", "dist/main.js"]
```

Notes:
- `api` is the package name of `apps/api` — adjust the `--filter`. On pnpm 10+, `pnpm deploy`
  requires `inject-workspace-packages=true` in `.npmrc` (or the `--legacy` flag).
- `USER node` — the official image ships an unprivileged `node` user; never run the API as root.
- The Dockerfile `HEALTHCHECK` covers runtimes that honour it (docker compose, other hosts);
  what gates a Railway deploy is the health check path configured on the service (below).
- Copying the whole repo into the builder stage busts the install cache on every change. For
  faster builds, copy the manifests and lockfile first (or use `pnpm fetch`) before the sources.

---

## Required health checks

Liveness vs readiness: `dev-core:logging-observability`. Readiness returns **503** when a
critical dependency fails; degraded optional dependencies don't fail it
(`dev-core:resilience-patterns`).

```typescript
// interfaces/http/health/health.controller.ts
// With app.setGlobalPrefix('api/v1') these routes are /api/v1/health/live and /api/v1/health/ready
@Controller('health')
@Public()
export class HealthController {
  @Get('live')   // Railway uses this — is the process up? No dependency pings.
  live() { return { status: 'ok' }; }

  @Get('ready')  // CI/CD uses this — can the instance serve traffic?
  async ready(@Res({ passthrough: true }) reply: FastifyReply) {
    const [db, cache] = await Promise.allSettled([this.db.ping(), this.redis.ping()]);
    const checks = {
      database: db.status === 'fulfilled' ? 'ok' : 'degraded',     // critical
      cache:    cache.status === 'fulfilled' ? 'ok' : 'degraded',  // optional
    };
    const ready = checks.database === 'ok';
    reply.status(ready ? 200 : 503);
    return { status: ready ? 'ok' : 'unavailable', timestamp: new Date().toISOString(), checks };
  }
}
```

**Configure in Railway** (the path must include the global prefix — the route that actually exists):
```
Health check path: /api/v1/health/live
Restart policy: always
```

---

## Required graceful shutdown

```typescript
// apps/api/src/main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.enableShutdownHooks();

  ['SIGTERM', 'SIGINT'].forEach(signal => {
    process.on(signal, async () => {
      await app.close();
      process.exit(0);
    });
  });

  // Railway injects PORT — listen on it, on all interfaces
  await app.listen(process.env.PORT ?? 3000, '0.0.0.0');
}
```

Without graceful shutdown, Railway kills the process abruptly during deploys,
which can corrupt in-flight requests.

---

## Minimum environment variables per service

```bash
NODE_ENV=production         # or staging
PORT=3000                   # injected by Railway — set it yourself only for local runs
DATABASE_URL=               # only with a direct Postgres client: transaction pooler (port 6543 in Supabase)
JWT_SECRET=                 # minimum 64 characters — generate with: openssl rand -base64 48
TOKEN_HASH_PEPPER=          # optional — keys the stored refresh-token hash (refresh tokens are opaque)
UPSTASH_REDIS_REST_URL=
UPSTASH_REDIS_REST_TOKEN=
SENTRY_DSN=
```

---

## Automatic deploy

With the **Railway GitHub App** connected to a service, Railway deploys every push to the
configured branch by itself — no CI step is needed (a `railway up` in CI would build and
deploy a second time; see `dev-patterns:github-actions-monorepo`). To deploy only after CI
passes, enable the service's "wait for CI" option instead of deploying from Actions.

```
Production service → branch: main
Staging service    → branch: develop
```

After each deploy, Railway runs the health check. If `/api/v1/health/live` does not respond
within the configured timeout, the new deployment is not promoted.

**Config as code:** keep build and deploy settings in a `railway.json` / `railway.toml` next to
the service (e.g. `dockerfilePath`, `healthcheckPath`, `healthcheckTimeout`,
`restartPolicyType`) so they are reviewed in PRs instead of living only in the dashboard.

---

## Rollback

```bash
# Via CLI
railway rollback --service api-production

# Migrations (if down is implemented)
npm run migrate:rollback --env production
```

---

## Limits and costs

Railway's plans and prices change — the old free tier with a monthly credit was
discontinued. Check the current plans on Railway's pricing page before sizing a project, and
record the plan you chose (and why) in the project's infrastructure doc.

**Trigger to scale:** sustained resource usage near the plan's limits or p95 latency > 800ms.
