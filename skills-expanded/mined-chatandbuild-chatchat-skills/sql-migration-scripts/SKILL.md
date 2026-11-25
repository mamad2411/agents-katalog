---
id: sql-migration-scripts
name: SQL Migration Scripts
description: Use this skill when drafting or reviewing MySQL or PostgreSQL migration scripts, schema changes, data backfills, index changes, permission updates, or operational SQL where locking, transactions, compatibility, rollout sequencing, validation, and rollback risk matter.
category: Databases
---

# SQL Migration Scripts

Use this skill to draft or review MySQL and PostgreSQL SQL changes as production migrations, not just syntactically valid SQL.

## Clarify First
- Which engine and version: PostgreSQL, MySQL, Aurora, Cloud SQL, RDS, PlanetScale, or another managed variant?
- Is the script changing schema, data, indexes, constraints, permissions, or maintenance state?
- How big are the affected tables and what write traffic is expected?
- Will this run once, repeatedly, inside a migration framework, or manually during an incident?
- Does the script need to remain compatible with older application behavior during rollout?
- What is the acceptable downtime, lock window, and rollback strategy?

## Migration Shape
Prefer a reviewable sequence:

1. Prechecks: engine/version, object existence, row counts, dependent indexes, constraints, permissions, and current data shape.
2. Compatibility step: add nullable columns, additive indexes, dual-write support, or backward-compatible objects before dependent application changes.
3. Backfill or data correction: chunk large updates and make repeated runs safe when possible.
4. Constraint tightening: add `NOT NULL`, uniqueness, foreign keys, generated values, or enum restrictions after data is valid.
5. Cleanup: remove old columns, triggers, indexes, or compatibility code only after rollout confidence.
6. Validation: postchecks that prove the intended state and surface partial failure.

## Engine-Specific Checks

### PostgreSQL
- Call out transaction boundaries. Some operations, including `CREATE INDEX CONCURRENTLY`, cannot run inside a normal transaction block.
- Prefer `CREATE INDEX CONCURRENTLY` for large hot tables when appropriate, and explain the tradeoff.
- Treat `ALTER TABLE`, constraint validation, column defaults, type changes, and rewrites as lock-sensitive.
- Use `NOT VALID` plus later validation for foreign keys and check constraints when that reduces rollout risk.
- For large updates, prefer chunking by primary key or a stable predicate instead of one unbounded `UPDATE`.

### MySQL
- State assumptions about version, storage engine, charset, collation, and managed-service behavior.
- Be explicit about DDL algorithms and locks where relevant, such as `ALGORITHM=INPLACE`, `ALGORITHM=INSTANT`, and `LOCK=NONE`, but do not assume every operation supports them.
- Treat index changes, column type changes, generated columns, foreign keys, and charset/collation changes as potentially table-copying or lock-heavy.
- For large data changes, use bounded batches and stable ordering; avoid long transactions on hot tables.
- Consider replication lag, online schema change tooling, and application compatibility before recommending direct DDL.

## Good Output
- SQL or pseudocode split into ordered, reviewable sections.
- Assumptions about engine, version, table size, traffic, and migration framework.
- Locking, rewrite, replication, and rollback notes next to risky steps.
- Precheck and postcheck queries.
- A clear callout when rollback is not a simple inverse script.

## Common Mistakes
- Writing one huge script with no checkpoints or validation.
- Mixing schema change, backfill, and cleanup in the same irreversible step.
- Assuming MySQL and PostgreSQL DDL have the same locking or transactional behavior.
- Adding constraints before proving existing data satisfies them.
- Treating rollback as obvious when data has been transformed or dropped.
