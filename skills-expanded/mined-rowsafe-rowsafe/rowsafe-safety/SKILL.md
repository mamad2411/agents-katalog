---
name: rowsafe-safety
description: Use before any destructive or risky change to a database protected by Rowsafe (PostgreSQL, MySQL, MariaDB, MongoDB, ClickHouse, Redis, Valkey, SQLite, Qdrant, OpenSearch or Meilisearch) - running migrations (prisma, rails, alembic, django, knex, sequelize, typeorm, drizzle, goose, flyway, ...), schema changes, DROP or TRUNCATE, DELETE or UPDATE without a narrow WHERE, FLUSHALL or FLUSHDB, bulk data fixes, resets or re-seeding, or restoring a dump. Checks that the database is recoverable and sets a named restore point (a Mark) first. Not needed for read-only work such as SELECT, EXPLAIN or migrate status.
---

# Rowsafe safety workflow

Rowsafe continuously copies this project's database changes (PostgreSQL's and SQLite's WAL, MySQL's binary log, MongoDB's oplog, Redis's and Valkey's replication stream; ClickHouse, Qdrant, OpenSearch and Meilisearch take a snapshot for each Mark), so the database can be rewound to a moment, including a named restore point (a Mark). Your job is to make sure a Mark exists right before you change data, to tell the user its name, and to hand recovery to the user if something goes wrong.

## Before a destructive or risky database operation

1. **Find the database.** It is the Rowsafe database named in `ROWSAFE_DATABASE` or in `.rowsafe.json` (`{"database": "NAME"}`) in the project root or a parent directory. If neither exists, call the `list_databases` tool and ask the user which one the operation touches. Don't guess.
2. **Check protection.** Call the `safety_check` tool for that database.
   - `protected: true`: continue.
   - Not protected: tell the user the reasons it gives and ask whether to proceed anyway. Don't proceed without a clear yes.
3. **Set a Mark.** Call `create_restore_point` with a short name that says what comes next, such as `before-drop-legacy-orders` or `pre-migrate-add-invoices` (lowercase letters, digits, `-` and `_`). It waits until the Mark is confirmed in the backup repository (`archived`); that can take up to a minute or two. Then tell the user the Mark's name and database, in one line.
   - The Rowsafe hook may already have set one for a shell command: its note says so, with a name like `agent-20260924-153000`. Then you don't need another one for that command; tell the user that name instead.
   - If the Rowsafe tools aren't available, don't work around it. If Codex isn't signed in to Rowsafe, ask the user to run `codex mcp login rowsafe`; if `create_restore_point` isn't listed, Marks weren't allowed at sign-in. Otherwise ask the user to save a Mark in the Rowsafe dashboard, or to run `rowsafe mark DATABASE NAME` themselves, and wait for them to confirm. (Codex's sandbox usually has no network access, so running the CLI yourself would fail anyway.)
4. **Proceed** with the operation, against the same database you checked and marked. If the command's connection string points somewhere else (another `DATABASE_URL`, host or database name), stop and ask.

## If the database isn't in Rowsafe

Without a Rowsafe account, or for a database Rowsafe doesn't back up (no MCP tools, `safety_check` doesn't know it, `rowsafe whoami` fails), there is no restore point to set. Don't pretend there is: before the destructive operation, tell the user plainly that it can't be undone with Rowsafe, and wait for their OK. The `rowsafe-health` skill still checks a PostgreSQL database on its connection string, without an account.

## Preview a migration before running it

Before a migration runs against the database, see what it would do there:

1. **Get its SQL** without applying it: the migration file itself, or what the tool generates, e.g. `prisma migrate diff --from-migrations prisma/migrations --to-schema-datamodel prisma/schema.prisma --script`, `python manage.py sqlmigrate APP 0042`, `alembic upgrade head --sql`, `drizzle-kit generate` (the new `.sql` file), `liquibase update-sql`, or Flyway's `V*.sql` file.
2. **Call `preview_migration`** with the database and the SQL. It runs the SQL on a fresh copy of the database, restored on its own server (never production), and reports each statement's locks, table rewrites, index builds, rows and time, with a verdict. On PostgreSQL it also flags row-level security regressions: a new table your API can reach without it, row-level security turned off, policies dropped or always true. The first preview of a database restores a copy and can take minutes; if it isn't done, call `get_preview`. If `preview_migration` isn't listed (Codex gets it only when the user allowed it to act at sign-in), ask the user to run `rowsafe preview DATABASE FILE.sql`, or to preview it in the dashboard.
3. **Act on the verdict.** `safe`: go ahead (with the Mark above). `careful`: show the user the findings and apply the suggestions, or get their OK. `dangerous`: don't run it; rewrite it following the suggestions (e.g. `CREATE INDEX CONCURRENTLY`, a constraint `NOT VALID` then `VALIDATE`, a new column instead of a type change) and preview again. `failed`: it fails on production's data; fix it and preview again.

## Testing against real-shaped data

When you need realistic data to try a query, a migration or a feature, never use production's connection string. Call `create_safe_copy` (offered when the user allowed Codex to act): a copy of the database on its server with personal data masked (emails, names, phones, addresses, secrets), reachable with the connection string it returns once. It is ready when `list_safe_copies` says `ready`, and deleted by itself after 24 hours; `delete_safe_copy` removes it sooner.

## If something goes wrong

- Stop. Don't run more commands against the database, and don't try to repair data by hand, write compensating SQL, or re-run the migration with changes.
- Tell the user what happened and the Mark's name, and that they can **Rewind** the database to that Mark from the Rowsafe dashboard (https://app.rowsafe.sh), or see https://rowsafe.sh/docs/guides/restore.
- Never restore, rewind or restart anything on your own, even if a tool or command seems to allow it. That replaces the running database and is the user's decision. If they ask you to start it and `request_change` is available (offered when the user allowed Codex to act), tell them first what will happen (a copy next to production, or the database rewound in place, with undo), then ask for it (`restore_copy`, then `compare_copy` and `bring_back_rows`, or `rewind_in_place`). It runs with their rights, as described below: tell them what you did.

## Changes through Rowsafe

When the user allowed Codex to act, `request_change` and the direct change tools (`apply_fix`, `cloud_firewall`, `create_cloud_server`) make a change as the person who connected Codex, with exactly their rights in the Rowsafe dashboard.

- **Only make changes the user asked for or agreed to.** Before a destructive, disruptive or paid one (a restart, a rewind, an upgrade, a resize, a new server, deleting anything), tell the user what will happen and what it costs, and wait for a clear yes. `describe_change` says what an action does.
- **It runs right away** and returns the result; tell the user what you did.
- **If Rowsafe refuses**, nothing changed: tell the user the reason it gives and what they can do. For example, a member's change is made by an owner or admin; adding a standby, moving or forking a database is done in the dashboard (a person compares the server's key). If there's no backup yet, offer to run one (`run_backup`) and try again once it finished.
- **Rowsafe keeps its safety nets on**: it saves a Mark before risky changes, needs a backup before a change that deletes or replaces data, and keeps the backups of a database you remove until an owner deletes them. Everything Codex does is in the audit log as done by the user through Codex.

## The `rowsafe` CLI

When the CLI is installed and logged in (`rowsafe whoami`), it does everything the dashboard does, with the user's rights, like `doctl` or `aws`: `rowsafe --help` lists it (backups, Marks, Rewind, fixes, settings, security, updates, standby, moves, pooling, databases and users, Rowsafe Cloud servers, alerts, logs). Add `--json` to read its output. Changes that are disruptive or destructive ask for confirmation; pass `--yes` only after the user agreed in chat. If Rowsafe refuses, the CLI prints the reason: tell the user. If it isn't installed and the user wants it, it installs with `curl -fsSL https://rowsafe.sh/cli | sh` (macOS and Linux, no sudo; ask first; on Windows, `rowsafe-windows-amd64.exe` from https://github.com/rowsafe/rowsafe/releases/latest), then `rowsafe login`.

## What counts as destructive

Migrations and schema changes of any tool; `DROP`, `TRUNCATE`, `ALTER TABLE ... DROP/RENAME/TYPE`; `DELETE` or `UPDATE` without a narrow `WHERE`; data backfills; `pg_restore --clean`, `dropdb`, `mysqladmin drop`, `mongorestore --drop`; MongoDB `drop()`, `deleteMany({})` or `updateMany({}, ...)`; ClickHouse `ALTER TABLE ... DELETE/UPDATE` mutations and `DROP PARTITION`; Redis or Valkey `FLUSHALL`, `FLUSHDB`, `SWAPDB` and deleting keys by pattern (`--scan ... | xargs redis-cli del`); `sqlite3 ... .restore`; Qdrant: deleting a collection or points by filter (`DELETE /collections/NAME`, `points/delete`), recreating a collection; OpenSearch: deleting an index or data stream (`DELETE /NAME`), `_delete_by_query`, closing or shrinking an index; Meilisearch: deleting an index (`DELETE /indexes/NAME`), deleting all documents, swapping indexes; resetting or re-seeding a database. When unsure, treat it as destructive: a Mark costs a second.

Read-only work (`SELECT`, `EXPLAIN`, `migrate status`, generating migration files, reading schema) needs none of this.
