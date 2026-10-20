---
name: pocketbase-developing
description: Complete PocketBase development toolkit for project initialization, dev server management, migration generation, schema inspection, and migration validation. Use when — (1) bootstrapping a new PocketBase project, (2) starting or stopping the dev server, (3) resetting the database, (4) creating migration files, (5) inspecting current schema, or (6) validating migrations.
---

# PocketBase

Covers project setup, dev server operations, migration creation, schema inspection, migration validation, and JS migration API.

## Prerequisites

- Go 1.23+ installed and on PATH

## Important: Script Execution Context

**Working Directory**: Execute all commands from the user's project root (where `pb/` is or will be located). The CLI uses `$(pwd)` to locate the project.

**Script Location**: This skill bundles `scripts/pbdev.sh`. Always invoke with the full path using this skill's directory: `bash <this-skill-dir>/scripts/pbdev.sh <command>`.

> **Discovery**: Run `bash <this-skill-dir>/scripts/pbdev.sh --help` to discover all available commands and options. Do not read the script source directly; rely on the CLI help output for authoritative usage details.

**Go commands**: Always use `go -C pb` from workspace root. Never `cd` into `pb/` directly.

## Setup Steps

Follow these steps in order when setting up a new PocketBase project.

### Step 1: Prompt for Configuration

Ask the user for the following values:

| Variable            | Description                | Default            |
| ------------------- | -------------------------- | ------------------ |
| `PB_PORT`           | Port for PocketBase server | `8090`             |
| `PB_ADMIN_EMAIL`    | Superuser email            | _(required)_       |
| `PB_ADMIN_PASSWORD` | Superuser password         | _(required)_       |
| `PB_MODULE_NAME`    | Go module name             | Infer from project |

### Step 2: Initialize Project

Run `bash <this-skill-dir>/scripts/pbdev.sh init` with all four configuration values. This creates the `pb/` directory structure, writes `pb/main.go`, creates `pb/.env`, adds PocketBase entries to `.gitignore`, initializes the Go module, and installs dependencies.

### Step 3: Verify Setup

Run `bash <this-skill-dir>/scripts/pbdev.sh start --reset` to confirm everything works.

Expected outcome:

- PocketBase compiles and starts
- Superuser is created
- Server is accessible at `http://127.0.0.1:<PB_PORT>`
- Admin dashboard at `http://127.0.0.1:<PB_PORT>/_/`

## CLI Commands

All commands source `pb/.env` for `PB_PORT`, `PB_ADMIN_EMAIL`, and `PB_ADMIN_PASSWORD`.

**Note**: `<SKILL_PATH>` below represents the full path to this skill directory. All commands must be invoked from the project root directory.

**Usage**: `bash <this-skill-dir>/scripts/pbdev.sh <command> [subcommand] [options]`

### Project Management

| Command                               | Description                                                                                   |
| ------------------------------------- | --------------------------------------------------------------------------------------------- |
| `init <MODULE> <PORT> <EMAIL> <PASS>` | Full project setup: directories, `main.go`, `pb/.env`, `.gitignore`, Go module, `go mod tidy` |
| `start`                               | Stop existing instance (if running), then start the dev server in foreground                  |
| `start --reset`                       | Stop instance, wipe data, create superuser, start fresh                                       |
| `start --background`                  | Start server in background, log to `pb/server.log`, save PID to `pb/.pid`                     |
| `start --reset --background`          | Combine reset and background modes                                                            |
| `stop`                                | Kill existing PocketBase instance (checks PID file and port)                                  |

### Migration Management

| Command                                 | Description                                                           |
| --------------------------------------- | --------------------------------------------------------------------- |
| `migration create <description> [type]` | Generate timestamped migration boilerplate (type: create/modify/seed) |

### Schema Operations

| Command                       | Description                                                                     |
| ----------------------------- | ------------------------------------------------------------------------------- |
| `schema inspect [collection]` | Dump current schema as JSON (requires running server, optional collection name) |
| `schema validate`             | Dry-run all migrations in clean environment to check for errors                 |

### Utilities

| Command   | Description                                                                                              |
| --------- | -------------------------------------------------------------------------------------------------------- |
| `install` | Copy this script to `scripts/pbdev.sh` in the current project root (creates folder, overwrites existing) |
| `--help`  | Show help message with all commands and examples                                                         |

## Iteration Workflow

| Action                       | Procedure                                                                                 |
| ---------------------------- | ----------------------------------------------------------------------------------------- |
| Initialize or update Go deps | Run `bash <this-skill-dir>/scripts/pbdev.sh init` (pass module name on first run)         |
| Start server (foreground)    | Run `bash <this-skill-dir>/scripts/pbdev.sh start`                                        |
| Start server (background)    | Run `bash <this-skill-dir>/scripts/pbdev.sh start --background`                           |
| Wipe DB and restart          | Run `bash <this-skill-dir>/scripts/pbdev.sh start --reset` (add `--background` if needed) |
| Stop server                  | Run `bash <this-skill-dir>/scripts/pbdev.sh stop` (or `Ctrl+C` if running in foreground)  |
| View background server logs  | `tail -f pb/server.log` or `cat pb/server.log`                                            |

### Schema Change Loop

The recommended workflow for iterating on schema:

1. **Create migration file** — Run `bash <this-skill-dir>/scripts/pbdev.sh migration create <description> [type]`
2. **Edit migration file** in `pb/pb_migrations/` with collection definitions
3. **Validate migrations** — Run `bash <this-skill-dir>/scripts/pbdev.sh schema validate` to test migrations in clean environment
4. **Start server** — Run `bash <this-skill-dir>/scripts/pbdev.sh start --reset` to wipe DB and apply all migrations
5. **Verify** — Check admin dashboard at `/_/` or inspect schema with `pbdev.sh schema inspect`

Migrations run automatically on server start. The `--reset` flag gives a clean slate every time, so you can freely edit migration files and re-test.

**Alternative: Quick validation** — Use `pbdev.sh schema validate` to test migrations without starting the server. This is faster for catching syntax errors and migration issues.

### Automigrate (Dashboard Mode)

When running via `go run` (which `pbdev.sh start` uses), `Automigrate` is enabled. Changes made in the admin dashboard (`/_/`) automatically generate JS migration files in `pb_migrations/`. Commit these files to version control.

### Hooks

Add JS hooks in `pb/pb_hooks/` using the `*.pb.js` naming pattern. They hot-reload automatically during development.

## Docs Lookup

PocketBase API docs are indexed in a local SQLite DB. **Before writing any PocketBase code or migrations, search the docs for the relevant API.**

```bash
# Search (FTS — no embeddings)
agent-docs-search --db <this-skill-dir>/dbs/pocketbase.db search "your query" --corpus pocketbase

# Browse a file's headings
agent-docs-search --db <this-skill-dir>/dbs/pocketbase.db outline "go-records.md" --corpus pocketbase

# Fetch a chunk by ID (from search results)
agent-docs-search --db <this-skill-dir>/dbs/pocketbase.db chunk <id>

# List all 50 indexed files
agent-docs-search --db <this-skill-dir>/dbs/pocketbase.db files --corpus pocketbase
```

Useful file prefixes: `go-*` (Go SDK), `js-*` (JS hooks/migrations), `api-*` (REST API), no prefix (concepts).

## JS Migration Reference

For the full JS migration API — collection creation, auth collections, modification, relations, seeding, raw SQL, field types, and API rules — see [references/migrations.md](references/migrations.md).
