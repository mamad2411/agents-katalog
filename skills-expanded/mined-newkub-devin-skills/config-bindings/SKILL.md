---
name: follow-service-cloudflare-config-bindings
description: Set/edit bindings and environments in wrangler config (KV, R2, D1, Durable Objects, vars)
argument-hint: "[scope]"
related:
  - follow-service-cloudflare
  - resolve-errors
  - report
---


## Goal

Set/edit bindings and environments in `wrangler.toml`/`wrangler.jsonc` so the Worker connects KV, R2, D1, Durable Objects, and vars correctly without clobbering the existing config

## Scope

- Covers: `kv_namespaces`, `r2_buckets`, `d1_databases`, `durable_objects`, `vars`, `env.<name>` environments
- Does not cover: install/auth (use `workflows/setup-wrangler`), deploy (use `workflows/deploy-worker`)

## Execute

### 1. Read Current Config

> Goal: Understand the existing config before editing

1. Read the existing `wrangler.toml` or `wrangler.jsonc` — if not found → do `workflows/setup-wrangler` or `wrangler init` first
2. Do `/deep-review-codebase` domain `review-config` if the config is suspected to mismatch real resources
3. Identify the bindings to add/edit from the argument or code usage (`env.MY_KV`, etc.)

### 2. Provision Resources

> Goal: Create resources on Cloudflare before binding

1. KV: `wrangler kv namespace create <NAME>` — keep the returned `id`
2. R2: `wrangler r2 bucket create <NAME>`
3. D1: `wrangler d1 create <NAME>` — keep the returned `database_id`
4. If the resource already exists → list to find the id (`wrangler kv namespace list`, `wrangler r2 bucket list`, `wrangler d1 list`)

### 3. Add Bindings

> Goal: Merge bindings into config without removing existing ones

1. Add only the necessary keys in the config:
   - KV → `[[kv_namespaces]]` with `binding`, `id`
   - R2 → `[[r2_buckets]]` with `binding`, `bucket_name`
   - D1 → `[[d1_databases]]` with `binding`, `database_name`, `database_id`
   - Durable Objects → `[[durable_objects.bindings]]` with `name`, `class_name` plus `[[migrations]]` for new classes
   - vars → `[vars]` for non-secret values
2. The binding name must match what the code references via `env.*`
3. Never put secrets in `vars` — use `wrangler secret put` via `/follow-secret-manager`
4. If unsure about the schema → check official docs via `/learn-from-web` or `/use-wrangler`

### 4. Configure Environments

> Goal: Separate staging/production with `env.*`

1. Add `[env.staging]` / `[env.production]` (or `env.staging` in jsonc)
2. Each env must have its own bindings — top-level bindings are not inherited into named environments
3. Provision separate resources per env (e.g. `CACHE-staging`, `CACHE-production`)

### 5. Verify

> Goal: Config valid and types matching

1. Run `wrangler types` to regenerate the `Env` interface
2. Run `wrangler deploy --dry-run` to validate the config without deploying
3. If needed → run `wrangler dev` to smoke test the real bindings
4. If broken → revert the key just changed then `/resolve-errors`; passes → `/report-before-after`

## Rules

### 1. Merge Not Overwrite

- Edit only the necessary keys — never rewrite the whole config
- Binding `name`/`binding` must match code usage everywhere

### 2. Secrets Separation

- Secrets → `wrangler secret put` only — never in the config
- Use `vars` only for non-secret values

### 3. Environment Isolation

- Named environments must declare their bindings completely
- Use per-env resource names for isolation

## Expected Outcome

- Bindings complete per code usage and `wrangler types` passes
- Environments correctly separate staging/production
- `wrangler deploy --dry-run` validates without clobbering the existing config

