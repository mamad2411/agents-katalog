---
name: background-jobs
description: Designs and reviews background jobs, task queues, workers and scheduled (cron) jobs - queue choice, small ID-based payloads, idempotent handlers, retries with backoff and dead-letter queues, timeouts and heartbeats, concurrency and rate limits, transactional enqueue, single-runner schedules, deduplication and graceful shutdown. Use when moving work out of a request, adding a worker or job (Sidekiq, Celery, BullMQ, Hangfire, Quartz, etc.), writing a cron job, or fixing duplicate, lost, stuck or piling-up jobs.
license: MIT
---

# Background Jobs

A job will run zero times, once, or more than once, possibly at the same time as itself, possibly hours late. Design every job so all of those outcomes are safe: enqueue it reliably, make the handler idempotent, bound its time and retries, and make failures visible.

## When to use

- Moving slow or failure-prone work out of a request (emails, exports, image processing, calls to third-party APIs, webhooks).
- Adding a worker, a queue, a scheduled job, or a recurring cleanup.
- Jobs are duplicated, lost, stuck, retried forever, or the queue keeps growing.

Not for: event streams between services and schema evolution (see the event-driven-architecture skill), or batch data pipelines (see the data-pipelines skill).

## Does it belong in a background job?

| Situation | Background job? |
| --- | --- |
| The user doesn't need the result to continue (email, thumbnail, audit export) | Yes |
| Work calls a slow or flaky third party | Yes, with retries |
| Work takes longer than the request timeout | Yes, return 202 plus a status resource (see the api-design skill) |
| The user needs the result in the same response, and it is fast | No, do it inline |
| The work must happen in the same transaction as the write | No, do it inline, or use the outbox so enqueue and write commit together |

## Choosing a queue

| Option | Good for | Watch out for |
| --- | --- | --- |
| **Database-backed queue** (a jobs table with `SELECT ... FOR UPDATE SKIP LOCKED`, or a library built on it) | Moderate volume; enqueue in the same transaction as the business write; no new infrastructure | Table bloat and vacuum load at high volume; polling cost |
| **Redis-based queue** (e.g. Sidekiq, BullMQ, RQ) | High throughput, low latency, rich features (scheduling, rate limits, uniqueness) | Durability depends on Redis persistence settings; enqueue is not transactional with your database |
| **Message broker / cloud queue** (RabbitMQ, SQS, Azure Service Bus, Google Pub/Sub) | Cross-service work, very high volume, managed retries and DLQs | At-least-once delivery; ordering only with specific features; visibility timeouts to tune |
| **Workflow engine** (e.g. Temporal, cloud step functions) | Long, multi-step processes with waits and compensation | Extra concepts and infrastructure; overkill for single-step jobs |

Default: use the queue the codebase already has. If there is none and the volume is moderate, a database-backed queue gives transactional enqueue for free.

## Workflow

1. **Write down the job contract:** name, payload fields, what it changes, whether it is safe to run twice, expected duration, and what happens if it fails permanently.
2. **Keep the payload small.** Pass IDs and a version or timestamp, not whole objects. The handler loads current data. This avoids stale data and oversized messages, and keeps PII out of the queue.
3. **Enqueue reliably** (see below). Never enqueue before the transaction that creates the data has committed.
4. **Make the handler idempotent** (see below).
5. **Set limits:** a per-job timeout, max attempts, backoff, and a dead-letter destination.
6. **Set concurrency** per queue and per downstream dependency.
7. **Handle shutdown:** finish or release in-flight jobs on SIGTERM.
8. **Add metrics and alerts** before shipping (see below).
9. **Test failure paths:** handler throws, worker killed mid-job, the same job delivered twice, downstream returns 429.

## Enqueue reliably

Two classic bugs:

- **Phantom job:** the job is enqueued, then the transaction rolls back. The worker runs for a record that doesn't exist.
- **Lost job:** the transaction commits, then the process crashes before the enqueue.

Fixes, best first:

1. **Same-database queue:** insert the job row in the same transaction as the business write.
2. **Transactional outbox:** write an outbox row in the same transaction, and have a relay publish it to the queue (see the resilience-patterns skill).
3. **After-commit hook** (e.g. `transaction.on_commit` in Django, `after_commit` in Rails, `afterCommit` hooks in ORMs that have them): this fixes phantom jobs but can still lose jobs on a crash. Only acceptable when a periodic reconciliation job catches anything missed.

## Idempotent handlers

Assume every job may be delivered more than once and may run concurrently with a copy of itself.

- **Check state first:** "if the invoice is already sent, return success."
- **Use an idempotency key** for external side effects (payment APIs, emails), derived from the job's business identity (e.g. `invoice-123-reminder-2`), not a random ID generated per attempt.
- **Record completion atomically:** a unique constraint on `(job_type, business_key)` in a processed-jobs table, written in the same transaction as the effect.
- **Guard concurrent runs** with a row lock or a short-lived distributed lock with a TTL, when two copies running in parallel would conflict.
- **Make steps resumable** for long jobs: checkpoint progress (e.g. last processed ID) so a retry continues rather than starting over.

## Retries, timeouts and dead letters

| Setting | Rule |
| --- | --- |
| Retry on | Transient errors only: timeouts, connection errors, 429, 5xx. Fail fast on validation errors and missing records. |
| Backoff | Exponential with jitter, capped (e.g. 30 s, 2 min, 10 min, 1 h). Respect `Retry-After` from downstream. |
| Max attempts | Finite. Pick from how long the work stays useful (an OTP email is useless after 10 minutes; a nightly export can retry for hours). |
| Job timeout | Below the queue's visibility/lease timeout, so the job can't be handed to a second worker while the first is still running. Long jobs extend the lease with heartbeats. |
| Dead-letter queue | Required. Failed jobs land there with the error and attempt count. Someone gets alerted, and there is a documented way to inspect and replay them. |
| Poison jobs | A job that crashes the worker (OOM, segfault, bad payload) must not loop forever. Count deliveries and dead-letter it after N. |

Replaying dead-lettered jobs in bulk, or purging a queue, changes production data or deletes work. Stop and get explicit confirmation from the user first.

## Concurrency and rate limits

- Set worker concurrency from what the **downstream** can take, not from CPU count: database connections, third-party rate limits, memory per job.
- Use separate queues (or priorities) for latency-sensitive jobs (password reset) and bulk jobs (re-index all users), so a bulk backfill can't starve them.
- Apply per-downstream rate limits (token bucket) shared across workers when calling rate-limited APIs.
- Large fan-out (one job enqueues a million children): enqueue in batches and throttle, or use the queue's batch feature. Never load all IDs into memory at once.

## Scheduled (cron) jobs

- **Exactly one runner per schedule.** With several app instances, a naive in-process scheduler runs the job N times. Use one of: the queue library's scheduler with a lock, a database advisory lock (e.g. PostgreSQL `pg_try_advisory_lock`), a lease row with expiry, leader election, or an external scheduler (Kubernetes CronJob with `concurrencyPolicy: Forbid`, cloud scheduler) that enqueues a job.
- **Make runs idempotent and catch-up safe.** Process "everything not yet processed" (by watermark or status column), not "the last 24 hours". A missed or doubled run then does no harm.
- **Time zones and DST:** schedule in UTC unless the business rule is in local time. For local-time schedules ("9:00 Europe/Berlin"), use a scheduler with time zone support and decide what happens on the skipped and repeated hour.
- **Overlap:** if a run can take longer than the interval, prevent overlap (lock, or skip if the previous run is still active).
- Log the start, end, item count and duration of every run, and alert when a run is missing, not only when it fails.

## Uniqueness and deduplication

- Prevent duplicate enqueues with a uniqueness key (library feature or a unique index) when the same logical job may be requested many times ("rebuild search index for product 42").
- Deduplication at enqueue does not remove the need for idempotent handlers. Retries and redelivery still happen.
- Debounce bursty triggers: enqueue with a short delay and a uniqueness key, so 50 edits produce one re-index.

## Graceful shutdown and deploys

- On SIGTERM: stop fetching new jobs, let in-flight jobs finish within a grace period, then release or re-queue the rest. Match the platform's termination grace period (see the kubernetes-deployments skill).
- Deploys run old and new worker code side by side. A job enqueued by new code may be picked up by an old worker and the other way round. Payload changes must be backward and forward compatible: add optional fields first, remove later.
- Renaming a job class or handler breaks jobs already in the queue. Keep an alias until the queue has drained.

## Metrics and alerts

| Metric | Why |
| --- | --- |
| Queue depth per queue | Backlog growing |
| **Age of oldest job** | The best single "are we behind" signal; alert on it |
| Processing time (histogram) | Slow jobs and timeouts |
| Failure and retry rate per job type | Broken handlers, failing downstream |
| Dead-letter count | Needs a human |
| Scheduled run missing | Silent cron failures |

Propagate a trace or correlation ID from the request that enqueued the job into the job's logs (see the observability skill).

## Anti-patterns

- **Enqueueing inside the transaction to a different system**: phantom jobs on rollback. Use the outbox or same-database queue.
- **Fat payloads**: whole objects in the job. They go stale, hit size limits, and leak PII into queue storage.
- **Infinite retries**: a permanently failing job retries forever and hides real failures. Cap attempts and dead-letter.
- **Retrying non-idempotent side effects** without an idempotency key: customers get charged or emailed twice.
- **Cron in every instance**: the job runs once per replica.
- **One queue for everything**: a bulk backfill delays password reset emails by an hour.
- **Timeout longer than the visibility timeout**: the job is handed to a second worker while the first is still running.
- **Swallowing exceptions** to "keep the worker alive": the job is marked successful and the work is silently lost.

## Done when

- Each job has a written contract: payload, idempotency strategy, timeout, max attempts, DLQ.
- Enqueue cannot create phantom or lost jobs (same-transaction queue, outbox, or after-commit plus reconciliation).
- Running any job twice, or concurrently, has been tested and is safe.
- Scheduled jobs have a single-runner guarantee and are catch-up safe.
- Queue depth, oldest-job age, failure rate and DLQ size are on a dashboard with alerts.
- Workers shut down gracefully and payload changes are compatible across a rolling deploy.
