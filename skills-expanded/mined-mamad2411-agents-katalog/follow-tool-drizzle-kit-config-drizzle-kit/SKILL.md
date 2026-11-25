---
name: follow-tool-drizzle-kit-config-drizzle-kit
description: Configure `drizzle.config.ts` — dialect, schema path, dbCredentials, out dir
argument-hint: "[scope]"
related:
  - run-drizzle-studio
  - run-verify
  - follow-secret-manager
---

## Goal

Configure `drizzle.config.ts` correctly — `dialect`, `schema`, `out`, `dbCredentials` — so generate/migrate/push work

## Scope

Use when creating/editing the drizzle-kit config — the migration workflow lives in `workflows/migrate-schema/SKILL.md`

## Execute

### 1. Read Current Config

> Goal: read the existing config before editing

1. Find `drizzle.config.ts` (or `.js`/`.json`) at the root — record the current keys
2. Identify the schema entrypoint — e.g. `./src/db/schema.ts` or the glob `./src/**/schema.ts` for multi-file
3. No config → create `drizzle.config.ts` at the root

### 2. Core Options

> Goal: set the main keys

1. Use `defineConfig` from `drizzle-kit` — type safety
2. `dialect` — `"postgresql"`, `"mysql"`, `"sqlite"`, `"turso"` etc. matching the real database (check official docs for dialect names)
3. `schema` — path/glob to the schema files
4. `out` — directory for generated migrations, e.g. `"./drizzle"` or `"./migrations"`
5. `dbCredentials` — `url` or dialect-specific fields (host/port/user/database) — always read from env vars (`process.env.DATABASE_URL!`), never hard-code

### 3. Additional Options

> Goal: set extra options as needed

1. `strict`/`verbose` — for generate/push safety and logging
2. `tablesFilter` — limit which tables drizzle-kit manages
3. `migrations` options — prefix/table settings when needed (see official docs)
4. Multiple databases/configs → create multiple config files and select with `--config=<path>`

### 4. Verify

> Goal: check the config works

1. Run `bunx drizzle-kit generate` on an unchanged schema — the config must parse (it may report no changes)
2. Or `bunx drizzle-kit check` to verify migration consistency when migrations already exist
3. Run `bunx drizzle-kit studio` or `/run-drizzle-studio` to confirm dbCredentials actually connect (when the DB is available)
4. If it breaks → revert the edited keys and report the diff

## Rules

### 1. Config Discipline

- always `defineConfig`; merge with the existing config, never overwrite
- `dbCredentials` from env only — use `/follow-secret-manager` for secrets
- the `schema` path must match the real entrypoint — a wrong glob = wrong/empty generate

### 2. Dialect

- `dialect` must match the real database — wrong = every SQL in the wrong dialect
- unsure about a key name → check the official docs — never guess

### 3. Multi-Config

- multiple DBs → multiple config files + the `--config` flag — never cram everything into one config

- Use /follow-secret-manager if needed
- Use /run-drizzle-studio if needed

## Expected Outcome

- `drizzle.config.ts` is correct — dialect/schema/out/dbCredentials match reality
- `drizzle-kit` commands parse the config and work
- Credentials stay safe via env vars
