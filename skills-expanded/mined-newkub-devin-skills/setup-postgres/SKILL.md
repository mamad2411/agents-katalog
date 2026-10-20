---
name: follow-lib-postgres-setup-postgres
description: Install the postgres.js driver and set up the connection string/client until usable
argument-hint: "[database-url-or-scope]"
related:
  - follow-lib-postgres
  - follow-lib-drizzle
  - follow-secret-manager
  - learn
  - resolve-errors
---

## Goal

Install the `postgres` (postgres.js) driver, set up the connection string, and create a client that can actually query — first-time setup only

## Scope

- use when the project has no postgres.js yet (if it exists already → verify only)
- covers: install, `DATABASE_URL`, the `postgres()` client, basic queries/transactions
- does not cover pool tuning — use `workflows/optimize-pool/SKILL.md` instead

## Execute

### 1. Check Precondition

> Goal: check the environment before setup

1. read `package.json` — if `postgres` is already present → skip to verify
2. confirm the PostgreSQL server is reachable (host, port, credentials)
3. check `DATABASE_URL` — if missing → stop and tell the user; store it via `/follow-secret-manager`, never commit
4. check the runtime — postgres.js needs TCP; on Cloudflare Workers use Hyperdrive or another driver (see the official docs)

### 2. Install

> Goal: install postgres as a runtime dependency

1. run `bun add postgres` (or the package manager per the lockfile)
2. confirm `postgres` lands in `dependencies`
3. if used with Drizzle → run `/follow-lib-drizzle` (drizzle uses postgres.js as its driver)

### 3. Create Client

> Goal: one exported client shared across the whole app

1. create `src/db/index.ts` (or follow the existing structure): `import postgres from "postgres"` then `const sql = postgres(process.env.DATABASE_URL)`
2. default options are enough at setup — pool sizing/`prepare` tuning belongs in `optimize pool`
3. export the single `sql` instance — never create a new client per request/module
4. on serverless: use Hyperdrive/PgBouncer pooling — don't open a connection per request

### 4. Basic Usage

> Goal: query with safe tagged templates

1. use tagged templates `` sql`SELECT * FROM t WHERE id = ${id}` `` — automatically parameterized
2. `sql.begin()` for transactions
3. `sql.listen(channel, onnotify)` for LISTEN/NOTIFY (add when needed)
4. close with `sql.end()` in teardown/graceful shutdown

### 5. Verify

> Goal: a smoke query really passes

1. run `` sql`SELECT 1` `` or a small query as a smoke test
2. run the project's lint/typecheck
3. if verify fails → run `/resolve-errors` max 3 rounds, then stop and report; passing → `/suggest-next-action`

## Rules

- Idempotent — if already set up, verify only; never create a duplicate client
- Never string-concat queries — always tagged templates; use `sql.unsafe()` only for dynamic queries that cannot be parameterized
- Connection string always from env — never hardcode host/credentials
- One client instance per process — if unsure about options → check the official docs (github.com/porsager/postgres)

## Expected Outcome

- `postgres` installed, `DATABASE_URL` set via env
- a single exported `sql` client shared across the app, smoke query passes
- ready for `workflows/optimize-pool/SKILL.md` if tuning is needed
