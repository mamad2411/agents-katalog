---
name: background-job-design
description: Moves slow or unreliable work off the request path into queues, with idempotent handlers, bounded retries with backoff and a dead-letter queue.
---

# Background job design

Assume every job runs twice and sometimes never gets its turn.

## Steps

1. Decide what moves. Move work that is slow, calls an external service, or can wait: email, exports, image processing, webhooks out. Keep inline anything the user must see the result of in the same response.
2. Enqueue after the database commit, or write the job in the same transaction (outbox table) so a rollback cannot leave a job pointing at nothing.
3. Pass identifiers, not objects: `{ orderId: 812 }`. The handler loads fresh state, which also lets it notice that the order was cancelled meanwhile.
4. Make the handler idempotent. Use a natural key or an idempotency key for the side effect (for example the payment provider's idempotency header, or an `email_sent_at` check inside a transaction). Running twice must produce one effect.
5. Classify errors. Permanent errors (validation, 4xx other than 408 and 429) go straight to the dead-letter queue. Transient errors retry with exponential backoff and jitter, for example 10 s, 1 min, 10 min, 1 h, capped at 5 attempts.
6. Set a visibility timeout longer than the longest job run, and a per-job timeout shorter than it.
7. Add a dead-letter queue with an alert on its depth, and a command to inspect and replay one job.
8. Log job id, attempt number, duration and outcome.

## Rules

- Never retry without a cap.
- Never put secrets or full personal records in a payload.
- One job does one thing.

## Report

Jobs added, idempotency approach per job, retry policy, dead-letter handling and how to replay.
