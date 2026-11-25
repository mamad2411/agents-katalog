---
name: mysql-change-safety
version: 1.0.0
description: Use when a task changes MySQL schema, indexes, triggers, stored procedures, persistent data in bulk, or migration behavior. Inspect readers/writers first, prefer backward-compatible changes, control lock/data risk, verify invariants, and keep rollback/recovery explicit.
---

# MySQL Change Safety

Reusable safety workflow for changes that can alter persistent MySQL structure or data.

This Skill is intentionally narrower than general database coding style. It activates when a change can affect stored data, compatibility, query plans, locking, derived values or multiple application paths.

## Activate when

Use this Skill for:
- `CREATE/ALTER/DROP/RENAME` of tables, columns or indexes;
- changes to column type/nullability/default/collation;
- new or changed triggers, stored procedures/functions/events;
- data migrations/backfills/bulk `UPDATE`/`DELETE`/`INSERT ... SELECT`;
- changes to derived/denormalized DB-maintained fields;
- migrations that must coexist with old/new application code;
- query/index changes where production performance or lock/write cost is material.

Do not activate for:
- ordinary read-only SQL investigation;
- a localized application query change with no schema/data migration and no material performance risk;
- generic naming/style questions -> `mauro-coding-style`.

## Ownership boundary

- General Mauro DB naming/conventions -> `mauro-coding-style`.
- Mauro CRUD framework behavior -> `mauro-crud`.
- Project-specific schema/business invariants -> repository/schema/`PROJECT.md`.
- Feature planning / debugging / review -> focused workflow skills.
- Deployment execution, production credentials and backup infrastructure -> deployment/recovery owners.

This Skill never substitutes assumptions for the real target schema.

## Source-of-truth order

1. actual target schema and DB metadata;
2. application readers/writers and SQL paths;
3. triggers/procedures/events maintaining related state;
4. repository migrations/dumps/documented invariants;
5. shared conventions;
6. assumptions.

If production metadata/row volume/version is unavailable, mark lock/performance conclusions as unverified.

## Change classification

Before implementation classify the change:

- **additive compatible** — new object/column/index that existing code can ignore;
- **behavioral compatible** — changes behavior without breaking old readers/writers;
- **data migration** — rewrites/backfills persistent rows;
- **contract change** — old and new code/schema cannot safely coexist;
- **destructive** — drops/truncates/deletes/loses precision or removes a contract;
- **performance/locking sensitive** — may materially affect hot/large tables or query plans.

A change may have multiple classifications.

Destructive, contract-breaking or high-lock-risk work requires an explicit migration/recovery decision; do not disguise it as incidental cleanup.

## Workflow

### 1. Inspect affected readers and writers

Before DDL or bulk DML:
- inspect actual table definition;
- find application code that reads/writes affected fields;
- inspect joins, reports, exports, background jobs and AJAX/API paths when relevant;
- inspect triggers/procedures/events that read/write the same values;
- identify derived/denormalized columns and their owner;
- determine MySQL/MariaDB version and storage engine when behavior depends on them.

Do not infer safety only from one PHP page.

### 2. Prefer expand -> migrate -> contract

When old/new application versions may coexist, prefer:
1. **expand** — add backward-compatible schema;
2. **migrate** — deploy code/backfill data while both contracts work;
3. **contract** — remove old schema only after no reader/writer depends on it.

Avoid rename/drop/type-tightening in the same deployment when a compatibility window is safer.

Do not introduce unrelated normalization, foreign keys, casing changes or schema cleanup as part of a focused task.

### 3. Column changes

For new/changed columns:
- choose type from observed domain/data requirements, not guesswork;
- decide nullability/default semantics explicitly;
- check existing rows before adding stricter constraints;
- check precision/truncation/collation implications before type changes;
- do not write DB-maintained derived fields from PHP merely because the column exists.

For Mauro schemas, use `mauro-coding-style` for naming such as `ID`, `IDEntita`, `IS_*`, `Tab_*`, and established Italian domain names.

### 4. Index changes

Before adding/removing an index:
- identify the query pattern it serves;
- inspect existing indexes for equivalent prefixes/duplicates;
- consider selectivity and ordering;
- consider write/storage cost;
- use `EXPLAIN`/runtime evidence where available.

Do not remove an index solely because one inspected query does not use it; verify other readers/workloads.

### 5. Triggers and stored routines

Treat DB-side logic as application code:
- inspect all affected trigger timing/events;
- preserve existing side effects and derived-field ownership;
- check recursion/cascade assumptions;
- test insert/update/delete paths relevant to the routine;
- do not duplicate in PHP logic that is intentionally DB-owned.

### 6. Bulk data migration

For material backfills/updates/deletes:
- define exact selection predicate and expected affected population;
- make the operation restartable/idempotent where practical;
- use bounded batches when table size/locking/runtime warrants it;
- avoid one unbounded production transaction without evidence it is safe;
- preserve an audit/recovery path for destructive transformations;
- validate migrated and non-migrated populations separately.

Never run a destructive bulk statement merely because a generated query looks plausible.

### 7. Locking and availability

DDL behavior varies by server/version/engine/operation.

- Do not claim an ALTER is online/non-blocking without verifying target behavior.
- For hot/large tables, assess lock duration, copy/rebuild behavior and deployment window.
- If evidence is unavailable, state the operational risk and leave production execution to the deployment/recovery workflow.

### 8. Rollback and forward recovery

Before risky migration, define what happens if code or migration fails midway.

Possible strategies:
- additive rollback by reverting application code while new schema remains;
- restore previous values from a captured mapping/export;
- forward-fix when reverse DDL would be more dangerous;
- backup/restore according to the system's existing recovery mechanism.

This Skill does not create or claim backups; verify backup/recovery state through the owning workflow.

## Verification

Load `references/change-checklist.md` for high-risk changes.

At minimum, as applicable:
- syntax/parse migration SQL;
- re-read resulting schema;
- verify affected row counts and representative values;
- verify null/uniqueness/range invariants;
- exercise relevant inserts/updates/deletes and DB-side derived behavior;
- compare query plan/performance evidence for index-sensitive changes;
- verify old/new application compatibility during expand/migrate phases;
- inspect final diff/migration for unintended destructive operations;
- explicitly report runtime/production checks not performed.

Never claim a schema/data migration succeeded on production from static SQL review alone.
