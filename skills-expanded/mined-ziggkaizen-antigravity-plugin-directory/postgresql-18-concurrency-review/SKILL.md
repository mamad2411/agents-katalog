---
name: postgresql-18-concurrency-review
description: Reviews PostgreSQL 18 concurrency behavior, transaction boundaries, race conditions, uniqueness, idempotency, replay defense, locking, isolation levels, outbox/inbox patterns, and critical state transitions. Use when a task mentions race conditions, concurrent writes, replay, idempotency, uniqueness, transactions, locks, queues, outbox, or trust-critical state changes.
license: MIT
compatibility: PostgreSQL 18 release line; scripts require bash.
---

# PostgreSQL 18 Concurrency Review

Use this skill for critical state transitions, replay defense, idempotency, uniqueness, retry behavior, duplicate submissions, row/advisory locks, queue consumers, and outbox/inbox workflows.

## Start Here

1. Identify the state transition and invariant.
2. Identify concurrent actors and retry sources.
3. Identify the database constraints that enforce correctness.
4. Identify the transaction boundary and isolation level.
5. Use supporting files:
   - `resources/concurrency-and-replay-checklist.md`
   - `resources/transaction-isolation-guide.md`
   - `examples/idempotency-and-uniqueness-patterns.md`
6. Run scripts with `--help` before using them:
   - `scripts/postgresql-18-transaction-pattern-check.sh`

## Review Principles

- Prefer database constraints for invariants.
- Avoid read-check-write races.
- Use `INSERT ... ON CONFLICT`, unique constraints, exclusion constraints, row locks, advisory locks, or serializable transactions when appropriate.
- Design retries as part of the behavior, not as an afterthought.
- Use idempotency keys for externally retried operations.
- Keep transactions short.
- Coordinate external side effects through outbox/inbox patterns.
- Test concurrent cases, not only single-threaded behavior.

## Workflows

Use `workflows/concurrency-review-workflow.md` for concurrency-sensitive PostgreSQL 18 changes.

## Expected Output

For concurrency tasks, provide:

- Invariant and race-risk summary.
- Transaction boundary and isolation recommendation.
- Required constraints/indexes.
- Retry/idempotency/replay behavior.
- Test plan for concurrent execution.
