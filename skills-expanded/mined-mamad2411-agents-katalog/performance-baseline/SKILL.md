---
name: performance-baseline
description: Establish a reproducible performance baseline (latency, throughput, resource usage, cost-per-request) per service, version-tagged, used for regression detection. Use when standing up perf testing or before optimization work.
source: self
date_added: 2026-05-01
---

# Performance Baseline

A baseline is the fingerprint of a service at a specific version + environment. Without it, you can't detect regression, claim improvement, or plan capacity.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Captured signals | p50/p95/p99 per endpoint, error rate, throughput, CPU/Mem/IO, GC pause, alloc rate, DB latency, $/1k req |
| Storage | Metrics in long-term Prometheus / VictoriaMetrics, summary in repo as JSON + dashboard link |
| Comparison | Git-tagged baselines (`baseline/<service>/<sha>`); diff via script in CI |
| Tools | k6, Gatling, OTel, Prometheus, Grafana, FinOps tags |
| Frequency | Weekly nightly + every release tag + on-demand pre-optimization |

## When to Use

- Standing up perf testing for a new service.
- Locking-in a known-good state before refactor / framework upgrade.
- Detecting drift release-over-release.
- Producing artifacts for vendor or customer perf SLAs.

## What Goes Into a Baseline

1. **Identity** — service, version SHA, environment (replica count, instance type, JVM flags), test profile, date.
2. **Workload definition** — realistic mix, RPS, ramp, duration, dataset cardinality, auth state. The same script must be re-runnable.
3. **Output metrics**
   - Latency: p50, p90, p95, p99, p99.9 per endpoint
   - Throughput: requests/s achieved vs. offered
   - Errors: rate by status class and by endpoint
   - Saturation: CPU%, mem RSS, heap, GC pause time/rate, sockets, FDs
   - Downstream: DB query p99, cache hit %, 3rd-party p99
   - Cost: $/1k req (sum of replica + DB + egress)
4. **Environment fingerprint** — k8s replica spec, JDK version, kernel, libc, NIC, region.
5. **Hash of test script** so future runs are unambiguous.

## Baseline Workflow

1. Wait for steady state (caches warm, JIT settled) — 5–10 min ramp + 30 min hold.
2. Run **N=3** consecutive runs; report median values.
3. Capture environment fingerprint and script hash.
4. Persist artifacts: `baselines/<service>/<sha>.json` + dashboard URL.
5. Compare against previous baseline; gate CI on regression budget.

## File Format

```json
{
  "service": "orders-api",
  "git_sha": "a1b2c3d",
  "tag": "v3.14.0",
  "env": { "replicas": 12, "instance": "m6i.large", "java": "21.0.6+9", "region": "eu-west-1" },
  "profile": { "rps": 800, "ramp_s": 300, "steady_s": 1800, "mix_hash": "sha256:7f..." },
  "metrics": {
    "endpoint": {
      "GET /products":      { "p50": 22, "p95": 138, "p99": 286, "rps": 558.6, "err_pct": 0.0 },
      "GET /products/:id":  { "p50": 38, "p95": 196, "p99": 410, "rps": 199.2, "err_pct": 0.0 },
      "POST /checkout":     { "p50": 71, "p95": 248, "p99": 612, "rps": 39.8,  "err_pct": 0.18 }
    },
    "cpu_pct_p99": 64.2,
    "heap_used_max_mb": 1488,
    "gc_pause_p99_ms": 41,
    "db_query_p99_ms": 18,
    "dollar_per_1k_req": 0.0072
  },
  "dashboard": "https://grafana/d/abc123?from=...&to=..."
}
```

## CI Regression Gate

```yaml
- name: perf baseline diff
  run: |
    node scripts/perf-diff.js baselines/orders-api/main.json baselines/orders-api/${{ github.sha }}.json
  env:
    BUDGET_LATENCY_P99_PCT: 5     # fail if any p99 worsens > 5%
    BUDGET_ERROR_RATE_ABS: 0.001
    BUDGET_COST_PCT: 5
```

```js
// scripts/perf-diff.js (essence)
const a = require(process.argv[2]); const b = require(process.argv[3]);
let fail = false;
for (const [ep, m] of Object.entries(b.metrics.endpoint)) {
  const base = a.metrics.endpoint[ep]; if (!base) continue;
  const drift = (m.p99 - base.p99) / base.p99 * 100;
  if (drift > Number(process.env.BUDGET_LATENCY_P99_PCT)) {
    console.error(`FAIL ${ep} p99 ${base.p99}ms → ${m.p99}ms (+${drift.toFixed(1)}%)`); fail = true;
  }
}
process.exit(fail ? 1 : 0);
```

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Single run baseline | Median of N=3, also store min/max |
| Comparing across environments | Pin env (replicas, instance type, region); baseline is env-scoped |
| Not capturing script hash | Future "same test" diverges silently — hash the workload |
| Average latency baselines | Tail (p95/p99) is what users feel and what regresses first |
| Ignoring cost | Include $/1k req — perf wins that double cost are losses |
| Stored only in Grafana | Persist JSON + dashboard URL in repo for diffability |
| Re-baselining on every regression | Re-baseline only on intentional, justified changes |

## Output Format

```
Baseline: orders-api v3.14.0 (sha a1b2c3d)
Run: 2026-05-01T10:00Z  N=3 (median)
Endpoints (p99 ms / rps / err%):
  GET /products             286 / 558.6 / 0.00
  GET /products/:id         410 / 199.2 / 0.00
  POST /checkout            612 /  39.8 / 0.18
CPU p99 64% | Heap max 1.5GB | GC p99 41ms | $/1k req $0.0072
Dashboard: <link>
Diff vs v3.13.0: latency +1.2% / cost −3.5% / errors flat   ✅ within budget
```

## References

- Google SRE Workbook — *Implementing SLOs*
- B. Gregg — *Systems Performance* 2e (latency, percentiles)
- k6 docs — Test types & metrics
- OpenTelemetry semantic conventions for HTTP
- FinOps Foundation — Unit economics
