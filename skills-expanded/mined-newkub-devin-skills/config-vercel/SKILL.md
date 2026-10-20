---
name: follow-service-vercel-config-vercel
description: Set/edit Vercel configuration — environment variables and `vercel.json` (rewrites, headers, functions, crons) — without clobbering existing settings
related:
  - follow-service-vercel
---

## Goal

Set/edit Vercel configuration — environment variables and `vercel.json` (rewrites, headers, functions, crons) — without clobbering existing settings

## Scope

- Covers `vercel.json`, `vercel env`, and project settings
- If the project is not linked yet → do `workflows/setup-vercel/SKILL.md` first
- Real deploy → `/deploy-to-vercel`

## Execute

### 1. Read Current Config

> Goal: Know the current config before editing

1. Read `vercel.json`, `.vercel/project.json`, and existing env files
2. Run `bunx vercel pull` to sync the latest project settings from the dashboard
3. Do `/deep-review-codebase` domain `review-config` or `/report-config-files` if drift must be known

### 2. Configure Environment Variables

> Goal: env vars correct per environment

1. Add a key with `bunx vercel env add KEY_NAME` — pick the environment (production/preview/development)
2. Sync to local with `bunx vercel env pull .env.local`
3. secrets → `/follow-secret-manager` first, then push up to Vercel — never put them in `vercel.json`

### 3. Configure vercel.json

> Goal: config file correct per schema

1. Edit only the necessary keys in `vercel.json` — merge with the existing one, never overwrite the whole file
2. Commonly used keys: `rewrites`, `redirects`, `headers`, `functions`, `crons`, `regions`, `ignoreCommand`
3. Set `buildCommand`/`outputDirectory` only when framework detection is wrong — see official docs https://vercel.com/docs/projects/project-configuration

### 4. Verify

> Goal: config works for real before deploy

1. Run `bunx vercel build` to check the config builds locally
2. Do `/run-verify` for lint, typecheck
3. If broken → revert the key just changed, then report the diff with `/report-before-after`

## Rules

- Never put secrets in `vercel.json` or commit `.env.local`
- Edit config incrementally — change one key then verify
- Every added env var must clearly state its target environment

## Expected Outcome

- env vars synced correctly between local and Vercel
- `vercel.json` passes schema and `vercel build` succeeds
- ready to deploy with `/deploy-to-vercel`
