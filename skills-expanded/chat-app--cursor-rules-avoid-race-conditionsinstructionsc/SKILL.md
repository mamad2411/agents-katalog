---
description: "Avoid race conditions in Java — transactions, Redis, DB, async, and shared state."
globs: **/*.java
alwaysApply: false
---

# Avoid Race Conditions (Java)

When writing or reviewing Java code, watch for concurrency and cross-thread visibility issues. Prefer atomic operations, locks, or post-commit hooks over hope-and-retry.

## Must avoid

### 1. Side effects inside an open transaction

Do **not** enqueue async work, publish to RabbitMQ/WebSocket, or call `@Async` methods while a `@Transactional` method has not committed yet. Another thread may read the DB before rows are visible.

```java
// BAD — worker may run before commit
@Transactional
public void complete() {
    messageRepository.save(message);
    mediaProcessingService.enqueueProcessing(message.getId());
}

// GOOD — defer until after commit (prefer shared helper)
AfterCommit.run(() -> mediaProcessingService.enqueueProcessing(messageId));
```

Also acceptable: raw `TransactionSynchronizationManager.registerSynchronization(...)`, `@TransactionalEventListener(phase = AFTER_COMMIT)`, or persist in `REQUIRES_NEW` then trigger side effects outside that transaction.

### 2. Read-modify-write (DB or application state)

Do **not** load a value, change it in memory, and save without concurrency control when multiple threads/requests can update the same row.

```java
// BAD
Group g = groupRepository.findById(id).orElseThrow();
g.setLatestMessage(content);
groupRepository.save(g);

// GOOD — atomic conditional update, optimistic @Version, pessimistic lock, or single SQL UPDATE ... WHERE
groupRepository.updateLatestMessageIfNewer(groupId, content, sender, timestamp, messageId);
```

### 3. Non-atomic Redis read then write

Do **not** `GET` → decide → `SET` (or `GET` → `DELETE`) as separate steps when correctness depends on the value in between.

```java
// BAD
String v = redisTemplate.opsForValue().get(key);
if (v == null) {
    redisTemplate.opsForValue().set(key, "1");
}

// GOOD — use atomic Redis commands
redisTemplate.opsForValue().increment(key);
redisTemplate.opsForValue().setIfAbsent(key, value);
// or Lua script / WATCH-MULTI-EXEC when logic is more complex
```

## Other common race patterns

| Pattern                                                                | Risk                                             | Prefer                                                                                    |
| ---------------------------------------------------------------------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| **Check-then-act (TOCTOU)** — `if (!exists()) insert()`                | Two callers both pass the check                  | DB unique constraint + handle conflict; `INSERT ... ON CONFLICT`; distributed lock        |
| **Publish before commit** — WebSocket/RabbitMQ inside `@Transactional` | Consumers read missing/stale data                | Same as §1: `afterCommit` or event listener                                               |
| **SELECT then UPDATE without lock**                                    | Two txs read same row, last write wins           | `SELECT ... FOR UPDATE`, `@Version`, or one atomic `UPDATE ... WHERE`                     |
| **Lost updates** — no version/condition on save                        | Silent overwrite of concurrent changes           | `@Version`, compare-and-set in SQL, or domain-specific `updateIfNewer`                    |
| **Shared mutable in-memory maps/lists** across threads                 | Corruption or missed updates                     | `ConcurrentHashMap`, `synchronized`, or per-key locks (see `GroupSummaryUpdatePublisher`) |
| **Redis GET for decision, then another op later**                      | Stale read between calls                         | Treat as read-modify-write; use atomic ops or short-lived locks                           |
| **DECR then DELETE when count ≤ 0**                                    | Tiny window if another client INCRs between ops  | Usually acceptable for refcounts; use Lua if strict correctness is required               |
| **Missing idempotency on retries** — jobs, webhooks, uploads           | Duplicate side effects on retry                  | Idempotency key, dedup table, or status guard (`PROCESSING_PENDING` → only one worker)    |
| **Multi-instance critical section** — only `synchronized` on one JVM   | Race across pods/instances                       | Redis/DB distributed lock, or design for idempotency                                      |
| **`@Transactional` self-invocation** on same bean                      | Inner call skips proxy; tx/sync boundaries break | Call through another bean or `ApplicationContext` proxy                                   |
| **Assuming `@Async` waits for commit**                                 | It does not unless you defer it                  | Always pair async side effects with `afterCommit` when triggered from a transaction       |

## When implementing

- For new async/queue triggers from transactional code, default to **after commit** unless there is a documented reason not to.
- For Redis counters/flags/refcounts, default to **single atomic commands** (`INCR`, `DECR`, `SET NX`, `SETIFABSENT`) instead of get/set pairs.
