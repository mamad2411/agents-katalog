---
name: deploy-ops
description: "Production deployment operations checklist with health checks and rollback guide. Trigger when: deploy to production, production release, go live, rollback, deployment checklist, 正式環境部署, 上線流程, 回滾, 部署清單, 部署上線."
metadata:
  category: ops
  version: "1.0"
---

# Deploy Ops

Guides production deployments using a structured pre-deploy checklist, step-by-step execution, health checks, and a documented rollback procedure.

## Purpose

Ensure every production deployment is safe, documented, and reversible by enforcing a pre-deploy checklist, executing deployment steps with monitoring, running health checks, and recording outcomes.

## Trigger

Apply when user requests:
- "deploy to production", "production release", "go live", "rollback"
- "deployment checklist", "正式環境部署", "上線流程", "回滾", "部署清單"

Do NOT trigger for:
- Setting up a CI/CD pipeline — use `ci-cd-pipeline`
- Deploying to a local or development environment — handle inline

## Prerequisites

- All CI tests must pass for the version being deployed
- The version must have been successfully deployed to staging
- A rollback plan must be documented before starting
- Deployer must have production deployment credentials

## Steps

1. **Pre-deploy checklist** — verify all conditions are met: CI tests pass, staging verified, database migrations tested on staging, rollback plan documented, stakeholders notified if user-facing downtime is expected
2. **Announce deployment window** — post to the team's status channel or status page if the deployment may cause downtime or degraded performance
3. **Execute deployment** — run the platform-specific deployment command (e.g., `kubectl apply`, `fly deploy`, `helm upgrade`, `eb deploy`)
4. **Run health checks** — verify all services return expected HTTP status codes, database connections are healthy, and critical endpoints respond within acceptable latency
5. **Monitor for 15 minutes** — watch error rate, p99 latency, and CPU/memory usage against pre-deployment baseline; set alert thresholds before deploying
6. **Document the deployment** — record version deployed, timestamp, deployer identity, deploy duration, and any issues or observations
7. **Execute rollback if anomaly detected** — trigger the rollback procedure immediately if error rate spikes, p99 latency degrades, or a critical health check fails; verify the previous version is live after rollback

## Output Format

File path: none (checklist and results printed to user; save to deployment log if applicable)

```
## Deployment: <version / PR number / tag>

### Pre-Deploy Checklist
[ ] All CI tests pass (run ID: <link>)
[ ] Staging successfully deployed and verified
[ ] Database migrations tested on staging
[ ] Rollback plan documented: <rollback command or procedure>
[ ] Stakeholders notified (if user-facing downtime possible)

### Deployment Steps
\`\`\`
<step-by-step commands used>
\`\`\`

### Health Check Results
| Service | Endpoint | Status | Latency | Notes |
|---------|----------|--------|---------|-------|
| API | /health | 200 OK | 45ms | — |
| DB | connection pool | healthy | — | — |

### Monitoring Summary (15 min post-deploy)
- Error rate: <before> → <after>
- p99 latency: <before> → <after>
- CPU/memory: within normal range / anomaly detected

### Post-Deploy Notes
<issues encountered, follow-up items, rollback triggered Y/N>
```

## Rules

### Must
- Always complete the full pre-deploy checklist before running any deployment command
- Always have a documented, tested rollback plan ready before deploying
- Always run health checks immediately after deployment completes
- Always document every production deployment — version, timestamp, deployer, outcome

### Never
- Never deploy directly to production without first deploying to staging
- Never skip pre-deploy checklist items "just this once" — every item exists because something broke without it
- Never deploy during peak traffic hours without explicit written approval from a stakeholder
- Never consider a deployment complete until 15 minutes of post-deploy monitoring shows no anomalies

## Examples

### Good Example

User: "Deploy v2.4.1 to production on Fly.io."

```
## Deployment: v2.4.1

### Pre-Deploy Checklist
[x] All CI tests pass (GitHub Actions run #1847 — all green)
[x] Staging successfully deployed and verified (deployed 2 hours ago, smoke tests pass)
[x] Database migrations tested on staging (migration 0042_add_user_preferences ran cleanly)
[x] Rollback plan documented: `fly releases rollback --app my-app v2.4.0`
[x] Stakeholders notified (no downtime expected — rolling deploy)

### Deployment Steps
\`\`\`
fly deploy --app my-app --image registry.fly.io/my-app:v2.4.1
\`\`\`

### Health Check Results
| Service | Endpoint | Status | Latency | Notes |
|---------|----------|--------|---------|-------|
| API | /health | 200 OK | 38ms | — |
| DB | connection pool | healthy | — | Pool size: 10/10 |
| Auth | /auth/ping | 200 OK | 22ms | — |

### Monitoring Summary (15 min post-deploy)
- Error rate: 0.02% → 0.02% (no change)
- p99 latency: 210ms → 205ms (slight improvement)
- CPU/memory: within normal range

### Post-Deploy Notes
Clean deployment. No issues observed. Rollback not triggered.
```

### Bad Example

```
I'll just push this straight to prod since staging looked fine last week and the fix is small.
```

> Why this is bad: No checklist, no staging verification for the current version, no rollback plan, no health checks, no documentation. "The fix is small" is the most common precursor to incidents. Skipping process "just this once" establishes a pattern that eventually causes an outage.
