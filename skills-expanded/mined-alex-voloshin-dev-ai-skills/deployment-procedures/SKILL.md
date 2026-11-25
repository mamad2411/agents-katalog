---
name: deployment-procedures
description: Use this skill when authoring or reviewing a deploy workflow that needs the strategy and rollback knowledge — the deployment strategy reference (rolling, blue-green, canary, recreate) plus rollback decision criteria, pre-deploy checklist, and post-deploy verification, loaded by the `/deploy-production` and `/deploy-staging` workflows; not a workflow itself.
disable-model-invocation: true
---

# Deployment Procedures — Strategy & Rollback Reference

Knowledge reference for deployment strategies (rolling, blue-green, canary, recreate) plus rollback decision criteria, pre-deploy checklists, health-check patterns, and post-deploy verification. Loaded by the `/deploy-production` and `/deploy-staging` workflows; not a workflow itself.

## When to Use

- Deploying application updates to production
- Planning rollback strategies before deployment
- Verifying production health after deployment
- Investigating post-deployment issues

## When NOT to Use

- Deploying to staging (use `/deploy-staging` workflow)
- Making infrastructure changes (use `/infra-change` workflow)
- Planning release version and changelog (use `/release` workflow)

## Deployment Strategies

| Strategy | When to Use | Risk | Downtime |
|---|---|---|---|
| **Rolling update** | Standard deploys, stateless services | Low | Zero |
| **Blue-Green** | Critical services, instant rollback needed | Low | Zero |
| **Canary** | High-risk changes, gradual validation | Medium | Zero |
| **Recreate** | Stateful services, breaking schema changes | High | Brief |

### Rolling Update (Default)

- Gradually replace old pods with new ones
- Health checks gate the rollout — unhealthy pods stop the rollout
- Configure `maxSurge` and `maxUnavailable` for rollout speed
- Monitor error rates during rollout window

### Canary Deployment

1. Deploy new version to small subset (5–10% traffic)
2. Monitor error rate, latency, and business metrics for 5–10 minutes
3. If healthy → gradually increase traffic (25% → 50% → 100%)
4. If degraded → route all traffic back to stable version

### Blue-Green Deployment

1. Deploy new version alongside current (green alongside blue)
2. Run full smoke tests against green
3. Switch traffic from blue to green
4. Keep blue running for instant rollback (15–30 minutes)
5. Decommission blue after confidence period

## Feature-Flag-Coupled Deploys (Decoupled Deploy)

Decoupled deploy ships the new code path **dark** (flag default off), then flips the flag in a second, independent action. The deploy itself is low-risk because the new code path is gated; risk shifts to the flag flip, which is reversible in seconds.

### When to use

- Behavior changes that need progressive rollout regardless of deploy strategy (rolling / blue-green / canary all benefit)
- Risky changes that need fast rollback without redeploy
- A/B tests, regional rollouts, or per-customer enablement
- Database migrations following an [expand-contract](../migrate/references/expand-contract.md) sequence — flag gates the read-from-new switch

### Workflow

1. **Deploy dark**: ship the code with the flag's default value set to OFF. The deploy is low-risk; old behavior continues.
2. **Verify in production**: run synthetics, check logs/metrics — the new code path is reachable but inert.
3. **Internal-only flip**: enable the flag for internal users (test rule on email domain or user ID). Verify behavior.
4. **Ramp**: 1% → 5% → 25% → 50% → 100%. Watch error rate, latency, and business metrics at each step. Pause or rollback the flag at the first regression.
5. **Cleanup**: once the flag has been at 100% for the agreed soak period (typically 1–2 weeks), remove the flag and the old code path in a follow-up PR. Stale flags rot — every flag must have a removal date.

### Platforms (vendor-neutral first, then vendor-specific)

| Platform | SDK marker | Notes |
|---|---|---|
| [OpenFeature](https://openfeature.dev) | `@openfeature/...` packages | Vendor-neutral standard. Pluggable provider (LD/Unleash/Flagsmith/Split). Default choice when starting fresh in 2026. |
| [LaunchDarkly](https://launchdarkly.com) | `launchdarkly-*-sdk` | Mature commercial. Strong UI, good targeting rules. |
| [Unleash](https://www.getunleash.io) | `unleash-client` / `@unleash/...` | Open-source + commercial. Good fit for self-hosted. |
| [Flagsmith](https://flagsmith.com) | `flagsmith` | Open-source + commercial. Lightweight. |
| [Split.io](https://split.io) | `@splitsoftware/splitio` | Strong experimentation focus (built-in metrics + statistical significance). |
| [GrowthBook](https://www.growthbook.io) | `@growthbook/growthbook-*` | Open-source. Strong A/B-test analysis. |

### Anti-patterns

- **Flag-only deploys with no kill date**: flags accumulate and become permanent state. Track flag age; remove on schedule.
- **Reading a flag in a hot path without local cache**: flag SDK call inside a per-request loop adds latency and a network failure mode. Cache flag values per request or per session.
- **Combining many flags into one big flip**: one big-bang flag breaks fast-rollback. One concern → one flag.

## Pre-Deployment Checklist

- [ ] All tests pass on release branch
- [ ] Staging deployment verified
- [ ] Database migrations tested (forward and rollback)
- [ ] Feature flags configured
- [ ] Monitoring dashboards ready
- [ ] On-call team notified
- [ ] Rollback plan documented and tested
- [ ] Release notes prepared

## Post-Deployment Verification

- [ ] Health endpoint returns 200
- [ ] Error rate ≤ pre-deploy baseline
- [ ] Latency P95 within SLO target
- [ ] No new error patterns in logs
- [ ] Key user journeys functional
- [ ] Database connections stable
- [ ] External integrations responding
- [ ] Alerts not firing

## Integration

- **Follows rules**: `Agent(devops-engineer)` (infrastructure), `Agent(sre-engineer)` (SLOs, monitoring)
- **Used by workflows**: `/deploy-production`, `/deploy-staging`
- **Companion resources**: `rollback-procedure.md`
