---
name: node-service-standards
description: Baseline standards for any Node.js service — TypeScript strict, ESM, project layout, boot-time config validation, dependency discipline, health endpoints, graceful shutdown, and process error handling. Use when scaffolding a new Node service or auditing an existing one.
---

# Node Service Standards

Applies to every Node service regardless of framework. These are the non-negotiable baselines.

## Language and modules

- **TypeScript in strict mode.** `strict: true` plus `noUncheckedIndexedAccess`, `noImplicitOverride`, `exactOptionalPropertyTypes`. No `any` without a written justification; prefer `unknown` at boundaries.
- **ESM** (`"type": "module"`). Use explicit file extensions in relative imports where the resolver requires them. No mixing CommonJS `require` into ESM source.
- Compile with a modern `target`/`lib` matching the pinned Node runtime.

## Project layout

- `src/` for source, `test/` or co-located `*.test.ts` for tests, `dist/` build output (git-ignored).
- Group by feature/domain, not by type. Keep a clear entrypoint (`src/main.ts`) that only wires and starts.
- One responsibility per module; keep files small enough to reason about.

## Config validated at boot (fail fast)

- Parse and validate all environment variables **once at startup** with a schema (zod/joi). Exit non-zero on any missing or malformed value — never boot half-configured.
- Export a typed, frozen config object; never read `process.env` elsewhere.

```ts
const Env = z.object({ NODE_ENV: z.enum(['development','production','test']), PORT: z.coerce.number(), DATABASE_URL: z.string().url() });
export const config = Object.freeze(Env.parse(process.env));
```

## Dependency discipline

- **Justify every new package.** Prefer the standard library and existing deps. A tiny utility is not worth a transitive-dependency and supply-chain surface.
- Adding a dependency that reaches system resources (network, filesystem, child processes, native bindings) or touches auth/crypto is a **gated architecture decision** — surface it and get human approval before adding, don't slip it in.
- Prefer well-maintained, widely-used libraries; check last-publish, open advisories, and install size.
- Keep `dependencies` vs `devDependencies` honest.

## Pinned runtime and lockfile

- Pin the Node version via `engines` in `package.json` and an `.nvmrc`/`.tool-versions`. CI enforces it.
- Commit the lockfile; install with `npm ci` (or the equivalent frozen-lockfile command) in CI and containers. Never `npm install` in a reproducible build.

## Health and readiness

- Expose `GET /healthz` (liveness — process is up) and `GET /readyz` (readiness — dependencies like DB/queue are reachable). Readiness gates traffic; liveness triggers restarts.
- Keep them cheap and unauthenticated (or lightly protected), returning fast.

## Graceful shutdown

- Handle `SIGTERM`/`SIGINT`: stop accepting new work, drain in-flight requests and jobs, close DB/queue/pool connections, flush logs, then exit 0. Force-exit after a bounded timeout.
- On shutdown, flip readiness to failing first so the load balancer stops routing.

## Process error handlers

- Attach `process.on('unhandledRejection')` and `process.on('uncaughtException')`: log with full context, then exit non-zero and let the orchestrator restart. Do not swallow and continue in an unknown state.

```ts
process.on('unhandledRejection', (e) => { logger.fatal({ err: e }); process.exit(1); });
```

## Security posture

- Run `npm audit` (or Snyk/Dependabot) in CI; triage advisories by real reachability, not just severity score.
- Never log secrets. Load them from env/secret manager, validated at boot.
- Run as a non-root user in containers; drop unnecessary capabilities.

## Anti-patterns

- Reading `process.env` throughout the code instead of one validated config.
- Booting with missing config and failing later at first use.
- `npm install` in CI/containers (non-reproducible builds).
- Catch-all handlers that keep the process alive after an uncaught exception.
- Adding heavy or system-reaching dependencies without review.
