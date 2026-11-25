---
name: deploy
description: Deploy TenantFlow to staging or production on Vercel. Handles build, test gate, and Vercel deployment.
---

# Deploy

Deploys TenantFlow to the target environment.

## Usage
- `/deploy` — deploy to staging (default)
- `/deploy --prod` — deploy to production (confirms before proceeding)

## Workflow

1. **Pre-flight check** — verify no uncommitted changes, run `npm run test`
2. **Build** — run `npm run build` and confirm it succeeds
3. **Deploy to staging** — run `vercel` (deploys to preview URL)
4. **Smoke test** — verify the preview URL loads and `/api/health` returns 200
5. **If --prod**: confirm with user, then run `vercel --prod`

## Project specifics
- Staging URL: Vercel preview URL (auto-generated)
- Production URL: tenantflow.vercel.app
- Deploy command: `vercel` (staging) / `vercel --prod` (production)
- Rollback: `vercel rollback`
- Database: Railway PostgreSQL — run `/migrate` before deploying if schema changed
