---
name: api-performance-testing
description: Design and execute API performance tests (load, stress, spike, soak) with k6 / Gatling / Locust, tied to SLOs, CI thresholds, and traceable bottlenecks. Use to validate latency/throughput before launch and detect regressions over time.
source: self
date_added: 2026-04-30
---

# API Performance Testing

Performance testing answers: *will the API meet its SLOs under expected and adverse conditions?* Not "is it fast?".

## Stack Baseline (2026)

| Tool | Strength |
| --- | --- |
| k6 0.55+ / k6 cloud | JS scripting, scenarios, browser, gRPC, native trends + thresholds |
| Gatling 3.13 | High-throughput JVM, Scala/Java/Kotlin DSL, rich reports |
| Locust 3.x | Python, distributed, easy custom logic |
| JMeter 5.6 | Legacy/large libraries, GUI |
| NBomber 5 | .NET-native |

Pair the runner with: APM (Datadog/New Relic/Honeycomb), tracing (OTel), DB profiling (pg_stat_statements), runtime profiles (async-profiler, pprof).

## When to Use Each Test Type

| Type | Question | Pattern |
| --- | --- | --- |
| Load | Does it meet SLOs at expected RPS? | Ramp to target, hold 30+ min |
| Stress | Where does it break? | Ramp until failure, observe knee |
| Spike | How does it react to sudden surge? | 10× within 30s, hold, drop |
| Soak | Does it leak/degrade over hours? | Target RPS for 4–24 h |
| Capacity | What's max sustainable RPS? | Step-load, find SLO knee |

## SLO-First Design

1. Source p50/p95/p99, error rate, throughput, and saturation targets from the SLO doc.
2. Encode them as runner thresholds — fail the build when violated.
3. Use **realistic** traffic mix (read/write ratio, payload sizes) from prod telemetry.

## k6 Example with Thresholds

```js
import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  scenarios: {
    steady: { executor: 'constant-arrival-rate', rate: 200, timeUnit: '1s',
      duration: '30m', preAllocatedVUs: 100, maxVUs: 500 },
  },
  thresholds: {
    http_req_failed: ['rate<0.005'],
    http_req_duration: ['p(95)<300', 'p(99)<800'],
    'http_req_duration{endpoint:checkout}': ['p(95)<450'],
  },
};
export default function () {
  const r = http.post(`${__ENV.BASE}/checkout`, JSON.stringify({}),
    { headers: { 'Content-Type': 'application/json' }, tags: { endpoint: 'checkout' } });
  check(r, { 'status 2xx': (r) => r.status < 300 });
  sleep(0.5);
}
```

## Workload Modeling

- Closed-model (VUs) for browser-like users; **open-model (arrival rate)** for APIs (recommended — avoids coordinated omission).
- Think time, pacing, ramp shape match prod patterns.
- Include cache-cold and cache-warm scenarios.

## Environment & Data

- Prod-like infra (same instance class, autoscaling settings, data volume).
- Isolated network; dedicated DB snapshot.
- Pre-seeded data sized to prod (record counts, index distribution).
- Disable test users from analytics; tag traffic with `x-load-test: true`.

## Bottleneck Diagnosis Loop

1. Reproduce; capture run_id.
2. Correlate runner timeline with APM/traces/logs by run_id tag.
3. RED + USE: latency, traffic, errors + utilization, saturation, errors per resource.
4. Drill: slow query? GC pause? lock contention? thread-pool exhaustion? downstream throttle?
5. Fix one thing; re-run; document delta.

## CI Integration

- Smoke perf (1 min, low RPS) on PR — guard against gross regressions.
- Full load nightly on staging.
- Trend report (p95, error rate) tracked over time; alert on > 10% regression vs 7-day median.

## Common Pitfalls

| Pitfall | Avoidance |
| --- | --- |
| VU count as "load" | Use arrival-rate; report RPS |
| Single warm endpoint hit | Realistic mix from prod |
| Coordinated omission ignored | Open model + record full distribution |
| Test machine is the bottleneck | Distribute load gen; monitor injectors |
| One-shot test, no trending | Persist results; alert on regression |
| Tests on dev hardware | Prod-like or budget-corrected |

## References

- k6 docs — https://grafana.com/docs/k6/
- Gatling docs — https://docs.gatling.io/
- Brendan Gregg — USE method — https://www.brendangregg.com/usemethod.html
- Gil Tene — "How NOT to Measure Latency" (coordinated omission)
- Google SRE Workbook — SLOs
