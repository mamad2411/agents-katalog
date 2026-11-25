---
name: migrations-overview
description: Use when picking or operating a schema migration tool — covers Alembic, sqlx, Atlas, goose, Drizzle, Prisma.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: database
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [postgres, orm-overview, sql]
---

# Migrations Overview

**Iron Law: migrations are forward-only in production. Pick one tool per project and stick with it.**

"Down" migrations are a development convenience. In production you fix forward — write a new migration that undoes the broken one. Anyone who tells you otherwise has never run a `down` against a 2 TB table at 3am.

## Tool comparison

| Tool                          | Language | Style                                | Schema source-of-truth    | Pick when                                     |
| ----------------------------- | -------- | ------------------------------------ | ------------------------- | --------------------------------------------- |
| **Alembic**                   | Python   | imperative (autogen from SQLAlchemy) | ORM models                | Python app with SQLAlchemy                    |
| **sqlx-cli**                  | Rust     | imperative SQL files                 | the migration files       | Rust + `sqlx`; minimal magic                  |
| **Atlas**                     | any      | declarative (HCL) **or** versioned   | declared schema (HCL/SQL) | Polyglot orgs, GitOps schemas, CI diff guards |
| **goose**                     | Go       | imperative SQL or Go funcs           | the migration files       | Go app, want plain SQL, simple binary         |
| **Drizzle** (`drizzle-kit`)   | TS       | declarative (generates SQL diffs)    | TS schema definitions     | TS app already using Drizzle ORM              |
| **Prisma** (`prisma migrate`) | TS       | declarative (Prisma schema → SQL)    | `schema.prisma`           | TS app already using Prisma                   |

## Alembic (Python)

```bash
alembic revision --autogenerate -m "add user.email_lower"
alembic upgrade head
```

- **Strength**: autogen from SQLAlchemy models catches most changes. Branch/merge supported.
- **Weakness**: autogen misses CHECK constraints, server defaults, enum changes, partial-index conditions. **Always diff the generated file** before commit.
- Stamp existing DBs with `alembic stamp head`. Set `compare_type = True` and `compare_server_default = True` in `env.py` or you'll miss column changes.

## sqlx-cli (Rust)

```bash
sqlx migrate add -r create_users      # creates timestamp_create_users.sql
sqlx migrate run
```

- **Strength**: dead simple. Files are SQL. Tracked via `_sqlx_migrations` table. Compile-time query checks via `sqlx::query!` work against the migrated schema.
- **Weakness**: no autogen. You write every line. No drift detection.
- Use `-r` to create reversible (up + down) pairs only in dev. Prod: forward-only.

## Atlas (any language)

```bash
atlas schema apply --to file://schema.sql --url $DATABASE_URL --dev-url $DEV_DB
atlas migrate diff add_users --to file://schema.sql --dev-url $DEV_DB
```

- **Strength**: declarative — write what the schema _should be_, Atlas diffs against live and generates the migration. CI lint (`atlas migrate lint`) catches destructive changes, missing concurrent index, blocking DDL. GitOps-friendly.
- **Weakness**: extra moving piece (the "dev DB" for diff). Steeper learning curve. HCL is another DSL.
- **Use Atlas Lint in CI** — catches `DROP COLUMN`, non-`CONCURRENTLY` index creation on live tables, statements that take `ACCESS EXCLUSIVE` lock for long periods.

## goose (Go)

```bash
goose -dir migrations create add_users sql
goose -dir migrations postgres "$DATABASE_URL" up
```

- **Strength**: single Go binary, embed migrations in your app (`embed.FS`), run on startup if you want. SQL or Go-function migrations.
- **Weakness**: no autogen, no schema diff. You write everything.
- `-- +goose Up` / `-- +goose Down` markers in SQL files. `-- +goose StatementBegin` / `End` for multi-statement migrations (functions, DO blocks).

## Drizzle (TS)

```bash
pnpm drizzle-kit generate           # diff TS schema → SQL migration
pnpm drizzle-kit migrate            # apply
```

- **Strength**: schema is TS — same source-of-truth as your queries. Generated SQL is plain SQL you commit and read.
- **Weakness**: generation occasionally produces wrong diffs (column renames as drop+add). **Read the generated SQL.** Rename handling has improved but still review.
- `drizzle-kit push` for dev — directly syncs without a migration file. Never use in prod.

## Prisma (TS)

```bash
pnpm prisma migrate dev --name add_users      # dev: generate + apply
pnpm prisma migrate deploy                    # prod: apply only
```

- **Strength**: `schema.prisma` is concise; great DX for greenfield TS apps. Migrate has resolve workflow for drift.
- **Weakness**: Prisma controls the schema dialect — features you want (partial indexes, advanced constraints, exclusion constraints) may not be expressible. Drops to raw SQL via `migrationStatements` but then you're partially-managed.
- `prisma migrate diff` is useful for CI checks even if your runtime isn't Prisma.

## Operational rules

| Rule                                                                                    | Why                                                                                                                                                                                                                                                                                                                                    |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Migrations run in CI**, not from a dev laptop                                         | Reproducibility; logged; rolled out via your deployment pipeline                                                                                                                                                                                                                                                                       |
| **One transaction per migration** where the tool supports it                            | Atomic; failed migration leaves a known state                                                                                                                                                                                                                                                                                          |
| **Postgres index changes use `CONCURRENTLY`** (and run outside transactions)            | Otherwise `CREATE INDEX` acquires `ShareLock` — reads continue, but DML (INSERT/UPDATE/DELETE) blocks for the duration. `CREATE INDEX CONCURRENTLY` and `ALTER TABLE ... ADD CONSTRAINT ... NOT VALID` / `VALIDATE CONSTRAINT` **cannot run inside a transaction** — put each in its own migration file so the tool runs it standalone |
| **Long-running data backfills are separate from DDL migrations**                        | DDL is fast; backfills can take hours — different deploy cadence                                                                                                                                                                                                                                                                       |
| **Never edit a merged migration file**                                                  | The hash changes; replicas have different history; chaos                                                                                                                                                                                                                                                                               |
| **Add nullable, backfill, then NOT NULL** for adding required columns to big tables     | Avoids blocking lock while NOT NULL is verified                                                                                                                                                                                                                                                                                        |
| **`SET lock_timeout` and `statement_timeout` at session start of the migration script** | Failed-fast beats silent-blocking-everything. Set per-session (the migration's connection), NOT in `postgresql.conf` — global values would time out legitimate application queries                                                                                                                                                     |

## Zero-downtime change patterns

| Change                           | Pattern                                                                                                                                                            |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Add column (nullable)            | `ALTER ... ADD ... NULL DEFAULT ...` — always cheap                                                                                                                |
| Add column (NOT NULL, big table) | `ALTER ... ADD ... NOT NULL DEFAULT <non-volatile-constant>` (PG 11+: no table rewrite; before PG 11 you must add nullable, backfill, then add NOT NULL via CHECK) |
| Drop column                      | Stop using it in app → deploy → drop in next migration                                                                                                             |
| Rename column                    | Add new, dual-write, backfill, swap reads, drop old (multi-deploy)                                                                                                 |
| Change type                      | Add new column, dual-write + cast, backfill, swap, drop                                                                                                            |
| Add NOT NULL                     | `ADD CONSTRAINT … CHECK (col IS NOT NULL) NOT VALID;` then `VALIDATE CONSTRAINT`                                                                                   |
| Add index                        | `CREATE INDEX CONCURRENTLY`                                                                                                                                        |
| Add FK                           | `ADD CONSTRAINT … NOT VALID;` then `VALIDATE CONSTRAINT`                                                                                                           |

## Anti-patterns

- **Down migrations as a production safety net.** They aren't one. Fix forward.
- **Multi-tool monorepos.** Alembic AND goose AND Atlas in one repo = drift, double-tracking, conflicting `_migrations` tables, doubled review burden. Pick one.
- **Hand-editing a migration file after merge.** Hash changes; replicas drift; CI passes but production fails. Write a new migration.
- **"Reversible" thinking outside test envs.** Once data is mutated, the down doesn't restore anything you care about.
- **Index changes without `CONCURRENTLY`.** `CREATE INDEX` acquires `ShareLock` — reads still work but writes block for the duration.
- **Hardcoded credentials in migration files.** Seed users with literal `password_hash` values, API keys, or test tokens in migration SQL = permanent secret-in-git. Read from secret store at run time, or document the safe-seed pattern in a runbook.
- **Migrations in the same transaction as long backfills.** Either the transaction lasts hours (locks pile up) or you split the backfill out (which you should have done).
- **Autogen without reading the diff.** Alembic, Drizzle, Prisma all miss things or generate destructive operations. Read every line.
- **Running migrations from a laptop into prod.** Use CI. Always.

## Hand-off

For ORM choice (often paired with the migration tool): `Skill(orm-overview)`. For Postgres-specific schema rules and DDL patterns: `Skill(postgres)`. For SQL constructs the migrations are generating: `Skill(sql)`.
