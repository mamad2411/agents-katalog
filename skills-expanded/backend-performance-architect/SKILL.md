---
name: backend-performance-architect
version: 1.0.0
description: Backend latency and throughput design — an impact-ordered playbook: query and index shape, cache layers and invalidation, moving work off the hot path (queues, outbox, precompute), fewer and parallel network hops, tail-latency controls (deadlines, retries, backpressure, load shedding, single-flight), then serialization and lock contention. Covers Go transport choices — unary RPC vs streaming/bidi gRPC, and when a fasthttp server is worth it. Use whenever a service feels slow, an endpoint misses its p99, a load test is coming, or someone asks whether a faster transport, framework or server would help.
---

# Backend Performance — Impact-Ordered Playbook

How to make a service faster, and **in what order**. Pairs with [performance-reviewer](../performance-reviewer/SKILL.md), which owns the findings report and the measurement discipline; this skill owns the decision of what to change and the design of the fix. Query design lives in [sql-architect](../../databases/sql-architect/SKILL.md), signals in [observability-architect](../../infra/observability-architect/SKILL.md). Wiring, snippets and decision tables in [RECIPES.md](RECIPES.md).

The premise: frameworks and languages move a request by a few percent. Query shape, cached work and hop count move it by 10x–1000x. Spending a week on the transport while a sequential scan sits under the endpoint is the most common way to "optimize" nothing.

## 1. The impact ladder

Order the work by the size of the win, not by how interesting it is.

| Rung | Lever | Typical win | Cost |
|---|---|---|---|
| 1 | Remove work — cache, precompute, move off the hot path | 10x–1000x | invalidation, staleness |
| 2 | Query and index shape | 10x–100x on the offending query | migration, write amplification |
| 3 | Fewer or parallel network hops | 2x–10x | coupling, error handling |
| 4 | Tail-latency controls | avoids 10x+ collapse under load | tuning, false positives |
| 5 | Serialization, transport, framework ([§7](#7-rung-5--transport-and-in-process)) | 1.1x–1.5x | rewrite, ecosystem loss |
| 6 | Micro-optimization — allocations, pools | 1.05x–1.1x | readability |

Two rules follow from the table:

- **Never climb down a rung while the one above is untouched.** If the endpoint waits on a query, a faster HTTP server cannot help.
- **Each rung has a stop condition.** Stop when the profile no longer shows the layer you were about to change. That is what keeps the last two rungs from consuming the time the first two deserve.

## 2. Measure, then pick a rung

Measurement is the input to the ladder, not a formality. Before changing anything:

- **Percentiles, per endpoint.** p50 is the cost of the work; p95/p99 is the cost of contention, GC, slow dependencies and queueing. An average hides the problem you were paged for.
- **The right tool per layer.** `EXPLAIN (ANALYZE, BUFFERS)` and `pg_stat_statements` for SQL; `pprof` (CPU, heap, mutex, block) for Go; a trace to see the hop where the request actually spends its time; RED+USE dashboards to know whether the problem is volume or latency.
- **A realistic shape.** Read/write mix, payload sizes, concurrency and cache hit ratio. A single-endpoint loop at concurrency 1 will not reproduce a p99 that only appears when the pool saturates.
- **One or two hot spots.** Almost every slow service has a small number of them, and they are rarely where the author guessed. Fix those and re-measure; do not batch a dozen speculative changes, or you will not know which one worked.

If the HTTP layer is not visible in the flame graph, transport work is off the table by definition.

## 3. Rung 1 — remove work

The cheapest request is the one the server never performs in full.

**Cache in layers, with an explicit invalidation story.**

- **In-process** — bounded (LRU or size cap) and TTL'd. Fastest, but per replica, so a write on one node is stale on the others. Good for reference data (currencies, feature flags, JWKS) with a revocation window you can tolerate.
- **Shared** — Valkey/Redis when several replicas must agree. Costs a hop; still 10x–100x cheaper than the query it replaces.
- **CDN / HTTP** — `Cache-Control`, `ETag`/`If-None-Match`, `stale-while-revalidate` for public, non-personal responses. The cheapest byte is the one that never reaches the origin.
- **Cache-aside by default**; write-through only when reads dominate and staleness is unacceptable and the write path can absorb the extra hop.

**Invalidate by design, not by hoping.** Version keys (`user:42:v7`), delete on write, TTL as a backstop. Never cache an authorization decision without a revocation path — a cached "allowed" outliving a revoked permission is a security bug with a latency win.

**Coalesce duplicate work.** N concurrent misses for the same key must produce one query (`singleflight` in Go), and TTLs should carry jitter so a fleet does not expire together. Cache negative results briefly; "not found" storms are the same stampede with different outcomes.

**Precompute and denormalize.** Materialized views, read models, counters maintained on write, and reports generated on a schedule instead of per request. The trade is always the same: read speed bought with write complexity.

**Move work off the hot path.** Email, push, audit trails, exports and webhooks belong behind a queue or the outbox pattern; the request returns `202` with a resource and the work happens in a worker. This is a correctness win too — a slow SMTP server should not be able to fail a sign-up.

## 4. Rung 2 — the database is usually the bottleneck

- **Index for the queries you have.** Every foreign key and every `WHERE`/`JOIN` column, composite indexes ordered most-selective-first, partial indexes for soft-deleted rows. See [sql-architect §3](../../databases/sql-architect/SKILL.md).
- **`EXPLAIN` tells the truth.** A `Seq Scan` on a large table, a `Sort` spilling to disk, or `actual rows` far from `plan rows` (stale statistics — run `ANALYZE`) are findings, not trivia.
- **Kill N+1.** A list endpoint that fires one query per parent is the single most common bug: batch with `IN`, a `JOIN`, or a loader. A handler emitting more than a handful of queries per request is suspect until proven otherwise.
- **Batch writes.** `COPY` / `UNNEST` / multi-row `INSERT` for bulk paths; one round trip beats N, and one transaction beats N commits.
- **Cursor pagination, not `OFFSET`.** `OFFSET 100000` is O(N) by construction.
- **Size the pool.** Too few connections queue requests; too many thrash the database. Start near `(cores × 2) + spindles`, cap the *total* across replicas, and put a pooler in front before the fleets multiply.
- **Read replicas** when reads dominate and bounded staleness is acceptable. Route explicitly (a distinct handle), never silently — a replica read that surprises a read-after-write test is a bug factory.
- **Partition when one table no longer fits the working set; shard only after single-node limits are measured.** "We might grow" is not a measurement.
- **Migrations are performance events.** `CREATE INDEX CONCURRENTLY`, no long `ACCESS EXCLUSIVE` locks on hot tables, backfills in batches.

## 5. Rung 3 — network hops and fan-out

- **Fewer calls per request.** Each hop adds latency, a failure mode and a timeout to tune. Inline what is cheap, cache what is stable.
- **Parallelize only what is independent**, with bounded concurrency (`errgroup.SetLimit`) so a fan-out cannot become a self-inflicted load spike.
- **Reuse connections everywhere.** One `http.Client` per target (never per request), one gRPC/Connect channel per target, HTTP/2 (or `h2c` on a private network) so concurrent calls share a connection instead of a pool of TCP handshakes.
- **Co-locate services with their data** — same region or zone. Cross-region hops cost milliseconds before any code runs; no amount of Go tuning buys them back.
- **Batch instead of looping.** A `GetMany`/`SendBatch` unary call replaces N round trips and N failure points. This is where most "reduce request/response" work actually pays off.

A multiplexed transport does not reduce the number of logical round trips. It removes handshakes and header overhead; each call still needs its answer.

## 6. Rung 4 — tail latency and graceful degradation

p99 is set by the worst moments: a GC pause, a lock convoy, one slow dependency, a retry storm. Controls, in order of value:

- **Deadlines on every outbound call**, propagated, and always shorter than the caller's own budget. An unbounded wait converts one slow dependency into a hung service.
- **Retries only for idempotent operations, with a budget**, exponential backoff and jitter, and a cap. Retrying a non-idempotent write duplicates data; retrying without a budget turns an outage into a meltdown.
- **Circuit breakers** so a failing dependency stops receiving traffic and the caller fails fast instead of queueing.
- **Hedged requests** only after measurement shows a long tail that is not caused by overload — a hedge doubles load by definition.
- **Bounded queues and backpressure.** Unbounded channels and unbounded worker pools convert overload into OOM and latency for everyone.
- **Load shedding with a priority order.** Reject early (`429`/`503` + `Retry-After`) and drop optional work first — analytics, prefetch, recomputation — so the requests that matter still succeed.
- **Degrade, don't fail.** Stale cache, partial response, a skipped enrichment. A service that answers slowly but correctly under overload is still down.

## 7. Rung 5 — transport and in-process

Choose the transport for semantics and operability; expect little from it in latency. Details and snippets in [RECIPES §5](RECIPES.md#5-go-transport-choices).

| Need | Choice |
|---|---|
| Unary internal RPC between services | Connect or gRPC unary over one pooled channel; HTTP/2 where available |
| Browser and mixed clients | REST or Connect — native gRPC needs a gRPC-Web proxy |
| Interactive, both sides push (telemetry, collaborative, long jobs with client steering) | Native gRPC bidi (`h2c`) or Connect bidi over HTTP/2 |
| One-way progress or subscription | Server-stream; or a message bus if the consumer may be offline |
| Maximum raw throughput on one narrow, HTTP/1.1-only endpoint | `fasthttp` on an isolated listener, measured against the baseline |

Two honest notes that save weeks:

- **Bidi does not reduce request/response count.** Every request still needs a response. It buys session semantics — server-initiated messages, cancellation, one connection with backpressure — not fewer round trips. If the goal is "fewer calls", batch or cache.
- **`fasthttp` is a narrow tool.** It wins on trivial handlers (roughly 1.5x–4x in microbenchmarks) and loses the `net/http` ecosystem: middleware, request-context cancellation, HTTP/2, streaming, `httptest`. Without cancellation, an abandoned request still burns CPU — a real problem for deliberately expensive work such as password hashing. Never migrate the main API; isolate a single hot endpoint on its own listener and benchmark it against the baseline before believing the number.

In-process, in decreasing order of payoff: fewer allocations on hot paths (preallocate, `sync.Pool`, avoid reflection-heavy codecs), serialization that avoids encoding the same data twice (protobuf internally, JSON at the edge), less lock contention (sharded maps, atomics, per-worker state), and bounded goroutines per request. Then stop — this rung is the last 5%.

## 8. Go notes

- **Expose `pprof` on a private listener**, never the public one. Profile with realistic load; a CPU profile of an idle process shows the scheduler.
- **`GOMEMLIMIT` and container limits before exotic allocation work.** Set a memory limit and let the GC do its job; most "GC pressure" is an oversized heap caused by an unbounded cache.
- **`database/sql` / `pgxpool` defaults are permissive.** `SetMaxOpenConns` explicitly; an unlimited pool is a coordinated outage waiting for traffic.
- **Propagate the request context**; `context.Background()` inside a handler silently removes cancellation and deadlines from everything downstream.
- **Benchmark with `-benchmem`** and compare allocations, not just nanoseconds. And benchmark the handler, not a helper that omits the database.
- **`GOMAXPROCS` follows cgroup limits in modern Go (1.25+)**; don't override it without a measurement that says so.

## 9. Anti-patterns

- Microbenchmark-driven architecture: a 20% win on a function that is 2% of the request.
- Caching without invalidation, or a shared cache key for per-user data.
- Retries without a budget, backoff or idempotency.
- Sharding, replicas or a message queue adopted before a single-node measurement.
- Swapping the HTTP framework or server as the *first* move.
- An ORM loop hiding N+1 behind readable code.
- Optimizing the average while the p99 is what users feel.
- Adding a background worker for work that was never slow.

## 10. What this skill does NOT do

- Write the findings report or the severity table — that is [performance-reviewer](../performance-reviewer/SKILL.md).
- Run load tests or capacity planning; those are operational exercises against a staging environment.
- Optimize anything that is not measurably slow. Without a profile, `EXPLAIN` plan or percentile, there is no finding.

## 11. Cross-skill ties

- [performance-reviewer](../performance-reviewer/SKILL.md) — the review mode: findings, severities, measurement evidence.
- [sql-architect](../../databases/sql-architect/SKILL.md) — indexing, N+1, cursor pagination, `EXPLAIN` reading.
- [go-architect](../../languages/go-architect/SKILL.md) — concurrency, allocation, interface and error design.
- [observability-architect](../../infra/observability-architect/SKILL.md) — RED/USE signals that reveal where to look.
- [grpc-architect](../../protocols/grpc-architect/SKILL.md) / [connectrpc-architect](../../protocols/connectrpc-architect/SKILL.md) — transport mechanics for the choices in §7.
- [rest-api-architect](../../protocols/rest-api-architect/SKILL.md) — pagination and rate limiting at the API edge.
- [grafana-architect](../../infra/grafana-architect/SKILL.md) — dashboards and SLOs that trigger the work.
