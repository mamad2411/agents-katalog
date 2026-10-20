---
name: backend-tail-latency
description: Investigate backend P99/P999 tail latency — coordinated GC, lock contention, queue depth, slow downstream, retry storms; surface ONE dominant cause.
---

# backend-tail-latency

> P50 latency is what the median user sees; P99 is what your worst-day user sees. Tail problems hide in coordinated phenomena, not single slow lines.

## When to use

- P99 / P999 latency is materially worse than P50 and you don't know why.
- A service is meeting P50 SLO but failing P99 SLO.

## Inputs

- The service + the affected route(s).
- Recent P50, P95, P99 percentiles and the timeframe of the regression.
- Available signals: flamegraphs, trace samples, GC logs, DB slow-query logs, dependency latencies.

## Procedure

Walk these in order; each is a common tail-latency root cause. Stop when one is the dominant signal (not when one is "plausible").

1. **Coordinated GC / runtime pauses**:
   - Look at GC pause histograms. Tail-of-tail (P99.9) is usually GC if pauses > 50ms.
   - Action: tune heap; switch GC algo (G1 / ZGC / Shenandoah); reduce allocation in hot path.
2. **Lock contention**:
   - Profile shows threads parked. Per-thread CPU is low but latency is high.
   - Action: shorten critical section; introduce read-write split; pool partitioning.
3. **Queue depth ahead of you**:
   - Worker pool / DB connection pool / external service queue.
   - Look at queue depth + wait time histograms. P99 wait often > P99 service.
   - Action: scale pool; cap upstream concurrency; add backpressure.
4. **Slow downstream**:
   - Trace samples show the long span isn't your code — it's a downstream call.
   - Look at downstream P99 latency for the affected timeframe; compare to baseline.
   - Action: timeout aggressively; hedged requests; fall back; add cache.
5. **Retry storms / cascade**:
   - 5xx rate downstream spikes; your tail balloons because retries pile on.
   - Action: token-bucket retry budget; circuit breaker; back off exponentially.
6. **Cold path / cold cache**:
   - First request after deploy / autoscaler spin-up is slow; warm requests fast.
   - Action: pre-warm on deploy; smaller batch sizes; concurrent prefetch.
7. **Single hot key / hot partition**:
   - One key in a cache / DB partition absorbs disproportionate traffic.
   - Action: read-through with local LRU; partition by user; rate-limit per key.

## Output

```text
Tail-latency investigation: <service>/<route>

Current state:
  P50: 60 ms   P95: 180 ms   P99: 1,400 ms   P99.9: 4,200 ms

Signals reviewed:
  - GC pause histogram         (max 80 ms; not the dominant signal)
  - Lock contention via async-profiler  (parked threads 8% of CPU)
  - DB connection pool         (P99 wait 22 ms; not it)
  - Stripe-client P99          (3,800 ms during peak — match!)
  - Retry storm                (no — Stripe-client retries off)

Dominant cause:
  Downstream Stripe-client P99 is 3,800 ms. Our P99 is 1,400 ms because we
  apply a 1s timeout, dropping the worst Stripe-client cases. Our P99.9
  catches the un-timeout-able subset.

First fix (single change):
  Switch to hedged requests against Stripe-client with a 200ms hedge delay
  (Tail at Scale, Dean & Barroso). Expected effect: ~60% reduction in P99
  latency and ~80% in P99.9 if Stripe's tail is independent across hedges.

Validation:
  Confirm the gain in staging before rolling to prod canary. Watch
  Stripe-client error rate doesn't materially rise.
```

## Quality bar

- One dominant cause named, with evidence.
- One first fix recommended, with the expected effect and how to validate it.
- Other signals reviewed are listed (so reviewer can argue with the elimination).

## Anti-patterns to avoid

- "Might be GC, might be locks, might be downstream" — narrow it down.
- Recommending 3 fixes at once. Pick the highest-leverage one; validate; iterate.
- Tuning GC because GC is famous without checking the GC pause histogram first.
- Adding cache without first checking the actual hit rate ceiling.
