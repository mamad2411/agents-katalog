---
name: php-migration-manager
audience: team
description: >
  Manages the full Laravel database migration lifecycle with safety checks and rollback planning
  (PHP analog of ef-/alembic-/sqlx-migration-manager). Covers create, review, apply, and
  rollback; enforces a reversible down(), expand-contract for zero-downtime changes, and guards
  against destructive operations in production. Use when creating or reviewing Laravel
  migrations, planning a schema change, applying/rolling back, or designing a zero-downtime
  migration.
---

# PHP Migration Manager (Laravel)

> "A migration you cannot roll back is a deployment you cannot reverse."

> "Schema changes are the riskiest deploys you make. Treat them that way."

## Core Philosophy

Laravel migrations are version control for the database. This skill manages their full lifecycle —
**create → review → test rollback → apply → verify** — with safety gates between each step. A migration
is code that runs against production data exactly once per environment; a mistake is not a failed build,
it is corrupted or destroyed data.

The central discipline is **reversibility**. Every `up()` has a matching `down()` that returns the schema
to its prior state. The central risk is **destructive change on a live table**: dropping a column,
renaming, or adding a non-nullable column with no default while the old code still runs. For those, the
**expand-contract** pattern (a.k.a. parallel change) replaces a single dangerous migration with a safe
sequence across multiple deploys.

**Non-Negotiable Constraints:**
1. **Every `up()` has a tested `down()`** — rollback is verified, not assumed
2. **No destructive operation without expand-contract** on a table with live traffic
3. **`migrate:fresh` / `migrate:refresh` / `wipe` are forbidden against any shared or production DB**
4. **Review before apply** — a migration is read and risk-rated before `artisan migrate` runs
5. **Backfills are batched** — never one unbounded `UPDATE` on a large table
6. **Indexes on large tables are added concurrently** where the driver supports it

The full domain principles, knowledge-base lookups, and anti-pattern catalog live in
`references/domain-principles-and-anti-patterns.md`. The AI discipline rules and error-recovery
procedures live in `references/discipline-and-recovery.md`.

## Workflow

### Phase 1: CREATE

```bash
php artisan make:migration create_orders_table          # new table
php artisan make:migration add_phone_to_users_table     # alter
```

Write both `up()` and `down()`. Prefer additive, nullable changes. See
`references/migration-safety-checklist.md` for column-by-column guidance.

### Phase 2: REVIEW

Read the migration and risk-rate it **before** applying. Classify each operation as
SAFE / CAUTION / DANGEROUS using `references/dangerous-operations.md`. Produce the Migration Review
report (see `references/output-templates.md`). DANGEROUS operations require an expand-contract plan.

### Phase 3: TEST ROLLBACK

Apply and immediately roll back in a scratch database to prove `down()` works.

```bash
php artisan migrate --database=scratch
php artisan migrate:rollback --database=scratch --step=1
php artisan migrate:status --database=scratch
```

If `down()` errors or leaves residue, fix it before going further.

### Phase 4: APPLY

```bash
php artisan migrate --step          # records each migration separately for granular rollback
php artisan migrate:status
```

### Phase 5: VERIFY

Confirm the schema, run the backfill (batched), and re-run the app's test suite. Produce the
Post-Apply Verification report (see `references/output-templates.md`).

## State Block

```xml
<php-migration-manager-state>
  phase: CREATE | REVIEW | TEST_ROLLBACK | APPLY | VERIFY | COMPLETE
  migration: [migration file]
  laravel_version: [detected]
  operation_class: SAFE | CAUTION | DANGEROUS
  expand_contract_required: true | false
  down_method_present: true | false
  rollback_tested: true | false
  backfill_required: true | false
  applied: true | false
  last_action: [description]
</php-migration-manager-state>
```

## Output Template

Two reports drive the lifecycle gates; full markdown templates are in `references/output-templates.md`:

- **Migration Review** — operation(s), risk class, reversibility, findings table, rollback plan, and the
  apply/backfill/expand-contract decision. Produced in Phase 2 before any apply.
- **Post-Apply Verification** — a checklist confirming the migration ran, schema matches intent, batched
  backfill reconciled, tests green, rollback rehearsed, and no long lock observed. Produced in Phase 5.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `php-feature-slice` | A new slice that needs schema changes uses this skill for the migration lifecycle. |
| `php-architecture-checklist` | The checklist flags missing `down()` and direct-SQL risks this skill prevents. |
| `php-security-review` | Reviews migrations for unsafe raw SQL and over-broad grants. |
| `php-api-scaffolder` | When an endpoint needs new tables/columns, sequence the migration before shipping the route. |
| `tdd-loop` | Backfill logic and data transformations are driven test-first against a scratch database. |
