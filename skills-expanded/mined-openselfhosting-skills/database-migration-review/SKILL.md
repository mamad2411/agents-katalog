---
name: database-migration-review
description: "Reviews database schema and data migrations for correctness, locking, backfills, rollback safety, compatibility, and data-loss risk. Use when adding, changing, or deploying migrations or modifying persisted data models."
license: MIT
metadata:
  author: OpenSelfHosting
  version: "1.0.0"
---

# Database Migration Review

## Goal
Reduce deployment and data-integrity risk by evaluating how schema and data changes behave across real deployment states.

## Workflow
1. Identify the database engine, version constraints, migration framework, current schema assumptions, table sizes if known, and deployment topology. Do not assume database behavior is portable across engines.
2. Read the migration and the adjacent application changes. Identify columns, indexes, constraints, defaults, data transforms, and backfill operations.
3. Check correctness and data preservation: nullability, uniqueness, foreign keys, duplicate/invalid existing rows, type conversion, truncation, time zones, collation, and ordering assumptions.
4. Evaluate operational behavior: full table scans, lock duration, index creation strategy, transaction support, replication lag, disk growth, write amplification, and timeout limits. Mark scale-dependent risks where actual table size is unknown.
5. Check deploy compatibility. Can old application code run against the new schema? Can new code run before backfill completes? Can deploys be rolled back without requiring an impossible reverse transform?
6. Prefer expand-and-contract for changes that span releases: add compatible structure, deploy dual-compatible code, backfill in bounded batches, verify, switch reads/writes, then remove obsolete structure in a later release.
7. Design idempotent, resumable backfills with checkpoints, bounded batches, observability, and a safe stop/retry path where appropriate.
8. Review rollback semantics. A down migration that drops newly written data is not truly safe. State when forward-fix is preferable to rollback.
9. Propose tests against realistic edge cases and a staging rehearsal. Never run a migration against production unless the user explicitly authorizes that operation.

## Report
Summarize the schema/data change, findings by severity, lock/data-loss/compatibility risks, rollout sequence, validation queries or tests, rollback/forward-fix plan, and assumptions such as table size or engine version.

## Review checklist
- Existing data remains valid or is deliberately repaired.
- New and old application versions are compatible during deployment.
- Backfill is bounded, resumable, observable, and safe to retry.
- Constraints are introduced only after data satisfies them.
- Index strategy matches database capabilities.
- Rollback behavior and irreversible effects are explicit.
- Backup and restore readiness are considered for high-impact changes.
