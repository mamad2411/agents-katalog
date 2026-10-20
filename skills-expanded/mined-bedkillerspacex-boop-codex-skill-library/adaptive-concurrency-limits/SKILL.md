---
name: adaptive-concurrency-limits
description: >
  Adaptive concurrency limits (TCP Vegas / gradient-style) for owned gateways and
  clients: limit in-flight requests from latency or outstanding work signals, shed load
  before collapse, and export limit gauges. Use when stabilizing microservices under
  overload, tuning Envoy/app concurrency, or replacing static max-concurrent with
  feedback control — not for DoS against third parties.
---

# Adaptive Concurrency Limits

## Scope And Authorization

- **In scope:** services, gateways, and clients you operate.
- **Out of scope:** load testing or overload experiments on systems without authorization.
- Change limits in staging first; production changes need rollback and dashboards.
- Redact customer identifiers from latency debug samples.
- Pair implementation with `code-quality-standards` and observability skills.

## When To Use

- Static thread/connection pools thrash under dependency slowdown (queue explosion).
- You need **auto-tuning concurrency** based on RTT/latency gradient (Vegas-like).
- Implementing Netflix concurrency-limits style algorithms, Resilience4j, or Envoy adaptive concurrency.
- Protecting databases or downstreams with client-side in-flight caps.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| HTTP API rate-limit / quota design | `api-rate-limit-design` |
| Retry / backoff patterns | `retry-backoff-patterns` |
| Observability metrics/tracing | `observability-metrics-tracing` |
| Classic load-test tooling only | perf / k6 skills in catalog |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Meaning |
| --- | --- |
| Concurrency limit `L` | Max in-flight requests (not QPS alone) |
| Vegas-like control | Raise `L` when latency ≈ baseline min; lower when latency inflation detected |
| Gradient / AIMD | Adjust `L` from gradient of latency vs inflight or additive-increase/multiplicative-decrease |
| Load shedding | Reject or fail-fast when inflight would exceed `L` |
| Long-lived vs short | Streams/WebSockets need separate budgets |
| Fairness | Per-route or per-tenant limits to avoid noisy neighbors |

**Relation to rate limits:** rate limits bound arrivals over time; concurrency limits bound simultaneous work — both often required.

## Workflow

### 1. Confirm scope and success criteria

1. Record service, critical dependencies, SLO latency, current static pools.
2. Success: under load spike, p99 degrades gracefully with controlled 503/429; dependency CPU stable; limit gauge adapts without oscillation storms.
3. Identify where to enforce: client SDK, app middleware, Envoy filter, mesh.

### 2. Baseline metrics

```text
# Required signals
- inflight_requests
- latency (RTT or handler time) — preferably EWMA
- success / timeout / 5xx rates
- queue depth if async
- current_limit gauge
```

```bash
# Example: scrape existing metrics
curl -sS localhost:9090/metrics | rg 'inflight|latency|concurrency'
```

1. Capture min RTT / no-load latency as `L_min` baseline window.
2. Note timeout configs — adaptive limits interact poorly with huge timeouts.

### 3. Choose algorithm and placement

| Placement | Pros | Cons |
| --- | --- | --- |
| Client library | Protects each dependency | Many clients to upgrade |
| App middleware | Single service control | Language-specific |
| Envoy adaptive concurrency | Central mesh policy | Learning curve / version features |

**Vegas-style sketch:**

```text
on_response(rtt):
  if rtt ≈ rtt_min: limit += increase (slow start / probe)
  if rtt > rtt_min * (1 + alpha): limit -= decrease (or set to inflight * beta)
  limit = clamp(limit, min_limit, max_limit)
on_start:
  if inflight >= limit: reject (shed)
```

### 4. Implement safely

1. Set `min_limit` high enough for healthy traffic; `max_limit` below dependency death threshold.
2. Separate limits **per dependency** and optionally per route class (read vs write).
3. Cooldown / smoothing to prevent flapping.
4. Prefer fail-fast errors with `Retry-After` only when retries are safe (`retry-backoff-patterns`).
5. Never use adaptive concurrency as sole authz or anti-abuse control.

**Pseudo middleware:**

```text
acquire():
  if inflight >= limit: return 503
  inflight++
release(rtt, success):
  inflight--
  update_limit(rtt, success)
```

### 5. Verify with controlled load

```bash
# Authorized staging load (example k6/hey)
hey -z 60s -c 200 https://staging.example/api/heavy
# Watch: current_limit, p99, dependency CPU, shed count
```

| Experiment | Expected |
| --- | --- |
| Gentle ramp | Limit rises; low shed |
| Dependency inject +200ms | Limit drops; shed increases; no cascade timeout storm |
| Recovery | Limit climbs without overshoot crash |
| Noisy neighbor route | Isolated limit protects critical path |

### 6. Observe and hand off

1. Dashboards: `concurrency_limit`, `inflight`, `shed_total`, dependency p99.
2. Alerts: shed rate sustained, limit pinned at min (dependency sick), limit pinned at max (not protecting).
3. Document interaction with circuit breakers and bulkheads.
4. Runbook: disable adaptive (fallback static) via feature flag.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Signal | RTT + timeouts | Only CPU of local pod |
| Shed | Fast 503 with metrics | Queue until OOM |
| Tuning | Clamped min/max | Unbounded limit growth |
| Scope | Per dependency | One global limit for all backends |
| Retries | Careful with shed | Blind retry storms on 503 |

## Output Checklist

- [ ] Placement and dependencies documented
- [ ] Baseline latency/inflight captured
- [ ] Algorithm + min/max clamps chosen
- [ ] Metrics for limit, inflight, shed exported
- [ ] Staging overload experiments recorded
- [ ] Interaction with retries/timeouts reviewed
- [ ] Feature-flag rollback path
- [ ] Dashboards/alerts
- [ ] `code-quality-standards` on code changes

## Rules

- Authorized load only.
- Concurrency limits protect systems; they are not a substitute for authn/z.
- Prefer measurable feedback (latency) over guesswork constants alone.
- Avoid retry amplification when shedding.
- Coordinate with rate-limit design for abuse vs overload distinction.
