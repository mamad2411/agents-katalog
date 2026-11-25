---
name: envoy-outlier-detection
description: >
  Envoy outlier detection for owned meshes/proxies: eject unhealthy upstream
  hosts on 5xx, consecutive gateway failures, success rate, and local origin
  errors; tune interval, base ejection time, max ejection percent. Use when
  cluster outlier_detection, panic threshold interaction, or flapping upstreams.
---

# Envoy Outlier Detection

## Scope And Authorization

- **In scope:** Envoy/Istio/service mesh clusters you operate.
- **Out of scope:** Tuning third-party public endpoints you do not own as a DoS.
- Aggressive ejection can reduce capacity—coordinate with SRE and error budgets.
- Test in stage with chaos before production tightening.
- Pair with `error-budget-policy-design` and retry/timeout skills.

## When To Use

- One bad pod/host poisoning a cluster with 5xx.
- Configuring passive health checks alongside active health checks.
- Investigating flapping ejection / insufficient capacity after eject.
- Aligning outlier settings with retry budgets to avoid retry storms.
- Reviewing Istio `DestinationRule` outlierDetection.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| ext_authz design | `envoy-ext-authz-basics` |
| Active health check only deep dive | Envoy HC docs + platform skill |
| SLO error budget policy | `error-budget-policy-design` |
| Load shedding product logic | resilience skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Consecutive 5xx | Eject after N consecutive errors |
| Success rate | Eject hosts below threshold in interval |
| Gateway failures | Connect/timeout errors as local origin |
| max_ejection_percent | Cap capacity loss (e.g. 10–50%) |
| base_ejection_time | Backoff; grows with eject count |
| Panic threshold | Host selection panic if too few healthy—align carefully |

## Workflow

### 1. Confirm scope and success criteria

1. Clusters/services, current error rates, min healthy hosts required.
2. Success: single bad host ejects quickly; cannot eject entire cluster; recovery automatic.

### 2. Inventory current settings

```bash
curl -s http://127.0.0.1:9901/config_dump | rg -n "outlier_detection" -A20
# Istio
kubectl get destinationrule -A -o yaml | rg -n "outlierDetection" -A15
```

1. Note active health checks already configured.
2. Capture baseline eject metrics if any.

### 3. Baseline failure modes

| Symptom | Possible cause |
| --- | --- |
| Sticky 5xx from one pod | Need consecutive_5xx eject |
| All hosts flapping | Thresholds too tight / shared dependency down |
| Traffic to zero hosts | max_ejection_percent too high + panic |
| Slow recovery | base_ejection_time too long |

### 4. Configure outlier detection (illustrative)

```yaml
clusters:
  - name: my_service
    connect_timeout: 0.25s
    outlier_detection:
      consecutive_5xx: 5
      interval: 10s
      base_ejection_time: 30s
      max_ejection_percent: 50
      enforcing_consecutive_5xx: 100
      success_rate_minimum_hosts: 3
      success_rate_request_volume: 100
      success_rate_stdev_factor: 1900
      consecutive_gateway_failure: 5
      enforcing_consecutive_gateway_failure: 100
```

```yaml
# Istio DestinationRule fragment
spec:
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 50
```

1. Start conservative; tighten using metrics.
2. Coordinate **retries**: retries to other hosts OK; unbounded retries amplify load.
3. Split bulkheads: dependency outage should not eject all hosts if errors are uniform—outlier helps **heterogeneous** host health.

### 5. Observe metrics

1. `cluster.my_service.outlier_detection.ejections_active`
2. `ejections_enforced_total` / detected counters
3. Upstream success rate and P99 latency during ejection events
4. Alert if ejected percent high for prolonged time (systemic issue, not one bad host)

### 6. Verify with evidence

1. Stage: inject 500s on one replica → that host ejects; others serve traffic.
2. Stage: all replicas 500 → cluster does not eject beyond max; panic/behavior documented.
3. Host recovery after healthy interval returns to pool.

### 7. Hand off

1. Runbook: systemic outage vs single bad pod.
2. Link dashboards; document interaction with HPA (eject ≠ scale).
3. Review settings when changing timeout/retry policy.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Cap | max_ejection_percent set | Can eject 100% silently |
| Tuning | Data-driven interval | Copy blog values blindly |
| Retries | Bounded + budgets | Infinite retry on 5xx |
| Uniform fail | Treat as dependency SEV | Eject all hosts pointlessly |
| Recovery | Automatic uneject | Manual only forever |

## Output Checklist

- [ ] Clusters in scope inventoried
- [ ] Outlier settings applied with max ejection cap
- [ ] Interaction with retries/timeouts reviewed
- [ ] Chaos evidence for single-host and all-host failure
- [ ] Metrics and alerts for prolonged ejection
- [ ] Runbook updated
- [ ] Residual risk noted

## Rules

- Owned proxies only; chaos in authorized env.
- Never remove ejection caps “to fix” capacity without root cause.
- Outlier is passive HC—not a substitute for fixing bad deploys.
- Align with error budgets for how aggressive to be.
- ext_authz is a different filter → `envoy-ext-authz-basics`.
