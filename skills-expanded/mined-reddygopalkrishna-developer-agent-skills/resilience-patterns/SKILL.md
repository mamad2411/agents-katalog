---
name: resilience-patterns
description: Makes services survive slow and failing dependencies - timeouts and deadline propagation, safe retries with backoff and jitter, retry budgets, circuit breakers, bulkheads, load shedding, backpressure, idempotent consumers, transactional outbox, sagas, health checks and graceful shutdown. Use when adding or reviewing calls to other services, databases, queues or third-party APIs, designing message consumers, fixing cascading failures or retry storms, or writing health probes and shutdown logic.
license: MIT
---

# Resilience Patterns

Every remote call can be slow, fail, or succeed without you knowing. Bound every wait, retry only what is safe to repeat, and make sure one failing dependency cannot take the whole system down with it.

## When to use

- Adding or reviewing code that calls another service, a database, a cache, a queue or a third-party API.
- Writing a message or event consumer.
- Investigating cascading failures, thread or connection pool exhaustion, retry storms, or duplicate side effects.
- Writing liveness/readiness probes or shutdown handling.

Not for: in-process error handling with no I/O, or choosing a message broker.

## Workflow

1. **Inventory the dependencies.** For the code in scope, list every outbound call: target, protocol, client library, whether the operation is idempotent, and what the caller does if it fails.
2. **Check timeouts first.** Find each client's connect timeout and request/read timeout. Many clients default to *no* timeout (for example Python `requests` and Go's zero-value `http.Client`). Set explicit values derived from the caller's own deadline.
3. **Classify failures.** For each call, mark which errors are transient (connection reset, 503, 429, gRPC `UNAVAILABLE`) and which are permanent (4xx validation, auth, 404). Only transient errors are retry candidates.
4. **Decide retries per call** with the table below. Retry at one layer only.
5. **Add isolation:** a circuit breaker for dependencies that can fail hard, bulkheads (separate pools or concurrency limits) so one slow dependency cannot use up shared threads or connections.
6. **Protect yourself:** bounded queues, concurrency limits and load shedding at the entry point.
7. **Make side effects idempotent** where delivery is at-least-once (queues, webhooks, retries). Use the outbox when a database write and a message publish must both happen.
8. **Define degraded behavior** for each dependency: cached value, default, partial response, or fail fast with a clear error.
9. **Verify** with tests that inject latency and errors (a fake server, a fault-injection proxy such as Toxiproxy, or your service mesh's fault injection). Watch for behavior, not just "no exception".

Pseudo-code for each pattern is in [references/patterns.md](references/patterns.md). Read it when implementing one.

## Timeouts and deadlines

- Every network call has a timeout. No exceptions, including database queries and cache reads.
- Set the connect timeout short (typically well under a second inside a data center) and the request timeout from the latency SLO of the dependency (for example a little above its p99.9), not a round number someone guessed.
- **Propagate deadlines.** If the incoming request has 800 ms left, a downstream call must not get a 2 s timeout. gRPC propagates deadlines through the context. Over HTTP, pass the remaining budget explicitly (a header your services agree on) and use your language's cancellation mechanism (Go `context`, .NET `CancellationToken`, JS `AbortSignal`).
- An inner timeout must be shorter than the outer one. Otherwise the caller gives up while work continues for nothing.
- Cancel abandoned work when the caller disconnects or the deadline passes.

## Retries

| Situation | Retry? |
|---|---|
| Idempotent read (GET, SELECT) failing transiently | Yes, with backoff and jitter |
| Idempotent write (PUT, DELETE, upsert by key) failing transiently | Yes |
| Non-idempotent write (POST create, charge, send) | Only with an idempotency key the server honors |
| 4xx validation, 401, 403, 404, 409 | No; it will fail the same way |
| 429 or 503 with `Retry-After` | Yes, but wait at least `Retry-After` |
| Timeout on a non-idempotent write | Never blindly; the first attempt may have succeeded |
| Circuit breaker open | No; fail fast or degrade |

Rules:

- **Exponential backoff with jitter**, capped: `sleep = random(0, min(cap, base * 2^attempt))` ("full jitter"). Without jitter, clients retry in synchronized waves.
- **Small attempt counts:** 2-3 total attempts is usual for synchronous calls. The user is waiting.
- **Retry at one layer.** Three layers each making 3 attempts turns one failure into 3 x 3 x 3 = 27 calls to the bottom service. Pick the layer closest to the failure (often the client library or the mesh) and disable retries elsewhere.
- **Retry budgets:** cap retries as a fraction of total traffic (for example around 10%), so that during an outage retries cannot multiply load. gRPC retry throttling and many meshes support this.
- Respect the overall deadline. Never retry past it.
- Log and count retries. A rising retry rate is an early warning.

## Circuit breakers

- **Closed:** calls flow; failures are counted over a sliding window.
- **Open:** after the failure rate passes a threshold (with a minimum number of calls), fail immediately for a cool-down period.
- **Half-open:** let a few trial calls through; close on success, re-open on failure.
- One breaker per dependency (and per endpoint if they fail independently), never one global breaker.
- Count timeouts and 5xx as failures; do not count 4xx caused by the caller.
- Pair it with a fallback and expose the breaker state as a metric.

## Bulkheads, load shedding, backpressure

- **Bulkheads:** a separate connection pool, thread pool or semaphore per dependency, sized to that dependency's capacity. A slow recommendations service must not use up the threads that serve checkout.
- **Concurrency limits at the entry point:** reject excess work early with 503 (or 429 for per-client limits) instead of queueing it until it times out. Adaptive concurrency limiters adjust the limit from observed latency.
- **Prioritize:** under overload, shed low-priority traffic (batch jobs, prefetch) before user-facing requests.
- **Bounded queues everywhere.** An unbounded queue hides overload until memory runs out, and every queued item is already late.
- **Backpressure:** consumers pull at their own rate (bounded prefetch on brokers, reactive streams), and producers slow down or drop when queues are full.

## Idempotency and messaging

- Assume at-least-once delivery from every queue, webhook and retrying client. Consumers must be idempotent.
- **Idempotent consumer:** record the message ID in a processed-messages table with a unique constraint, *in the same transaction* as the side effect. Skip the message if the ID already exists.
- **Natural idempotency** is better when available: upserts by business key, `SET status = 'shipped' WHERE status = 'packed'`, absolute values instead of increments.
- **Transactional outbox:** never write to the database and then publish to a broker as two independent steps, because a crash between them loses or duplicates events. Write the event to an `outbox` table in the same transaction as the state change, then a relay (polling, or change data capture such as Debezium) publishes it and marks it sent. Consumers still dedupe.
- **Sagas** for multi-service workflows: a sequence of local transactions, each with a compensating action (refund, release, cancel). Orchestration (one coordinator) is easier to reason about than choreography (services react to each other's events) once there are more than about three steps. Compensations must themselves be idempotent and retryable.
- Poison messages: after N failed attempts, move the message to a dead-letter queue with the error, alert, and keep consuming.

## Graceful degradation

For each dependency, write down the fallback before an incident forces the choice:

| Dependency down | Typical fallback |
|---|---|
| Recommendations, personalization | Static or popular defaults |
| Pricing or inventory read | Short-lived cached value, clearly marked stale |
| Search | Basic database query, or a clear "temporarily unavailable" |
| Payments, auth | Fail closed with a clear error; never fake success |

## Health checks and shutdown

- **Liveness:** "is this process broken beyond recovery?" Check only the process itself (event loop responsive, no deadlock). **Never check dependencies in liveness.** If you do, a database outage makes the orchestrator restart every instance, which is a self-inflicted outage.
- **Readiness:** "should this instance receive traffic now?" Fail it while starting, while draining, and when a dependency it cannot work without is unreachable.
- **Startup probe** (Kubernetes) for slow-starting apps, so liveness does not kill them during boot.
- Keep probes cheap, and give them their own timeout.

Graceful shutdown on SIGTERM:

1. Fail readiness so the load balancer stops sending new requests. In Kubernetes, endpoint removal is asynchronous, so keep serving for a few seconds (a `preStop` sleep) before closing listeners.
2. Stop accepting new connections and messages; stop consumer polling.
3. Finish in-flight requests and messages within a bounded time.
4. Flush telemetry, close pools, and exit before the orchestrator's grace period ends (Kubernetes default `terminationGracePeriodSeconds` is 30).

## Libraries (check current docs before adding)

| Stack | Common choices |
|---|---|
| Java/Kotlin | Resilience4j (Hystrix is in maintenance mode; do not adopt it) |
| .NET | Polly; `Microsoft.Extensions.Http.Resilience` for `HttpClient` |
| Python | tenacity (retries); explicit `timeout=` on every client |
| Go | `context` deadlines; sony/gobreaker or failsafe-go |
| Node.js | `AbortSignal.timeout()`; cockatiel or opossum |
| Platform | Service mesh or proxy (Envoy, Istio, Linkerd) timeouts, retries, outlier detection |

If a mesh already retries, do not add application-level retries on the same calls.

## Anti-patterns

- **No timeout because "the service is fast"** — it is fast until it isn't, and then every thread waits on it.
- **Retrying everything** — retrying 400s, retrying non-idempotent POSTs, retrying at every layer.
- **Retries without jitter** — synchronized retries knock the dependency over again as soon as it recovers.
- **Liveness probe that checks the database** — turns a database blip into a full restart storm.
- **Dual writes** (database commit, then publish) — lost or phantom events; use the outbox.
- **Catch-and-ignore fallbacks** that return wrong data silently (zero balance, empty cart) — degrade visibly.
- **Unbounded in-memory queues and pools** — they turn overload into out-of-memory crashes.
- **Circuit breaker shared across all dependencies** — one bad dependency blocks healthy ones.

## Done when

- Every outbound call has explicit connect and request timeouts that fit inside the caller's deadline.
- Retries exist only for transient errors on idempotent (or idempotency-keyed) operations, use capped exponential backoff with jitter, and happen at exactly one layer.
- Hard-failing dependencies have a circuit breaker and a defined fallback.
- Queues and pools are bounded; overload is rejected early with 503/429.
- Consumers are idempotent; database writes paired with events use an outbox.
- Liveness checks only the process; readiness and shutdown drain cleanly.
- Fault-injection tests (latency, errors, dependency down) show the expected degraded behavior.

## References

- [references/patterns.md](references/patterns.md) — pseudo-code for backoff, circuit breaker, idempotent consumer, outbox relay, saga and graceful shutdown. Read it when implementing any of them.
