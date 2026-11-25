---
name: chaos-mesh-networkchaos
description: >
  Chaos Mesh NetworkChaos for owned Kubernetes clusters: delay, loss, duplicate,
  corrupt, partition, direction/selectors, scheduling, and safe rollback. Use when
  Chaos Mesh network experiments, pod network latency inject, or partition tests —
  only on authorized clusters with blast-radius controls.
---

# Chaos Mesh Networkchaos

## Scope And Authorization

- **In scope:** Kubernetes clusters you operate with Chaos Mesh installed and approval.
- **Out of scope:** Injecting faults into clusters/namespaces you do not own.
- NetworkChaos can partition critical controls — exclude kube-system unless explicitly intended and approved.
- Pair with `chaos-engineering-basics` for program design.

## When To Use

- Simulating latency/loss between services in K8s.
- Testing timeouts, retries, circuit breakers under partition.
- Game days using Chaos Mesh CRDs.
- Validating multi-AZ assumptions with selective pod targets.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Chaos program / hypothesis design | `chaos-engineering-basics` |
| Pod kill / stress only | other Chaos Mesh experiment types / docs |
| Service mesh fault injection (Istio) | mesh skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| NetworkChaos mode | Effect |
| --- | --- |
| delay | Latency + jitter |
| loss | Packet drop % |
| duplicate | Packet dup |
| corrupt | Bit corruption |
| bandwidth | Throttle (if supported in version) |
| partition | Isolate directionally from targets |

Selectors: namespace, label, pod phase; external targets via direction `to` / `from`.

## Workflow

### 1. Confirm authorization and success criteria

1. Cluster, namespaces allowed, on-call, abort plan.
2. Success: experiment applies only to selected pods; hypothesis measured; clean deletion restores network.
3. Verify Chaos Mesh controllers healthy.

```bash
kubectl -n chaos-mesh get pods
kubectl get crd | rg networkchaos
```

### 2. Identify targets carefully

```bash
kubectl -n app get pods -l app=checkout -o wide
# Double-check labels before apply
```

1. Use **namespace + label** selectors; avoid empty selectors.
2. Exclude system namespaces in defaults.
3. Prefer phase-limited experiments with duration.

### 3. Write NetworkChaos manifest

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: checkout-to-payments-delay
  namespace: app
spec:
  action: delay
  mode: one            # one | all | fixed | fixed-percent | random-max-percent
  selector:
    namespaces:
      - app
    labelSelectors:
      app: checkout
  delay:
    latency: "200ms"
    correlation: "50"
    jitter: "50ms"
  direction: to
  target:
    mode: all
    selector:
      namespaces:
        - app
      labelSelectors:
        app: payments
  duration: "10m"
```

**Partition example sketch:**

```yaml
spec:
  action: partition
  mode: all
  selector:
    namespaces: [app]
    labelSelectors: { app: checkout }
  direction: both
  target:
    mode: all
    selector:
      namespaces: [app]
      labelSelectors: { app: payments }
  duration: "5m"
```

1. Always set `duration` or a schedule you control.
2. Review Chaos Mesh version fields — APIs differ slightly.

### 4. Pre-flight

1. Hypothesis + abort metrics from `chaos-engineering-basics`.
2. Confirm network plugin compatibility (CNI) with Chaos Mesh requirements.
3. Notify channel; ensure `kubectl delete` path works for your RBAC.

### 5. Apply and observe

```bash
kubectl apply -f networkchaos-delay.yaml
kubectl -n app describe networkchaos checkout-to-payments-delay
# Watch targets
kubectl -n app get pods -l app=checkout
# App metrics / traces
```

1. Validate only intended paths slow (compare control service).
2. Abort:

```bash
kubectl -n app delete networkchaos checkout-to-payments-delay
# Confirm recovery
```

### 6. Safety patterns

| Control | Practice |
| --- | --- |
| RBAC | Only chaos operators can create NetworkChaos |
| Namespace | Deny creation in prod without label gate |
| Duration | Hard cap; no infinite |
| Mode | Start `one` pod before `all` |
| Dashboard | Chaos Mesh UI restricted |
| Schedule | `Schedule` CR with off-hours if used |

### 7. Hand off

1. Store experiment YAML in repo with hypothesis doc.
2. Record outcomes; file resilience tickets.
3. Clean any residual experiments (`kubectl get networkchaos -A`).
4. Apply `code-quality-standards` to experiment GitOps.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Selector | Explicit ns+labels | Cluster-wide empty selector |
| Duration | 5–15m timed | Forgotten perpetual chaos |
| Start | mode one | All replicas all services |
| Abort | Immediate delete + verified | Leave for morning |
| Scope | app ns | Random kube-system partition |
| Docs | Hypothesis linked | Mystery YAML in cluster |

## Output Checklist

- [ ] Authorization and abort owner set
- [ ] Chaos Mesh healthy
- [ ] Selectors reviewed (no empty match-all)
- [ ] Duration set
- [ ] Hypothesis metrics watched
- [ ] Experiment applied and observed
- [ ] Deleted and recovery verified
- [ ] No residual NetworkChaos left
- [ ] Learnings ticketed
- [ ] YAML stored with review

## Rules

- Authorized clusters only; production requires extra approval.
- Never omit selectors/duration on shared clusters.
- Delete is part of the experiment — verify recovery.
- NetworkChaos is not a substitute for good timeouts — it tests them.
- Program-level practice → `chaos-engineering-basics`.
