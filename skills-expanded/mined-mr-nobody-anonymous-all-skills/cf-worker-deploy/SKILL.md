---
name: cf-worker-deploy
description: Validate and deploy Cloudflare Workers with preview, secret, and rollback safeguards.
category: development
aliases:
- cloudflare
- worker
- cf
- edge
triggers:
- Deploy to Cloudflare Workers
- Publish worker
- Cloudflare deployment
- Update worker
keywords:
- cloudflare
- worker
- deploy
- edge
- serverless
- wrangler
dependencies:
- optional:wrangler
risk: high
version: 1.0.0
source: custom
enabled: true
capabilities:
- cf-worker-deploy
- development
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- cloudflare
- deploy
- development
- edge
- worker
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Cf Worker Deploy

## Purpose
Validate and deploy Cloudflare Workers with proper preview testing, secret management,
and rollback capabilities. The skill ensures safe deployments with minimal disruption.

## When to Use
- Deploying or updating a Cloudflare Worker
- Managing worker secrets and environment variables
- Rolling back a problematic deployment
- Testing workers in preview mode before production

## When NOT to Use
- For non-Cloudflare deployments (use appropriate cloud skill)
- Without proper Cloudflare authentication
- When rollback isn't possible (stateless workers)

## Capabilities
- Local validation and linting
- Preview deployment to staging
- Production deployment with traffic splitting
- Secret management (set, update, rotate)
- Environment variable management
- Rollback to previous version
- Deployment history and logs
- Traffic percentage controls

## Inputs
- `action` (required) — one of: validate, preview, deploy, rollback, secrets
- `worker_name` (required) — target worker
- `environment` (optional) — production, staging, preview
- `traffic_percentage` (optional) — for gradual rollouts

## Workflow
1. **Validate** — Run linting and type checks
2. **Preview** — Deploy to preview environment
3. **Test** — Verify preview is functional
4. **Confirm** — User approval for production
5. **Deploy** — Push to production with monitoring
6. **Verify** — Confirm successful deployment
7. **Rollback** — If issues detected, revert

## Tools
- Wrangler CLI (wrangler.toml configuration)
- Cloudflare API

## Examples
**User:** "Deploy my worker to production"
**Response:**
```
Validating worker...
âœ“ Linting passed
âœ“ Type checks passed

Preview deployment: âœ“ Success
Preview URL: https://my-worker.preview.pages.dev

Deploy to production? Say "confirm" to proceed.

After deployment, I'll monitor for errors and can rollback if needed.
```

## Safety
- ALWAYS validate before deployment
- ALWAYS use preview mode first
- Require explicit confirmation for production
- Monitor for errors after deployment
- Keep rollback path available
- Never expose secrets in logs or responses

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical development category.
