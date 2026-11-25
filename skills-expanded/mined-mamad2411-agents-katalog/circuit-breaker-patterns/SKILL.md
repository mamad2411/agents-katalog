---
name: circuit-breaker-patterns
description: >
  Design and operate circuit breakers for dependency isolation: closed/open/half-open
  states, failure/slow-call thresholds, probe recovery, bulkheads, and fallbacks.
  Use when preventing cascading failure toward a slow or erroring peer (熔断, fail-fast),
  complementing retries and load shedding — not as a substitute for fixing the dependency
  or for authz decisions.
---

# Circuit Breaker Patterns

## Scope And Authorization

- **In scope:** services and libraries you own; production changes under normal change control.
- **Out of scope:** deliberately degrading third-party customer systems; using breakers to hide security failures.
- Prefer canary / one dependency first; measure error budgets before global rollouts.
- Redact customer IDs from breaker metrics dashboards when exporting evidence.
- Pair code with `code-quality-standards` and retry skills (`retry-backoff-patterns`, language retry packs).

## When To Use

- Downstream dependency is flaky/slow and retries amplify load.
- You need **fail-fast** when open, limited **probes** in half-open, and controlled recovery.
- Designing bulkhead isolation (separate pools/breakers per dependency).
- Tokens: circuit breaker, open/closed/half-open, failure rate, slow call, fallback, bulkhead, 熔断.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Retry/backoff only | `retry-backoff-patterns` / language `*-retry-policy` |
| Client-side load balancing | `client-side-load-balancing` |
| Rate limit / load shedding edge | rate-limit / gateway skills |
| gRPC deadlines | `grpc-deadline-and-retry` |
| Implementation style | `code-quality-standards` |

## State Machine

| State | Behavior | Transition |
| --- | --- | --- |
| **Closed** | Calls pass; count failures/slow calls in sliding window | Open if threshold exceeded |
| **Open** | Fail fast (or fallback); no calls to dependency | After `waitDuration`, go half-open |
| **Half-open** | Allow limited probe calls | Success → closed; failure → open |

## Key Parameters

| Parameter | Guidance |
| --- | --- |
| Failure rate threshold | e.g. 50% of calls in window — tune with traffic volume |
| Minimum throughput | Do not open on 1–2 errors; require N calls in window |
| Slow call duration + rate | Treat “success but 5s” as failure for user-facing SLOs |
| Wait duration in open | Long enough for dependency recovery; short enough for SLO |
| Permitted probes in half-open | Small (1–N concurrent); avoid thundering herd |
| Ignore exceptions | Do not trip on business 4xx if those are normal |

## Workflow

### 1. Confirm scope and success criteria

1. Dependency name, SLOs (latency/error), owner, blast radius if open.
2. Success: cascading timeouts drop; dependency load falls when open; recovery automatic without manual restart.
3. Rollback: feature flag to disable breaker or widen thresholds.

### 2. Inventory call sites

1. List outbound clients (HTTP/gRPC/DB/queue) and existing timeouts/retries.
2. Detect **retry storms** (client retry × mesh retry × queue redelivery).
3. Note thread/connection pool sizes (bulkhead candidates).

### 3. Baseline metrics

1. Capture p95/p99, error rate, concurrent in-flight, timeout counts **before** breaker.
2. Record dependency incident history (how long outages last).
3. Define fallback behavior (cache, default, degrade feature, fail message).

### 4. Implement breaker + bulkhead

**Logical config (library-agnostic):**

```text
slidingWindow: count(100) or time(60s)
minimumNumberOfCalls: 20
failureRateThreshold: 50%
slowCallDurationThreshold: 2s
slowCallRateThreshold: 80%
waitDurationInOpenState: 30s
permittedNumberOfCallsInHalfOpenState: 5
automaticTransitionFromOpenToHalfOpen: true
```

**Ordering with retries:**

1. Set **timeouts** tighter than caller SLO.
2. Put breaker **around** the client; retries should usually be **inside** or carefully coordinated so retries do not multiply while open.
3. Prefer **one** retry layer; see `retry-backoff-patterns`.
4. Separate breaker instances **per dependency** (and per critical operation if needed).
5. Bulkhead: dedicated connection pool / semaphore so one peer cannot exhaust the process.

**Fallback sketch:**

```text
onCallNotPermitted / onError:
  return cached value OR degraded DTO OR typed error for UX
  emit metric circuit_breaker_state=open
  do not retry immediately in a tight loop
```

### 5. Verify with evidence

```bash
# Unit: force failures → state open → fail-fast without calling mock
# Integration: toxiproxy/fault inject latency → slow-call open
# Load: dependent service 100% 500 → caller p99 stable via fallback
# Metrics: circuit_breaker_state, failed, not_permitted, successful
```

1. Prove open state blocks calls (mock invocation count = 0 while open).
2. Prove half-open allows limited probes then closes on success.
3. Chaos: kill dependency; confirm no thread pool exhaustion on caller.

### 6. Observe and operate

1. Dashboard: state over time, not_permitted rate, dependency health.
2. Alert when open longer than dependency RTO or flapping half-open.
3. Runbook: when open is correct (dependency down) vs mis-tuned threshold.

### 7. Hand off

1. Document parameters and rationale per dependency.
2. Link fallback product behavior (what users see).
3. Apply `code-quality-standards`; avoid silent catch-all fallbacks that hide bugs.

## Interaction With Other Patterns

| Pattern | Relationship |
| --- | --- |
| Timeout | Required foundation; breaker without timeout is incomplete |
| Retry | Complementary; unbounded retry defeats breaker |
| Bulkhead | Isolate pools so one open dependency does not starve others |
| Rate limit | Protects your service; breaker protects you from peers |
| Hedging | Can increase load; usually disable when breaker open |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | One breaker per dependency | Global breaker for all egress |
| Thresholds | Min call volume + rate | Open after single blip |
| Fallback | Explicit degrade path | Swallow errors, return empty 200 |
| Retries | Budgeted, jittered | Retry while open in hot loop |
| Metrics | State + not_permitted | Only HTTP 500 count |
| Security | Failures still authorized | Using breaker to skip auth checks |

## Output Checklist

- [ ] Dependencies and SLOs listed
- [ ] Timeouts and retry layers mapped
- [ ] Breaker parameters chosen and documented
- [ ] Bulkhead/pools separated where needed
- [ ] Fallback behavior product-approved
- [ ] Tests for open / half-open / close paths
- [ ] Metrics and alerts live
- [ ] Feature flag / rollback documented
- [ ] Residual risk (false open under low traffic) noted

## Rules

- Circuit breakers are for **stability**, not access control.
- Prefer evidence from fault injection over production-only tuning.
- Do not “temporarily” disable breakers in prod without ticket and expiry.
- Focus this skill on breaker design/ops; route pure retry, LB, and mesh policy to their skills.
