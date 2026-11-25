---
name: alembic-migration-manager
audience: team
description: >
  Manages the full Alembic migration lifecycle with safety checks and rollback planning. Python
  analog of ef-migration-manager. Use when creating, reviewing, or applying database migrations
  in Python projects using SQLAlchemy and Alembic.
---

# Alembic Migration Manager

> "Every migration is a one-way door. Make sure you know what's on the other side. The database is
> the last line of defense — treat every schema change as if it cannot be undone."

## Core Philosophy

Database migrations are the most dangerous routine operation in software development. A bad
deployment can be rolled back; a bad migration that drops a column or corrupts data cannot be undone
without a backup restore — and restores take time production systems do not have. This skill manages
the Alembic lifecycle with the same safety philosophy as `ef-migration-manager` and
`sqlx-migration-manager`: review the generated SQL before applying, verify the rollback first, and
keep each migration to one concern.

**Non-Negotiable Constraints:**
1. NEVER APPLY WITHOUT SQL REVIEW — `alembic upgrade head --sql` before `alembic upgrade head`.
2. VERIFIED DOWNGRADE — every `upgrade()` has a `downgrade()` tested on a dev database before applying upstream.
3. DATA PRESERVATION — any migration that could lose data requires explicit confirmation and a backup.
4. ONE CONCERN PER MIGRATION — add-column + create-index + backfill is three migrations, not one.
5. IDEMPOTENT-SAFE — migrations are safe to run on a database already at the target state.

Full principle table, KB lookups, command sequences, anti-patterns, discipline rules, and error
recovery live in `references/conventions.md`.

## Workflow

```
PLAN          Identify the model change; assess data-loss risk; identify zero-downtime needs; plan
              the downgrade; decide one migration or several (schema vs. data backfill).
              Run: alembic current · alembic history · alembic check (must be clean).

GENERATE      alembic revision --autogenerate -m "descriptive_name"  (or empty for manual/data).
              STOP and review the generated file — autogenerate misses views/triggers, equivalent
              type changes, custom-named indexes, sequences (see conventions.md).

REVIEW SQL    alembic upgrade head --sql  AND  alembic downgrade -1 --sql. Verify: matches intent,
              no unexpected DROP/data loss, acceptable locks. (Lock detail: dangerous-operations.md.)

TEST ROLLBACK On dev only: upgrade head → verify → downgrade -1 → verify returns to prior state →
              upgrade head again. (Checklists: migration-safety-checklist.md.)

APPLY         alembic upgrade head → alembic current to confirm. Roll back with downgrade -1 if needed.
```

**Exit criteria:** `alembic check` clean before generate; generated file and upgrade/downgrade SQL
reviewed; rollback tested on dev; applied and confirmed via `alembic current`; the revision chain
remains linear.

## State Block

```
<alembic-migration-state>
phase: PLAN | GENERATE | REVIEW_SQL | TEST_ROLLBACK | APPLY | COMPLETE
migration_name: [descriptive name]
data_loss_risk: none | low | medium | high
zero_downtime_required: true | false
sql_reviewed: true | false
rollback_tested: true | false
current_revision: [revision ID or "head"]
target_revision: [revision ID or "head"]
last_action: [description]
next_action: [description]
</alembic-migration-state>
```

## Output Template

- **Migration review checklist, rollback verification** — `references/output-templates.md`.
- **Per-operation locking/data-loss detail by database** — `references/dangerous-operations.md`.
- **Pre/post-apply checklists, rollback sequence** — `references/migration-safety-checklist.md`.
- **Principle table, KB lookups, command sequences, anti-patterns, discipline rules, error recovery** — `references/conventions.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `python-feature-slice` | When a feature needs schema changes, use this skill for the migration lifecycle. |
| `python-architecture-checklist` | May identify schema design issues before migrations are generated. |
| `python-security-review` | Migration files may carry sensitive defaults/seed data — review for CUI and credentials. |
| `ef-migration-manager` / `sqlx-migration-manager` | Cross-references for .NET and Rust stacks — identical safety philosophy, different tooling. |
