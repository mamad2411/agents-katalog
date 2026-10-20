---
name: follow-service-cloudflare-migrate-pages-to-workers
description: Migrate Pages → Workers (Static Assets + Worker script) with cutover/rollback
argument-hint: "[scope]"
related:
  - follow-service-cloudflare
  - resolve-errors
  - report
---


## Goal

Migrate the project from Cloudflare Pages to Workers (Static Assets + Worker script) safely — the site behaves the same and rollback is possible

## Scope

- Covers: Pages static site → Workers Static Assets, Pages Functions (`functions/`) → Worker routes, `_redirects`/`_headers`, cutover and rollback
- Never mix with feature work — one commit per migration step so it can be bisected

## Execute

### 1. Plan Migration

> Goal: Map from→to clearly before starting

1. Do `/plan`: list what Pages currently uses — static output dir, `functions/` routes, `_redirects`, `_headers`, env vars/secrets, custom domains
2. Read the official migration guide (Workers Static Assets docs) — if unsure, do `/learn` (web)
3. Write the rollback path: the original Pages project stays until cutover succeeds — revert by pointing the domain back
4. If the scope is unclear or it affects a production domain → `/ask-me`

### 2. Create Worker Config

> Goal: `wrangler.jsonc`/`wrangler.toml` for Workers + assets

1. Set `name`, `main` (worker entry), and `compatibility_date` to the current date
2. Point `assets` at the original Pages static output dir (check official docs for the latest assets config fields)
3. Move vars from Pages settings → `vars` and secrets → `wrangler secret put`
4. Run `wrangler types` after setting the config

### 3. Migrate Functions To Worker

> Goal: `functions/` handlers work inside the Worker

1. Map each `functions/<route>.ts` → a route in the Worker `fetch` handler
2. Move `context.env` bindings → the Worker's `env` — bindings must match (see `workflows/config-bindings`)
3. Convert `_redirects`/`_headers` → logic in the Worker or assets config per official docs
4. Test locally with `wrangler dev` for every migrated route
5. If routes fail → `/resolve-errors`

### 4. Deploy And Verify

> Goal: The new Worker is live and compared against the original Pages

1. Deploy to a staging env first with `wrangler deploy --env staging` (see `workflows/deploy-worker`)
2. Smoke test every route against the original Pages URL — status, headers, and content must match
3. Deploy production with `wrangler deploy`, then point custom domains/routes at the Worker
4. Verify the real domain, and keep the original Pages project as rollback until stable

### 5. Cleanup

> Goal: Shut down the old setup after stable

1. After production is stable (user-confirm window) → disable/delete the Pages project
2. Remove unused config and do `/update-references` if files moved
3. Do `/report-before-after` summarizing the URLs, routes, and bindings that changed

## Rules

### 1. Rollback First

- The original Pages project must stay rollback-ready until the new Worker is stable — never delete before confirm
- One commit per migration step so it can be bisected/reverted

### 2. Parity Check

- Every route/redirect/header must be compared against the original Pages — never assume
- Bindings and env vars must be complete before deploy

### 3. Docs First

- assets config fields and limits can change — rely on official docs via `/use-wrangler` instead of guessing

## Expected Outcome

- The site runs fully on Workers with every route/redirect matching the original Pages
- The custom domain points to the Worker and the rollback path (original Pages) is ready
- A clear before/after report is produced

