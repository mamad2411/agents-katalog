---
name: follow-lib-drizzle-migrate-schema
description: Manage Drizzle migrations — generate/migrate/push flow with a rollback path
argument-hint: "[strategy-or-scope]"
related:
  - follow-lib-drizzle
  - deep-review-codebase
  - plan
  - run-test
  - report-before-after
---

## Goal

Manage Drizzle schema changes safely — pick a strategy (generate/migrate vs push vs pull), review SQL before applying and always have a rollback path

## Scope

- Use when changing `schema.ts` or syncing the schema with the database
- Covers: `drizzle-kit generate`, `migrate`, `push`, `pull`, `check` and rollback notes
- Does not cover first-time setup — do `workflows/setup-drizzle/SKILL.md` first

## Execute

### 1. Plan Migration

> Goal: identify from→to and choose a strategy before acting

1. Run `/plan` — read the schema diff, identify the changed tables/columns/indexes and tables with real data
2. Choose the strategy per use case — see [../../references/cli.md](../../references/cli.md):
   - Development/prototyping: `bunx drizzle-kit push`
   - Production/team: `bunx drizzle-kit generate` + `bunx drizzle-kit migrate`
   - Existing database with no schema: `bunx drizzle-kit pull`
3. If the change is destructive (drop column/table, rename, type change on real data) → always back up the database first
4. Run `/deep-review-codebase` to check the state of the current migration files

### 2. Generate And Review

> Goal: generate the migration SQL and review it before applying

1. Run `bunx drizzle-kit generate --name=<descriptive-name>`
2. Open the generated SQL file in the `out` directory — check every statement, especially `DROP`/`ALTER` that may lose data
3. If the SQL doesn't match the intent → fix the schema then regenerate (never edit snapshot/meta directly)
4. Separate commit per migration — never mix with feature work

### 3. Apply Migration

> Goal: apply migrations in order local → staging → production

1. Local: run `bunx drizzle-kit migrate` then test the related queries
2. Staging/production: apply via the deploy pipeline or `migrate()` in startup code — don't run manually on prod without a runbook
3. Check drift with `bunx drizzle-kit check` after applying
4. Run the tests touching the changed tables (do `/run-test`)

### 4. Prepare Rollback

> Goal: have a rollback path that actually executes

1. drizzle-kit doesn't generate down-migrations automatically — write the rollback SQL yourself or prepare a restore from backup
2. Store the rollback script alongside the migration (e.g. `migrations/rollback/<name>.sql`) or state the restore procedure in notes
3. Rename/type change → the rollback must reverse every step including data backfill
4. If rollback isn't possible (destructive + no backup) → stop and tell the user before applying

## Rules

- Production must always use `generate` + `migrate` — never `push` on a database with important data
- Review the generated SQL every time before applying — the tool may drop/create instead of alter
- Destructive changes require a backup first — no backup = no apply
- Check the version in `package.json` — v1.0 RC has `drizzle-kit up`, `push --explain`, migration folder v3
- If unsure about a command/flag → run `/learn-from-web` to check the official docs

## Expected Outcome

- Migration files generated, reviewed and applied in env order
- `drizzle-kit check` shows no drift — schema matches the database
- Rollback path is stated and testable
- Before/after reported with `/report-before-after`
