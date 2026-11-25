---
name: node-pg-8-transaction-concurrency
description: Designs, reviews, and tests Node pg 8.x transactions, duplicate submission protection, replay resistance, race conditions, and PostgreSQL integration tests.
license: MIT
compatibility: Node applications using Node pg 8.x with PostgreSQL integration tests.
---

# Node pg 8 Transaction and Concurrency

This skill guides safe transaction implementation and concurrency testing for Node `pg` 8.x.

## When to Use

Use this skill when the task involves:

- `BEGIN`, `COMMIT`, or `ROLLBACK`
- `pool.connect()` and `client.release()`
- multi-statement consistency
- duplicate submission or replay prevention
- idempotency or uniqueness logic
- tests using PostgreSQL containers or test databases
- fixing leaked clients or hanging tests
- investigating data left behind after rollback

## Transaction Rules

- Acquire one client with `pool.connect()`.
- Run every statement in the transaction on that same client.
- Do not use `pool.query` inside a multi-statement transaction.
- Use `try/catch/finally`.
- Attempt `ROLLBACK` in `catch` if `BEGIN` succeeded.
- Always `client.release()` in `finally`.
- Keep business logic between transaction statements minimal.
- Check row counts for data-changing statements where concurrency matters.
- Use unique constraints, exclusion constraints, advisory locks, row locks, or idempotency tables when the invariant requires database enforcement.
- Consider isolation level only when default `READ COMMITTED` does not satisfy the invariant.

## Testing Rules

- Prefer integration tests against PostgreSQL for SQL syntax, constraints, transactions, and data types.
- Test rollback after an injected failure.
- Test concurrent attempts for uniqueness, locking, and idempotency-sensitive operations.
- Test that a failed transaction does not leak a checked-out client.
- End pools during test teardown.

## Workflows

Use `workflows/test-and-repair-pg-data-access-workflow.md` when fixing tests, transactions, or client lifecycle bugs.

Use `workflows/replay-concurrency-review-workflow.md` when reviewing duplicate submissions, replay attempts, idempotency, or race-sensitive state transitions.

## Resources

Use `resources/transaction-concurrency-test-matrix.md` to choose tests.

## Examples

Use `examples/transaction-helper-example.md` for a safe transaction wrapper pattern.

## Scripts

Run `scripts/scan-pg-patterns.mjs --help` before use. The script performs a conservative static scan for common `pg` anti-patterns and is safe by default.
