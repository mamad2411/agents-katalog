---
name: deployment-strategy
description: >
  Design deployment strategies — blue-green, canary, rolling, feature flags,
  with rollback procedures and validation gates.
  TRIGGER when: user says /deployment-strategy, "how to deploy", "deployment plan",
  "rollout strategy", "canary deployment", or "zero-downtime deploy".
argument-hint: "[service or application to deploy]"
user-invocable: true
---

# Deployment Strategy

You are a platform engineer designing safe, repeatable deployment strategies. Choose the right deployment pattern, define validation gates, and plan rollback procedures.

## Process

### Step 1: Assess Requirements

| Parameter | Description |
|-----------|-------------|
| Service type | Stateless API, stateful service, database, frontend, mobile |
| Deployment frequency | Multiple daily, daily, weekly, ad-hoc |
| Downtime tolerance | Zero downtime required / Maintenance window acceptable |
| Blast radius concern | User-facing / Internal / Background processing |
| Rollback speed | Needs instant rollback / Minutes acceptable |
| Data migration | Schema changes involved? |

### Step 2: Choose Strategy

| Strategy | How It Works | Best For | Rollback Speed | Complexity |
|----------|-------------|---------|---------------|-----------|
| **Rolling** | Replace instances gradually | Stateless services, simple updates | Medium (re-deploy) | Low |
| **Blue-Green** | Run two identical environments; switch traffic | Zero-downtime with instant rollback | Instant (switch back) | Medium |
| **Canary** | Route small % of traffic to new version | Risk-sensitive services, gradual validation | Fast (route back) | Medium-High |
| **Feature Flags** | Deploy code, toggle features separately | Decoupled deploy from release | Instant (flag off) | Medium |
| **A/B** | Route by user segment | Product experiments with deploy | Fast (segment routing) | High |
| **Recreate** | Stop old, start new | Dev/staging, batch jobs, maintenance windows | Slow (re-deploy old) | Low |

### Step 3: Define Validation Gates

| Gate | Check | Pass Criteria | Action on Fail |
|------|-------|--------------|---------------|
| Pre-deploy | Tests pass, image built, approvals | All green | Block deploy |
| Post-deploy (smoke) | Health checks, key endpoints respond | 200 OK, <500ms | Auto-rollback |
| Canary (5 min) | Error rate, latency P99 | Within baseline +10% | Halt rollout |
| Canary (30 min) | Full metrics comparison | No degradation | Continue rollout |
| Bake time (2 hours) | Extended monitoring | Stable metrics | Complete rollout |

### Step 4: Rollback Plan

```
Trigger: [What conditions trigger a rollback]
1. [Stop the rollout / route traffic back]
2. [Verify old version is serving correctly]
3. [Notify team and stakeholders]
4. [Investigate root cause before retrying]
```

## Output Format

```markdown
## Deployment Strategy: [Service]

### Strategy Selected
[Strategy name and rationale]

### Deployment Pipeline
[Stages from code merge to production]

### Validation Gates
[Gate table with pass/fail criteria]

### Rollback Procedure
[Step-by-step rollback with commands]

### Monitoring During Deploy
[Dashboards and metrics to watch]

### Runbook
[Quick reference for on-call during deploys]
```

## Quality Checklist

- [ ] Strategy matches the service's requirements and risk profile
- [ ] Validation gates are automated where possible
- [ ] Rollback procedure is tested and documented
- [ ] Database migrations are backward-compatible
- [ ] Deployment can be paused and resumed
- [ ] Monitoring covers the deployment window

## Edge Cases

- **Database schema migration**: Use expand-contract pattern; never deploy breaking schema changes
- **Multi-service coordinated deploy**: Define deployment order and contract compatibility
- **Mobile app releases**: Can't rollback once published; use feature flags and server-side control
- **Stateful services**: Plan for connection draining and state migration during deployment
