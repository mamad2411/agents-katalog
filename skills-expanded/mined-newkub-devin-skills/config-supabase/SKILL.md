---
name: follow-service-supabase-config-supabase
description: Set/edit Supabase configuration — env vars, `supabase/config.toml`, RLS policies, and client options — without overwriting the existing config
related:
  - follow-service-supabase
---

## Goal

Set/edit Supabase configuration — env vars, `supabase/config.toml`, RLS policies, and client options — without overwriting the existing config

## Scope

- Manage env vars (`SUPABASE_URL`, keys) via a secret manager
- Edit `supabase/config.toml` (auth, storage, edge runtime)
- Enable/edit RLS policies on tables
- Does not cover first-time install → use `workflows/setup-supabase/SKILL.md`

## Execute

### 1. Read Current Config

> Goal: Know the current config state before editing

1. Read the existing `supabase/config.toml` and `.env*`
2. Do `/check-secrets env-vars` to identify missing or duplicated vars
3. Do `/deep-review-codebase` domain `review-config` if the local config is suspected to differ from remote
4. If there is no `supabase/config.toml` at all → do `workflows/setup-supabase/SKILL.md` instead

### 2. Configure Env Vars

> Goal: Set environment variables completely and securely

1. Define `SUPABASE_URL` and `SUPABASE_ANON_KEY` for the client (public)
2. Define `SUPABASE_SERVICE_ROLE_KEY` for server-side only — store it in `/follow-secret-manager`
3. Use the `NEXT_PUBLIC_`/`VITE_` prefix per framework for values exposed to the client
4. Never edit the existing config unnecessarily — merge only the needed keys

### 3. Configure Auth And Services

> Goal: Edit only the needed `config.toml` sections

1. Edit the `[auth]` section — `site_url`, `additional_redirect_urls`, providers per use
2. Edit `[storage]`, `[edge_runtime]`, or other sections only for the necessary keys
3. Reference the parent's `references/supabase-config.md` or official docs for key names

### 4. Configure RLS And Client Options

> Goal: Guard data access and set client options correctly

1. Enable RLS on every table exposed via the API — `alter table <name> enable row level security`
2. Create policies with `create policy` through a migration, not by editing the dashboard directly
3. Set client options such as `auth: { persistSession, autoRefreshToken }` per the use case
4. Run `supabase db diff` before push to review changes

### 5. Verify

> Goal: Confirm the new config works

1. Run `supabase start`/`supabase status` to confirm the local stack picks up the new config
2. Do `/run-verify` and test a basic query/auth flow
3. If it fails → revert the keys just changed, do `resolve-errors` max 3 rounds, then report the diff

## Rules

- Merge with the existing config — never overwrite the whole `config.toml`
- Secrets only through `/follow-secret-manager` — never put them in `config.toml` or commit
- Every table the client accesses must have RLS enabled + explicit policies
- Test the config locally before pushing to remote
- If unsure about a key name/option → check official docs or `learn` (web)

## Expected Outcome

- Env vars complete, secure, and clearly separated client vs server
- `config.toml` merged without clobbering existing settings
- RLS enabled with policies delivered via migration
- Verify passes and a short before/after report is produced
