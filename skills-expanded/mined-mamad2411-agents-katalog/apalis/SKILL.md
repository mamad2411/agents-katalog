---
name: apalis
description: "Applies when building or reviewing Apalis job processing systems. Covers job definition, storage backends, retry strategies, scheduling, and monitoring."
---

# Apalis

## Job definition

1. **Jobs as plain structs with Serialize/Deserialize.** Job trait is a marker; serde + unique NAME are the contract.
2. **Keep payloads small — IDs, not data blobs.** Handler fetches full data.
3. **Make handlers idempotent.** Retries mean duplicate execution.

## Workers and storage

4. **`apalis-redis` for distributed, `apalis-sql` for transactional enqueue with existing DB.**
5. **Set concurrency explicitly with `.concurrency(n)`.** CPU-bound: match cores. IO-bound: higher.
6. **Pass dependencies through worker state**, not global statics. `.data(pool.clone())`.

## Reliability

7. **RetryPolicy layer, not manual retries.** Exponential backoff, max retries, dead-letter.
8. **TimeoutLayer for execution limits.** Hung calls block worker slots.
9. **Monitor for multi-worker management and graceful shutdown.**

## Scheduling

10. **`apalis-cron` with CronStream for scheduled jobs.**
11. **Monitor queue depth and failure counts.** Unmonitored queues back up silently.
12. **In-memory storage for testing.** Push, run one tick, assert.
