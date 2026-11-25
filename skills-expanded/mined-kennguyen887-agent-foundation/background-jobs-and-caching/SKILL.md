---
name: background-jobs-and-caching
description: Use when adding background jobs (Bull queues) or a Redis cache to a backend service — multi-queue architecture, enqueue/process, dynamic delayed jobs, job idempotency via a DB lock, graceful shutdown, and Redis caching (read-through wrap, key conventions, event-driven + prefix-SCAN invalidation). NestJS/TypeORM reference, framework-flexible. Complements (not replaces) the SQS cross-service events pattern.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Background jobs & caching

In-process async work (Bull + Redis) and a Redis cache for a backend service. Examples NestJS/TS,
neutral `listing`/`payment` domain. principle → **▸ Example** → **▸ Other stacks**. Cross-service
async (vs this in-process Bull) → the SQS events pattern in `write-service-code` §6.

## When to use
Time-critical, in-process async (reminders, expiry/timeout actions, retries, fan-out) and caching hot
reads. **Bull (this skill) = in-process, Redis-backed, supports delays + per-queue retry; SQS =
cross-service.** Complementary — don't merge them.

## 1. Bull job queues
- **One named queue per job type**, not a single mega-queue — independent concurrency + retry:
  ```ts
  BullModule.registerQueue({ name: REMINDER_QUEUE }, { name: PAYMENT_EXPIRY_QUEUE });
  ```
  Set **default job options** centrally: `removeOnComplete: true`, `removeOnFail: { age: <1h>, count: <N> }`
  (so Redis doesn't fill with finished jobs), plus a **retry policy** — `attempts: <n>` with
  `backoff: { type: 'exponential', delay: <ms> }` — so a transient failure retries with growing delay
  instead of dying on the first error or hammering the dependency instantly.
- **Producer** injects the queue; **processor** handles it:
  ```ts
  @InjectQueue(PAYMENT_EXPIRY_QUEUE) private queue: Queue;
  await this.queue.add(JOB.expirePayment, { paymentId }, opts);

  @Processor(PAYMENT_EXPIRY_QUEUE)
  class PaymentExpiryProcessor {
    @Process(JOB.expirePayment) async handle(job: Job) { await this.commandBus.execute(new ExpirePaymentCommand(job.data)); }
  }
  ```
- **Dynamic delays from business time** (remind N hours before, expiry windows) — compute with the
  date lib, **clamp ≥ 0**:
  ```ts
  const delay = Math.max(dayjs(startTime).subtract(2, 'hour').diff(dayjs()), 0);
  await this.reminderQueue.add(JOB.remind, { id }, { delay });
  ```
- **Idempotency via a DB lock** — at-least-once delivery means a job can run twice; guard with a
  unique-key insert (a `locking_records` table), skip on conflict:
  ```ts
  async runOnce(jobId: string, execute: () => Promise<void>) {
    try { await this.lockRepo.insert({ id: jobId }); }   // PK/unique → throws if already seen
    catch { return; }                                     // already processed → skip
    await execute();
  }
  ```
  *Alternative — a Redis lock for short-window/HTTP dedup:* `SET lock:<key> 1 PX <ttl> NX` succeeds
  only if the key is absent; a `null` reply means a duplicate is already in flight → skip (fail-safe:
  treat errors as "locked"). Lighter than a DB row for idempotency-key/endpoint dedup; the DB-row
  lock is better for a permanent once-only guarantee.
- **Graceful shutdown** — drain in-flight jobs on deploy:
  ```ts
  export class JobQueueModule implements OnApplicationShutdown {
    async onApplicationShutdown() { await this.queue.close(); }   // wait for active jobs
  }
  ```
- **No cron lib for data-driven timing** — model "do X at time T" as a *delayed job*, not a cron
  sweep (jobs persist in Redis, survive restarts). Use a scheduler only for fixed wall-clock tasks —
  and guard a recurring/cron job against **overlap** (a slow run must not double-fire) with the same
  Redis `SET NX` lock: skip the run if the lock is already held.
▸ *Other stacks:* any job lib (BullMQ, Sidekiq, Celery, River) — same shape: named queues, delayed
jobs, idempotent handlers, drain on shutdown.

## 2. Redis caching
- **One `CacheService`** wraps the cache client; read-through with `wrap`:
  ```ts
  cache.wrap(key, () => fetchExpensive(), ttlSeconds);   // get-or-compute-and-store
  ```
- **Key conventions:** a central `CACHE_PREFIX` registry (no scattered string literals); composite
  keys must serialize **stably** — `` `${PREFIX.LISTING}:${stableStringify(query)}` `` (unsorted object
  keys → different strings → silent cache misses).
- **Invalidate on write, in the handler/event** (not scattered in services): after a mutation, delete
  the affected keys — and **all variants** (v1/v2) — with `Promise.all`:
  ```ts
  await Promise.all([
    cache.del(`${PREFIX.LISTING_DETAIL}:${id}`),
    cache.del(`${PREFIX.LISTING_DETAIL_V2}:${id}`),
  ]);
  ```
- **Bulk invalidate by prefix with SCAN, never `KEYS`** (`KEYS` blocks Redis): stream
  `scanStream({ match: 'PREFIX:*' })` → `pipeline.unlink(...)`.
- **TTL from config** (a default + per-key override); don't hard-code.
▸ *Other stacks:* any cache (Redis/Memcached) — read-through wrapper, prefixed + stably-serialized
keys, invalidate-on-write, SCAN-not-KEYS for bulk.

## Verification
- **One queue per job type, finished jobs evicted:** `redis-cli KEYS "bull:*"` shows a key set per queue (not one mega-queue); after a job completes `redis-cli LLEN bull:<queue>:completed` stays ~0 (`removeOnComplete`). `grep -rn "@InjectQueue\|@Process\|registerQueue" src` — producers/processors paired per queue; no `add(..., { delay: <negative> })` (clamped via `Math.max(…, 0)`).
- **Idempotent + drains:** enqueue the same `jobId` twice → the side effect runs **once** (`SELECT count(*) FROM locking_records WHERE id='<jobId>'` = 1). `grep -rn "runOnce\|OnApplicationShutdown" src` present; SIGTERM with a job in flight → process waits, `redis-cli LLEN bull:<queue>:active` reaches 0 before exit.
- **Cache discipline:** reads go through `cache.wrap` (`grep -rn "\.wrap(" src`); keys come from the prefix registry, no raw literals; **anti-pattern check `grep -rn "\.keys(" src` → empty** (bulk invalidation must use `scanStream`, never `KEYS`). After a mutation, `redis-cli GET "<PREFIX>:<id>"` → `nil` (invalidated, all variants).

## Related
- `write-service-code` — §6 (SQS cross-service events; complementary) + Robustness (transactions/event handlers).
- `database-migrations` (the locking-records table is a migration) · `code-conventions`.
