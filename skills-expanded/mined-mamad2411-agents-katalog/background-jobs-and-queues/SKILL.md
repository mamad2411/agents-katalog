---
name: background-jobs-and-queues
description: Moving work off the request path with queues (BullMQ) — idempotent at-least-once handlers, retries/backoff/DLQ, small payloads, scheduling, the outbox pattern, and queue observability. Use when adding background jobs, async processing, or scheduled tasks.
---

# Background Jobs and Queues

Apply when moving work off the request/response path or adding scheduled processing.

## When to move work off the request path

Push to a queue when the work is: slow (external API calls, PDF/image processing), retryable, fan-out (notifications), or must survive a client disconnect. Keep the HTTP handler fast: validate, enqueue, return `202`/an id. Do **not** do heavy or unreliable work synchronously in the request.

## BullMQ conventions

- **One queue per domain concern** (`emails`, `image-processing`, `webhooks`), each with its own worker and concurrency tuned to the workload.
- Name jobs; keep a typed payload schema per job.
- Configure a Redis connection deliberately (persistence expectations, eviction policy `noeviction` for a durable queue).

```ts
const emailQueue = new Queue('emails', { connection });
await emailQueue.add('welcome', { userId }, {
  attempts: 5,
  backoff: { type: 'exponential', delay: 2000 },
  removeOnComplete: 1000,
  removeOnFail: false, // keep failures for inspection / DLQ handling
});
```

## Handlers are idempotent (at-least-once)

- **Exactly-once delivery is a lie.** Queues (and their retries, and worker crashes after side effects) give you **at-least-once** — design every handler to be safe to run more than once.
- Key each job by a stable business id; before acting, check whether the effect already happened (a `processedJobs` record, a unique constraint, an idempotency key on the downstream call). Make the operation naturally idempotent where possible (upsert, not insert).

## Retries, backoff, and DLQ

- Set finite `attempts` with **exponential backoff** so transient failures recover without hammering downstreams.
- Distinguish **retryable** (timeouts, 5xx, rate limits) from **permanent** (validation, 4xx) failures — fail fast and don't retry the permanent ones.
- Route exhausted/failed jobs to a **dead-letter queue** (or keep `removeOnFail: false` and a failed-jobs handler) for inspection and manual replay. Alert on DLQ growth.

## Small payloads

- Put **ids, not blobs**, in job payloads. The handler fetches current data from the DB when it runs — this avoids stale data, keeps Redis small, and dodges payload size limits.

## Scheduling / cron jobs

- Use repeatable/cron jobs (BullMQ repeatable jobs or a scheduler) for periodic work. Ensure a single scheduler instance owns the schedule (avoid duplicate triggers across replicas).
- Make scheduled work idempotent and safe to skip/overlap; guard long-running jobs with a lock so two runs don't overlap.

## Outbox pattern for reliability with DB writes

When a job must be enqueued as a result of a DB change, a crash between the DB commit and the enqueue loses the job (or a rollback after enqueue creates a phantom). Fix with the **transactional outbox**:

1. In the **same DB transaction** as the business write, insert a row into an `outbox` table.
2. A separate relay polls unpublished outbox rows and publishes them to the queue, marking them sent.

This guarantees the job is enqueued **iff** the DB change committed (at-least-once, consumers idempotent).

## Queue observability

- Emit metrics for **queue depth**, **oldest job age (latency)**, **processing rate**, and **failure/DLQ counts**.
- Alert on: growing backlog, rising job age (workers can't keep up), and DLQ entries.
- Log job start/finish with the job id and correlation id propagated from the originating request (see `observability-logging`).

## Gated architecture decision

**Introducing a new queue technology or message broker** to the system (a new Redis/Kafka/SQS/RabbitMQ dependency, or a fundamentally new async transport) is a **gated architecture decision** — surface it and get human approval. Adding another queue on the existing broker is routine; adding a new broker is not.

## Anti-patterns

- Doing slow/retryable work synchronously in the HTTP handler.
- Non-idempotent handlers that double-charge/double-send on retry.
- Large blobs in payloads; stale data captured at enqueue time.
- Infinite retries with no backoff; no DLQ, so failures vanish.
- Enqueue outside the DB transaction (lost/phantom jobs) instead of an outbox.
- No metrics on depth/age — silent backlog until it's an outage.
