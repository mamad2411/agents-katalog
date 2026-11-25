---
name: follow-lib-drizzle-setup-drizzle
description: Install Drizzle ORM, create schema.ts and the db client, ready to use
argument-hint: "[dialect-or-driver]"
related:
  - follow-lib-postgres
  - follow-lib-zod
  - run-drizzle-studio
  - learn
  - resolve-errors
---

## Goal

Install Drizzle ORM, the driver, and `drizzle-kit`, then create `drizzle.config.ts`, `schema.ts` and the db client so queries really run — first-time setup only

## Scope

- Use when the project has no Drizzle yet or needs a fresh setup (if it exists already → verify only)
- Covers: install, `drizzle.config.ts`, `src/db/schema.ts`, `src/db/index.ts`
- Does not cover migrations — do `workflows/migrate-schema/SKILL.md` instead

## Execute

### 1. Check Precondition

> Goal: check the environment and current state before setup

1. Confirm the runtime (`bun --version` or `node --version`) and that the database server/file is ready
2. Read `package.json` — if absent → stop and report; if `drizzle-orm` is already there → skip to verify
3. Check `DATABASE_URL` or the related env — if a secret/env is missing → stop and tell the user

### 2. Install Packages

> Goal: install `drizzle-orm`, the driver, and `drizzle-kit`

1. Run `bun add drizzle-orm` then `bun add -D drizzle-kit` (or the package manager matching the lockfile)
2. Install the driver per runtime/database — see [../../references/components/drivers.md](../../references/components/drivers.md)
3. Confirm the dependencies landed correctly in `package.json` (`drizzle-orm` as a runtime dep, `drizzle-kit` as dev)
4. If unsure about a version/API → run `/learn-from-web` to check the official docs

### 3. Configure drizzle.config.ts

> Goal: create the minimal necessary config

1. Create `drizzle.config.ts` with `defineConfig` — see [../../references/components/config.md](../../references/components/config.md)
2. Specify `dialect`, `schema`, `out` and `dbCredentials.url` read from `DATABASE_URL`
3. Specify `driver` only when using a special driver (`turso`, `d1-http`, `pglite`, `neon-http`, etc.)
4. Never hardcode credentials — store secrets via `/follow-secret-manager`

### 4. Define Schema And Client

> Goal: create `schema.ts` and the db client exporting `db`

1. Create `src/db/schema.ts` with `pgTable`/`mysqlTable`/`sqliteTable` per the dialect — see [../../references/api/schema.md](../../references/api/schema.md)
2. Create types with `typeof table.$inferSelect` and `$inferInsert`; define `relations()` if using relational queries
3. Create `src/db/index.ts` that calls `drizzle(url, { schema })` then exports the `db` instance — for SQLite enable WAL mode (`PRAGMA journal_mode = WAL`)
4. Never expose credentials in source code

### 5. Verify Setup

> Goal: smoke check that the setup really works

1. Run `bunx drizzle-kit check` or a small query (e.g. `db.select().from(table).limit(1)`) as a smoke test
2. Run the project's lint/typecheck
3. If verification fails → run `/resolve-errors` max 3 rounds, then stop and report; if it passes → `/suggest-next-action`

## Rules

- Idempotent — if setup already exists, only verify; never reinstall/overwrite the existing config
- Write the minimal config first, then add options — never copy a full config from docs unnecessarily
- Always read credentials from the environment, never commit secrets
- Check the version in `package.json` before choosing an API (v0.x `relations()` vs v1.0 RC `defineRelations()`)

## Expected Outcome

- `drizzle-orm`, `drizzle-kit` and the driver fully installed in `package.json`
- `drizzle.config.ts`, `src/db/schema.ts`, `src/db/index.ts` ready to use
- Smoke query runs green — ready to do `workflows/migrate-schema/SKILL.md`
