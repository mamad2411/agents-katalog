---
name: migration-gen
description: Generates a database migration file for schema changes
argument-hint: <description-of-change>
user-invocable: true
allowed-tools: Read Glob Bash Edit
effort: low
---

## Generate Database Migration

Change: **$ARGUMENTS**

1. Detect ORM/migration tool:
```bash
cat package.json | grep -E '"prisma"|"drizzle"|"typeorm"|"knex"|"sequelize"|"migrate"'
ls prisma/ migrations/ db/migrations/ 2>/dev/null | head -10
```

2. Read the current schema:
```bash
cat prisma/schema.prisma 2>/dev/null || ls migrations/ 2>/dev/null | tail -3 | xargs -I{} cat migrations/{}
```

3. Generate the migration based on the requested change:
   - Additive changes (new table, new column with default) - safe
   - Destructive changes (drop column, rename) - add warning and suggest renaming strategy
   - Data migrations - separate from schema migrations

4. For Prisma: generate migration name and schema change, then ask to run:
```bash
npx prisma migrate dev --name $ARGUMENTS
```

For raw SQL: generate up/down migration files.

5. **Always generate a `down` migration** (rollback).

6. Flag any changes that require a deployment strategy (e.g., add-then-backfill, not rename directly).
