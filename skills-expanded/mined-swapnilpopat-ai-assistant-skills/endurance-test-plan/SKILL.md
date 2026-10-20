---
name: endurance-test-plan
description: Plan a soak/endurance test (2–72h+) to detect leaks, drift, GC degradation, connection pool starvation, log/disk fill, and certificate/clock issues. Use before launch, after major changes, and quarterly for critical services.
source: self
date_added: 2026-05-01
---

# Endurance (Soak) Test Plan

Short load tests miss slow killers — heap creep, file-descriptor leaks, log rotation, certificate expiry, midnight cron spikes, GC pause drift, DB bloat. Soak tests reveal them.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Duration | 2 h smoke, 24 h standard, 72 h pre-launch |
| Tools | k6 0.55 (`constant-arrival-rate`), Gatling 3.13, Locust 3, Vegeta |
| Profile | Steady arrival rate at ~70–80% of measured capacity, realistic request mix |
| Observability | Prometheus + Grafana dashboards, OTel traces, JFR/JFR-collect, GC logs, heap snapshots at intervals, log volume metric |
| Infra | Mirror prod replica count, instance type, dependency latencies |
| Data | Realistic ID space; rotate users; idempotency keys; log archival |

## When to Use

- Pre-launch readiness for a service or new major version.
- After memory model changes (new framework version, native libs, JVM upgrade).
- Quarterly for tier-1 services.
- After incidents that point to drift (slow leak, unbounded growth).

## Plan Structure

1. **Goal & success criteria** — e.g., "Service maintains SLO over 24 h at 70% capacity; heap, fd, conn-pool stable; no error-rate drift > 0.05%/h."
2. **Load profile**
   - Constant arrival rate (open model) — not closed VUs (which mask saturation).
   - Realistic mix per endpoint (writes, reads, expensive paths).
   - Embedded "ambient" tasks (cron, batch) at their normal cadence.
3. **Environment** — staging or pre-prod sized like prod; downstream dependencies real (or contract-realistic mocks with realistic latency).
4. **Observability checklist (must be on dashboards)**
   - p50/p95/p99 latency per endpoint
   - Error rate per endpoint
   - CPU/Mem/Heap/RSS, GC pause time/rate, GC promoted bytes
   - Open file descriptors, sockets, threads, connections
   - DB connection pool used, wait time, deadlocks; DB CPU; replication lag
   - Cache hit ratio, eviction rate
   - Disk usage (logs, tempfs), inode count
   - Outbound 3rd-party rate-limit consumption
   - Certificate days-to-expiry visible (catches mid-soak rotations)
5. **Markers** — emit a marker every hour into logs/metrics for easy dashboard correlation.
6. **Failure injection (optional)** — trigger a single restart at hour 6 and 18 to confirm graceful behavior under cumulative load.
7. **Exit criteria** — see below.
8. **Post-test analysis** — heap diff, GC reports, top queries, log volume per hour, error timeline.

## Exit Criteria

- Latency p99 drift ≤ 10% over the run.
- Error rate ≤ SLO and not increasing.
- Heap usage stable (sawtooth around steady mean) — RSS growth ≤ 5%/24h.
- GC pause p99 stable; promoted bytes per minute stable.
- File descriptors / sockets / threads stable (no monotonic growth).
- DB connection pool wait time near zero; no growth.
- Disk usage growth predictable (log rotation works).
- 0 OOM, 0 segfault, 0 unintended restart.
- All restart cycles recovered within RTO.

## Code

### k6 24 h soak

```js
import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  scenarios: {
    soak: {
      executor: 'constant-arrival-rate',
      rate: 800,           // 70% of measured peak capacity
      timeUnit: '1s',
      duration: '24h',
      preAllocatedVUs: 400,
      maxVUs: 1500,
    }
  },
  thresholds: {
    http_req_failed: ['rate<0.005'],
    'http_req_duration{kind:read}':  ['p(99)<400'],
    'http_req_duration{kind:write}': ['p(99)<700'],
  },
};

const mix = [
  { w: 70, fn: () => http.get(`${__ENV.BASE}/products`,    { tags: { kind: 'read' }})  },
  { w: 20, fn: () => http.get(`${__ENV.BASE}/orders/me`,    { tags: { kind: 'read' }})  },
  { w: 10, fn: () => http.post(`${__ENV.BASE}/cart`, '{"sku":"A"}', { tags: { kind: 'write' }}) },
];

export default function () {
  const r = Math.random() * 100;
  let acc = 0;
  for (const t of mix) { acc += t.w; if (r < acc) { t.fn(); break; } }
  sleep(0.05);
}
```

### Heap snapshot every 6h (Java)

```bash
while true; do
  jcmd $PID GC.heap_dump /perf/heap-$(date +%H).hprof
  sleep 21600
done
```

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Closed-model VUs (Vegeta closed loop) | Use open model — VUs add back-pressure that hides saturation |
| Restart-then-soak | Soak from steady state; restart hides leaks via reset |
| Mocked downstreams with no latency | Inject realistic latencies; mocks at 0ms aren't realistic |
| No markers / no rolling dashboards | Hourly markers + 24h Grafana boards required |
| Auto-scaling masking growth | Pin replicas for the soak |
| Log volume not measured | Disk fills from `INFO` floods are common |
| Certs / tokens rotating mid-soak | Test deliberately across rotation boundaries |
| Stopping at the first wobble | Investigate before aborting — wobbles are why we soak |

## Output Format

```
Soak: orders-api  rate=800 RPS  duration=24h  replicas=12 (pinned)
Result: ✅ Pass
Latency drift:  p99 318→335ms (+5.3%) within 10% budget
Errors:         0.07% steady; no upward trend
Heap:           sawtooth 1.2–1.6GB; old gen stable
GC:             pause p99 41→44ms; promoted bytes flat
Threads/FDs:    flat
DB pool:        wait 0; max in-use 9/12
Disk:           +180MB logs (rotated 4×)  ✅
Restarts:       2 controlled at h6 / h18, both recovered < 90s
Findings:
  - Cache eviction rate doubled after h12 (look at Redis maxmemory)
  - Outbound to tax-svc rate-limit 92% of quota (consider local quota)
```

## References

- k6 — Soak: <https://grafana.com/docs/k6/latest/testing-guides/test-types/soak-testing/>
- B. Gregg — *Systems Performance* 2e
- Brendan Gregg — heat maps for latency: <https://www.brendangregg.com/HeatMaps/latency.html>
- Google SRE Workbook — Eliminating Toil & On-call
- JEP 425 (Loom), 405 (Pattern Matching) GC docs for JVM
