---
name: performance-engineering
description: Diagnoses performance problems measurement-first - profiling, budgets, queueing, caching - and guards wins in CI. Triggers - this endpoint is slow, hitting the latency budget, memory keeps growing under load, optimize this, N+1 query, high CPU, load test.
---

# Performance Engineering

Optimization without measurement is decoration: it adds complexity, changes a
number nobody tracks, and often makes things worse. The rule is absolute —
**measure, find the actual bottleneck, fix that one thing, measure again.**

Engineers' intuitions about where time goes are wrong most of the time. That is
not a skill deficiency; it is the nature of layered systems.

## Start with a number

Before touching anything, answer:

1. **What is slow, specifically?** An endpoint, a job, a page interaction — not
   "the app".
2. **How slow, at which percentile?** p50 and p99 are different problems: p50 is
   a code path, p99 is usually contention, GC, or a cold cache.
3. **What is the target?** From `CONSTRAINTS.md`. Without it there is no
   definition of done and optimization never ends.
4. **Under what conditions?** Concurrency, data volume, cache state. A benchmark
   on an empty table measures nothing.

No number, no work. Get the measurement first even if it takes a day.

## Find the bottleneck

| Layer | Tool | Typical finding |
|---|---|---|
| End to end | Distributed trace, browser timeline | Which span owns the time |
| Application CPU | Sampling profiler, flame graph | One hot function, or serialization |
| Application wait | Async profiler, thread dump | Blocked on I/O or a lock |
| Database | Query plan, slow log, `pg_stat_statements` equivalent | Missing index, N+1, seq scan |
| Memory | Heap profile, allocation profile | Retention leak, oversized buffers |
| Network | Timing breakdown | Chatty calls, TLS handshakes, payload size |
| Frontend | Lighthouse, performance panel | JS bundle, main-thread blocking, layout thrash |

Profile under **realistic load and realistic data volume**. Most performance
bugs are invisible at 100 rows and dominant at 10 million.

## Usual suspects, ranked by frequency

1. **N+1 queries** — a query inside a loop. Batch or join.
2. **Missing or unusable index** — verify with the plan; a function on the
   column or an implicit cast defeats the index.
3. **Unbounded result set** — `SELECT *` with no limit, loading an entire table
   into memory.
4. **Serialization overhead** — often larger than the query it wraps.
5. **Chatty network calls** — ten round trips where one batched call would do.
6. **Work repeated per item** that could be hoisted out of the loop.
7. **Lock contention** — throughput plateaus while CPU stays low.
8. **Cold start / missing connection pooling** — reconnecting per request.
9. **Frontend bundle size** — the dominant cost of most "slow page" reports.

## Two laws worth internalizing

**Amdahl** — optimizing a path that accounts for 5% of time yields at most 5%.
Work on the biggest span, always.

**Little's law** (`L = λW`) — concurrency = arrival rate × time in system. It
explains why latency explodes near saturation: as utilization approaches 100%,
queue length grows without bound. A system at 85% utilization is already in the
steep part of the curve. **Adding capacity at 95% utilization buys far more
than a code optimization** — and conversely, a small latency reduction can
produce a large throughput gain by pulling you off the cliff.

## Caching: last resort, not first

A cache is a second copy of the truth with a staleness policy and an
invalidation problem. Before adding one, ask whether the underlying operation
can simply be fast.

When you do cache, decide explicitly: what is the key (including every input
that affects the result — a cache key missing a tenant id is a data-leak bug);
what is the TTL; how is it invalidated; what happens on a stampede when a hot
key expires (single-flight or jittered TTL); and what is the correctness cost
of serving stale data.

## Verify and protect

- Measure again after the fix, the same way as before. Record both numbers in
  the PR.
- Add the budget to CI where possible (bundle size, query count per request,
  benchmark regression threshold). A win with no guard regresses within months.
- Keep the complexity you added proportional to the gain. A 3% improvement that
  makes the code unreadable is a net loss — revert it.

## Exit checklist

- [ ] Baseline measured, with percentile, load and data volume stated
- [ ] Target from `CONSTRAINTS.md` written down before the work
- [ ] Bottleneck identified by a profile or plan, not by intuition
- [ ] One change at a time, each measured
- [ ] After-measurement recorded next to the before
- [ ] A regression guard exists in CI
- [ ] Added complexity is justified by the measured gain
