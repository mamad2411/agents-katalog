---
name: deploy-production
description: Use this skill when shipping to production after staging is green, when a deploy needs a documented rollback plan, or when the APPROVE-gate workflow is required — the deploy-to-production workflow (final checks, approval gate, deploy, verify, rollback plan) that uses the `deployment-procedures` skill and requires explicit APPROVE before any production mutation.
disable-model-invocation: true
argument-hint: "[service-name] [version]"
---

# Deploy to Production

Production deployment with mandatory approval gates, verification, and rollback plan. Every step that mutates production requires explicit user APPROVE.

**⚠️ SAFETY: No production mutation runs without explicit user APPROVE. This is a stricter gate than `/deploy-staging` — production deploys require BOTH the standard "APPROVE" confirmation AND a separate explicit acknowledgment of the rollback plan from Step 5.**

## 0. Gather Context

Read `CLAUDE.md` (or `AGENTS.md`) at the project root to identify:
- Cloud platform (GCP, Azure, AWS) — apply `cloud-platforms` skill for platform-specific commands
- Deployment method (Kubernetes, Helm, Docker Compose, serverless)
- Production environment configuration (namespace, cluster, region)
- CI/CD pipeline (GitHub Actions, GitLab CI, Jenkins)

This determines which deployment commands and health checks apply.

### 0a. Detect GitOps / progressive-delivery controller — route first

Before running `helm upgrade` / `kubectl apply` directly against production, check whether a controller owns the apply step.

| Marker | System | What this means for production deploys |
|---|---|---|
| `Application` / `ApplicationSet` CRDs in Git | [Argo CD](https://argo-cd.readthedocs.io) | Production manifest changes flow through git PR → Argo CD reconciles. Manual `helm upgrade` will be reverted on next sync. Use `argocd app sync <name>` only for intentional out-of-band promotion. |
| Flux `HelmRelease` / `Kustomization` CRDs | [Flux](https://fluxcd.io) | Same model as Argo CD. Manual override via `flux reconcile helmrelease <name>`. |
| `Rollout` CRDs (`argoproj.io/v1alpha1`) | [Argo Rollouts](https://argoproj.github.io/argo-rollouts/) | Progressive delivery — promotion via `kubectl argo rollouts promote <name>` or automatic per AnalysisTemplate. Replaces manual canary monitoring (Step 3c). |
| `Canary` CRDs (`flagger.app/v1beta1`) | [Flagger](https://docs.flagger.app/) | Same — promotion driven by Prometheus / Datadog metrics analyzer. |

If a controller is detected: skip imperative `helm upgrade` / `kubectl apply` in Step 3; promote via the controller. The 5–10 minute monitoring window in Step 4 is replaced by the controller's analyzer-based promotion (which is the modern best practice — automated SLO-based promotion gates the rollout, not a static wall-clock window).

### 0b. Detect feature-flag platform

If the codebase imports a feature-flag SDK, prefer **decoupled deploy**: ship code dark, then flip the flag separately, ramp, observe.

| Marker | Platform | Approach |
|---|---|---|
| `import { Client } from '@launchdarkly/...'` / `LaunchDarkly` SDK | [LaunchDarkly](https://launchdarkly.com) | Deploy with flag default OFF. Flip flag in LD UI after deploy passes smoke. Rollback = flip flag, no redeploy needed for the new code path. |
| `unleash-client` / `@unleash/...` | [Unleash](https://www.getunleash.io) | Same pattern via Unleash UI. |
| `@openfeature/...` | [OpenFeature](https://openfeature.dev) (vendor-neutral) | Same pattern via the underlying provider (LD/Unleash/Flagsmith/Split). |
| `flagsmith` / `splitsoftware` SDKs | Flagsmith / Split.io | Same pattern. |

Decoupled deploy fundamentally changes Step 3: the deploy itself is low-risk because the new code path is gated. The risk shifts to the flag flip, which is reversible in seconds.

### 0c. Change-window / freeze check

If the project has a documented change-freeze policy (e.g., end-of-quarter freeze, major-event blackout), verify the current date is OUTSIDE the freeze window. Hard stop if inside; require documented exception.

## 1. Pre-Deployment Checklist

### 1a. Staging Verification

Confirm that staging deployment was successful:

- [ ] `/deploy-staging` completed successfully
- [ ] QA testing passed on staging
- [ ] No critical bugs found in staging
- [ ] Performance acceptable on staging

If staging was not verified — **STOP**. Run `/deploy-staging` first.

### 1b. Release Readiness

- [ ] Version tagged (`/release` completed)
- [ ] Changelog updated
- [ ] All tests pass on the release branch
- [ ] Database migrations tested (forward and rollback)
- [ ] Feature flags configured (if applicable)
- [ ] Monitoring dashboards ready
- [ ] On-call team notified

### 1c. Risk Assessment

| Factor | Assessment |
|---|---|
| **Breaking changes** | Yes/No — migration guide ready? |
| **Database migrations** | Yes/No — reversible? |
| **Infrastructure changes** | Yes/No — `/infra-change` completed? |
| **Third-party dependencies** | Yes/No — API compatibility verified? |
| **Traffic impact** | Low/Medium/High |
| **Rollback complexity** | Simple (revert image) / Complex (DB migration) |

If Risk = HIGH, apply `Agent(sre-engineer)` for SLO impact assessment.

## 2. Prepare Deployment

### 2a. Identify Deployment Method

Same as `/deploy-staging` Step 1c — but with production configuration.

### 2b. Backup Current State

```
# Record current deployment state for rollback
kubectl get deployment -n production -o yaml > pre-deploy-state.yaml
```

Or for Helm:
```
helm get values <release> -n production > pre-deploy-values.yaml
helm history <release> -n production
```

### 2c. Deployment Plan

Present the deployment plan:

```
## Production Deployment Plan
- **Version**: [current] → [new]
- **Method**: [K8s/Helm/Docker/Platform]
- **Migrations**: [list if any]
- **Config changes**: [list if any]
- **Expected downtime**: [none / X minutes]
- **Rollback plan**: [documented in Step 5]
- **Monitoring**: [dashboards to watch]
```

**⚠️ STOP. Request APPROVE before proceeding to Step 3. Production deploys require explicit acknowledgment of the rollback plan in addition to the deployment plan — confirm both with the user.**

## 3. Deploy — REQUIRES EXPLICIT APPROVE

Only after the user explicitly approves:

### 3a. Run Migrations (if applicable)

```
# Database migration
<migration-command>
```

Verify migration completed successfully before proceeding.

### 3b. Deploy Application

**Kubernetes / Helm:**
```
helm upgrade --install <release> <chart> \
  -n production \
  -f values-production.yaml \
  --set image.tag=<tag>
```

**Rolling update strategy** — monitor pod rollout:
```
kubectl rollout status deployment/<name> -n production --timeout=300s
```

### 3c. Canary (if applicable)

If using canary deployment:
1. Deploy to canary (small % of traffic)
2. Monitor error rates and latency for 5–10 minutes
3. If metrics are healthy → proceed to full rollout
4. If degradation detected → rollback canary immediately

## 4. Post-Deployment Verification

### 4a. Health Check

```
// turbo
kubectl get pods -n production -o wide
```

```
curl -s <production-url>/health
```

### 4b. Smoke Tests

Run the project's existing smoke suite — do NOT improvise from generic checklists. Detect and execute (in priority order):

| Marker | Run command |
|---|---|
| `tests/smoke/` directory + `pytest`/`vitest`/etc. | Project test runner against that path |
| `e2e/` or `tests/e2e/` with Playwright config (`playwright.config.ts`) | `npx playwright test --grep @smoke` (filter by `@smoke` annotation) |
| `cypress/e2e/smoke/*` | `npx cypress run --spec 'cypress/e2e/smoke/**'` |
| Postman / Newman collection | `npx newman run smoke.postman_collection.json` |
| K6 / Artillery script | run against the prod URL with a low-rate profile |

Fallback when no smoke suite exists (write down for follow-up — every project should ship one):
- [ ] Application responds on production URL (HTTP 200)
- [ ] Health endpoint returns 200
- [ ] Authentication flow works (login + session retrieval)
- [ ] Core API endpoints respond correctly (3-5 representative routes)
- [ ] One key user journey end-to-end

### 4c. Monitor (5–10 minutes)

Watch for:
- **Error rate**: Should not increase vs pre-deploy baseline
- **Latency**: P50, P95, P99 within SLO targets
- **CPU/Memory**: No unusual spikes
- **Logs**: No new error patterns

```
// turbo
kubectl logs -n production -l app=<app-name> --tail=100 --since=5m
```

```
// turbo
kubectl get events -n production --sort-by='.lastTimestamp' --field-selector type!=Normal
```

## 5. Rollback Plan

If issues detected — execute rollback immediately:

**Helm:**
```
helm rollback <release> <previous-revision> -n production
```

**Kubernetes:**
```
kubectl rollout undo deployment/<name> -n production
```

**Database migration rollback:**
```
<rollback-migration-command>
```

After rollback:
- Verify application is healthy
- Notify team of rollback
- Create incident ticket for investigation

## 6. Memory Write (L4)

Append a deploy event to `.ai-skills-memory/runs.jsonl` per `memory-discipline.md` retention rules. Production deploys are long-retention events:

```json
{"ts": "<ISO8601>", "event": "deploy", "env": "production", "service": "<name>", "version_from": "<old>", "version_to": "<new>", "method": "k8s|helm|docker|platform", "status": "success|fail|rolled_back", "duration_ms": N, "rollback": <bool>, "approved_by": "<user>"}
```

## 7. Summary

```
## Production Deployment Summary
- **Version**: [old] → [new]
- **Deployed at**: [timestamp]
- **Method**: [K8s/Helm/Docker/Platform]
- **Migrations**: [applied/N/A]
- **Health check**: [pass/fail]
- **Smoke tests**: [pass/fail]
- **Monitoring**: [stable/issues detected]
- **Rollback**: [not needed / executed at timestamp]
- **Production URL**: [url]
- **Next steps**: [monitoring period, team notification, release announcement]
```

## Integration

- **Preceded by**: `/deploy-staging` (staging verification), `/release` (version tag)
- **Roles**: `Agent(devops-engineer)`, `Agent(sre-engineer)`, `Agent(devops-architect)` (deployment strategy design)
- **Skills**: `deployment-procedures` skill
- **Memory writes**: L4 `runs.jsonl` (deploy event per Step 6)
