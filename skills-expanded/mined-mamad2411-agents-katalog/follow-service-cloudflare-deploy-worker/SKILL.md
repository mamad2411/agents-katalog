---
name: follow-service-cloudflare-deploy-worker
description: Deploy a Worker to staging→production with verify and rollback path
argument-hint: "[scope]"
related:
  - follow-service-cloudflare
  - resolve-errors
  - report
---


## Goal

Deploy the Worker to Cloudflare until it is live and verified — deploy staging before production with a rollback path

## Scope

- Covers: `wrangler deploy`, `--env <name>`, `wrangler deployments list`, post-deploy smoke test
- If the deploy target is not a single Worker (Pages, framework, CI pipeline) → use `/deploy-to-cloudflare` instead
- Prerequisites: auth ready (`workflows/setup-wrangler`), config/bindings complete (`workflows/config-bindings`)

## Execute

### 1. Pre-Deploy Checks

> Goal: Ready for a real deploy before acting

1. Run `wrangler whoami` to confirm the account — CI uses `CLOUDFLARE_API_TOKEN` via `/follow-secret-manager`
2. Do `/run-check` — lint/typecheck/tests must pass
3. Run `wrangler deploy --dry-run` to validate config and bundle
4. Confirm secrets are complete with `wrangler secret list`

### 2. Deploy Staging

> Goal: Verify on staging before production

1. Run `wrangler deploy --env staging`
2. Capture the deployment URL and version id from the output
3. Smoke test the real endpoint with `curl` or a browser — it must return the expected response
4. If it fails → `/resolve-errors` max 3 rounds, then stop and report

### 3. Deploy Production

> Goal: Production live safely

1. Confirm with the user before deploying to production
2. Run `wrangler deploy` (or `wrangler deploy --env production` when using a named env)
3. Capture the deployment URL and version id

### 4. Post-Deploy Verify

> Goal: Production really works

1. Run `wrangler deployments list` to see the active deployment and version history
2. Smoke test the production URL — health endpoint and critical routes
3. Check logs briefly with `wrangler tail` to confirm no errors
4. If it fails → roll back to the previous version (`wrangler rollback` or redeploy the previous version — see official docs), then report
5. Success → report the URL + version, then `/suggest-next-action`

## Rules

### 1. Staging First

- Always deploy staging and verify before production
- Production deploy requires user confirm

### 2. Keep Evidence

- Capture URL + version id for every deployment
- Use `wrangler deployments list` as the source of truth for deploy status

### 3. Rollback Ready

- Identify the previous version to roll back to before a production deploy
- If unsure about the rollback command → check official docs

## Expected Outcome

- Worker live on production with URL + version id
- Smoke tests pass and logs are clean
- Rollback path ready if needed

