---
name: follow-service-cloudflare
description: Use Cloudflare Workers, Pages, D1, KV, R2, Nitro via Wrangler CLI for develop and deploy
argument-hint: "[setup-wrangler|config-bindings|deploy-worker|migrate-pages-to-workers|verify] [scope]"
related:
  - follow-secret-manager
  - open-web-for-config-secret
  - create-cloudflare
  - deploy-to-cloudflare
  - resolve-errors
  - follow-tool-mise
  - follow-tasks

---

## Goal

Use the Cloudflare platform to develop, build, deploy, and manage Workers, Pages, D1, KV, R2, Queues, Workflows, and the Nitro preset via the Wrangler CLI

## Scope

Used for:
- Cloudflare Workers — serverless edge deployment with the Wrangler CLI
- Cloudflare Pages — static site hosting and preview deployments
- D1 databases — migrations, queries, bindings
- KV namespaces, R2 buckets, Queues, Workflows, Hyperdrive, Vectorize
- Nitro preset for Nuxt and other frameworks deploying to Cloudflare
- Secrets, environment variables, bindings, and CI/CD integration
- Local development, staging/production deploy, version management, and rollback

## Execute

### 1. Install And Authenticate

> Goal: Install the Wrangler CLI and connect to the Cloudflare account

Latest: `wrangler@4.141.0`, `@cloudflare/workers-types@5.20260926.1` (verified 2026-09-26)

1. Install Wrangler with `bun add -D wrangler`
2. Check the version with `wrangler --version` (must be >= 4.0)
3. Log in with `wrangler login` or use `CLOUDFLARE_API_TOKEN` for CI
4. Verify authentication with `wrangler whoami`
5. Install `@cloudflare/workers-types` for TypeScript support

### 2. Initialize Project

> Goal: Create and configure the project

1. Create a new project with `wrangler init project-name` or `npm create cloudflare@latest`
2. Use `wrangler deploy` without a config file — Wrangler 4.68+ auto-detects the framework and creates `wrangler.jsonc`
3. Configure `name`, `main`, `compatibility_date`, `compatibility_flags` in the config
4. Enable the `nodejs_compat` flag for Node.js modules
5. See details in [references/init-and-config.md](references/init-and-config.md)

### 3. Local Development

> Goal: Develop and test in the local environment

1. Run the local dev server with `wrangler dev`
2. Use `--port 8787` for a custom port
3. Use `--local` for local-only mode
4. Use `--remote` for accessing remote resources
5. Check logs and test bindings locally
6. If the project has a `package.json`, set the `dev` script to `wrangler dev` instead of the default dev server (see Rules Package Scripts)

### 4. Configure Bindings

> Goal: Configure D1, KV, R2, Queues, and bindings

1. Create a D1 database with `wrangler d1 create my-db`
2. Create a KV namespace with `wrangler kv namespace create CACHE`
3. Create an R2 bucket with `wrangler r2 bucket create my-bucket`
4. Add bindings in `wrangler.jsonc` or use automatic provisioning (beta)
5. Run `wrangler types` to generate `worker-configuration.d.ts`
6. See details in [references/bindings.md](references/bindings.md) and [references/d1-migrations.md](references/d1-migrations.md)

### 5. Manage Secrets

> Goal: Manage secrets and environment variables

1. Set secrets with `wrangler secret put SECRET_NAME`
2. List secrets with `wrangler secret list`
3. Delete secrets with `wrangler secret delete`
4. Use `vars` for non-secret variables
5. Never commit secrets to git

### 6. Typecheck And Build

> Goal: Check types and build

1. Run `wrangler types` to generate the `Env` interface
2. Run `bun run typecheck` and fix errors until it passes
3. Run `bun run build` or `wrangler deploy --dry-run`
4. Check the bundle size (limit 1 MB for Workers)
5. Optimize the bundle if it exceeds the limit
6. If the deploy target is Cloudflare Workers/Pages, set the `build` script in `package.json` to `wrangler build` instead of the default build (see Rules Package Scripts); then run the build with `bun run build`

### 7. Deploy Staging And Production

> Goal: Deploy to staging before production

1. Add a staging environment in `wrangler.jsonc` under `env.staging`
2. Run `wrangler deploy --env staging --dry-run` to inspect
3. Deploy staging: `wrangler deploy --env staging`
4. Test the staging environment with curl or a browser
5. Deploy production: `wrangler deploy`
6. See details in [references/versions-and-rollback.md](references/versions-and-rollback.md)

### 8. Nitro Preset

> Goal: Deploy Nitro-based apps (Nuxt, TanStack Start) to Cloudflare

1. Set `NITRO_PRESET=cloudflare_module` (or the `nitro.config.ts` `preset`) — the canonical config lives in the `/follow-lib-nitro` `deploy-preset` workflow
2. `bun run build` → `wrangler deploy` — bindings/secrets follow the `deploy-worker` workflow below

### 9. Advanced Features

> Goal: Use advanced features

1. Use `wrangler pages deploy` for Pages projects (see [references/pages.md](references/pages.md))
2. Use `wrangler queues` for message queues
3. Use `wrangler workflows` for workflows
4. Use `wrangler hyperdrive` for database connections
5. Use `wrangler vectorize` for vector embeddings
6. Use `wrangler triggers deploy` for cron schedules (see [references/triggers-and-cron.md](references/triggers-and-cron.md))
7. Use Rust instead of TypeScript on Workers with `workers-rs` (see [references/workers-rs.md](references/workers-rs.md))

### 10. CI/CD, Logs And Troubleshoot

> Goal: Set up CI/CD, monitor logs, and debug

1. Set up CI/CD with `CLOUDFLARE_API_TOKEN` (see [references/ci-cd.md](references/ci-cd.md))
2. Use `wrangler tail` for live logs (see [references/tail-and-logs.md](references/tail-and-logs.md))
3. Enable `observability.enabled` in the config
4. Use `WRANGLER_LOG=debug` for verbose logging
5. See error codes in [references/troubleshooting.md](references/troubleshooting.md)

### Workflows

> Goal: dispatch to the workflow matching the topic/argument

| Topic/Argument | Workflow |
|----------------|----------|
| `setup`, `install`, `login`, `auth` | `workflows/setup-wrangler/SKILL.md` — wrangler install, auth, `whoami` |
| `config`, `bindings`, `kv`, `r2`, `d1`, `vars`, `env` | `workflows/config-bindings/SKILL.md` — bindings and environments |
| `deploy`, `worker` | `workflows/deploy-worker/SKILL.md` — `wrangler deploy`, staging/production, verify |
| `migrate`, `pages-to-workers` | `workflows/migrate-pages-to-workers/SKILL.md` — Pages → Workers migration |
| `verify`, `verify-connection` | `workflows/verify-connection/SKILL.md` — `wrangler whoami`, resource access, bindings ready |
| `d1`, `migrations`, `sql` | `workflows/use-d1/SKILL.md` — D1 create/migrate/query/batch |
| `storage`, `cache` | `workflows/use-storage/SKILL.md` — KV + R2 + Cache API patterns |
| `queue`, `cron`, `workflow`, `durable`, `jobs` | `workflows/use-jobs/SKILL.md` — Queues, Cron, Workflows, Durable Objects |

1. If the argument matches a topic → read `workflows/<name>/SKILL.md` and follow the flow there — do not execute from this table directly
2. If no argument → follow steps 1-10 in order

## Rules

### 1. Configuration Management

- Use `wrangler.jsonc` as the single source of truth (recommended for new projects)
- Always set `compatibility_date` to the current date
- Enable the `nodejs_compat` flag for Node.js modules
- Use environment-specific configs with `env.staging`, `env.production`
- Never hardcode secrets in config files

### 2. Binding Management

- Create resources via the CLI before binding them in config
- Use descriptive names for namespaces and buckets
- Run `wrangler types` when adding or renaming bindings
- Use environment-specific bindings for isolation
- Clean up unused resources

### 3. Secret Security

- Never commit secrets to version control
- Use `/follow-secret-manager` to manage `CLOUDFLARE_API_TOKEN` and secrets before injecting them into Wrangler
- Use `wrangler secret put` instead of editing config files
- Rotate secrets regularly
- Use environment-specific secrets

### 4. Deployment

- Always deploy staging before production
- Use `--dry-run` to inspect before a real deploy
- Use versioning for rollback capability
- Use `CLOUDFLARE_API_TOKEN` for automated deploys

### 5. Build Process

- Typecheck fails: fix before building
- Build fails: analyze and fix
- Optimize the bundle if it exceeds the 1 MB limit
- Generate types with `wrangler types`, never hand-write them

### 6. Package Scripts

When a task or project uses Cloudflare (Workers/Pages), set the `package.json` scripts as follows:

- `dev`: `wrangler dev` — replaces the default dev server (`bun run src/index.ts`, `vite dev`, `next dev`, etc.)
- `build`: `wrangler build` — replaces `bun build`/`vite build`/`next build` when deploying to Cloudflare
- `deploy`: `wrangler deploy`
- `deploy:staging`: `wrangler deploy --env staging` (when a staging environment exists)

Note: if the installed Wrangler version does not support the `build` subcommand, use `wrangler deploy --dry-run` or `wrangler deploy` before the real deploy

- Use /open-web-for-config-secret if needed (service cloudflare)
- Use /create-cloudflare-token if needed
- Use /deploy-to-cloudflare if needed
- Use /resolve-cicd if needed
- Use /follow-tool-mise if needed
- Use /follow-tasks if needed

- Use /resolve-errors if needed
## Merged Details → Extracted

All domain details have been extracted into real files:

- **workflows/**: `setup-wrangler`, `config-bindings`, `deploy-worker`, `migrate-pages-to-workers`, `verify-connection`, `use-d1`, `use-storage`, `use-jobs` — dispatched per the `### Workflows` table above
- **references/**: `apis`, `bindings`, `ci-cd`, `commands`, `d1-migrations`, `init-and-config`, `install-and-auth`, `overview`, `package-manifest`, `pages`, `routes`, `tail-and-logs`, `triggers-and-cron`, `troubleshooting`, `versions-and-rollback`, `website`, `workers-overview`, `workers-rs`


##### Source

- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Wrangler Install/Update](https://developers.cloudflare.com/workers/wrangler/install-and-update/)
- [Wrangler Configuration](https://developers.cloudflare.com/workers/wrangler/configuration/)
- [Get Started Guide](https://developers.cloudflare.com/workers/get-started/guide/)
- [Automatic Configuration](https://developers.cloudflare.com/workers/framework-guides/automatic-configuration/)

## Expected Outcome

- Wrangler CLI installed and configured correctly
- Workers or Pages deployed smoothly with gradual rollouts and rollback
- Bindings and secrets managed securely
- D1 migrations working both locally and remotely
- Nitro preset configured for Nuxt
- CI/CD integration running automatically
- Observability enabled with tail debugging
- Problems resolvable from the troubleshooting guide
