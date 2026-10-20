---
name: deployment
last_reviewed: 2026-09-06
group: Ship and run
description: >-
  Ship it: platform config for Vercel, Netlify, Fly, Railway, AWS, env secrets, checklists, and
  rollback. Use when deploying applications to cloud environments.
---

# Deployment

Deployments fail on environment drift, schema mismatches, and unverified secrets. A reliable deployment pipeline specifies target platform configurations explicitly, manages environment secrets strictly through platform vaults, verifies database migration forward-compatibility, and guarantees automated rollback in under 60 seconds.

## 1. Platform Configuration Archetypes

### A. Vercel (`vercel.json`)
Used for Next.js, SvelteKit, and frontend/serverless architectures:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["iad1"],
  "cleanUrls": true,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ]
}
```
- **CLI Commands**: `vercel deploy` (preview), `vercel deploy --prod` (production promote).
- **Environment Scope**: Segregate variables between Development, Preview, and Production.

### B. Netlify (`netlify.toml`)
Used for static sites, Jamstack, and Netlify Edge functions:
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    Strict-Transport-Security = "max-age=31536000; includeSubDomains; preload"
```
- **CLI Commands**: `netlify deploy`, `netlify deploy --prod`.

### C. Fly.io (`fly.toml`)
Used for full-stack Node.js, Go, Python, and containerized long-running services:
```toml
app = "production-app"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 1

[[http_service.checks]]
  grace_period = "10s"
  interval = "15s"
  method = "GET"
  timeout = "5s"
  path = "/healthz"
```
- **CLI Commands**: `fly launch`, `fly secrets set KEY=VALUE`, `fly deploy`, `fly releases rollback`.

### D. Railway (`railway.json` / Nixpacks)
Used for microservices, Redis, PostgreSQL, and background worker queues:
```json
{
  "$schema": "https://railway.com/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm run build"
  },
  "deploy": {
    "startCommand": "node dist/index.js",
    "healthcheckPath": "/healthz",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```
- **CLI Commands**: `railway up`, `railway variables set KEY=VALUE`.

### E. Cloudflare Pages & Workers (`wrangler.toml`)
Used for edge compute, global APIs, and static assets with serverless bindings:
```toml
name = "edge-api"
main = "src/index.ts"
compatibility_date = "2026-01-01"

[vars]
ENVIRONMENT = "production"

[[kv_namespaces]]
binding = "CACHE"
id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
- **CLI Commands**: `wrangler secret put KEY`, `wrangler deploy`.

### F. AWS (App Runner / ECS Fargate / CDK)
Used for enterprise multi-tenant architectures and private VPC deployments:
- Inject secrets via AWS Secrets Manager or SSM Parameter Store using IAM task roles (`arn:aws:iam::...`). Never bake `.env` into container layers.
- App Runner: define `apprunner.yaml` with build and run stages, health checks, and auto-scaling rules (min 1, max 10 instances).
- ECS Fargate: configure Blue/Green deployments using AWS CodeDeploy with automatic rollback triggered on CloudWatch 5xx alarm breaches.

## 2. Zero-Downtime Migration & Rollback Discipline
- **Expand/Contract Database Pattern**:
  1. *Phase 1 (Expand)*: Add nullable column or new table. Deploy migration.
  2. *Phase 2 (Dual Write)*: Deploy application code writing to both old and new schemas.
  3. *Phase 3 (Backfill)*: Asynchronously backfill historical data.
  4. *Phase 4 (Contract)*: Deploy code reading exclusively from new schema; drop old column in a subsequent release.
- **Rollback Runbook**:
  - Keep previous deployment artifact/image digest tagged (`:v3.0.0-previous`).
  - Automated platform rollback: `fly releases rollback`, `vercel rollback [deployment-url]`, or AWS ECS task definition reversion.

## Critical Rules
1. Never run destructive database migrations (`DROP COLUMN`, `ALTER TABLE ... RENAME`) in the same deployment as application code changes.
2. Production builds must run from committed git SHAs, never uncommitted local dirty states.
3. Every production service must expose an unauthenticated, lightweight `/healthz` endpoint verifying process vitality and database connectivity.

## Verification Checklist
- [ ] Target platform configuration file (`vercel.json`, `fly.toml`, `netlify.toml`, `railway.json`, `wrangler.toml`) committed and validated.
- [ ] Environment secrets populated in platform vault; no secrets committed to git or exposed in client bundles.
- [ ] Health check endpoint (`/healthz`) verified returning HTTP 200 before cutover.
- [ ] Database migrations tested in staging for forward-compatibility.
- [ ] Instant rollback mechanism (CLI command or container rollback) verified and tested.

## Anti-Patterns
- NEVER run database migrations inside the container startup script (`CMD`); execute migrations as a separate pre-deploy step or release phase.
- NEVER deploy to production with `latest` Docker tags; pin immutable content digests (`sha256:...`).
- NEVER store production encryption keys or credentials in repository `.env.production` files.
