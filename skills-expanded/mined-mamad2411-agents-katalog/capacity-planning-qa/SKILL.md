---
name: capacity-planning-qa
description: Forecast required capacity (CPU, memory, IOPS, network, DB connections, replicas) using load-test outputs, traffic forecasts, headroom and cost models. Use before launches, scale events, and quarterly planning.
source: self
date_added: 2026-05-01
---

# Capacity Planning (QA)

Capacity planning turns measured **service capacity** into a **provisioning recommendation** that meets SLOs at forecast load with budgeted headroom — and proves it with experiments, not vibes.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Inputs | RPS forecast (per endpoint), request mix, p95/p99 SLOs, growth rate, peak-to-mean ratio |
| Test types | Load (sustained), Stress (find knee), Spike, Soak (endurance) |
| Tools | k6, Gatling, Locust, Vegeta; Kubernetes HPA/KEDA, AWS Auto Scaling, Karpenter |
| Models | Little's Law (`L = λW`), Universal Scalability Law (USL), queueing theory (M/M/c) |
| Forecasting | Prophet, simple seasonal+trend, business calendar (BFCM, sale events) |
| Cost | per-replica cost, GB-hour, request-cost, FinOps tagging |

## When to Use

- Pre-launch sizing of a new service.
- Quarterly capacity review.
- Major marketing event (Black Friday, sale, SuperBowl spot).
- Migration / re-architecture forecast.
- Cost optimization (over-provisioned vs. SLO).

## Method

1. **Forecast the load**
   - Per endpoint: median RPS, peak RPS, peak-to-mean ratio, growth rate (YoY).
   - Compose from business drivers (orders/sec → API calls fan-out).
2. **Define SLOs** clearly (p95 latency, error rate, availability) — capacity is meaningless without a target.
3. **Measure capacity** via load + stress tests:
   - **Steady-state capacity**: max RPS where SLO holds for 60+ min on N replicas.
   - **Knee point**: RPS where p99 starts to climb non-linearly (Stress).
4. **Per-replica capacity** = steady-state ÷ replicas.
5. **Required replicas** = `peak_RPS / per_replica_capacity × (1 + headroom)`. Headroom 30–50% covers spikes, deploys, AZ failure.
6. **Apply Little's Law** to size pools (DB connections, threadpool, queue depth):
   `concurrency = throughput × latency`
7. **USL fit** to detect contention/coherency before they bite at scale.
8. **Validate** — run a **soak** at predicted peak for 2+ hours. Confirm no leaks, no GC drift, no DB connection blow-up.
9. **Cost** the recommendation; explore alternatives (smaller replica + more, or vice versa) and pick best $/RPS at SLO.

## Worked Example

- Forecast peak: 1,200 RPS on `/checkout` for BFCM 2026 (current peak 480, growth 1.5x year-on-year, marketing 1.6x lift).
- SLO: p99 ≤ 600ms, error rate ≤ 0.5%.
- Measured per-replica capacity: 60 RPS at SLO (`m6i.large`, 2 vCPU, 4 GB).
- Required replicas: `1200 / 60 × 1.4 (headroom) = 28`.
- DB pool sizing (Little's Law): peak DB throughput ≈ 1,200 × 1.4 = 1,680 q/s; mean q latency 5 ms → concurrency 8.4 → pool size 12 per replica × 28 = 336 (verify Postgres `max_connections`; use PgBouncer transaction-pooling if > server limit).
- Verify with soak at 1,200 RPS × 2 h. Watch heap, GC, DB locks, S3 throttling.
- Cost: 28 × $73/mo + DB step-up + cache → $X — compare alternatives.

## Code

### k6 Soak

```js
export const options = {
  scenarios: {
    soak: { executor: 'constant-arrival-rate', rate: 1200, timeUnit: '1s', duration: '2h', preAllocatedVUs: 600, maxVUs: 1500 }
  },
  thresholds: { http_req_failed: ['rate<0.005'], http_req_duration: ['p(99)<600'] }
};
```

### USL fit (Python)

```python
import numpy as np
from scipy.optimize import curve_fit
def usl(N, lam, sigma, kappa):  # Gunther's USL
    return (lam * N) / (1 + sigma * (N - 1) + kappa * N * (N - 1))
N  = np.array([1, 2, 4, 8, 16, 32])
X  = np.array([60, 118, 232, 430, 720, 950])    # measured throughput per replica count
popt, _ = curve_fit(usl, N, X, p0=[60, 0.05, 0.001], maxfev=10000)
print('lambda, sigma, kappa =', popt)
```

`sigma` is contention; `kappa` is coherency cost. Use to predict ceiling before hitting it.

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| "Just enable autoscaling" | HPA reacts on minutes; spikes happen in seconds — pre-warm or KEDA + scheduled scaling |
| Per-replica capacity from a tiny test | Test at the actual replica spec & with realistic mix |
| Ignoring downstream limits (DB, 3rd-party) | DB connections / API rate-limits often bottleneck before app |
| Headroom guessed | Use AZ failure scenario as headroom anchor (lose 1/3 capacity, still meet SLO) |
| Forecasting from last year only | Add growth + marketing lift + a buffer scenario |
| No soak | Leaks and GC drift only show in 2+ h tests |
| Cost not part of plan | Always present 2–3 cost/perf options |
| Plan never re-validated | Re-test post-launch and quarterly |

## Output Format (capacity plan)

```
Service: orders-api
Forecast peak: 1200 RPS @ 2026-11-29 14:00 UTC
SLO: p99 600ms, error 0.5%, availability 99.9%
Per-replica capacity: 60 RPS (m6i.large)
Recommendation:
  - Replicas: 28 baseline + HPA to 40 (+headroom for AZ loss)
  - DB pool: 12/replica via PgBouncer, max_connections=400
  - Cache: Redis cluster x 3 shards (rps × 0.4 hit-bypass)
Cost (mo): $5,180 baseline + $0.08/extra-RPS-hour scale-out
Validation: soak passed at 1200 RPS × 2h; p99 488ms; 0 errors
Alternates considered:
  A. 56 × m6i.medium → +$420/mo, +headroom
  B. 14 × m6i.xlarge → −$340/mo, lower bin-pack risk
Re-test trigger: forecast change >10% or replica spec change
```

## References

- B. Gregg — *Systems Performance* 2e
- N. Gunther — *Guerrilla Capacity Planning* (USL)
- Google SRE Book — Capacity planning chapters
- Little's Law: <https://en.wikipedia.org/wiki/Little%27s_law>
- k6 Soak: <https://grafana.com/docs/k6/latest/testing-guides/test-types/soak-testing/>
