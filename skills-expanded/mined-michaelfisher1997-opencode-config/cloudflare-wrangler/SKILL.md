---
name: cloudflare-wrangler
description: Cloudflare Workers CLI for deploying, developing, and managing Workers, KV, R2, D1, Vectorize, Hyperdrive, Workers AI, Containers, Queues, Workflows, Pipelines, and Secrets Store. Use before running wrangler commands to ensure correct syntax and best practices.
license: Apache 2.0
metadata:
  source: https://github.com/cloudflare/skills
  category: cloudflare
---

# Wrangler CLI

Your knowledge of Wrangler CLI flags, config fields, and subcommands may be outdated. **Prefer retrieval over pre-training**.

## Retrieval Sources

| Source | How to retrieve | Use for |
|--------|----------------|---------|
| Wrangler docs | `https://developers.cloudflare.com/workers/wrangler/` | CLI commands, flags, config reference |
| Wrangler config schema | `node_modules/wrangler/config-schema.json` | Config fields, binding shapes, allowed values |
| Cloudflare docs | `https://developers.cloudflare.com/workers/` | API reference, compatibility dates/flags |

## FIRST: Verify Wrangler Installation

```bash
wrangler --version  # Requires v4.x+
```

If not installed:
```bash
npm install -D wrangler@latest
```

## Key Guidelines

- **Use `wrangler.jsonc`**: Prefer JSON config over TOML. Newer features are JSON-only.
- **Set `compatibility_date`**: Use a recent date (within 30 days).
- **Generate types after config changes**: Run `wrangler types` to update TypeScript bindings.
- **Local dev defaults to local storage**: Bindings use local simulation unless `remote: true`.

## Quick Start

```bash
npx wrangler init my-worker
npx create-cloudflare@latest my-app
```

## Core Commands

| Task | Command |
|------|---------|
| Start local dev server | `wrangler dev` |
| Deploy to Cloudflare | `wrangler deploy` |
| Deploy dry run | `wrangler deploy --dry-run` |
| Generate TypeScript types | `wrangler types` |
| View live logs | `wrangler tail` |
| Delete Worker | `wrangler delete` |
| Auth status | `wrangler whoami` |

## Minimal Config

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2026-01-01"
}
```

## Full Config with Bindings

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2026-01-01",
  "compatibility_flags": ["nodejs_compat"],
  "vars": { "ENVIRONMENT": "production" },
  "kv_namespaces": [{ "binding": "KV", "id": "<KV_NAMESPACE_ID>" }],
  "r2_buckets": [{ "binding": "BUCKET", "bucket_name": "my-bucket" }],
  "d1_databases": [{ "binding": "DB", "database_name": "my-db", "database_id": "<DB_ID>" }],
  "ai": { "binding": "AI" },
  "vectorize": [{ "binding": "VECTOR_INDEX", "index_name": "my-index" }],
  "hyperdrive": [{ "binding": "HYPERDRIVE", "id": "<HYPERDRIVE_ID>" }],
  "durable_objects": { "bindings": [{ "name": "COUNTER", "class_name": "Counter" }] },
  "triggers": { "crons": ["0 * * * *"] },
  "env": {
    "staging": { "name": "my-worker-staging", "vars": { "ENVIRONMENT": "staging" } }
  }
}
```

## Local Development

```bash
wrangler dev                              # Local mode (default)
wrangler dev --env staging                # Specific environment
wrangler dev --local                      # Force local-only
wrangler dev --test-scheduled             # Test cron handlers
wrangler dev --port 8787                  # Custom port
```

Use `.dev.vars` for local development secrets.

## Deployment

```bash
wrangler deploy                    # Deploy to production
wrangler deploy --env staging      # Deploy specific environment
wrangler deploy --dry-run          # Validate without deploying
wrangler secret put API_KEY        # Set secret interactively
wrangler secret list               # List secrets
wrangler versions list             # List recent versions
wrangler rollback                  # Rollback to previous version
```

## KV

```bash
wrangler kv namespace create MY_KV
wrangler kv key put --namespace-id <ID> "key" "value"
wrangler kv key get --namespace-id <ID> "key"
wrangler kv key list --namespace-id <ID>
```

## R2

```bash
wrangler r2 bucket create my-bucket
wrangler r2 object put my-bucket/path/file.txt --file ./local-file.txt
wrangler r2 object get my-bucket/path/file.txt
```

## D1

```bash
wrangler d1 create my-database
wrangler d1 execute my-database --remote --command "SELECT * FROM users"
wrangler d1 migrations create my-database create_users_table
wrangler d1 migrations apply my-database --remote
wrangler d1 export my-database --remote --output backup.sql
```

## Vectorize

```bash
wrangler vectorize create my-index --dimensions 768 --metric cosine
wrangler vectorize insert my-index --file vectors.ndjson
wrangler vectorize query my-index --vector "[0.1, 0.2, ...]" --top-k 10
```

## Queues

```bash
wrangler queues create my-queue
wrangler queues consumer add my-queue my-worker
```

## Workflows

```bash
wrangler workflows list
wrangler workflows trigger my-workflow --params '{"key": "value"}'
```

## Observability

```bash
wrangler tail                     # Stream live logs
wrangler tail --status error      # Filter by status
wrangler tail --format json       # JSON output
wrangler check startup            # Profile Worker startup time
```

## Best Practices

1. Version control `wrangler.jsonc` - treat as source of truth
2. Run `wrangler types` in CI to catch binding mismatches
3. Use environments for staging/production separation
4. Update `compatibility_date` quarterly
5. Use `.dev.vars` for local secrets - never commit secrets
6. Test locally with `wrangler dev` before deploying
7. Use `--dry-run` before major deploys

## Keywords

Cloudflare, Wrangler, CLI, Workers, deploy, KV, R2, D1, Vectorize, Queues, Workflows
