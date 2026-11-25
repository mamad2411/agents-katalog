---
name: create-migration
description: Create a new numbered database migration SQL file following project conventions
---

# Create Migration

Create a new PostgreSQL migration file in the project's migration directory.

## Steps

1. **Find the migration directory and next number:**
   Read `.claude/enterprise-state/stack-profile.json` for `structure.migration_dir`.
   ```bash
   ls $MIGRATION_DIR/ | grep -E '^[0-9]+_' | sed 's/_.*//' | sort -n | tail -1
   ```
   Add 1 to get the next number.

2. **Create the file** at `$MIGRATION_DIR/{NNN}_{description}.sql`
   - Use snake_case for the description
   - Match the argument provided by the user (e.g., `/create-migration add_customer_notes`)

3. **File template:**
   ```sql
   -- Migration {NNN}: {Description in plain English}
   -- {Brief explanation of what this migration does}

   {SQL statements here}
   ```

4. **SQL conventions:**
   - Use `CREATE TABLE IF NOT EXISTS` for new tables
   - Use `CREATE INDEX IF NOT EXISTS` for indexes
   - Use `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` for new columns (requires DO block):
     ```sql
     DO $$
     BEGIN
       IF NOT EXISTS (SELECT 1 FROM information_schema.columns
         WHERE table_name = 'table' AND column_name = 'column') THEN
         ALTER TABLE table ADD COLUMN column TYPE;
       END IF;
     END $$;
     ```
   - Use `TIMESTAMPTZ` not `TIMESTAMP` for all date/time columns
   - Default timestamps: `DEFAULT NOW()`
   - Always add relevant indexes for foreign keys and common query patterns
   - NO transaction wrapping (migrations should be single-statement or idempotent)

5. **Output:** Print the created file path and contents for review.

## Arguments
- First argument: migration description in snake_case (e.g., `add_customer_notes`)
- If no argument, ask the user what the migration should do.
