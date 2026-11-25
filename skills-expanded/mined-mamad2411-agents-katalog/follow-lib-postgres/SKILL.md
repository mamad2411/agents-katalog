---
name: follow-lib-postgres
description: Use the postgres (postgres.js) driver — tagged templates, connection pool, listen/notify
argument-hint: "[target-or-scope]"
related:
  - run-verify
  - run-test
  - run-drizzle-studio
  - follow-lib-drizzle
---

## Goal

Use the postgres (postgres.js) driver — tagged templates, connection pool, listen/notify

## Scope

Use when the task involves this library/tool — setup, usage, debugging, or best practices (lib postgres)

- Covers: the `postgres` (postgres.js) driver — tagged templates, pool, transactions, LISTEN/NOTIFY, `sql.subscribe`
- Not covered: ORM/schema layer — use `/follow-lib-drizzle` (drizzle uses postgres.js as its driver); the `Bun.sql` built-in for Bun-only projects
- No CLI — used via programmatic API only (thus none)
- Latest: `postgres@3.4.9` (verified 2026-09-13)
- References: [apis](references/apis.md) 
## Execute

### Workflows

| Topic | Workflow |-------|----------| Setup | `workflows/setup-postgres/SKILL.md` — install, connection string, client | Optimize | `workflows/optimize-pool/SKILL.md` — pool sizing, prepared statements 
### 1. Setup And Usage

> Goal: use correctly per the official docs

1. Create `postgres(url, {max, prepare})` — default pool of 10 connections
1. Use tagged templates `` sql`SELECT * FROM t WHERE id = ${id}` `` — automatically parameterized
1. Use `sql.begin()` for transactions, `sql.listen(channel, onnotify)` for LISTEN/NOTIFY, and `sql.notify(channel, payload)` to send a notify
1. Use `sql.subscribe(pattern, onrow)` for realtime row changes (e.g. `'insert:events'`, `'*:users'`) — creates a dedicated connection automatically
1. Pairs well with Drizzle — drizzle uses postgres.js as its driver

### 2. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` if related tests exist
3. Check the latest official docs before using an uncertain API (lib postgres)

## Rules

- Never string-concat queries — always use tagged templates; `sql.unsafe()` only for dynamic queries that can't be parameterized
- Close connections with `sql.end()` in teardown
- On serverless, use Hyperdrive/PgBouncer pooling — don't open a connection per request

- Use `/run-verify` if needed
- Use `/run-test` if needed
- Use `/run-drizzle-studio` if needed
- Use `/follow-lib-drizzle` if you want an ORM layer

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (lib postgres)
- No known security/performance pitfalls (lib postgres)
- Lint, typecheck, tests pass
