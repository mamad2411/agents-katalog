---
name: quacker-ops
description: >-
  Operational playbook for the Quacker agent-operated repo: bootstrap, verify,
  deploy, Supabase migrations, secret propagation, and user gate unblocking.
---

# Quacker Ops

Use when operating, deploying, or debugging the Quacker codebase.

## System requirements

```bash
yarn check:requirements
```

Full list: [`docs/system-requirements.md`](../../docs/system-requirements.md). Agent also checks MCP servers `plugin-supabase-supabase` and `plugin-vercel-vercel` via GetMcpTools.

| Missing | User action |
| ------- | ----------- |
| `gh` | `brew install gh && gh auth login` |
| Supabase CLI | `brew install supabase/tap/supabase` or Supabase Cursor Plugin |
| Vercel deploy | Vercel Cursor Plugin or `VERCEL_TOKEN` + `npx vercel` |
| Playwright hang | Install Chrome; see `.cursor/rules/playwright-chrome.mdc` |
| Local supabase start | Docker optional — use remote Supabase instead |

## Bootstrap

```bash
yarn bootstrap   # scripts/bootstrap.sh
```

Creates `.env.local` from `.env.example` if missing. Starts local Supabase when CLI is available.

## Verify (definition of done)

```bash
yarn verify      # scripts/verify.sh
```

Runs lint, build, vitest, playwright. Must pass before marking work complete.

## Deploy

```bash
yarn deploy      # scripts/deploy.sh
```

Requires in `.env.local`: dev vars for verify; `*_PROD` + `VERCEL_TOKEN` for deploy.

```bash
yarn sync:vercel-env   # Preview → dev; Production → prod
yarn deploy            # prod Supabase + Vercel production only
```

See [`docs/environments.md`](../../docs/environments.md).

## Secret propagation (from `.env.local`)

```bash
gh secret set SUPABASE_ACCESS_TOKEN < <(grep SUPABASE_ACCESS_TOKEN .env.local | cut -d= -f2-)
gh secret set SUPABASE_PROJECT_ID < <(grep SUPABASE_PROJECT_ID .env.local | cut -d= -f2-)
gh secret set SUPABASE_SERVICE_ROLE_KEY < <(grep SUPABASE_SERVICE_ROLE_KEY .env.local | cut -d= -f2-)
vercel env add VITE_SUPABASE_URL production
vercel env add VITE_SUPABASE_ANON_KEY production
```

## Supabase local dev

```bash
supabase start
# Studio: http://127.0.0.1:54323
# Inbucket (magic links): http://127.0.0.1:54324
```

Local anon URL/key are printed by `supabase start`. Use them in `.env.local` for local dev.

`supabase link` creates `supabase/.temp/` and `supabase/.branches/` — both gitignored. Update `.gitignore` when adding new CLI-generated paths.

## User gate unblocking

Ask the user **only** when MCP/CLI cannot proceed. Otherwise execute the setup yourself.

| Blocked | User action (only if needed) | Agent then |
| ------- | ---------------------------- | ---------- |
| MCP `needsAuth` after `mcp_auth` | Add `SUPABASE_ACCESS_TOKEN` to `.env.local` | `create_project`, migrations, keys, auth, env sync |
| No Vercel MCP / token | Add `VERCEL_TOKEN` (+ org/project IDs if unknown) | `yarn sync:vercel-env`, deploy |
| No Supabase account | Create account (one-time) | Full Supabase setup via MCP |

**Do not ask the user to:** create Supabase projects, copy API keys from the dashboard, configure auth URLs, or run `gh secret set` / `vercel env add`.

| Blocked | Agent action (no user handoff) |
| ------- | ------------------------------ |
| Need dev/prod project | `create_project` → `apply_migration` → update `.env.local` |
| Magic link redirect fails | PATCH auth config via Management API |
| Vercel env out of sync | `yarn sync:vercel-env` |

## Failure recovery

- **Migration failed**: read error, fix SQL, `supabase db reset` locally, re-run verify
- **E2e flaky on realtime**: use `expect.poll` in tests; check RLS policies
- **E2e hangs at startup (agent/local)**: Playwright uses installed Chrome (`channel: 'chrome'`), not bundled Chromium — see `.cursor/rules/playwright-chrome.mdc`
- **Build fails on types**: re-run `supabase gen types typescript --local`
