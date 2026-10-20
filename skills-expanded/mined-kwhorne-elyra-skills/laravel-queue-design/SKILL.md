---
name: laravel-queue-design
description: Design Laravel queue jobs that survive production - idempotency, retries and backoff, failure handling, batching, chaining, and Horizon tuning. Use when the user creates or reviews queued jobs, debugs stuck or duplicated jobs, asks about retries or failed_jobs, or moves slow work out of the request cycle.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep, edit
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [laravel, queues, jobs, horizon, background-processing]
---

# Laravel Queue Design

A queued job **will** run twice, run late, or run after the world changed under it. Design every job for those three facts and production gets boring — in the good way.

## When to use

- Creating or reviewing queued jobs, listeners, or notifications
- "Jobs are stuck / duplicated / silently failing"
- Moving slow work (mail, exports, API calls) out of the request
- Setting up or tuning Horizon / queue workers

## Principles

- **At-least-once means duplicates.** Every handler must tolerate running twice — idempotency is the entry fee, not a nice-to-have.
- **Small payload, fresh state.** Pass IDs, re-fetch inside the job. The world at dispatch time is not the world at run time.
- **Failure is a feature.** Decide per job what retry, backoff, and final failure *mean* — the defaults are guesses.
- **One job, one outcome.** A job that does five things fails five ways and retries all of them.

## Process

### 1. Design the job

```php
class ProcessRefund implements ShouldQueue
{
    public function __construct(public int $orderId) {}   // ID, not model state you'll trust later

    public $tries = 3;
    public $backoff = [10, 60, 300];          // seconds; spread retries out
    public $timeout = 120;                     // must be < retry_after in queue config!

    public function handle(): void
    {
        $order = Order::findOrFail($this->orderId);   // fresh state
        if ($order->refunded) return;                  // idempotency check
        // ...
    }
}
```

- Eloquent models in constructors are fine (`SerializesModels` re-fetches), but **decisions made on dispatch-time state are stale** — re-check conditions in `handle()`
- `$timeout` < `retry_after` (queue config) or the job runs twice *concurrently* — the classic Laravel queue foot-gun

### 2. Make it idempotent

Pick the mechanism that fits:

- **State check:** `if ($order->refunded) return;` — re-read, then act
- **Unique jobs:** `ShouldBeUnique` to prevent duplicate dispatch
- **DB constraint:** unique index + `firstOrCreate`/upsert absorbs the duplicate
- **External calls:** pass an idempotency key to the payment/API provider

### 3. Decide the failure story

- `failed(Throwable $e)` method: notify, mark the domain object, compensate
- Don't retry the unretryable: validation-type failures → `$this->fail($e)` immediately
- Poison-pill protection: `$tries`/`$maxExceptions` so one bad payload doesn't loop forever
- Monitor `failed_jobs` — a table nobody looks at is a black hole. Alert on growth; `queue:retry` after fixing the cause

### 4. Compose bigger work

| Need | Tool |
|---|---|
| Steps in order, abort on failure | Job chain (`Bus::chain`) |
| Fan-out N items + completion hook | Batch (`Bus::batch(...)->then(...)->catch(...)`) |
| Per-tenant/user serialization | `WithoutOverlapping` middleware |
| External API rate limits | `RateLimited` middleware, dedicated queue |

For batches: items must be independently retryable; `allowFailures()` if one bad item shouldn't sink the batch.

### 5. Separate queues by SLA

- `high` (user-facing: mail verification, receipts), `default`, `low` (exports, sync)
- Workers: `--queue=high,default,low` priority order, or dedicated workers per queue
- One slow queue must not starve fast ones — that's the whole point of separation

### 6. Operate it

- Horizon: balance/processes per queue, alert on wait time, watch failed rate
- Deploys: `queue:restart` (workers hold old code in memory until restarted)
- Track queue **wait time** (latency from dispatch to start) — it's the user-facing number

## Output format

```markdown
## Queue review: <job/feature>

| Job | Idempotent via | tries/backoff | timeout<retry_after | On final failure |
|-----|----------------|---------------|---------------------|------------------|
| …   | state check    | 3 / 10-60-300 | ✅ 120<300          | notify + mark    |

### Gaps (ranked)
1. <job>: <risk> → <fix>

### Queue topology
high: …, default: …, low: … — workers: …
```

## Anti-patterns

- ❌ Serializing a model and trusting its attributes at run time (stale decisions)
- ❌ `$timeout` ≥ `retry_after` — concurrent double execution by design
- ❌ Default retries on a non-idempotent job touching money
- ❌ One giant job processing 10 000 rows instead of a batch of small ones
- ❌ `failed_jobs` as a write-only table with no alerting
- ❌ Forgetting `queue:restart` on deploy, then debugging "old code" for an hour
- ❌ Everything on the `default` queue — exports starving password-reset mails
