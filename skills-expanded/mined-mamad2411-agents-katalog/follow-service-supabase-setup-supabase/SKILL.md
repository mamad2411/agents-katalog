---
name: follow-service-supabase-setup-supabase
description: Install the Supabase CLI, create the local project, link it to the remote project, and init the `@supabase/supabase-js` client ready to use — first-time setup only
related:
  - follow-service-supabase
---

## Goal

Install the Supabase CLI, create the local project, link it to the remote project, and init the `@supabase/supabase-js` client ready to use — first-time setup only

## Scope

- Install and authenticate the Supabase CLI
- `supabase init`, `supabase link`, `supabase start` for local development
- Create the client from env vars
- Does not cover advanced env/RLS/config → use `workflows/config-supabase/SKILL.md`

## Execute

### 1. Check Prerequisites

> Goal: Confirm prerequisites before installing (idempotent)

1. Read `package.json` to identify the package manager (`bun`, `npm`, `pnpm`)
2. Check whether `supabase/config.toml` or a `supabase/` directory already exists → if so, skip to verify
3. Check Docker for the local stack — if absent → stop and tell the user to install it
4. If there is no Supabase account/project → stop and tell the user to create one from the dashboard

### 2. Install And Authenticate CLI

> Goal: Install and log in the Supabase CLI

1. Install the CLI with `bun add -D supabase` or the system package manager (`brew`, `scoop`)
2. Check the version with `supabase --version`
3. Log in with `supabase login` or set `SUPABASE_ACCESS_TOKEN` for CI
4. Confirm authentication with `supabase projects list`

### 3. Initialize And Link Project

> Goal: Create the local project and connect it to remote

1. Initialize with `supabase init` → creates `supabase/config.toml`
2. Link remote with `supabase link --project-ref <project-ref>`
3. Start the local stack with `supabase start`
4. Run `supabase status` to read the local `API URL`, `anon key`, `service_role key`

### 4. Install Client And Verify

> Goal: Create a client that reads from env and test the connection

1. Install the client SDK with `bun add @supabase/supabase-js`
2. Store `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` in `/follow-secret-manager`, then inject them into `.env`
3. Create the client with `createClient(url, anonKey)` in `src/lib/supabase.ts` (or a suitable path)
4. Do `/run-verify` and test a basic query — if it fails → do `resolve-errors` max 3 rounds

## Rules

- Use `supabase/config.toml` as the single source of truth
- Never hardcode keys or commit secrets — always use `/follow-secret-manager`
- `SUPABASE_SERVICE_ROLE_KEY` is server-side only — never expose it to the client
- If unsure about a command/API → check official docs or do `learn` (web) first
- When done, do `/suggest-next-action`

## Expected Outcome

- Supabase CLI installed, logged in, and project linked successfully
- Local stack runs and `supabase status` shows all values
- Client ready to use and a query passes verify
