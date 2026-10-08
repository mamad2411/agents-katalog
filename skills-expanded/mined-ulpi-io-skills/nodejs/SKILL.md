---
name: nodejs
version: 1.1.0
description: |
  Write Node.js and Bun backend code the way THIS project already does it, not by generic
  defaults — a TypeScript-first reference that detects the runtime and carries the real
  conventions for HTTP servers, Zod boundary validation, typed error handling, pino logging,
  database access, auth, BullMQ queues, caching, async and graceful-shutdown patterns, security,
  CLI tooling, testing, and observability, so a change lands idiomatic and review-ready instead
  of merely running. Use when a task touches this project's Node.js or Bun backend and should
  follow its conventions rather than generic defaults.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
argument-hint: "[Node.js/Bun backend task or subsystem]"
arguments:
  - request
when_to_use: |
  Use when the task touches Node.js or Bun backend code: HTTP servers, API endpoints, database
  queries, auth, jobs, caching, logging, testing, CLI tools, or deployment. Examples: "add an API
  endpoint", "fix this async error", "set up BullMQ jobs", "add request validation", "build a CLI
  command", "containerize this service". Do NOT use for frontend-only work, or when a framework
  owns the surface — Next.js (nextjs), NestJS (nestjs), or Laravel (laravel); this is the
  framework-agnostic backend surface.
effort: high
---

<EXTREMELY-IMPORTANT>
This skill is a routing shell over the Node.js/Bun reference set.

Non-negotiable rules:
1. Read `references/stack.md` first to determine the runtime (Node.js or Bun), framework, and locked decisions.
2. Then load only the references needed for the actual task.
3. **TypeScript strict mode** — no `any`, no implicit returns, no unchecked index access.
4. **All async functions must handle errors** — no unhandled promise rejections. Use try/catch or `.catch()` at every boundary.
5. **Input validation at system boundaries** — Zod schemas on every external input (request bodies, query params, env vars, CLI args). Never trust `req.body`.
6. **Structured logging via pino** — no `console.log` in production code. JSON to stdout, parsed by log aggregators.
7. **Graceful shutdown** — handle SIGTERM/SIGINT, drain connections, finish in-flight work, close DB pools.
8. **No secrets in code or logs** — env vars validated at startup, never logged, never in error responses.
</EXTREMELY-IMPORTANT>

# nodejs

## Inputs

- `$request`: The backend task, subsystem, bug, or feature being worked on

## Goal

Route Node.js/Bun backend work through the project's conventions so implementation follows the established patterns for server architecture, data access, error handling, and deployment.

## Step 0: Read the stack contract

Always start with:

- `references/stack.md`

That establishes: runtime (Node.js or Bun), framework (Express/Fastify/Hono/none), ORM, test runner, package manager, and locked dependency choices.

If `bun.lockb` or `bunfig.toml` exists, the runtime is Bun — also load `references/bun-runtime.md` for native API differences.

**Success criteria**: The project's runtime, framework, and toolchain choices are explicit before implementation starts.

## Step 1: Load only the relevant references

Use the routing table to pick reference files. Do not bulk-load the full reference tree.

| Task | Read |
|------|------|
| Runtime, TypeScript, package manager, locked deps | `references/stack.md` |
| Folder conventions, entry points, monorepo layout | `references/project-structure.md` |
| Express/Fastify/Hono patterns, middleware, routing | `references/http-server.md` |
| REST conventions, versioning, pagination, error responses | `references/api-design.md` |
| Zod/AJV input validation, DTO patterns | `references/validation.md` |
| Prisma/Drizzle/Knex, migrations, connection pooling | `references/database.md` |
| JWT, sessions, OAuth2, RBAC, middleware guards | `references/auth.md` |
| Error classes, async error boundaries, HTTP error responses | `references/error-handling.md` |
| pino structured logging, request correlation, log levels | `references/logging.md` |
| vitest/jest/bun test, supertest, test factories, coverage | `references/testing.md` |
| Promises, streams, worker threads, AbortController, shutdown | `references/async-patterns.md` |
| helmet, CORS, rate limiting, input sanitization, dep audit | `references/security.md` |
| Redis, in-memory caching, cache invalidation patterns | `references/caching.md` |
| BullMQ, job patterns, retry strategies, dead-letter queues | `references/queues-jobs.md` |
| Env validation, dotenv, config modules, secrets management | `references/config.md` |
| OpenTelemetry, health checks, metrics, distributed tracing | `references/observability.md` |
| Multi-stage Dockerfile, .dockerignore, prod vs dev images | `references/docker.md` |
| ws/Socket.io, connection lifecycle, scaling, rooms | `references/websockets.md` |
| commander/yargs, argument parsing, exit codes, stdin/stdout | `references/cli.md` |
| Bun-native APIs, bun test, bun build, Bun.serve, Bun.$ | `references/bun-runtime.md` |

Multiple tasks? Read multiple files. The references are self-contained.

**Success criteria**: Only the task-relevant backend conventions are in play.

## Step 2: Implement with the core backend guardrails

Keep these rules active:

- TypeScript strict mode with `noUncheckedIndexedAccess`
- all external input validated at the boundary (Zod schemas)
- errors are typed, caught, and returned as structured HTTP responses
- logging via pino child loggers with request correlation IDs
- database access through the project's ORM/query builder, not raw SQL strings
- mutations wrapped in transactions where atomicity matters
- graceful shutdown: SIGTERM handler drains server, closes pools, exits cleanly
- env vars validated at startup — fail fast on missing required config
- no `any`, no `as` type assertions unless justified with a comment
- if Bun runtime: prefer `Bun.serve()`, `Bun.file()`, `bun test` over Node.js equivalents

**Success criteria**: The change matches the project's backend architecture instead of generic defaults.

## Step 3: Verify the affected surface

Use the narrowest relevant verification:

- unit tests (`vitest run`, `jest`, or `bun test`)
- integration tests with supertest or actual HTTP calls
- type checking (`tsc --noEmit`)
- linting (`eslint .`)
- if Docker: build the image and verify it starts

**Success criteria**: The changed backend surface still builds, type-checks, and passes tests.

## Guardrails

- Do not inline the whole Node.js handbook in `SKILL.md`.
- Do not skip `references/stack.md`.
- Do not use `console.log` in production code — use pino.
- Do not bypass input validation at API boundaries.
- Do not leave unhandled promise rejections.
- Do not hardcode secrets, ports, or environment-specific values.
- Do not add `disable-model-invocation`; this is a normal domain skill.

## When To Load References

- `references/stack.md`
  Always.

- `references/bun-runtime.md`
  When the project uses Bun (detected via `bun.lockb` or `bunfig.toml`).

- then only the task-relevant files under `references/`

## Output Contract

Report:

1. which references were loaded
2. the architecture pattern chosen
3. the change made
4. the verification run
