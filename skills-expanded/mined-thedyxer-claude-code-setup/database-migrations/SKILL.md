---
name: database-migrations
description: Plan and implement database schema or data migrations, including backfills and rollback strategy, when persistent data changes.
---

# Database migrations

Inspect the current schema, migration framework, data volume assumptions, and application read and write paths. Plan the transition so old and new code can coexist when a rolling deployment requires it. For nontrivial changes, separate additive schema changes, backfills, cutover, and cleanup. Account for constraints, locks, indexes, defaults, nullability, and irreversible data transforms.

Provide a rollback or forward-fix plan appropriate to the change. Test the migration against a representative local database and verify both schema and application behavior. Do not claim a rollback can restore deleted data unless a backup or explicit recovery path exists.
