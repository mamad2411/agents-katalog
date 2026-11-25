---
name: spike-test-plan
description: Plan and execute spike tests that simulate sudden, brief traffic surges (sale launches, marketing pushes, retry storms) to validate auto-scaling, queueing, back-pressure, and graceful degradation. Use when traffic is bursty.
source: self
date_added: 2026-05-01
---

# Spike Test Plan

Spike tests model **sudden onset** — going from baseline to many multiples in seconds — and verify the system absorbs it without errors, latency cliffs, or cascading failure. Distinct from load (sustained) and stress (find the knee).

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Tool | k6 0.55 (`ramping-arrival-rate` with sharp stages), Gatling 3.13 |
| Multipliers | 5×, 10×, 20× baseline; spike duration 30s–5min |
| Defenses validated | HPA/KEDA, Karpenter, queueing, back-pressure (429/503), circuit breakers, retries-with-jitter, edge throttling (Cloudflare/CloudFront/Akamai), CDN cache shields |
| Observability | Latency heatmaps, queue depth, dropped/throttled counters, autoscaler events, cold-start counts |
| Environments | Staging mirroring prod replica baseline + autoscaler config |

## When to Use

- Pre-launch for any service that can be triggered by marketing, push notifications, sale events, or news.
- Post-incident validation of a "thundering herd" or retry storm fix.
- Validating a new autoscaler / queue / back-pressure change.
- API/Webhook receivers with bursty producers.

## Plan Structure

1. **Threat model** — list spike sources (sale start, push notification, cold cache rebuild, partner webhook retry, scrape).
2. **Spike profile**
   - **Magnitude**: 5–20× baseline RPS.
   - **Onset**: 1–10 seconds (true spike) vs. 30–60s (soft surge).
   - **Hold**: 30s–5min.
   - **Repeat**: single, double-spike (validates recovery between), or stairstep.
3. **Pre-spike state** — warm caches at baseline for 5–10 min.
4. **Defenses-in-test** — declare which mitigations are expected to engage (HPA, queue, throttle, CDN absorb).
5. **Pass criteria** — no 5xx; user-visible 429/503 budget; p99 latency cap during spike; recovery to baseline within target seconds; no DLQ growth.
6. **Observability** — autoscaler event timeline, queue depth, breaker open events, retry counters.
7. **Cleanup & repeat** — drain backlog; verify no orphaned state.

## k6 Reference Profile

```js
import http from 'k6/http';

export const options = {
  scenarios: {
    baseline: {
      executor: 'constant-arrival-rate',
      rate: 100, timeUnit: '1s',
      duration: '10m', preAllocatedVUs: 100, maxVUs: 4000,
      startTime: '0s',
    },
    spike: {
      executor: 'ramping-arrival-rate',
      startRate: 100, timeUnit: '1s',
      preAllocatedVUs: 200, maxVUs: 4000,
      startTime: '10m',
      stages: [
        { target: 1500, duration: '5s'  },   // 15× in 5s
        { target: 1500, duration: '2m'  },   // hold
        { target:  100, duration: '15s' },   // drop
        { target:  100, duration: '5m'  },   // recover
        { target: 1500, duration: '5s'  },   // double-spike
        { target: 1500, duration: '60s' },
        { target:  100, duration: '15s' },
      ],
    },
  },
  thresholds: {
    'http_req_failed{kind:5xx}': ['rate<0.001'],     // 5xx ≤ 0.1%
    'http_req_failed{kind:429}': ['rate<0.05'],      // user-visible throttle ≤ 5%
    'http_req_duration{phase:spike}': ['p(99)<1500'],
    'http_req_duration{phase:recover}': ['p(99)<400'],
  },
};

export default function () {
  const phase = __ITER < 600 ? 'baseline' : 'spike'; // approximate
  const r = http.get(`${__ENV.BASE}/products`, { tags: { phase } });
  const cls = r.status >= 500 ? '5xx' : r.status === 429 ? '429' : 'ok';
  r.tags.kind = cls;
}
```

## What to Watch (live)

- Autoscaler events: HPA scale-up time vs. spike onset (often 30–90s — usually too slow).
- Queue depth growth and drain time.
- 429/503 from the edge — desirable as a relief valve; should NOT turn into 500s downstream.
- Retry storm signals (RPS climbs **after** failure starts) → ensure jittered retries, budget breakers.
- Cold-start counts (cold replicas, cold lambdas, cold connections).
- Downstream rate-limit headers — partner APIs cap you before you cap yourself.

## Designing for Spikes (defensive checklist)

- Edge throttle / CDN cache shield enabled and sized for ≥ peak forecast.
- Pre-warmed pool / minimum replicas ≥ baseline × 1.5.
- KEDA scheduled scale-out 5 min before known events (sale launch).
- Bounded queue with shed-load (return 429 with Retry-After) instead of unbounded.
- Retries: client-side jittered exponential, **per-request budget** capped.
- Circuit breakers per downstream; fast-fail when target degraded.
- Idempotency keys mandatory on POST so safe replay doesn't double-charge.
- Log sampling under load (don't melt the log pipeline).

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| HPA expected to absorb a 5-second spike | Pre-warm or KEDA scheduled; HPA reacts in 30–90s |
| Unbounded queues "for safety" | Bounded + shed-load; unbounded queues turn into outages |
| Every error is a 5xx | Use 429/503 with Retry-After; clients must respect it |
| Retries without jitter | Synchronized retries amplify the spike |
| Profile uses closed VUs | Closed model under-loads at saturation; use open model |
| Single spike test | Double-spike validates recovery + no orphan state |
| Edge / CDN bypassed in test | Test through the real edge; absorption is half the story |
| Logging amplifies the spike | Sample at info; ensure log-fwd resilient |

## Output Format

```
Spike Test: orders-api  10× over 10s; hold 2m; double-spike 60s
Pass: ✅ with caveats
During spike:
  5xx rate           0.04%  (≤0.1%)  ✅
  429 rate           3.1%   (≤5%)    ✅
  p99 latency       1.18s   (≤1.5s)  ✅
  HPA scale-up      62s     (n/a, pre-warm engaged)
Recovery:
  p99 back to baseline   28s
  Queue drain            41s
Findings:
  - tax-svc client briefly held DB connections during retry burst — add bulkhead
  - log volume tripled; sampling kicks in correctly
Recommendation: ship; tune tax-svc bulkhead in next sprint
```

## References

- k6 — Spike testing: <https://grafana.com/docs/k6/latest/testing-guides/test-types/spike-testing/>
- AWS — Best practices for queue-based load leveling
- Marc Brooker — *Timeouts, Retries, and Backoff* (jitter)
- Heroku — Thundering herd & log compression
- Cloudflare — Cache shield: <https://developers.cloudflare.com/cache/concepts/cache-shield/>
