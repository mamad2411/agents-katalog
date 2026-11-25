---
name: cloudflare_wrangler_cheatsheet
description: Quick reference mapping Cloudflare product surfaces (Workers, Pages, KV, R2, D1, DNS) to the wrangler CLI commands teams use day to day.
---

# Wrangler & Cloudflare surface cheatsheet

> Unofficial, agentstack-authored. Not affiliated with or endorsed by Cloudflare.

Use this skill to pick the right `wrangler` command for a Cloudflare task without
guessing. Commands assume Wrangler v3+; run `wrangler --version` if unsure.

## Workers

- Develop locally: `wrangler dev` (add `--remote` to run against the edge).
- Deploy: `wrangler deploy` (scope with `--env <name>`).
- Validate a build only: `wrangler deploy --dry-run --outdir dist`.
- Live logs: `wrangler tail`.
- Roll back: `wrangler deployments list`, then `wrangler rollback <id>`.

## Secrets & vars

- Set a secret: `wrangler secret put <NAME>` (value entered interactively).
- List secrets: `wrangler secret list`. Delete: `wrangler secret delete <NAME>`.
- Plaintext config vars live in `[vars]` in `wrangler.toml` — never secrets.

## KV (key-value)

- Create namespace: `wrangler kv namespace create <BINDING>`.
- Write/read: `wrangler kv key put <KEY> <VALUE> --binding <BINDING>` /
  `wrangler kv key get <KEY> --binding <BINDING>`.

## R2 (object storage)

- Create bucket: `wrangler r2 bucket create <NAME>`.
- Upload/download: `wrangler r2 object put <BUCKET>/<KEY> --file <PATH>` /
  `wrangler r2 object get <BUCKET>/<KEY>`.

## D1 (SQL)

- Create db: `wrangler d1 create <NAME>`.
- Run SQL: `wrangler d1 execute <NAME> --command "SELECT 1"` or
  `--file ./schema.sql`. Use `--local` for the local dev database.

## Pages

- Deploy a build output dir: `wrangler pages deploy <DIST_DIR> --project-name <NAME>`.
- List projects/deployments: `wrangler pages project list` /
  `wrangler pages deployment list --project-name <NAME>`.

## DNS & zones

- DNS records are managed via the dashboard, API, or Terraform — `wrangler` does
  not edit DNS. Use the Cloudflare MCP or API to read zone and record state, and
  treat record changes as reviewed infrastructure changes, not ad-hoc edits.

## Conventions

- Match the binding name in `wrangler.toml` to the variable name your code reads
  from `env` so config and runtime stay in sync.
- Use `--local` for D1/KV during development to avoid mutating production data.

## Boundaries

- Never echo secret values; set them only via `wrangler secret put`.
- Destructive commands (`r2 bucket delete`, `kv namespace delete`,
  `d1 execute` with DROP/DELETE) are irreversible — confirm the target and
  environment before running, and never run them in bulk without asking.
