---
name: pocketbase-developing2
description: PocketBase development toolkit for project initialization, server management, migration creation, and schema iteration. Use when — (1) bootstrapping a new PocketBase project, (2) starting or stopping the dev server, (3) creating migration files, (4) writing JS hooks, or (5) looking up PocketBase Go/JS API docs.
---

# PocketBase

Covers project setup, dev server operations, migration creation, and JS hook authoring.

## Prerequisites

- Go 1.23+ on PATH

## Docs

Before writing any PocketBase code or migrations, read the relevant doc files from this skill.

See [llms-full.txt](llms-full.txt) for the full index of all 50 PocketBase documentation files. Files are in `references/pocketbase-docs/` — read them as needed. Key prefixes:

- `go-*` — Go SDK (hooks, routing, records, migrations, etc.)
- `js-*` — JS hooks and migrations
- `api-*` — REST API endpoints
- no prefix — conceptual docs (auth, collections, relations, files)

## Project Setup

### Step 1: Prompt for configuration

Ask the user for:

| Variable            | Description                | Default            |
| ------------------- | -------------------------- | ------------------ |
| `PB_PORT`           | Port for PocketBase server | `8090`             |
| `PB_ADMIN_EMAIL`    | Superuser email            | _(required)_       |
| `PB_ADMIN_PASSWORD` | Superuser password         | _(required)_       |
| `PB_MODULE_NAME`    | Go module name             | Infer from project |

### Step 2: Initialize project

Run `bash <this-skill-dir>/scripts/init.sh --agents` to get the full argument reference, then run with the values from Step 1. Do not read the script source.

### Step 3: Verify setup

```bash
go -C pb run . serve --http=0.0.0.0:<PB_PORT>
```

Expected: PocketBase starts, superuser created (from the migration), admin dashboard at `http://127.0.0.1:<PB_PORT>/_/`.

## Dev Server Commands

Always run from the project root using `go -C pb`. Never `cd` into `pb/`.

| Goal                      | Command                                              |
| ------------------------- | ---------------------------------------------------- |
| Start dev server          | `./devpb`                                            |
| Start with alternate env  | `./devpb --env=staging`                              |
| Wipe data and restart     | `rm -rf pb/pb_data && ./devpb`                       |
| Create superuser manually | `go -C pb run . superuser upsert <email> <password>` |
| Build binary              | `bash scripts/build.sh`                              |

**Automigrate**: When running via `go run`, automigrate is enabled — schema changes in the admin dashboard auto-generate JS migration files in `pb/pb_migrations/`. Commit these files.

**JS Hooks**: Add `*.pb.js` files in `pb/pb_hooks/`. They hot-reload automatically during development.

## Migration Workflow

1. Create a migration file: `pb/pb_migrations/<unix_timestamp>_<description>.js`
2. Write migration using the JS API (see JS Migration Reference below)
3. Wipe DB and restart to apply: `rm -rf pb/pb_data && go -C pb run . serve ...`
4. Verify in admin dashboard at `/_/`

Migrations run in filename order on server start. The `--reset` pattern (wipe + restart) gives a clean slate for iterating.

## JS Migration Reference

See [references/pocketbase-docs/js-migrations.md](references/pocketbase-docs/js-migrations.md) for the full JS migration API.

**Migration structure:**

```javascript
/// <reference path="../pb_data/types.d.ts" />

migrate(
  (app) => {
    // UP: apply changes
  },
  (app) => {
    // DOWN: revert changes
  },
)
```

**Field types**: `text`, `number`, `bool`, `email`, `url`, `date`, `autodate`, `select`, `file`, `relation`, `json`, `editor`, `password`, `geopoint`

**API rules**: `null` = superuser only, `""` = public, `"@request.auth.id != ''"` = auth required, `"@request.auth.id = id"` = owner only
