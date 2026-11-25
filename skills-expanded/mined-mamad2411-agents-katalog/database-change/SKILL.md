---
name: database-change
description: Safely change database schema, model, repository, index, migration, or persistence behavior.
---

# Database Change

## Workflow

1. Read project persistence docs and maps.
2. Inspect exact schema/model, repository/query, service usage, and tests.
3. Plan compatibility, migration, backfill, and rollback needs.
4. Make the smallest safe persistence change.
5. Add or update schema, repository, migration, or integration tests.
6. Update database docs and context maps when shape or ownership changes.

## Boundaries

- Do not run destructive data operations without approval.
- Do not store secrets or sensitive values insecurely.
- Do not make incompatible schema changes without a migration or compatibility plan.

## Output

- Relevant files or docs inspected.
- Work completed or plan produced.
- Tests or verification run or recommended.
- Docs updated or skipped with reason.
- Remaining risks, assumptions, and handoffs.
