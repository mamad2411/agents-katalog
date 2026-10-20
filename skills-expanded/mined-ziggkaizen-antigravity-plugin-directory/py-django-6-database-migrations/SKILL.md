---
name: py-django-6-database-migrations
description: Plans, generates, reviews, and repairs Django 6.0 schema and data migrations. Use when changing models, constraints, indexes, historical migrations, or deployment-sensitive database behavior.
license: MIT
compatibility: Requires Django 6.0 and Python 3.12, 3.13, or 3.14.
---

# py-django-6 Database Migrations

## When to Use

Use this skill for:

- Model field changes.
- Index and constraint changes.
- Data migrations.
- Migration conflicts.
- Squashing migrations.
- Reviewing migration safety before deployment.
- Database-specific migration concerns.

## Workflows

- Use `workflows/migration-planning-workflow.md` before generating or editing migrations.
- Use `workflows/migration-review-workflow.md` when reviewing generated migrations.

## Resources and Scripts

- `resources/migration-safety-checklist.md`
- `scripts/check-django-migrations.sh`

Run scripts with `--help` before using them.

## Migration Rules

1. Prefer generating migrations from model changes with `python manage.py makemigrations`.
2. Do not hand-edit generated migrations unless there is a clear reason.
3. Do not modify already-applied migrations without explicit approval.
4. Use `apps.get_model()` in `RunPython` migrations.
5. Keep schema and data migrations separate when risk is non-trivial.
6. Make data migrations idempotent where possible.
7. Avoid unbounded data updates in a single transaction on large tables.
8. For large tables, plan batching, backfills, nullable-to-non-nullable transitions, and deployment ordering.
9. Check database engine behavior before relying on locks, concurrent indexes, deferrable constraints, generated columns, or advanced SQL.
10. Always review reverse migration behavior.

## Verification Commands

Use the repository’s Python executable or environment wrapper.

```bash
python manage.py makemigrations --check --dry-run
python manage.py showmigrations
python manage.py migrate --plan
python manage.py test
```

Use `python manage.py sqlmigrate <app_label> <migration_name>` when SQL review is useful.
