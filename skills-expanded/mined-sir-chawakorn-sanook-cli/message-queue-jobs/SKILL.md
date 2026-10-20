---
name: message-queue-jobs
description: Builds async job and message-queue workflows (producers/consumers, idempotency, retries with backoff, dead-letter queues, exactly-once semantics) when offloading work or decoupling services.
when_to_use: User wants background jobs, a queue/worker, event-driven processing, or to fix duplicate processing, lost messages, retry storms, or poison messages. Covers Redis/SQS/Kafka/RabbitMQ/Celery/BullMQ-style systems.
---

---
name: message-queue-jobs
description: Builds async job and message-queue workflows (producers/consumers, idempotency, retries with backoff, dead-letter queues, exactly-once semantics) when offloading work or decoupling services.
when_to_use: User wants background jobs, a queue/worker, event-driven processing, or to fix duplicate processing, lost messages, retry storms, or poison messages. Covers Redis/SQS/Kafka/RabbitMQ/Celery/BullMQ-style systems.
---

# Message Queue & Async Jobs

## When to Use

Reach for this skill when the task is one of:

- **Offload slow work** — email, image/video processing, report generation, webhooks out → move it off the request path so the API responds fast.
- **Decouple services** — service A emits an event, service B reacts, without a synchronous call chain.
- **Fan-out / scheduled / batch** — one event triggers N workers, or work runs on a timer.
- **Fix a broken queue** — symptoms map to root causes:

| Symptom | Likely root cause | Section |
|---|---|---|
| Same side effect happens twice (double charge, double email) | At-least-once delivery + non-idempotent handler | Steps 1, 3 |
| Messages vanish, work never runs | Ack-before-process, or no DLQ for failures | Steps 2, 4 |
| Worker hammers a downstream into outage | Fixed-interval retries, no jitter, no backpressure | Steps 4, 5 |
| One bad message blocks the whole partition/queue | No poison-message handling / no DLQ | Step 4 |
| Queue depth climbs forever | Consumers slower than producers, no throttle/autoscale | Steps 5, 6 |

If the work is fast, in-process, and never needs a retry, **do not add a queue** — it's complexity you'll pay for forever. Say so.

## Steps

### 1. Pick broker + delivery semantics first (this decides everything else)

- Match broker to existing infra — don't add a new system if one is already running:
  - **Redis-backed lib** (BullMQ / Celery+Redis / Sidekiq): simplest, low-latency jobs, single region. Good default for app-level background jobs.
  - **Managed queue** (SQS-style): zero ops, built-in DLQ + visibility timeout. Default when on that cloud.
  - **Log/stream** (Kafka-style): ordered, replayable, high-throughput, multi-consumer fan-out. Use for event sourcing / analytics, **not** for simple job offload.
  - **AMQP broker** (RabbitMQ-style): rich routing (topic/fanout exchanges), per-message TTL.
- **Assume at-least-once. Build for it.** True exactly-once delivery does not exist across a network. What you actually deliver is **at-least-once delivery + idempotent processing = effectively-once.** Kafka's "exactly-once" only holds for read→process→write *inside one Kafka transaction*; the moment a handler touches an external API or DB outside that transaction, you're back to at-least-once. Design idempotency (Step 3) regardless.
- Decide ordering need now: most jobs don't need it. If they do, you need a partition/group key and it caps your parallelism (one in-flight per key).

### 2. Design producer, consumer, and a versioned message schema

- **Message = a typed envelope, not a blob.** Required fields:
  ```
  { id, type, version, occurred_at, idempotency_key, payload, attempts }
  ```
- Put a **stable `idempotency_key`** in the message at produce time (e.g. derived from the business event: `order:1234:charge`). Do **not** use the broker's auto-generated message id — it changes on redelivery.
- **Keep payloads small.** Send IDs/references, not large rows or files. Store blobs in object storage and pass the key. Big payloads blow past broker size limits (SQS 256KB, etc.) and slow every consumer.
- **Schema versioning:** consumers must tolerate unknown fields and handle old `version` values during rolling deploys. Never reuse a field name with a new meaning — add a new field and bump `version`.
- **Producer flush:** confirm the broker accepted the message (await the publish ack) before you report success upstream. Fire-and-forget producers silently drop messages on broker hiccups.

### 3. Make handlers idempotent — this is the load-bearing step

Retries are guaranteed, so a handler that runs twice must produce the same result as running once.

- **Dedup table / dedup key (preferred for side-effects):** before doing work, `INSERT idempotency_key` into a table with a UNIQUE constraint. If the insert conflicts, the message was already processed → ack and skip. Do the insert and the side-effect in the **same transaction** where possible.
- **Natural idempotency:** prefer operations that are safe to repeat — `UPSERT` / `SET x=v` over `INSERT` / `x = x + 1`. Use conditional writes (`UPDATE ... WHERE status='pending'`).
- **External calls:** pass the `idempotency_key` to downstream APIs that support it (payment providers do). Wrap non-idempotent calls in your own dedup check.
- **Set a TTL on dedup keys** longer than your max retry window (e.g. retries span 1h → keep keys ≥ 24h), then expire them so the table doesn't grow unbounded.

### 4. Retries with backoff + a dead-letter queue

- **Exponential backoff WITH jitter.** Never fixed-interval, never un-jittered — synchronized retries cause a thundering herd that takes the downstream out a second time.
  ```
  delay = min(cap, base * 2 ** attempt)
  delay = random_between(0, delay)   # full jitter
  ```
- **Bounded max attempts** (typically 3–6). On exceeding, route the message to a **dead-letter queue (DLQ)** — never drop it, never retry forever.
- **Classify failures before retrying:**
  - *Transient* (timeout, 5xx, throttle) → retry with backoff.
  - *Permanent* (validation error, 4xx, malformed payload = **poison message**) → DLQ immediately, attempts wasted otherwise.
- **Poison messages:** one un-handleable message must not block the queue/partition behind it. With a DLQ this is automatic; with ordered Kafka partitions you must skip-and-DLQ explicitly or the partition stalls forever.
- **Have a DLQ drain plan:** an alarm on DLQ count + a documented redrive (fix bug → replay DLQ back to main queue). A DLQ nobody watches is a silent data-loss bucket.

### 5. Backpressure so consumers never overwhelm anything

- **Bounded concurrency** per worker (`prefetch` / `concurrency` / `maxInFlight`). Default low (e.g. 5–10) and raise with evidence. Unbounded concurrency = OOM and downstream meltdown.
- **Visibility timeout / ack deadline > p99 processing time.** Too short → the message redelivers *while you're still processing it* → duplicate work. Too long → slow recovery after a crash. Set it, and for long jobs heartbeat/extend it.
- **Throttle on queue depth:** when depth or consumer lag exceeds a threshold, slow producers or scale consumers — don't just pile on.
- **Rate-limit the downstream**, not just the queue (token bucket on the external API), so a sudden backlog drain doesn't exceed third-party quotas.

### 6. Observability — you can't operate a queue you can't see

Emit and alarm on, at minimum:

- **Queue depth** (backlog size) and **trend** — rising = consumers losing.
- **Oldest-message age / consumer lag** — the real "are we behind?" signal (depth alone lies when message size varies).
- **DLQ count** — should be ~0; any nonzero needs eyes.
- **Processing latency** (p50/p99) and **throughput** (msgs/sec).
- **Retry rate** — a spike means a downstream is degrading; alarm before it becomes a DLQ flood.
- **Trace context:** propagate a `trace_id` from producer through consumer so one logical operation is followable across the async boundary.

### 7. Test failure injection before you ship

Happy-path passing proves nothing here. Add tests that prove correctness under failure:

1. **Duplicate delivery** — send the same message twice → assert the side-effect happens exactly once (proves Step 3).
2. **Out-of-order / delayed** — deliver messages out of order → assert correctness if you claimed ordering, or assert order-independence if you didn't.
3. **Poison message** — feed a malformed payload → assert it lands in the DLQ and the next good message still processes.
4. **Crash mid-process** — kill the worker after the side-effect but **before ack** → restart → assert no duplicate (visibility timeout redelivers; idempotency must absorb it).
5. **Retry exhaustion** — force a permanent failure → assert it stops at max attempts and DLQs, no infinite loop.

## Common Errors

- **Ack-before-process.** Acking on receive (or `auto-ack`/`enable.auto.commit=true` with default timing) loses the message if the worker dies mid-job. **Always ack/commit only after the work + its side-effects are durably committed.**
- **Using the broker's message id as the idempotency key.** It changes on redelivery, so dedup never matches and you process duplicates anyway. Use a business-derived key set at produce time (Step 2).
- **Believing "exactly-once delivery" exists.** Vendors sell at-least-once or at-most-once. "Exactly-once" is a *processing* property you build with idempotency, not a delivery guarantee you buy.
- **Fixed-interval or un-jittered retries.** Turns one downstream blip into a synchronized retry storm. Always exponential + full jitter (Step 4).
- **Visibility timeout shorter than processing time.** The message reappears and a second worker starts the same job → guaranteed duplicates that look like a "random" bug. Measure p99, set timeout above it, extend for long jobs.
- **No DLQ.** Failures either retry forever (resource burn, head-of-line block) or get dropped (silent data loss). There is no good third option without a DLQ.
- **Unbounded concurrency / prefetch.** A backlog drain spins up unlimited in-flight work → OOM or a downstream outage. Always cap (Step 5).
- **Giant payloads in the message.** Hits broker size limits and bloats every consumer's memory. Send a reference; store the blob elsewhere.
- **Producer doesn't await the publish ack.** Fire-and-forget drops messages on transient broker errors and you never know. Confirm acceptance before reporting success.
- **Non-idempotent handler "fixed" by hoping retries won't happen.** They will. Idempotency is mandatory, not optional, under at-least-once.

## Verify

Before declaring done, confirm each — with evidence, not assertion:

- [ ] Idempotency test passes: same message delivered 2x → side-effect occurs once (show the test + run output).
- [ ] DLQ exists and is wired: poison message → lands in DLQ, queue keeps draining (show it).
- [ ] Retries use exponential backoff **with jitter** and a finite max-attempts (show the config/code).
- [ ] Ack/commit happens **after** the side-effect commits, not before (point to the line).
- [ ] Visibility timeout / ack deadline > measured p99 processing time (state both numbers).
- [ ] Concurrency/prefetch is bounded (show the value).
- [ ] Metrics emitted for queue depth, oldest-message age, DLQ count, retry rate; alarm on DLQ > 0.
- [ ] Crash-mid-process test: kill before ack → restart → no duplicate (show run).
- [ ] Producer awaits publish ack; payload carries a stable `idempotency_key` and `version`.

If any box can't be checked with a real run/config, it is **not** done — fix the root cause, don't loosen the test.

## Related

- `update-config` — to install a queue-health check or DLQ alarm as a recurring hook/job.
