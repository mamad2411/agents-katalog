---
name: backpressure-patterns
description: >
  Backpressure patterns for owned services: bounded queues, load shedding, admission
  control, slow-consumer handling, timeout budgets, and reactive streams signals.
  Use when systems overload under traffic spikes or slow dependencies — not for
  DDoS attacks against third parties.
---

# Backpressure Patterns

## Scope And Authorization

- **In scope:** Systems you own or are authorized to tune (APIs, workers, streams).
- **Out of scope:** Generating attack traffic against third-party systems.
- Load tests need approval; production shedding drops user work — communicate SLOs.
- Pair with queue skills (`aws-sqs-fair-queues`, `azure-servicebus-sessions`) when messaging-specific.
- Use `code-quality-standards` for implementation.

## When To Use

- Cascading timeouts, unbounded queue memory growth, thread pool exhaustion.
- Designing admission control at API edge or worker pool.
- Choosing between buffering, dropping, sampling, or rejecting work.
- Reactive/streaming pipelines (Rx, reactive streams, Kafka consumers) with slow sinks.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| SQS multi-tenant fairness | `aws-sqs-fair-queues` |
| Service Bus sessions | `azure-servicebus-sessions` |
| Retry/backoff only | `retry-backoff-patterns` |
| Observability instrumentation | `observability-metrics-tracing` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Pattern | Intent |
| --- | --- |
| Bounded queue | Cap memory; block or reject when full |
| Load shedding | Drop/reject low-priority work under pressure |
| Admission control | Limit in-flight requests (token bucket, concurrency) |
| Slow consumer | Pause pull/poll; avoid infinite buffer |
| Timeout budget | End-to-end deadlines; cancel work |
| Bulkheads | Isolate pools per dependency |
| Tooling | Metrics (queue depth, reject rate), load tests, circuit breakers |

## Workflow

### 1. Confirm scope and success criteria

1. Service, critical vs optional endpoints, SLOs (latency, error rate), authorization for tests.
2. Success: under overload, system stays up; returns 429/503 predictably; recovers without restart.
3. Define which work is shed first (bulk ops, exports, non-critical features).

### 2. Inventory failure modes

```bash
# Examples — adapt to stack
# - Queue depth / memory RSS
# - Thread pool active / queued
# - Dependency p99 latency
# - GC pressure
```

1. Map every unbounded buffer (channels, lists, Kafka auto-commit with processing lag).
2. List retries that amplify load (retry storms).
3. Note autoscaling signals (CPU only may be wrong).

### 3. Baseline under controlled load

1. Authorized load test: ramp to break; capture saturation metric.
2. Record memory at failure, error types, recovery time.
3. Identify first resource exhausted (connections, heap, disk, CPU).

### 4. Apply patterns

**Concurrency limit (sketch):**

```text
semaphore = N  # max in-flight
on request:
  if not semaphore.try_acquire():
    return 503 or 429 + Retry-After
  try handle()
  finally release()
```

**Bounded queue:**

```text
queue.capacity = C
if full:
  policy = block | drop_oldest | drop_newest | reject_producer
```

**Timeout budget:**

```text
deadline = now + 2s
propagate cancel to downstream; do not start work if remaining < min
```

1. Prefer **reject early** at edge over deep buffering.
2. Combine with **retry-backoff** + jitter; honor `Retry-After`.
3. Bulkheads: separate pools for payment vs catalog dependencies.
4. Messaging: pause consumption when handler lag high; set max prefetch.
5. Priorities: protect interactive traffic; shed batch.
6. Circuit break half-open after cooldown when dependency unhealthy.

### 5. Verify with evidence

1. Load test: latency plateaus, reject rate rises, memory stable.
2. Kill dependency: callers fail fast, not hang.
3. Recovery: when load drops, success rate returns without manual flush.
4. Unit tests for queue-full policies.

### 6. Observe and harden

1. Metrics: in-flight, queue depth, shed count, timeout count, dependency health.
2. Alerts on sustained shed rate and queue near capacity.
3. Dashboards for SLO burn under shedding (good shedding still has user impact).

### 7. Hand off

1. Document policies (N concurrency, C queue, priority order).
2. Runbook: when to raise limits vs scale out vs disable feature flags.
3. Client guidance for 429/503 retries.

## Pattern Selection

| Symptom | First pattern |
| --- | --- |
| Heap OOM from buffers | Bound queues + drop/reject |
| Thread starvation | Concurrency limits + bulkheads |
| Retry storms | Budget + breaker + jitter |
| Kafka lag explosion | Pause poll / reduce prefetch |
| UX latency blowup | Shed noncritical + edge admission |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Buffers | Bounded with policy | Infinite channel “for smoothness” |
| Rejection | Explicit 429/503 | Silent drop without metrics |
| Retries | Client backoff | Immediate tight retry loops |
| Isolation | Bulkheads per dependency | One pool for all IO |
| Testing | Load test + chaos dependency | Only happy-path unit tests |

## Output Checklist

- [ ] Overload symptoms and first resource documented
- [ ] Critical vs sheddable work classified
- [ ] Bounded queues / admission control implemented
- [ ] Timeout budgets and bulkheads considered
- [ ] Load test shows stable memory and predictable rejects
- [ ] Metrics and alerts for depth/shed/timeouts
- [ ] Client retry guidance published
- [ ] `code-quality-standards` applied

## Rules

- Authorized testing only; no third-party stress attacks.
- Fail predictable; measure shedding.
- Prefer early rejection over unbounded buffer.
- Propagate cancellation and deadlines.
- Align retries with backpressure (don’t fight it).
