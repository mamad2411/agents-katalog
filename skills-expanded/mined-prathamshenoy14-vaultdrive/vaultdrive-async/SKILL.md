---
name: vaultdrive-async
description: Design, implement, or review VaultDrive RabbitMQ, transactional-outbox, purge-worker, reconciliation, retry, recovery, or asynchronous object-cleanup changes where durable PostgreSQL state and cross-system failure handling matter.
---

# VaultDrive asynchronous work

Use this skill for durable background processing that spans PostgreSQL, RabbitMQ, and Garage/S3. Treat the principles below as the agreed direction for future implementation, not evidence that workers, queues, outbox tables, or job schemas already exist.

## Read first

- Inspect `git status` and only the affected lifecycle, repository, migration, storage-boundary, and integration-test files.
- Read the pending-purge, consistency, test-evidence, and known-gap sections of `docs/architecture.md`, plus the relevant phases and undecided items in `docs/development-roadmap.md`.
- Use ADR-0002 for PostgreSQL/Garage separation, ADR-0005 for upload lifecycle, ADR-0006 for the implemented purge-request boundary, and ADR-0007 for current coordination.
- Load `.agents/skills/vaultdrive-concurrency/SKILL.md` whenever the work intersects hierarchy, namespace, lifecycle races, or lock ordering.

## Existing boundary

- Implemented: uploads reserve `UPLOADING` metadata, write bytes outside database transactions, then conditionally transition to `READY` or `FAILED`; uncertain finalization deliberately retains the object for later reconciliation.
- Implemented: file and folder permanent-delete requests record durable `purge_requested_at` intent under current hierarchy/row coordination and do not call Garage.
- Planned: RabbitMQ, transactional outbox, workers, durable job/claim state, retries/backoff, checkpoints, physical purge finalization, reconciliation, dead-letter handling, and related observability. Verify the current docs and code before changing this boundary.

## Planned design invariants

- PostgreSQL is authoritative for business metadata, outbox events, durable work state, attempts, and checkpoints. RabbitMQ carries work notifications; it is not the sole durable job record.
- Commit a business-state transition and its outbox record atomically in one PostgreSQL transaction. Publish after commit through an asynchronous relay. Design for both duplicate publication and duplicate/redelivered consumption.
- Consumers must be idempotent and must safely claim or conditionally advance durable work so competing workers cannot perform an unsafe transition. Use bounded retry/backoff, record recoverable progress, and make abandoned claims or missed notifications recoverable after crashes.
- Never hold a metadata database transaction or hierarchy lock across Garage/S3 I/O. Persist intent or claim work briefly, perform storage I/O outside the transaction, then conditionally record the known outcome in another short transaction.
- Treat object deletion as retryable and compatible with an already-missing object. When an outcome is uncertain, do not make metadata claim bytes are gone; retain durable state and retry or reconcile safely.
- File purge must coordinate with upload finalization and late object writes. Never delete the key for an `UPLOADING` record until its active writer is fenced or otherwise proven unable to write afterward. Do not invent that fencing mechanism—document and decide it with the lifecycle transition and race tests.
- Folder purge must process bounded subtree batches, checkpoint durable progress, and delete metadata bottom-up only when descendants and their storage outcomes make removal safe. Preserve the pending-purge ancestry barrier throughout partial progress.
- Reconciliation of stale `UPLOADING` and `FAILED` rows must use explicit age and lifecycle eligibility plus conditional transitions. Avoid blind cleanup after an uncertain finalization because the object may belong to a committed `READY` row.
- Preserve ownership, ancestor accessibility, advisory-lock ordering, optimistic/pessimistic coordination, namespace uniqueness, and non-leaking errors defined by the concurrency skill. PostgreSQL constraints remain authoritative.
- Do not invent queue names, exchanges, routing keys, outbox/job columns, claim leases, terminal states, retention, or retry counts. Surface these as decisions, record accepted choices in an ADR, and add append-only Flyway migrations when implementation requires schema.

## Verification

- Test atomic business-state/outbox persistence with PostgreSQL and verify publishing occurs only from committed records.
- Use RabbitMQ integration tests for acknowledgement/redelivery behavior and PostgreSQL integration tests for claims and transitions; use a real S3-compatible service when storage outcomes matter.
- Cover duplicate publication/delivery, idempotent replay, competing workers, transient and exhausted retries, crash points before and after external I/O, stale-claim recovery, and missed-notification recovery.
- Add deterministic upload-versus-purge races, including late object writes and both transition winner orders. For folder purge, verify bounded restart from checkpoints and safe bottom-up finalization.
- Assert durable database state and object presence/absence, not only messages or method calls. Report unavailable PostgreSQL, RabbitMQ, or Garage infrastructure exactly; test presence is not proof of a passing system.
