---
name: bulkhead-isolation
description: >
  Bulkhead isolation for owned services: partition capacity by dependency or tenant,
  limit concurrent calls, isolate thread/connection pools, fail fast with fallbacks,
  and protect core paths from noncritical storms. Use when bulkhead pattern, isolate
  dependency pool, cabin partition, or noisy-neighbor concurrency limits — pair with
  `bulkhead-threadpool-isolation` for thread-pool specifics.
---

# Bulkhead Isolation

## Scope And Authorization

- **In scope:** Services and platforms you operate.
- **Out of scope:** Load-testing third-party APIs beyond agreements; intentional customer DoS.
- Validate in staging with production-like pool sizes.
- Redact tenant identifiers in public postmortems as required.
- Pair with `retry-backoff-patterns`, circuit breakers, and `code-quality-standards`.

## When To Use

- One dependency (or tenant) can exhaust shared workers/connections and stall everything.
- You need separate ceilings for critical vs noncritical outbound calls.
- Designing graceful degradation: search can fail while checkout continues.
- Reviewing microservice mesh timeouts without pool isolation (incomplete resilience).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Thread pool mechanics in detail | `bulkhead-threadpool-isolation` |
| Retry/backoff only | `retry-backoff-patterns` |
| Cache stampede | `cache-stampede-defense` |
| Full chaos experiments | `chaos-engineering-basics` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Bulkhead type | Isolates | Example |
| --- | --- | --- |
| Dependency | Outbound client resources | Payments pool vs analytics pool |
| Tenant / customer | Noisy neighbor | Per-tenant concurrency caps |
| Feature / priority | Critical path | Checkout vs recommendations |
| Data plane | DB pools | Read replica pool vs write |
| Compute | Queues / workers | Separate worker groups |

**Companion patterns:** timeouts, circuit breaker, load shedding, admission control.

## Workflow

### 1. Confirm scope and success criteria

1. List critical user journeys and their dependencies.
2. Success: injected dependency latency/errors do not breach critical SLO; dashboards show per-bulkhead saturation.
3. Define failure UX (stale data, hide widget, fail request).

### 2. Inventory shared resources

```text
# Map shared choke points
- app server worker threads / event loop blocking
- HTTP client max connections / streams
- DB pool size
- queue consumers
- memory / CPU cgroup limits
```

1. Find “one client bean” used for all outbound HTTP.
2. Find global DB pool shared by background jobs and user requests.
3. Identify multi-tenant keys for noisy-neighbor risk.

### 3. Baseline behavior

1. Load test with slow dependency (controlled) and measure error rates of unrelated endpoints.
2. Capture pool metrics: active/idle/wait, queue depth, rejections.
3. Document current timeouts (often missing).

### 4. Design bulkheads

**Rules of thumb:**

1. Separate **connection + concurrency limits** per dependency.
2. Size sum of bulkheads ≤ process capacity (leave headroom).
3. Prefer fail-fast rejection (`429`/`503` with retry-after) over unlimited queueing.
4. Critical bulkheads get reserved capacity that noncritical cannot borrow (or only borrow under policy).

**Example partitioning:**

| Bulkhead | Max concurrent | Timeout | Fallback |
| --- | --- | --- | --- |
| `payments` | 40 | 2s | fail order hard |
| `recommendations` | 20 | 200ms | empty list |
| `email` | 10 | 1s | async queue |
| `tenant_default` | 10 per tenant | — | 429 |

```java
// Conceptual resilience4j-style bulkhead
BulkheadConfig.custom()
  .maxConcurrentCalls(20)
  .maxWaitDuration(Duration.ZERO) // fail fast
  .build();
```

```python
# Conceptual: separate httpx clients / limits per dependency
limits_payments = httpx.Limits(max_connections=40, max_keepalive_connections=20)
limits_recs = httpx.Limits(max_connections=20, max_keepalive_connections=10)
```

### 5. Implement and wire observability

1. Metrics: `bulkhead_accepted`, `bulkhead_rejected`, `bulkhead_in_use`, wait time.
2. Logs: rejection reason without flooding (sample).
3. Trace attributes: dependency name, bulkhead name.
4. Alerts: sustained rejection on critical bulkhead; saturation >80%.

### 6. Verify

```bash
# Staging: chaos latency on recommendations dependency only
# Expect: home page recommendations degrade; checkout success stable
k6 run scripts/checkout_under_rec_latency.js
```

1. Prove noncritical storm → rejects/fallbacks; critical success rate holds.
2. Prove bulkhead too small → intentional reject metrics (tune).
3. Test retry interaction: retries must not bypass bulkhead (amplification).

### 7. Hand off

1. Runbook: which features degrade when bulkhead X rejects.
2. Capacity review when traffic doubles — resize deliberately.
3. Code review checklist: new dependency requires new bulkhead, not shared client.
4. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Pools | Per dependency limits | One global HTTP pool for all |
| Queues | Bounded + fail fast | Unbounded wait queue |
| Critical path | Reserved capacity | Best-effort share equally under load |
| Retries | Respect bulkhead | Retry storms punch through |
| Tenants | Per-tenant caps | One tenant fills all workers |
| Proof | Fault injection evidence | “We set a timeout so we’re fine” |

## Output Checklist

- [ ] Critical journeys and dependencies mapped
- [ ] Shared pools inventoried
- [ ] Bulkhead matrix (limits, timeouts, fallbacks) documented
- [ ] Implementation per dependency/tenant as designed
- [ ] Metrics and alerts live
- [ ] Staging fault injection proves isolation
- [ ] Retry/circuit breaker interaction reviewed
- [ ] Runbook updated
- [ ] `code-quality-standards` applied

## Rules

- Isolation without timeouts is incomplete; combine patterns.
- Sum of bulkheads must fit process/DB capacity.
- Fail fast on noncritical; protect revenue paths first.
- Authorized load/chaos only.
- For executor/thread-pool detail use `bulkhead-threadpool-isolation`.
