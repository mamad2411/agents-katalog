---
name: blue-green-deploy-checklist
description: >
  Blue/green deployment checklist for owned apps: dual environments, health gates,
  LB/DNS/weight cutover, DB migration compatibility, session stickiness, rollback,
  and post-cutover drain. Use when blue-green deploy, idle environment swap, weighted
  target groups, DNS flip cutover, or zero-downtime release validation — not canary
  analysis alone or chaos experiments.
---

# Blue Green Deploy Checklist

## Scope And Authorization

- **In scope:** Applications and infrastructure you operate (K8s, ECS, VMs, CDN origins) with change windows as required.
- **Out of scope:** Cutting traffic on systems you do not own; unapproved production DNS changes.
- Prefer staging full-path rehearsal before production cutover.
- Redact customer hostnames and secrets from cutover logs shared broadly.
- Pair app/migration code with `code-quality-standards`; pair progressive delivery metrics with `canary-analysis-basics` when using partial traffic.

## When To Use

- You maintain two parallel environments (blue=live, green=idle candidate) and swap traffic.
- Need faster rollback than rolling updates (instant re-point).
- Releases must keep old version runnable until green proves healthy.
- Coordinating LB listener rules, target groups, Ingress, API Gateway stages, or DNS weighted records.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Metric-driven canary / automated analysis | `canary-analysis-basics` |
| Chaos / fault injection | `chaos-engineering-basics`, `chaos-mesh-networkchaos` |
| DB migration expand/contract patterns | `database-migration-safety` |
| CI/CD pipeline wiring | `ci-cd-pipeline-patterns` |
| Feature flags without dual env | `feature-flag-patterns` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Environments | Blue (prod traffic), green (new version); labels must never be ambiguous |
| Cutover plane | L7 LB weights, target group swap, Ingress service, DNS weighted / short TTL |
| Health | Synthetic + real health checks on green **before** any production weight |
| Data plane | Forward-compatible schema; dual-write or expand/contract before cutover |
| Sessions | Sticky sessions, Redis session store, JWT stateless — plan affinity loss |
| Rollback | Keep blue warm until green soak complete; one command re-point |

## Workflow

### 1. Confirm scope and success criteria

1. Record app name, env names (blue/green identifiers), owner, change ticket, blast radius (regions, tenants).
2. Success: green receives 100% traffic with SLOs held; rollback tested; blue decommissioned only after soak.
3. Pre-declare rollback owner and maximum decision time (e.g. 5 minutes to flip back).

### 2. Inventory topology

```bash
# Examples — pick what matches your platform
kubectl get deploy,svc,ingress -n prod -o wide
aws elbv2 describe-target-groups --query "TargetGroups[].TargetGroupName"
aws elbv2 describe-rules --listener-arn "$LISTENER_ARN"
# DNS TTL awareness
dig +noall +answer app.example.com
```

1. Map: CI artifact → green deploy → health URL → cutover control → observability dashboards.
2. List shared resources: DB, queues, caches, feature flags, third-party webhooks.
3. Confirm capacity: green sized like blue for full load (not half-canary capacity unless staged).

### 3. Baseline live blue

1. Capture golden signals: latency p95/p99, error rate, saturation, business KPI (checkout success).
2. Note current version SHA/tag on blue.
3. Export LB/DNS config snapshot for rollback evidence.

### 4. Deploy and validate green (no prod traffic)

1. Deploy identical config shape with new artifact to green.
2. Run migrations that are **backward compatible** with blue still serving (`database-migration-safety`).
3. Smoke green via internal URL / test listener / hosts header — not public DNS yet.

```bash
# Internal smoke examples
curl -fsS "https://green-internal.example/healthz"
curl -fsS -H "Host: app.example.com" "https://green-lb.example/readyz"
# Contract / integration suite against green
npm run test:smoke -- --base-url "$GREEN_URL"
```

**Pre-cutover gate (all must pass):**

| Gate | Pass criteria |
| --- | --- |
| Health | `/healthz` and `/readyz` green; deps reachable |
| Version | Correct SHA/tag headers or build id |
| Migrations | Expand complete; blue still works |
| Config | Secrets/feature flags present for green |
| Synthetic | Critical user journeys pass on green |
| Security | TLS cert valid for intended hostnames |

### 5. Cutover

**Weighted LB (gradual blue-green hybrid):**

1. 5% → watch 5–15 min → 25% → 50% → 100% (or jump 0→100 if checklist-only pure swap).
2. At each step: error rate, latency, queue lag, 5xx by version tag.

**Hard swap:**

1. Flip listener default action / Ingress service / DNS to green.
2. Keep blue instances **running** and receiving zero weight.
3. Invalidate CDN if HTML/assets versioned incorrectly; prefer immutable asset URLs.

```bash
# Example: kubectl switch Service selector to green color
kubectl patch svc app -n prod -p '{"spec":{"selector":{"color":"green"}}}'
# Example: AWS weighted target forward (conceptual — use console/IaC carefully)
# Update rule weights: blue=0 green=100
```

**DNS cutover notes:**

- Lower TTL well before the window (e.g. 60s) if DNS is the switch.
- Expect client cache residual; LB switch is usually cleaner than DNS for true instant rollback.
- Update both apex and regional records if multi-region.

### 6. Post-cutover soak and drain

1. Soak period (org-defined: 30m–24h) with blue still scalable.
2. Drain in-flight: connection draining / `preStop` hooks / queue consumers finish on blue.
3. Watch for dual-version issues: cache keys, message schema, webhook retries to old hosts.
4. Only then scale blue to zero or reassign as next idle.

### 7. Rollback

```text
1. Decision: SLO burn or explicit abort
2. Re-point traffic control to blue (same mechanism as cutover)
3. Verify blue health + error rate recovery
4. Freeze green; file incident notes
5. Do NOT run irreversible “contract” DB migrations until green is permanent
```

### 8. Hand off

1. Record final version, cutover timestamps, weights history, dashboards links.
2. Tag release; update runbook with any surprise (session loss, sticky cookies).
3. Schedule blue rebuild as the new idle environment for next release.

## Compatibility Matrix

| Concern | Blue-green safe approach | Unsafe |
| --- | --- | --- |
| DB schema | Expand → deploy → contract later | Drop column while blue live |
| APIs | Additive fields; tolerant readers | Hard rename without dual support |
| Jobs | Version-aware consumers or pause | Two versions fight same partition |
| SPA assets | Content-hash filenames | `app.js` overwrite mid-cutover |
| Webhooks | Shared endpoint; idempotent handlers | IP allowlists only for blue |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Validation | Full smoke on green pre-traffic | “Deployed = live” |
| Rollback | Blue warm + one flip | Immediate terminate blue |
| Data | Expand/contract migrations | Destructive migration mid-swap |
| DNS | TTL planned + LB preferred | 1-hour TTL surprise |
| Observability | Version-dimensioned metrics | Only aggregate 5xx |
| Ownership | Named rollback commander | Chat-only improvisation |

## Output Checklist

- [ ] Scope, envs, ticket, rollback owner recorded
- [ ] Topology and cutover mechanism documented
- [ ] Blue baseline metrics captured
- [ ] Green deployed and smoke-tested without prod traffic
- [ ] Migration compatibility verified
- [ ] Cutover executed with monitored weights/swap
- [ ] Soak complete; blue drained per plan
- [ ] Rollback path dry-run or previously proven
- [ ] Release notes / runbook updated
- [ ] `code-quality-standards` / migration skills applied as needed

## Rules

- Never destroy blue until soak criteria pass.
- Schema and message changes must tolerate two app versions during the window.
- Prefer LB weight flips over long-TTL DNS for instant rollback.
- Authorized production changes only; rehearse in staging.
- Route pure canary metric analysis to `canary-analysis-basics`.
