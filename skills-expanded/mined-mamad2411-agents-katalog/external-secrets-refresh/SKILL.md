---
name: external-secrets-refresh
description: >
  External Secrets Operator refresh and rotation behavior for owned clusters:
  refreshInterval, provider-side rotation, rollout triggers, stale Secret risk,
  and forcing resync. Use when ESO secrets lag after rotation, refreshInterval
  tuning, or app pods not picking up new values. Complements
  external-secrets-operator.
---

# External Secrets Refresh

## Scope And Authorization

- **In scope:** ESO-managed secrets on clusters you operate.
- **Out of scope:** Forcing rotation on shared secrets without owner approval.
- Refresh rate trades provider API cost/rate limits vs staleness after rotation.
- Apps may cache env vars at process start—refreshing the Secret ≠ reloading the process.
- Pair with `external-secrets-operator` for store design and `secrets-management-hygiene`.

## When To Use

- Credentials rotated in Vault/SM but pods still use old values.
- Tuning `spec.refreshInterval` per secret class.
- Designing rotation: provider TTL vs ESO pull vs app reload.
- Incident: emergency revoke requires fast propagation.
- Understanding `Force sync` / annotations / controller behavior for your ESO version.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Initial ESO/store/IAM setup | `external-secrets-operator` |
| Org-wide rotation policy | `secrets-management-hygiene` |
| App env loading patterns | `env-config-12factor` |
| Implementation quality baseline | `code-quality-standards` |
| Feature flag kill | feature-flag skills |

## Domain Focus

| Area | Guidance |
| --- | --- |
| refreshInterval | Shorter for high-risk creds; longer for stable certs |
| Provider rotation | Source of truth rotates independently |
| Propagation | ESO updates K8s Secret → volume/env reload behavior |
| Rollout | Restart/rollout when env-injected (not always file watch) |
| Emergency | Manual annotate/resync + rollout |
| Observability | Last sync time, generation, errors |

## Workflow

### 1. Confirm scope and success criteria

1. Secrets in scope, max acceptable stale time, rate-limit budget.
2. Success: documented propagation path; rotation drill meets RTO.

### 2. Inventory refresh settings

```bash
kubectl get externalsecret -A -o custom-columns=\
NAME:.metadata.name,NS:.metadata.namespace,REFRESH:.spec.refreshInterval,READY:.status.conditions[0].status
```

1. Group secrets: DB passwords, API tokens, low-risk config.
2. Note apps using `env` vs mounted files vs CSI.

### 3. Baseline staleness paths

| Injection | After Secret updates |
| --- | --- |
| envFrom / env valueFrom | **No auto-reload**—needs pod restart |
| Mounted file | May see update depending on kubelet/atomic mounts |
| App reads API each time | May not use K8s Secret at all |
| Sidecar/reloader | Optional controller restarts on annotation |

### 4. Set refresh policy

```yaml
spec:
  refreshInterval: 5m   # high-churn tokens
# vs
  refreshInterval: 1h   # stable shared secrets
# vs
  refreshInterval: 24h  # rarely changing
```

1. Align with provider rotation period (refresh < TTL with margin).
2. Avoid sub-minute global intervals that hammer APIs unless required.
3. Document that refreshInterval is pull cadence—not push webhook (unless you add one).

### 5. Wire app reload

1. Prefer file mounts + apps that re-read, or
2. Use reloader tools (e.g. stakater/Reloader) keyed on Secret annotations, or
3. Explicit rollout job in rotation pipeline:

```bash
# After verifying Secret data keys changed (do not print values)
kubectl -n payments rollout restart deploy/payments-api
kubectl -n payments rollout status deploy/payments-api
```

### 6. Verify with evidence (rotation drill)

1. Rotate secret in provider (stage).
2. Wait ≤ refreshInterval or force resync per ESO docs/annotation for your version.
3. Confirm Secret resourceUpdated generation/annotations change.
4. Confirm app uses new credential (health query / canary auth).
5. Time the full path; record RTO.

### 7. Hand off

1. Runbook: emergency revoke (provider disable + force sync + restart all consumers).
2. Alerts: ExternalSecret not Ready; sync age > threshold.
3. Owners for each rotated secret and dependent deployments.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Interval | Risk-based | 24h on 1h-TTL tokens |
| App reload | Planned restart/reloader | Assume env updates live |
| Drill | Timed stage rotation | Never tested until breach |
| Force sync | Documented break-glass | SSH edit Secret manually forever |
| Cost | Balanced pull rate | 10s refresh all secrets |

## Output Checklist

- [ ] ExternalSecrets refresh intervals inventoried
- [ ] Injection method per app known
- [ ] Reload strategy defined
- [ ] Rotation drill timed with evidence
- [ ] Emergency revoke steps documented
- [ ] Alerts on stale/error sync
- [ ] Residual risk noted

## Rules

- Owned systems only; coordinate rotation with secret owners.
- Refresh ≠ process reload—design both.
- Do not print secret values while verifying.
- Store/IAM design → `external-secrets-operator`.
- Prefer short-lived credentials when possible.
