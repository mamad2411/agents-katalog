---
name: rowsafe-health
description: Use when the user asks whether a PostgreSQL database is healthy, why it is slow, which queries take the most time, what is running or stuck right now, which tables or indexes are bloated or unused, or how its settings should be tuned. Works with or without a Rowsafe account, on a connection string (or DATABASE_URL), with the rowsafe CLI.
---

# Database health with Rowsafe

The `rowsafe` CLI checks a PostgreSQL database and says what to fix, in plain language. It needs no Rowsafe account: give it a connection string. Reads are read-only, with short timeouts, and nothing is sent to Rowsafe.

## Which database

- Logged in to Rowsafe (`rowsafe whoami` succeeds) and the project names its database (`.rowsafe.json` or `ROWSAFE_DATABASE`): use `rowsafe pulse` and the commands below without a connection string, or the MCP tools (`database_health`, ...).
- Otherwise, pass the connection string the app uses, e.g. `DATABASE_URL` from `.env`: `rowsafe pulse "postgres://..."`. When not logged in, the CLI also reads `DATABASE_URL` from the environment. Passwords can also come from `PGPASSWORD` or `~/.pgpass`. Never print a password back to the user.
- Without an account, only PostgreSQL works. If it is another engine, say so.

Codex's sandbox usually has no network access. If the CLI can't reach the database (or `rowsafe.sh`), ask the user to let the command run with network access, or to run it themselves; don't work around the sandbox.

## Commands

Add `--json` when you read the output yourself.

- `rowsafe pulse CONN`: health score 0-100 and findings, each with what to do. Exit status 3 below 70.
- `rowsafe insights CONN`: largest tables, unused and duplicate indexes, bloat, vacuum.
- `rowsafe top CONN`: the queries that took the most time (needs `pg_stat_statements`).
- `rowsafe activity CONN`: queries running, or idle in a transaction, for over a minute.
- `rowsafe settings CONN`: the settings that matter. `rowsafe tune CONN --memory 16GB --cpus 4 --workload web` suggests settings that suit the server (Rowsafe can't see another server's memory over a connection: ask the user).
- `rowsafe help local` lists them all.

## Fixes

`rowsafe fix CONN` lists what pulse can fix (clean up tables, end a stuck session, drop an unused or duplicate index, tune settings). A fix changes production: tell the user what it does and get a clear yes in chat first, then run `rowsafe fix CONN NUMBER --yes`. `rowsafe tune CONN ... --yes` applies settings with `ALTER SYSTEM` and a reload (nothing restarts); same rule. Never run either just because a finding exists.

## What it can't do without an account

There are no backups, restore points (Marks) or restore tests without the Rowsafe agent on the database server. Before a destructive change on a database that isn't in Rowsafe, tell the user it can't be undone with Rowsafe. If they want that safety net, Rowsafe's agent runs on their own server and backs up to their own bucket: https://rowsafe.sh (then the `rowsafe-safety` skill applies).

## Installing the CLI

If `rowsafe` isn't installed, ask the user first, then: `curl -fsSL https://rowsafe.sh/cli | sh` on macOS and Linux (no sudo). On Windows, download `rowsafe-windows-amd64.exe` (or `-arm64.exe`) from https://github.com/rowsafe/rowsafe/releases/latest and run it as `rowsafe.exe`.
