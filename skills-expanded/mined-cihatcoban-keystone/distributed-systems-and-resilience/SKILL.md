---
name: distributed-systems-and-resilience
description: Makes code survive partial failure - timeouts, retries, idempotency, backpressure, circuit breakers, outbox, sagas. Triggers - calling an external API, how should retries work, timeout, duplicate messages from the queue, webhook, exactly once, cascading failure.
---

# Distributed Systems and Resilience

The moment a call crosses a process boundary, three things become possible that
were impossible before: it can be slow, it can fail halfway, and **you cannot
tell those apart from success**. Code that assumes a network call behaves like
a function call works perfectly until the day it takes the system down.

## The rules that are never optional

1. **Every network call has a timeout.** No exceptions. A default of "infinite"
   is how one slow dependency exhausts your connection pool and stops
   everything. Set connect and read timeouts separately, and make the total
   budget shorter than your caller's timeout.
2. **Every write is idempotent, or it is broken.** A timeout does not mean the
   write did not happen. The retry will duplicate it unless the operation has a
   key the receiver deduplicates on.
3. **Every retry has a bound and jitter.** Unbounded retry is a denial-of-service
   attack on your own dependency. Synchronized retries (no jitter) produce
   thundering herds that keep a recovering service down.
4. **Only retry what is retryable.** A 400 will fail identically forever.
   Retrying deterministic failures burns budget and hides the real error.

## Timeout and retry policy

| Parameter | Sensible default | Notes |
|---|---|---|
| Connect timeout | 1–3 s | Failure to connect is fast in a healthy network |
| Read timeout | Derived from the caller's budget, not from the dependency's p99 | Slower than this and you are queueing, not waiting |
| Attempts | 3 total | More rarely helps; it just delays the error |
| Backoff | Exponential from ~100 ms, with **full jitter** | `sleep = random(0, min(cap, base·2^n))` |
| Retry budget | ≤ 10% of traffic may be retries | Above this, you are amplifying an outage |
| Retryable | Timeouts, connection errors, 429, 502/503/504 | Never 4xx except 429 |

Retry at **one** layer. Retries nested at three layers multiply: 3 × 3 × 3 = 27
requests for one logical call.

## Idempotency

| Technique | Use when |
|---|---|
| Client-generated idempotency key, stored with the result | External writes, payments, order creation |
| Natural unique key + upsert | Ingestion of records with a stable external id |
| Conditional write (compare-and-set on a version) | State transitions; also prevents lost updates |
| Deduplication window on a message id | Queue consumers |

Store the **result** against the key, not just the fact of having seen it —
otherwise a retry after a crash returns nothing and the caller retries forever.

"Exactly once delivery" does not exist. What exists is at-least-once delivery
plus idempotent processing, which is indistinguishable from the outside. Design
for that, and stop looking for the setting.

## Failure isolation

| Pattern | Problem it solves |
|---|---|
| **Circuit breaker** | Stops hammering a dead dependency; fails fast while it recovers. Trip on error rate over a window, half-open to probe |
| **Bulkhead** | Separate connection pools/thread pools per dependency, so one slow dependency cannot consume all capacity |
| **Backpressure** | Bounded queues that reject or shed load when full. An unbounded queue converts a throughput problem into an out-of-memory crash |
| **Load shedding** | Reject low-priority work early under stress, preserving the critical path |
| **Graceful degradation** | Serve stale cache, partial results or a reduced feature instead of an error |
| **Hedged request** | Send a duplicate after p95 to cut tail latency — only for idempotent reads |

**Fail fast beats failing slow.** A fast error is recoverable; a hanging request
consumes resources from everyone else and turns a local fault into a global one.

## Cross-service workflows

- **Transactional outbox** — write the business change and the outgoing message
  in the *same local transaction*, to an outbox table; a relay publishes it.
  This eliminates the "committed but never published" and "published but rolled
  back" failures that "save then publish" always has.
- **Saga** — a sequence of local transactions with explicit compensating
  actions. Required when a workflow spans services. Design the compensation
  *before* the happy path: a refund is not always the inverse of a charge.
- **Two-phase commit across services** — avoid. The coordinator's availability
  becomes everyone's availability.
- **Choreography vs orchestration** — events (choreography) couple loosely but
  the overall flow exists nowhere and is undebuggable past ~3 steps; an explicit
  orchestrator couples more but the flow is visible. Prefer orchestration for
  business-critical, multi-step workflows.

## Clocks, ordering and state

- Never trust a clock for ordering across machines; use logical versions or a
  sequencer. Clock skew is real and will reorder your events.
- Messages arrive out of order and duplicated. Consumers must tolerate both.
- A cache invalidation that "just misses" is a stale read; decide the staleness
  budget explicitly rather than pretending it is zero.

## Testing failure

If a failure mode has never been exercised, assume the handling is wrong.

- Unit-test the retry/backoff policy with a fake clock
- Integration-test against a dependency that returns 500s, hangs, and closes
  connections mid-response
- Verify idempotency by replaying the same request and asserting one effect
- Load-test until something breaks — knowing *which* thing breaks first is the
  point, and you want to learn it before a customer does

## Exit checklist

- [ ] Every outbound call has connect and read timeouts, and a total budget
- [ ] Retries: bounded, jittered, only on retryable classes, at exactly one layer
- [ ] Every write path has an idempotency mechanism, and the result is stored
- [ ] Queues are bounded; behavior when full is a decision, not an accident
- [ ] Dependencies are isolated (separate pools) and have a breaker or equivalent
- [ ] Events published via outbox, not "save then publish"
- [ ] Multi-service workflows define compensation before implementation
- [ ] Failure paths are covered by tests, not only reasoning
