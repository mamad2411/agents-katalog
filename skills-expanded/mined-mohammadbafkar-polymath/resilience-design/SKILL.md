---
name: resilience-design
description: Design resilience for a dependency call path — timeout, retry with backoff+jitter, circuit breaker, bulkhead, fallback, load-shedding — with a failure-mode table.
---

# resilience-design

> Every remote call fails eventually. Resilience is deciding what happens then — on purpose, with numbers — instead of discovering it during an incident.

## When to use

- A service calls a dependency (DB, API, queue) and you need the failure behavior specified, not implicit.
- Retries or timeouts already exist but caused a retry storm or cascading failure.
- A workflow invokes `polymath-architecture:resilience-design`.

Not this when: you are setting the latency/throughput target itself — that is `polymath-performance:perf-budget` / `backend-tail-latency`. This skill specifies behavior under failure, not the budget.

## Inputs

- The call path and the dependency's SLO/latency profile.
- Whether the call is on a user-blocking path or background.
- Idempotency of the operation (decides whether retry is even safe).

## Procedure

1. **Set a timeout** on every remote call — derived from the dependency's p99, not a round number. No timeout is the root cause of most cascading outages.
2. **Decide retry**: only if the operation is idempotent or made so with an idempotency key. Use exponential backoff **with jitter**; cap attempts. Never retry a 4xx-class permanent error.
3. **Add a circuit breaker** when a dependency can stay down: trip on an error-rate/latency threshold, go half-open to probe recovery. State the trip and reset conditions numerically.
4. **Isolate with bulkheads**: separate connection pools / thread pools per dependency so one slow dependency can't exhaust everything. Name the pool sizes.
5. **Define the fallback** for the open-circuit / timeout case: cached value, degraded response, queue-for-later, or a clean error. "Spin forever" is not a fallback.
6. **Shed load** at the edge under overload (reject early with 429 + Retry-After) rather than collapsing; protect with a concurrency limit.
7. **Avoid the anti-patterns**: retries layered at multiple tiers (multiplicative storm), retry without jitter (thundering herd), unbounded queues (hides the failure until OOM).
8. **Build the failure-mode table**: for each failure (timeout, 5xx, connection refused, slow), the chosen response and the user-visible effect.

## Output

- A one-page spec: per-call timeout, retry policy (attempts, backoff, jitter, idempotency basis), circuit-breaker thresholds, bulkhead sizing, fallback behavior, load-shed rule.
- The failure-mode → response table.

## Quality bar

- Every remote call has an explicit, justified timeout.
- Retry is only enabled where the operation is idempotent, always with jitter and a cap.
- Each pattern's threshold is a number with a rationale, not "tune later".
- A fallback is named for every tripped/timed-out path.
