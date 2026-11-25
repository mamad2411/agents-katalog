---
name: database-migration-skill-generator
description: "Generate a project-specific database migration skill. Use for any project with a database to document migration patterns. Triggers on: generate migration skill, create migration patterns, database-migration-skill-generator."
type: meta
generates: migrations
trigger:
  condition: database exists
---

# Database Migration Skill Generator

Generate a project-specific `migrations` skill that documents exactly how to create and run database migrations in THIS project.

---

## The Job

1. Read project context (`docs/project.json`)
2. Analyze existing migration setup
3. Ask clarifying questions about migration patterns
4. Generate `docs/skills/migrations/SKILL.md`
5. Update `project.json` to record the generated skill

---

## Step 1: Read Project Context

```bash
cat docs/project.json
```

Extract:
- `database.type` — postgres, mysql, mongodb, etc.
- `database.client` — supabase, prisma, drizzle, goose, alembic, etc.
- `database.migrationsPath` — where migrations live
- `commands.migrate` — migration command
- `commands.migrateCreate` — create migration command

---

## Step 2: Analyze Existing Migration Setup

```bash
# Find migration files
find . -type d -name "migrations" | head -5
find . -type f -name "*.sql" | grep -i migrat | head -10

# Check for migration tools
ls package.json 2>/dev/null && grep -E "prisma|drizzle|kysely" package.json
ls go.mod 2>/dev/null && grep -E "goose|migrate" go.mod

# Look at existing migrations
ls -la supabase/migrations/ 2>/dev/null || \
ls -la prisma/migrations/ 2>/dev/null || \
ls -la migrations/ 2>/dev/null
```

---

## Step 3: Clarifying Questions

```
I found the following migration setup:

Database: [detected]
Migration Tool: [detected]
Migrations Path: [detected]

Please confirm or correct:

1. What migration tool do you use?
   A. Supabase CLI (supabase migration)
   B. Prisma Migrate
   C. Drizzle Kit
   D. Goose
   E. Alembic
   F. Raw SQL files
   G. Other: [specify]

2. How are migrations run?
   A. Automatically on deploy (CI/CD)
   B. Manually via CLI
   C. Both

3. Do you use any seed data?
   A. Yes, seeds run after migrations
   B. Yes, separate seed command
   C. No seed data

4. Any special conventions?
   A. Timestamped file names
   B. Sequential numbered files
   C. Named migrations (e.g., 001_create_users)
```

---

## Step 4: Generate the Skill

Create `docs/skills/migrations/SKILL.md`:

```markdown
---
name: migrations
description: "Create and run database migrations in [PROJECT_NAME]"
project-specific: true
generated-by: database-migration-skill-generator
generated-at: [DATE]
---

# Database Migrations Skill

How to create and manage database migrations in this project.

---

## Quick Reference

| Task | Command |
|------|---------|
| Create migration | `[MIGRATE_CREATE_CMD]` |
| Run migrations | `[MIGRATE_CMD]` |
| Check status | `[MIGRATE_STATUS_CMD]` |
| Rollback | `[ROLLBACK_CMD]` |

---

## Migration Tool

This project uses **[MIGRATION_TOOL]** for database migrations.

- **Database:** [DATABASE_TYPE]
- **Migrations path:** `[MIGRATIONS_PATH]`
- **Naming convention:** `[YYYYMMDDHHMMSS]_[description].sql`

---

## Creating a Migration

### Step 1: Generate Migration File

\`\`\`bash
[MIGRATE_CREATE_CMD] [description]

# Example:
[MIGRATE_CREATE_CMD] add_status_to_tasks
\`\`\`

This creates: `[MIGRATIONS_PATH]/YYYYMMDDHHMMSS_add_status_to_tasks.sql`

### Step 2: Write the Migration

\`\`\`sql
-- [MIGRATIONS_PATH]/YYYYMMDDHHMMSS_add_status_to_tasks.sql

-- Add status column to tasks
ALTER TABLE tasks ADD COLUMN status TEXT NOT NULL DEFAULT 'pending';

-- Add index for common queries
CREATE INDEX idx_tasks_status ON tasks(status);

-- Add check constraint
ALTER TABLE tasks ADD CONSTRAINT chk_tasks_status 
  CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled'));
\`\`\`

### Step 3: Run the Migration

\`\`\`bash
[MIGRATE_CMD]
\`\`\`

---

## Common Migration Patterns

### Add a Column

\`\`\`sql
ALTER TABLE [table] ADD COLUMN [column] [TYPE] [constraints];

-- Example with default
ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT true;

-- Example nullable
ALTER TABLE users ADD COLUMN phone TEXT;
\`\`\`

### Remove a Column

\`\`\`sql
ALTER TABLE [table] DROP COLUMN [column];
\`\`\`

### Create a Table

\`\`\`sql
CREATE TABLE [table_name] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id),
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE [table_name] ENABLE ROW LEVEL SECURITY;

-- Create RLS policy
CREATE POLICY "[table]_org_policy" ON [table_name]
  FOR ALL USING (organization_id = (auth.jwt() ->> 'organization_id')::uuid);

-- Create indexes
CREATE INDEX idx_[table]_org ON [table_name](organization_id);
\`\`\`

### Add a Foreign Key

\`\`\`sql
ALTER TABLE [table] ADD COLUMN [fk_column] UUID REFERENCES [other_table](id);

-- With cascade
ALTER TABLE [table] ADD COLUMN [fk_column] UUID 
  REFERENCES [other_table](id) ON DELETE CASCADE;
\`\`\`

### Create an Index

\`\`\`sql
-- B-tree (default, good for equality and range)
CREATE INDEX idx_[table]_[column] ON [table]([column]);

-- Composite index
CREATE INDEX idx_[table]_[cols] ON [table]([col1], [col2]);

-- Partial index
CREATE INDEX idx_[table]_active ON [table]([column]) WHERE is_active = true;

-- GIN index (for arrays, JSONB)
CREATE INDEX idx_[table]_tags ON [table] USING GIN (tags);
\`\`\`

### Add Enum Type

\`\`\`sql
-- Create the type
CREATE TYPE task_status AS ENUM ('pending', 'in_progress', 'completed', 'cancelled');

-- Use in table
ALTER TABLE tasks ADD COLUMN status task_status NOT NULL DEFAULT 'pending';
\`\`\`

### Add Check Constraint

\`\`\`sql
ALTER TABLE [table] ADD CONSTRAINT chk_[name] CHECK ([condition]);

-- Example
ALTER TABLE orders ADD CONSTRAINT chk_orders_amount CHECK (amount >= 0);
\`\`\`

---

## RLS Policies (Supabase)

Every table with user data needs RLS:

\`\`\`sql
-- Enable RLS
ALTER TABLE [table] ENABLE ROW LEVEL SECURITY;

-- Standard org-scoped policy
CREATE POLICY "[table]_org_access" ON [table]
  FOR ALL 
  USING (organization_id = (auth.jwt() ->> 'organization_id')::uuid);

-- Read-only for specific role
CREATE POLICY "[table]_read" ON [table]
  FOR SELECT
  USING (true); -- or specific condition

-- Insert with user check
CREATE POLICY "[table]_insert" ON [table]
  FOR INSERT
  WITH CHECK (created_by = auth.uid());
\`\`\`

---

## Migration Checklist

Before creating a migration:

- [ ] Is this change backwards compatible?
- [ ] Do I need to backfill data?
- [ ] Are there dependent tables that need updating?
- [ ] Will this lock the table for too long?

When writing the migration:

- [ ] Use descriptive file name
- [ ] Add comments explaining the change
- [ ] Include RLS policy for new tables
- [ ] Add appropriate indexes
- [ ] Handle existing data if needed

After running:

- [ ] Verify migration ran successfully
- [ ] Check application still works
- [ ] Test affected features

---

## Troubleshooting

### Migration Failed

\`\`\`bash
# Check migration status
[MIGRATE_STATUS_CMD]

# See error details
[CHECK_LOGS_CMD]
\`\`\`

### Need to Rollback

\`\`\`bash
# Rollback last migration
[ROLLBACK_CMD]
\`\`\`

**Note:** Some migrations cannot be rolled back (e.g., DROP COLUMN). Plan accordingly.

### Conflict with Team

If someone else pushed a migration:

1. Pull latest changes
2. Run migrations to catch up
3. Check for conflicts
4. Create your migration

---

## Environment-Specific

### Local Development

\`\`\`bash
[LOCAL_MIGRATE_CMD]
\`\`\`

### Staging/Production

Migrations run automatically in CI/CD pipeline when deploying.

**Never run migrations manually in production** unless absolutely necessary.

---

## Key Files

| File | Purpose |
|------|---------|
| `[MIGRATIONS_PATH]/` | Migration files |
| `[SEED_PATH]` | Seed data (if applicable) |
| `[CONFIG_PATH]` | Database/migration config |
```

---

## Step 5: Update project.json

Add to `skills.generated[]`:

```json
{
  "name": "migrations",
  "generatedFrom": "database-migration-skill-generator",
  "generatedAt": "2026-02-20"
}
```

---

## Customization by Tool

### Supabase

```bash
MIGRATE_CREATE_CMD="supabase migration new"
MIGRATE_CMD="supabase db push"
MIGRATE_STATUS_CMD="supabase migration list"
MIGRATIONS_PATH="supabase/migrations"
```

### Prisma

```bash
MIGRATE_CREATE_CMD="npx prisma migrate dev --name"
MIGRATE_CMD="npx prisma migrate deploy"
MIGRATE_STATUS_CMD="npx prisma migrate status"
MIGRATIONS_PATH="prisma/migrations"
```

### Drizzle

```bash
MIGRATE_CREATE_CMD="npx drizzle-kit generate:pg --name"
MIGRATE_CMD="npx drizzle-kit push:pg"
MIGRATIONS_PATH="drizzle/migrations"
```

### Goose (Go)

```bash
MIGRATE_CREATE_CMD="goose create"
MIGRATE_CMD="goose up"
MIGRATE_STATUS_CMD="goose status"
ROLLBACK_CMD="goose down"
MIGRATIONS_PATH="migrations"
```
