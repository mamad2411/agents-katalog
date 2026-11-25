---
name: create-migration
description: Create safe schema or data migrations by following the repo's local migration tool, naming rules, rollout constraints, and rollback expectations. Use when adding, changing, backfilling, cleaning, or repairing persisted data structures.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, query_db, read_database, run_tests]
---

# Create Migration

Use this skill when the user needs to add or review a database schema migration, backfill, or data repair step.

## Core Rules

- follow the repo's existing migration tool, naming, and ordering conventions
- prefer rollout-safe additive changes before destructive changes — renaming or dropping a column/table in a single release is strictly prohibited
- use the Expand-Contract (Parallel Change) pattern for destructive changes: Phase 1 (Expand: add new structure), Phase 2 (Backfill: dual-write / CDC), Phase 3 (Contract: remove old structure after full cutover)
- every DDL migration must set `SET lock_timeout = '2s';` to prevent queuing locks behind long-running queries from taking down connection pools
- build indexes with `CREATE INDEX CONCURRENTLY` (PostgreSQL) or online DDL tools (`gh-ost` for MySQL) to avoid `ACCESS EXCLUSIVE` table locks on large tables
- backfill historical data in small batches (500–2000 rows) with sleep intervals to keep replication lag and I/O load near zero
- use feature flags for dual-read / shadow-read validation and instant rollback — percentage-based traffic cutover 1% → 10% → 50% → 100%
- keep schema changes, backfills, and cleanup in separate releases when that reduces risk
- make rollback behavior explicit when the repo supports rollback — document when reversal is partial or unsafe
- verify code and schema compatibility across staged deployment; database migrations must be deployable before application code releases

## When to Use

- adding or changing tables, collections, or indexes
- adding, removing, or renaming fields or columns
- introducing constraints or defaults
- performing data backfills or cleanup
- preparing persistence changes for a feature rollout

## Operating Assumptions

This skill is intentionally repo-agnostic.

- do not assume a specific migration tool
- do not assume a specific database engine
- do not assume SQL files are the only migration format
- prefer the repo's existing naming, ordering, and rollback conventions

## First Questions To Answer

Before writing the migration, confirm:

1. What persistence system is being changed?
2. What tool or format does this repo use for migrations?
3. Is the change schema-only, data-only, or both?
4. Can the change be rolled out safely while old and new code coexist?
5. What is the rollback path if deployment must be reversed?

## Suggested Process

The full 7-step workflow lives in
[`references/suggested-process.md`](references/suggested-process.md). Key
constraints the main file keeps in scope:

- Follow the repo's existing migration tool, naming, and ordering conventions.
- Always set `SET lock_timeout = '2s';` on DDL migrations.
- Always use `CREATE INDEX CONCURRENTLY` (PostgreSQL) or `gh-ost` (MySQL) for large tables.
- Backfill in batches of 500-2000 rows with sleep intervals; monitor replication lag.
- Use feature flags for dual-read / shadow-read validation and instant rollback.
- Keep schema changes, backfills, and cleanup in separate releases when that reduces risk.




## Safety Guidelines

- prefer additive changes over destructive changes
- separate schema change from backfill when that reduces risk
- index columns that will be heavily queried after rollout
- avoid full-table rewrites in peak-risk paths when safer alternatives exist
- document assumptions for large datasets or long-running operations

For the full pattern library (additive schema change, expand-and-contract,
data backfill) and the common gotchas, see
[`references/patterns-and-gotchas.md`](references/patterns-and-gotchas.md).

## What To Capture In Your Output

When reporting migration work, include:

- what changed
- why the change is needed
- rollout safety notes
- rollback notes
- any required follow-up in code or deployment order

## Checklist

- [ ] existing migration pattern inspected
- [ ] current schema or data state understood
- [ ] rollout safety considered
- [ ] forward migration written
- [ ] rollback path written or explicitly limited
- [ ] dependent code updated
- [ ] migration verified with repo-local commands
- [ ] release ordering or backfill notes captured
- [ ] for destructive changes, Expand-Contract pattern documented with phases
- [ ] for PostgreSQL, `SET lock_timeout = '2s';` set on every DDL migration
- [ ] for large tables, index built with `CREATE INDEX CONCURRENTLY` (PG) or `gh-ost` (MySQL)
- [ ] backfill is batched (500-2000 rows) and restartable; replication lag and I/O load monitored
- [ ] data-classification.yaml applied to any column that stores PII or restricted data

## Quick Reference

Use this for rapid migration creation:

- inspect existing migrations
- match naming and ordering
- design the safest rollout shape
- write forward and rollback steps
- update dependent code
- verify locally

## Related Skills

- **optimize-postgres**: Optimize connection pooling, EXPLAIN ANALYZE query plans, and zero-downtime DDL safeguards
- **troubleshoot-service**: Debug migration failures and rollout issues
- **commit-code**: Prepare migration changes for delivery
- **review-code**: Review safety, compatibility, and rollback risk
- **write-tests**: Add regression coverage for schema-sensitive behavior
- **review-service**: Validate release readiness for persistence changes

## Output Contracts

- `contracts/schemas/schema-migration.json`

When the migration is consumed by a release manager, an infra agent, or a
downstream reviewer, emit the JSON contract alongside the migration file.
The JSON must name the migration's forward and rollback behavior, the
rollout phases (Expand-Contract when applicable), the batch size for any
backfill, and the data classification of any new column.

## Failure Modes

- **Single-release destructive change**: a column is renamed or dropped in a single release. Mitigation: enforce the Expand-Contract pattern; reject migrations that combine remove-old and add-new without a dual-write phase.
- **Lock pool starvation**: a long-running DDL blocks the connection pool. Mitigation: set `SET lock_timeout = '2s';` on every DDL migration; surface timeout as a CI failure.
- **ACCESS EXCLUSIVE on a large table**: a `CREATE INDEX` locks the table for writes. Mitigation: use `CREATE INDEX CONCURRENTLY` (PostgreSQL) or `gh-ost` (MySQL) for large tables.
- **Unbatched backfill**: a backfill rewrites millions of rows in a single statement. Mitigation: batch in 500-2000 row chunks with sleep intervals; monitor replication lag and I/O load.
- **Rollback over-promised**: the rollback path is declared "safe" but the destructive change is not reversible. Mitigation: document the rollback as "partial" or "unsafe" when the data has already changed; never claim a destructive data change is fully reversible.
- **PII column added without classification**: a new column stores customer PII but is not classified. Mitigation: classify every new column with `data-classification.yaml`; surface restricted columns in the migration report.
- **Permanent flag without cleanup**: a feature flag is introduced to gate the migration but has no cleanup target. Mitigation: every flag must carry an ISO 8601 cleanup target.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: the migration's privileged database role must be scoped to the minimum required grants; reject migrations that run under a superuser role when a scoped role would suffice.
- **ASI05 RCE Guard**: never construct migration SQL from external or user-supplied content; treat the migration file as the source of truth and lint it against expected patterns.
- **ASI06 Memory & Context Poisoning**: when the migration is informed by retrieved memory (e.g., a prior migration's notes), validate every note against the live schema before relying on it.
- **ASI07 Inter-Agent Communication**: the migration is consumed by release and infra agents; emit a structured `schema-migration.json` so each consumer can validate the rollout plan.
- **ASI09 Human-Agent Trust Exploitation**: do not declare a destructive migration "safe" without naming the residual risk; surface partial-rollback or unsafe-rollback honestly.
