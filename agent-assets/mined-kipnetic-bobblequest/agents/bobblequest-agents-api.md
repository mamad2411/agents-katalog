# apps/api

Bun-native HTTP server and composition root for the monorepo. Hono handles CORS, `/health`, and
raw-body webhook routes; `@hono/trpc-server` mounts the tRPC router at `/trpc/*`; Zod guards every
boundary. Exports `AppRouter` (from `src/routers/index.ts`) as the `@t/api` package — consumed by
`apps/web`, `apps/website`, `apps/mobile`, and `apps/desktop` as a typed client. Runs as three
independent Railway services: HTTP (`src/index.ts`), Worker (`src/worker.ts`), Cron (`src/cron.ts`).

Root AGENTS.md: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\AGENTS.md

---

## Tech Stack

| Piece | Version |
|---|---|
| Runtime | Bun 1.3.11 |
| HTTP framework | hono ^4.0.0 |
| tRPC server | @trpc/server ^11.0.0 |
| tRPC/Hono bridge | @hono/trpc-server ^0.4.0 |
| Auth | @clerk/backend ^3.4.0 |
| Webhook verification | svix ^1.92.2 |
| Validation | zod ^3.23.0 |
| Test runner | vitest ^2.1.0 |
| Linter/formatter | @biomejs/biome ^2.4.13 |

---

## Entry Points

| Role | Absolute path |
|---|---|
| HTTP server boot | C:\Users\jager\OneDrive\Documents\GitHub\template-repo\apps\api\src\index.ts |
| AppRouter export | C:\Users\jager\OneDrive\Documents\GitHub\template-repo\apps\api\src\routers\index.ts |
| DI composition root | C:\Users\jager\OneDrive\Documents\GitHub\template-repo\apps\api\src\composition.ts |
| Worker entrypoint | C:\Users\jager\OneDrive\Documents\GitHub\template-repo\apps\api\src\worker.ts |
| Cron entrypoint | C:\Users\jager\OneDrive\Documents\GitHub\template-repo\apps\api\src\cron.ts |
| Clerk auth middleware | C:\Users\jager\OneDrive\Documents\GitHub\template-repo\apps\api\src\middleware\clerkAuth.ts |
| tRPC init + procedures | C:\Users\jager\OneDrive\Documents\GitHub\template-repo\apps\api\src\trpc\index.ts |

---

## Run / Test / Build

```
bun run dev                               # full stack from monorepo root (recommended)
bun --cwd apps/api run dev                # API only (hot-reload)
bun --cwd apps/api run worker:dev         # worker (watch)
bun --cwd apps/api run cron               # cron (one-shot)
bun --cwd apps/api run test               # vitest run (CI)
bun --cwd apps/api run test:coverage      # with coverage report
bun --cwd apps/api run check              # biome lint
bun --cwd apps/api run typecheck          # tsc --noEmit
bun --cwd apps/api run build && bun --cwd apps/api run start   # prod
```

---

## Conventions

- `AppRouter` is the sole public contract — five client apps import it as a type from `@t/api`.
  Never bypass tRPC with raw `fetch` to internal API routes.
- Every tRPC procedure input must have a Zod schema. All mutations use `protectedProcedure`.
  `adminProcedure` additionally asserts `publicMetadata.role === 'admin'`.
- Procedures depend only on ports (`ctx.db`, `ctx.auth`, `ctx.analytics`, `ctx.cache`, …).
  No direct SDK imports (`@clerk/backend`, `ioredis`, etc.) inside routers or procedures.
- `buildContainer()` in `src/composition.ts` is the single composition root. Registrar order is
  fixed: config → logger factory → logger → cache / db / auth / analytics → billing.
  Never construct a second container; never resolve tokens outside of `createContext` or entrypoints.
- Webhook routes (`/api/webhooks/clerk`, `/api/webhooks/revenuecat`) sit outside the tRPC mount and
  require raw body access before any JSON parser. Keep them in `src/routes/webhooks/`.
- Job handlers live in `src/jobs/handlers/<name>Handler.ts` as typed factory functions. Register
  them in `src/jobs/registerJobHandlers.ts`. Producers call `ctx.queue.enqueue(name, payload)`.
- tRPC v11: no transformer on the server; clients must not set `transformer` either.
- Config comes from `ConfigRepository` (`ctx.config`). No `process.env` reads inside routers.

---

## Banned in This Scope

- Raw `fetch` calls to internal `/trpc/*` routes — use the tRPC client.
- Direct SDK imports in routers (`@clerk/backend`, `ioredis`, `postgres`, etc.) — use ports only.
- `process.env` reads inside routers or procedures — read from `ctx.config`.
- `express` — Hono only.
- `any`, `@ts-ignore`, `as` casts to silence errors.
- `axios`, `lodash`, `moment`/`dayjs` (see root AGENTS.md Banned section).
- A second `buildContainer()` call — one container per process, always.

---

## Links

- Architecture deep-dive: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\docs\architecture\apps\api.md
- Composition root rules: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\.agents\rules\composition-root.md
- Dependency injection rules: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\.agents\rules\dependency-injection.md
- Error handling rules: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\.agents\rules\error-handling.md
- Testing runner config: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\.agents\rules\testing-runner.md
- Import rules: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\.agents\rules\import-rules.md
- Queue architecture: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\docs\architecture\platform\queue.md
