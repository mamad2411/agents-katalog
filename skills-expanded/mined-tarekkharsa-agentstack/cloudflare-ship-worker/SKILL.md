---
name: cloudflare_ship_worker
description: Ship a Cloudflare Worker correctly — configure wrangler, set bindings and secrets, run a dry-run, deploy, and verify.
---

# Ship a Cloudflare Worker

> Unofficial, agentstack-authored. Not affiliated with or endorsed by Cloudflare.

Use this skill when deploying a Cloudflare Worker (new or existing) and you want
the deploy to be repeatable, reviewable, and safe to roll back.

## Workflow

1. Read `wrangler.toml` (or `wrangler.jsonc`) end to end. Confirm `name`,
   `main` (the entry script), and `compatibility_date` are set. A missing or
   stale `compatibility_date` is the most common cause of surprising runtime
   behavior — set it to the day you are shipping unless the project pins one
   deliberately.
2. Inventory every binding the Worker needs and confirm it exists in config:
   KV namespaces, R2 buckets, D1 databases, Queues, Durable Objects, service
   bindings, and `vars`. A binding referenced in code but absent from config
   fails at runtime, not at build.
3. Set secrets out of band with `wrangler secret put <NAME>` — never commit them
   to `wrangler.toml` or `vars`. Verify with `wrangler secret list`.
4. Validate before shipping: `wrangler deploy --dry-run --outdir dist` builds the
   bundle without publishing. Read the binding summary it prints and confirm it
   matches step 2.
5. Deploy to the intended environment explicitly: `wrangler deploy` for the
   default, or `wrangler deploy --env staging` / `--env production`. Do not let
   ambiguity decide which environment ships.
6. Verify the live deploy: hit the route or `workers.dev` URL, then tail logs
   with `wrangler tail` to confirm requests land and bindings resolve.
7. If anything looks wrong, roll back with `wrangler rollback` (or `wrangler
   deployments list` then `wrangler rollback <id>`) rather than hot-patching.

## Conventions

- Use named environments (`[env.staging]`, `[env.production]`) instead of editing
  one shared config per deploy. Promote the same code across environments.
- Keep `compatibility_date` and `compatibility_flags` under version control so a
  deploy is reproducible from a clean checkout.
- Prefer `--dry-run` in CI as a fast build/config check on every PR.

## Boundaries

- Never print, commit, or echo secret values; set them with `wrangler secret put`.
- Confirm the target environment before running `wrangler deploy` against
  production — a wrong `--env` can overwrite live config and bindings.

When using the Cloudflare MCP, use it to read account resources and binding
configuration to cross-check `wrangler.toml`; perform the actual deploy with the
`wrangler` CLI so it is logged and reproducible.
