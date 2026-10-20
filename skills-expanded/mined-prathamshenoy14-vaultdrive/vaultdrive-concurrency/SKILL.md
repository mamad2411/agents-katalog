---
name: vaultdrive-concurrency
description: Design, implement, or review VaultDrive hierarchy, namespace, file-lifecycle, and PostgreSQL concurrency changes where lock order, transaction boundaries, race behavior, or storage/metadata coordination matters.
---

# VaultDrive concurrency

Use this skill for changes whose correctness depends on concurrent folder/file operations. Keep claims tied to current code and tests; label future workers or other design directions as planned.

## Read first

- Inspect `git status` and the exact services, repositories, migrations, and tests touched by the task.
- Read the concurrency model and test-evidence sections of `docs/architecture.md`.
- Treat `docs/decisions/0007-concurrency-locking.md` as the locking authority. Consult ADR-0002, ADR-0004, ADR-0005, or ADR-0006 only when the change touches storage separation, uniqueness, upload/trash, or pending purge.
- Inspect `HierarchyCoordinator`, `PostgresHierarchyCoordinator`, and the closest PostgreSQL concurrency tests. Avoid a repository-wide audit.

## Preserve these invariants

- Acquire PostgreSQL transaction-scoped advisory locks through `HierarchyCoordinator` inside an active JPA transaction. The coordinator uses that transaction's connection; commit or rollback releases the lock.
- Use the owner-scoped exclusive hierarchy lock for folder structural mutations and the shared hierarchy lock for compatible file metadata operations. Do not change stable key derivation casually: mixed deployments must contend on identical keys, and hash collisions may conservatively serialize unrelated work.
- Lock before reading protected folder, file, ancestry, eligibility, or subtree state. Re-read inside the same short transaction, then validate and write. Never base a protected mutation on state loaded before its coordinating lock.
- Preserve documented lock order. Restore currently uses owner hierarchy lock, eligible file-row lock, then destination namespace exclusive lock. Document any new order and test it.
- Shared hierarchy locks do not serialize same-file writers. Use the entity version for ordinary optimistic updates; map stale competing writes to conflict rather than allowing lost updates.
- When transitions compete for one lifecycle state, use the repository's stronger primitive: pessimistically lock the freshly queried eligible row for restore versus purge, or use an expected-status plus expected-version conditional update for `UPLOADING -> READY|FAILED`. Assert exactly one valid winner.
- Keep PostgreSQL uniqueness constraints authoritative. Pre-checks and namespace locks improve errors and deterministic allocation but never replace partial unique indexes, `NULLS NOT DISTINCT`, ownership foreign keys, or other schema guards. Add a new Flyway migration for schema changes.
- Never perform Garage/S3 object-storage I/O inside a metadata database transaction or while holding hierarchy locks. Reserve/finalize metadata in short transactions and perform upload or best-effort cleanup between/after them through `ObjectStorageService`; make partial and uncertain outcomes explicit.
- Preserve ownership and ancestor-access checks without observable cross-user leakage.

## Concurrency tests

- Use real PostgreSQL integration tests for database locking or isolation behavior; mocks cannot establish it.
- Create committed fixtures before launching workers. Give each worker its own transaction, normally through `TransactionTemplate` or the transactional service boundary.
- Force the intended interleaving with `CountDownLatch` or `CyclicBarrier`: signal only after the relevant lock/read/flush, prove the competitor is blocked with a bounded timeout when blocking is the contract, then release the first transaction.
- Use bounded waits, release latches and stop executors in `finally`, unwrap asynchronous failures, and assert final persisted state—not only future completion or exception type.
- Cover both winner orders when either request may commit first. For optimistic races, synchronize after both reads and assert one winner, one stale-write failure, and no mixed/lost update. For conditional transitions, assert the affected-row outcome and durable lifecycle state.
- Keep tests deterministic through explicit coordination rather than sleeps. Run focused tests first, then the relevant full suite with the configured PostgreSQL environment; report unavailable infrastructure exactly.

## Implementation boundary

Current behavior and evidence are summarized in `docs/architecture.md` and ADR-0007. Durable purge requests exist, but purge/reconciliation workers, claiming, retry/backoff, final deletion, and their race coverage remain planned. Do not describe test presence as a passing result or planned behavior as implemented.
