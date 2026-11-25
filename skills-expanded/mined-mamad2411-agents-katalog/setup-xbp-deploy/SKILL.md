---
name: setup-xbp-deploy
description: >
  One-shot xbp Cloudflare Worker deploy setup for static docs/apps: wrangler
  assets, package deploy scripts, .xbp [[workers]] + cloudflare-worker provider,
  CF account readiness, xbp deploy pipeline, live health verify. AUTO-RUN the
  global workflow setup-xbp-deploy when the user asks to set up CF/xbp deploy,
  wire a Worker on xbp.app, deploy apps/docs via Cloudflare, or /setup-xbp-deploy.
---

# setup-xbp-deploy

## Auto-run

When the user message matches any of:

- set up / wire **xbp deploy** for Cloudflare
- deploy **apps/docs** (or a static site) as a **Cloudflare Worker**
- custom domain on **`*.xbp.app`** via xbp
- scaffold **wrangler** + **`[[workers]]`** for this repo
- `/setup-xbp-deploy`

…immediately launch the global workflow (do not only describe steps):

```text
name: setup-xbp-deploy
args: {
  "app": "<worker app name if known>",
  "script_name": "<CF script name if known>",
  "root": "apps/docs",
  "service": "docs",
  "domain": "<host without scheme if known>",
  "assets_dir": "dist",
  "dry_run": false,
  "skip_deploy": false
}
agent_budget: 32
```

Omit unknown optional fields. Prefer `domain` like `my-product.xbp.app` (no `https://`).

Then tell the user the run is in `/workflows`. On completion, report:

- live domain URL + workers.dev
- files written (wrangler, package.json, `.xbp/xbp.toml`)
- redeploy one-liner: `xbp deploy <service> --to cloudflare --run --yes`
- scratch report path

## What the workflow does

| Phase | Work |
|-------|------|
| Scope | Infer app root, script name, domain (blume site / `*.xbp.app`), existing xbp/wrangler |
| Auth | `xbp config cloudflare status`; auto-set account ID when single account |
| Scaffold | `wrangler.jsonc`, deploy scripts, root `docs:deploy*`, `[[workers]]`, provider flip, gitignore |
| Deploy | `xbp deploy <svc> --to cloudflare --run --yes` (fallback workers/wrangler) |
| Verify | HTTP 200 on custom domain |
| Report | Redeploy commands + footguns |

## Args

| Arg | Default | Meaning |
|-----|---------|---------|
| `app` | infer | `[[workers]]` name |
| `script_name` | infer | Cloudflare Worker name |
| `root` | `apps/docs` or `.` | App directory |
| `service` | `docs` / app | `services[]` to flip to cloudflare-worker |
| `domain` | blume site or `<product>.xbp.app` | Custom domain host |
| `assets_dir` | `dist` | Static assets dir |
| `kind` | `static` | assets-only wrangler |
| `dry_run` | false | Plan only |
| `skip_scaffold` | false | Deploy only |
| `skip_deploy` | false | Scaffold only |
| `skip_build` | false | `deploy:worker` only |
| `force` | false | Overwrite wrangler.jsonc |
| `account_id` | — | Force CF account ID |
| `health_path` | `/` | Probe path |

## Manual invoke

```text
/setup-xbp-deploy
```

or

```text
/workflow setup-xbp-deploy domain=my-app.xbp.app root=apps/docs
```

## Redeploy (after setup)

```powershell
xbp deploy docs --to cloudflare --run --yes --env production
# or
xbp cloudflare workers --app <app> deploy run   # --app before deploy
pnpm docs:deploy
```

## Non-goals

- Does not set up Kubernetes / OCI for the same service
- Does not create Cloudflare Workers Builds Git triggers (optional follow-up)
- Does not invent container-backed workers (use `xbp cloudflare init` for those)
- Does not commit or push

## Lessons baked in (from real deploy)

1. Prefer **native** scaffold: `xbp cloudflare init --kind assets --worker-root apps/docs --domain <host> --service docs --write` (then `xbp deploy docs --to cloudflare --run --yes`). This workflow remains for monorepos that need multi-file inference.
2. Single-account tokens auto-select account ID on `xbp config cloudflare status` / deploy readiness.
3. `--app` is accepted on parent, mid, or leaf: `workers deploy run --app X` works.
4. Service must be `provider = cloudflare-worker` with `[[workers]]` registered.
)
