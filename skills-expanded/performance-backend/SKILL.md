---
name: performance-backend
description: "Fast services: a latency budget per request, the database first (queries, indexes, N+1, pooling), caching, serialisation and payload size, compression, connection reuse, concurrency limits and backpressure, async I/O, batching and pipelining, moving CPU work off the request path, timeouts, and scaling out statelessly. Read before optimising a server or an API endpoint."
---

# Fast services

A slow endpoint gets the generated treatment: a Redis cache in front of it,
the pool raised to 200, everything made async, a bigger instance, talk of a
rewrite in another language, while the request still makes 40 queries in
series and waits on a partner API with no timeout. This skill breaks a
request down, fixes it in the order that pays, and sets the limits that
keep a service fast under load. The method (baseline, one change at a
time, percentiles) is in `performance`; this is what to change on a server.

## 1. A latency budget per request

- A target per kind of endpoint, as a percentile at the server: reads a
  user waits on, p95 under 200 to 300ms; writes, under 500ms; anything
  that needs seconds becomes a job with a status (`backend-jobs`).
- Split the budget along the path so each part knows its share. For a
  300ms read: auth 10ms, database 100ms, one external call 100ms, CPU and
  serialisation 30ms, the rest margin. A part that cannot fit gets a
  timeout inside the budget, a cache, or leaves the request path.
- Independent calls run concurrently: the request then costs the slowest,
  not the sum.
- Expose the breakdown in staging with `Server-Timing` (browser DevTools
  show it in the request's Timing tab):

  ```http
  Server-Timing: db;dur=53.2, pricing;dur=88.0, render;dur=12.4
  ```

## 2. Break a slow request down

Traces first: with OpenTelemetry or the project's APM, the spans of a slow
request show where the time went. Read the shape:

| Shape in the trace | Meaning |
|---|---|
| A comb of many identical short database spans | N+1 |
| One long database span | a slow query: plan, index, rows fetched |
| External calls one after another | serial calls that could run concurrently |
| A gap with no span | CPU in the app (profile it) or waiting for a connection |
| Fast spans, slow total | queueing before the handler: workers or pool saturated |

- Without tracing: log each phase's duration with the request id, turn on
  the slow query log, count queries per request.
- Measure pool waits. Most pools expose the time to acquire a connection
  and the number waiting; a request that waits 400ms for a connection
  shows no slow query anywhere.
- CPU inside the handler (serialisation, templating, crypto, compression,
  large JSON parsing): profile it (`performance-profiling`).

## 3. The database first

Most slow endpoints are slow in the database (`database-queries`,
`database-indexes`):

- **N+1**: one query for the list, one per row for its relations. Load
  them in one query: a join, `WHERE id = ANY($1)`, the ORM's eager loading
  (`include`, `with`, `select_related` and `prefetch_related`,
  `selectinload`, `preload`), DataLoader for GraphQL resolvers.
- **Missing index**: a sequential scan on a large table in `EXPLAIN
  (ANALYZE, BUFFERS)`; add an index for the filter plus the sort.
- **Too much data**: `SELECT *` with large text or JSON columns, no
  `LIMIT`, thousands of ORM objects loaded to count or sum them. Select the
  columns needed, aggregate in SQL, paginate by keyset.
- **Long transactions**: no external call, email or upload inside a
  transaction; it holds locks and a connection for the whole call.
- **Limits in the database**: `statement_timeout` (for example `5s` for
  the web role), `idle_in_transaction_session_timeout`, `lock_timeout` for
  migrations.

**Pool sizing** follows the database, not the thread count:

- Pools add up: instances x pool size stays under `max_connections` (100
  by default in Postgres, each connection a process of several MB), with
  room left for migrations, jobs and admin sessions.
- Small pools are usually faster. A common starting point is about twice
  the database server's cores in active connections across all instances;
  past that, connections contend for the same cores and disks.
- Many instances or serverless: a pooler (PgBouncer in transaction mode,
  RDS Proxy, the platform's own). Transaction mode breaks session state
  (`SET`, advisory locks, `LISTEN`); prepared statements need PgBouncer
  1.21+ with `max_prepared_statements`.
- Pool exhaustion shows as every endpoint slowing at once. Causes: a slow
  query, a long transaction, a connection not released on an error path.
  Raising the pool size only moves the queue into the database.
- Read replicas take read-heavy load; a read that must see the user's own
  write goes to the primary.

## 4. Caching, after the query is fixed

A cache in front of a slow query hides it until the cache misses; then
every miss is slow and a cold start is an outage. Fix the query, then
cache what is read often, costly to produce and tolerant of staleness
(`backend-caching` holds keys, invalidation and stampede protection).

- HTTP caching first for public GETs (`Cache-Control`, `ETag` and `304`),
  so the request never reaches the app.
- Memoise within a request: the same lookup made by five parts of one
  request runs once (a request-scoped map, DataLoader).
- Measure the hit ratio and the latency of a miss, not just of a hit.

## 5. Payloads and serialisation

- Send what the client uses: selected fields, paginated lists
  (`backend-api`: default 25, maximum 100), nested collections only when
  asked for.
- Compress text responses over about 1 KB: gzip at level 5 or 6, or
  brotli at 4 to 6 for dynamic responses (11 only for static assets
  compressed at build time); zstd for clients that send it in
  `Accept-Encoding`. Compress once, at the proxy or CDN (nginx, Caddy's
  `encode zstd gzip`) or in the framework, not both. Never recompress
  images, video or archives.
- Serialisation can dominate CPU for large responses. Measure, then use
  the fast path the stack offers: Fastify response schemas
  (fast-json-stringify), orjson or pydantic v2's `model_dump_json`,
  System.Text.Json source generation, sonic or go-json in Go.
- Binary formats (protobuf, MessagePack) between internal services, when
  payloads are large and the measurement says JSON is the cost.

## 6. Connection reuse

A new connection pays DNS, then TCP and TLS, before the request can even
be sent: 2 to 3 extra round trips (tens of milliseconds across regions)
plus handshake CPU.

- One HTTP client per process, reused, with keep-alive and a pool:
  - Node: `fetch` (undici) pools by default; the global `http` agent keeps
    connections alive since Node 19.
  - Go: one `http.Client`; read each body to the end and `Close()` it, or
    the connection is not reused; raise `Transport.MaxIdleConnsPerHost`
    (default 2) for a busy upstream.
  - Python: one `requests.Session` or `httpx.Client` (`AsyncClient`),
    never `requests.get` per call.
  - JVM: one `java.net.http.HttpClient`. .NET: `IHttpClientFactory`, or one
    `HttpClient` over a `SocketsHttpHandler` with `PooledConnectionLifetime`
    set. Rust: one `reqwest::Client`, cloned.
- HTTP/2 to upstreams that support it multiplexes requests over one
  connection; gRPC always does.
- Behind a load balancer, the server's keep-alive timeout must outlast the
  balancer's idle timeout (60s on AWS ALB), or requests fail with 502 when
  the server closes a connection the balancer reuses. In Node, raise
  `server.keepAliveTimeout` (default 5s) and keep `headersTimeout` above it.

## 7. Concurrency, limits and backpressure

- **I/O-bound services** use async I/O or cheap threads: Node's event
  loop, asyncio, tokio, goroutines, Java virtual threads (JDK 21+), .NET
  async. One blocking call inside an async runtime stalls every request on
  that thread: sync file or crypto calls in Node, `requests` or
  `time.sleep` under asyncio, blocking code in a tokio task (use
  `spawn_blocking`).
- **CPU-bound work** needs cores, not async: a worker pool sized to the
  cores (`worker_threads` or piscina in Node, processes in Python unless it
  runs a free-threaded build, rayon or `spawn_blocking` in Rust); Go
  spreads goroutines over `GOMAXPROCS`.
- **Bound everything**: a semaphore per downstream dependency, bounded
  queues, a maximum of requests in flight per instance. An unbounded queue
  turns overload into minutes of latency, then an OOM kill.
- **Shed load early**: at the limit, answer `503` with `Retry-After` (or
  `429` for a client over its rate limit) in milliseconds, instead of
  accepting work that will time out anyway. Drop requests that waited in a
  queue past their deadline: the client has already gone. Shed the least
  important work first (prefetches, analytics, background refreshes).
- **Failing dependencies**: timeouts and a circuit breaker that fails fast.
  Retries use backoff with jitter, happen at one layer only and stay within
  a budget (about 10% extra requests), or they multiply the load that
  caused the failure.

## 8. Batching and pipelining

- **Multi-get and bulk writes**: `MGET`, `WHERE id = ANY($1)`, one
  `INSERT ... VALUES` of 500 to 1,000 rows per statement (Postgres takes at
  most 65,535 parameters per statement), `COPY` for large loads, the
  provider's batch API.
- **Coalescing**: identical concurrent requests share one call (Go's
  `singleflight`, a map of in-flight promises in Node); DataLoader gathers
  the keys requested in one tick into one query.
- **Pipelining**: many commands sent without waiting for each reply: Redis
  pipelines (one round trip for N commands), Postgres pipeline mode
  (libpq 14+, pgx batches).
- The trade: a batch window (1 to 10ms) adds latency to the first item for
  throughput; say so when you add one.

## 9. CPU work off the request path

- Work the response does not need goes to a job (`backend-jobs`): email,
  webhooks, thumbnails, search indexing, reports, exports.
- Precompute what is read far more often than it changes: a counter
  maintained on write, a summary table, a materialised view refreshed on a
  schedule (`REFRESH MATERIALIZED VIEW CONCURRENTLY` needs a unique index).
- Heavy CPU (image and video processing, PDF rendering, model inference)
  runs in its own service or worker pool, scaled apart from the API.
- Long answers stream: first byte early, then chunks or server-sent
  events, instead of a whole response built in memory.

## 10. Timeouts and deadlines

- Every outbound call has a timeout (`backend-integrations`), and inside a
  request it fits what is left of the request's budget: a 30s timeout on a
  call made during a 300ms request is no timeout.
- Pass the deadline and cancellation down: Go `context.WithTimeout`,
  `AbortSignal.timeout(ms)` with `fetch`, `asyncio.timeout()` (Python
  3.11+), `tokio::time::timeout`, gRPC deadlines. When the client
  disconnects, stop the work.
- The server itself: Go's `http.Server` has no timeouts until you set
  `ReadHeaderTimeout`, `ReadTimeout`, `WriteTimeout` and `IdleTimeout`.
  Node defaults to `requestTimeout` 300s and `headersTimeout` 60s.
- Deeper layers get shorter timeouts, so a dependency gives up before its
  caller does and the caller can still answer.

## 11. Cold starts and serverless

- A cold start is runtime boot, module loading, initialisation and first
  connections. Measure it apart from warm requests (AWS Lambda prints
  `Init Duration` in a cold invocation's `REPORT` line).
- Make it smaller: fewer and lighter dependencies, bundled and tree-shaken
  code, rarely used modules imported lazily, clients and pools created
  outside the handler so warm invocations reuse them.
- Or keep instances warm: provisioned concurrency or SnapStart (Java,
  Python and .NET) on Lambda, minimum instances on Cloud Run and similar.
- Databases need a pooler or an HTTP driver: a connection per invocation
  exhausts `max_connections` at the first spike.

## 12. Memory and GC

GC pauses show as p99 spikes lined up with collections, and a high
allocation rate per request costs CPU and pause time. Measure bytes
allocated per request and the GC share of CPU; the settings and fixes are
in `performance-memory`.

## 13. Scaling out

- Stateless instances, so any instance serves any request: sessions in a
  shared store or a signed cookie, uploads in object storage, no in-memory
  state that must agree across instances. No sticky sessions: they
  unbalance load and lose state on every deploy.
- Measure throughput per instance at the latency target with a load test
  (`performance-load`); capacity grows with instances only until a shared
  resource saturates, usually the database. Each new instance brings its
  own pool: check `max_connections` before scaling out.
- Autoscale on the signal that saturates first: CPU for CPU-bound
  services; concurrency, queue depth or latency for I/O-bound ones. New
  instances take time to boot and warm, so keep headroom.
- Shared caches (Redis, Valkey) for data that must agree across instances;
  an in-process cache only for small, hot, rarely changing data.

## Check it

- The same load test (`performance-load`) before and after: p50, p95,
  p99, throughput and error rate at the same arrival rate.
- A trace of the slow endpoint before and after: fewer spans, no comb of
  queries, no unexplained gaps.
- Queries per request counted, with a test asserting the count where the
  stack allows it.
- Pool metrics under load: waiting near zero, acquire times in single
  milliseconds.
- The project's tests pass; what could not be run (no staging, no
  permission to load test) is said plainly.

## Avoid

A cache in front of an unfixed query; a bigger pool to cure pool waits; a
pool per request or a client per call; blocking calls inside an async
runtime; unbounded queues and concurrency; retries without backoff, budget
or idempotency; calls without timeouts, or timeouts longer than the
request; external calls inside a transaction; sticky sessions; compressing
twice or compressing images; a new serialiser without a measurement; a
speed-up claimed from one request in a browser.
