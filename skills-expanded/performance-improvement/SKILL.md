---
name: performance-improvement
description: Measurement-first performance work — backend latency, database queries, frontend load times, memory, cost. Use when something is slow, when optimizing, before adding caches, or when the user says "performance", "slow", "optimize", "speed up", "latency", "memory", "N+1", or "page load".
---

# Performance Improvement

The iron law: **no optimization without a measurement, and no "it's faster now" without a second measurement.** Guessed bottlenecks are wrong more than half the time; optimizing a guess makes code worse and no faster.

## The loop (never skip a step)

1. **Define the target.** "Fast" is not a spec. Get a number: "list endpoint p95 < 300ms", "page interactive < 2s on mid-range mobile", "report generates in < 30s". Without a target you cannot stop, and unstoppable optimization destroys codebases.
2. **Measure where the time actually goes.** Profile or trace the real path with realistic data volume — 10 rows in dev hides everything. One request timed end-to-end, broken into segments: network / app CPU / DB / external calls / rendering.
3. **Fix the biggest segment only.** One change at a time.
4. **Re-measure the same way.** Keep the change only if the number moved meaningfully. Record before/after in the commit/PR.
5. Repeat until the target is met, then **stop** — the target is the permission to stop.

## Where the time usually is (check in this order)

### Database — the culprit ~70% of the time in CRUD apps
- **N+1 queries**: the single most common backend perf bug. Detect by logging/counting queries per request (an ORM loop over rows, each lazy-loading a relation). Fix with joins/eager loading/batched IN queries. Any list endpoint doing >5 queries deserves suspicion.
- **Missing indexes**: `EXPLAIN ANALYZE` the slow query. Seq scan on a big table in a hot path → index the filter/sort columns (composite, leading with equality columns; tenant id first in multi-tenant).
- **Fetching too much**: SELECT only needed columns for lists; paginate everything (keyset for deep pages); never load all rows to count them (`COUNT(*)`) or to filter in app code what SQL can filter.
- **Chatty transactions**: many round trips inside one request → batch into fewer statements; move multi-row inserts to bulk operations.

### External calls
- Sequential awaits that could be parallel; missing timeouts (a "slow" system is often one hung dependency); calls in loops that need batching; synchronous calls that belong in a background job (see system-design).

### App code
- Only after DB and I/O are clean: accidental O(n²) (lookup in a list inside a loop → use a set/dict), repeated parsing/serialization of the same data, loading whole files into memory to stream them out.

### Frontend
- Measure with the browser's own tools (Lighthouse/Performance tab) on throttled mobile, not your dev machine.
- Usual suspects in order: oversized/unoptimized images, render-blocking or oversized JS bundles (analyze the bundle; lazy-load routes and heavy components), waterfalls of dependent fetches (parallelize or move to the server), missing caching headers on static assets, re-render storms (fix state placement before reaching for memo).
- Perceived speed counts: skeletons, optimistic updates, and streaming beat a spinner even at equal latency.

## Caching is the last resort, not the first

A cache is a bug you haven't had yet (staleness, invalidation, memory). Before caching: fix the query, add the index, batch the calls. Cache when the computation is *irreducibly* expensive and read-heavy — then follow system-design's cache rules (source of truth, invalidation, max staleness, tenant-scoped keys).

## Load & capacity sanity

- Before launch or a big campaign: one basic load test of the golden path at 2–3× expected peak (any tool — k6, locust, even a bash loop with concurrency). You're looking for the knee: where latency bends and errors start.
- Watch connection limits: DB max_connections vs app pool size × instances is the classic silent ceiling.
- Memory leaks announce themselves as restarts-fix-it: track RSS over hours under steady load if you suspect one.

## Anti-patterns to refuse

- Micro-optimizing readable code (loop unrolling, clever bit tricks) in an app whose time is 95% I/O.
- Adding Redis/queues/read-replicas to fix what one index fixes.
- "It feels faster" as evidence. Numbers or it didn't happen.
- Benchmarking dev builds, cold caches, or localhost and drawing production conclusions.
