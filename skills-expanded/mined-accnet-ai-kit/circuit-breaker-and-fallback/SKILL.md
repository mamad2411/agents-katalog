---
name: circuit-breaker-and-fallback
description: Design and review circuit breakers, timeouts, retry budgets, bulkheads, and safe fallbacks for remote dependencies. Use when a service must contain failures, avoid retry amplification, and degrade predictably.
---

# Circuit Breaker and Fallback

1. Set an end-to-end budget and a shorter per-attempt timeout.
2. Retry transient idempotent operations with jitter and a bounded budget.
3. Define breaker scope, threshold, open duration, and half-open probes.
4. Isolate concurrency with bulkheads and protect the fallback.
5. Mark degraded responses explicitly and test recovery and flapping.

Never return stale or synthetic fallback data where correctness requires current authoritative data.
