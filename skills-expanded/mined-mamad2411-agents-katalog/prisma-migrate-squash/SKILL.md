---
name: prisma-migrate-squash
description: "Squash all Prisma migrations into a single clean init migration. Use this skill whenever the user wants to squash, collapse, consolidate, or clean up Prisma migrations — even if they say things like \"too many migrations\", \"clean up migration history\", \"reset migration files\", \"create a fresh init migration\", or \"start fresh with Prisma\". Trigger on any mention of Prisma + squash/collapse/consolidate/clean/reset/fresh. This skill handles the full workflow: detecting your schema, generating a timestamp, running migrate diff, flagging manual fixes needed (e.g., pgvector HNSW indexes), and marking the migration as applied across environments."
---

# Prisma Migrate Squash

Squashing migrations collapses your entire migration history into one clean `init` migration that represents the current schema state. The result is a single SQL file that can bootstrap a fresh database, while production databases skip it (already applied).

## When to squash

- Migration folder is cluttered after months of development
- Onboarding new developers who don't need history
- Preparing for a major version release
- Dev database drift is causing `migrate dev` consistency errors

## A common mistake to avoid

**Do not use `prisma migrate dev --name init` to squash.** That command creates a new incremental migration based on schema drift — it does not collapse existing migrations. Use `prisma migrate diff --from-empty` as described below.

## Step-by-step process

### Step 1: Inspect before you delete

Before touching anything, read the project to understand what you're working with. This matters because some things in migration history — like custom pgvector HNSW indexes, PostGIS GIST indexes, or raw SQL seed data — won't survive the `migrate diff` regeneration and need to be manually preserved.

```bash
# Count and list migrations
ls prisma/migrations/ | grep -v migration_lock.toml
```

Read `prisma/schema.prisma` to check for special extensions (`extensions = [vector]`, PostGIS, etc.).

Scan the existing migration files for any custom SQL that Prisma can't represent in the schema model:
- `CREATE INDEX ... USING hnsw` or `USING ivfflat` (pgvector)
- `CREATE INDEX ... USING gist` (PostGIS)
- `INSERT` statements (seed/reference data)
- `CREATE EXTENSION` calls

Copy any of these down — you'll need to manually re-add them after Step 4.

### Step 2: Delete existing migration folders

Keep `migration_lock.toml` — it records the provider and must not be deleted.

```bash
find ./prisma/migrations -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +
```

### Step 3: Create the new init migration directory

Use a real timestamp so the migration name is meaningful and sortable:

```bash
# Generate timestamp in Prisma format: YYYYMMDDHHmmss
TIMESTAMP=$(date -u +%Y%m%d%H%M%S)
mkdir -p "./prisma/migrations/${TIMESTAMP}_init"
touch "./prisma/migrations/${TIMESTAMP}_init/migration.sql"
echo "Created: prisma/migrations/${TIMESTAMP}_init/migration.sql"
```

### Step 4: Generate the squashed SQL

This command diffs from an empty database to your current schema, producing the full CREATE TABLE / CREATE INDEX statements:

```bash
npx prisma migrate diff \
  --from-empty \
  --to-schema-datamodel ./prisma/schema.prisma \
  --script > "./prisma/migrations/${TIMESTAMP}_init/migration.sql"
```

After generating, **always inspect the output** for index definitions that need manual correction. Prisma doesn't know about extension-specific index methods.

#### Common manual fixes

**pgvector (halfvec/vector HNSW indexes)**

Prisma generates plain B-tree indexes for vector columns:
```sql
-- Prisma generates (wrong for similarity search):
CREATE INDEX "Persona_embedding_idx" ON "Persona"("embedding");

-- Replace with HNSW index for cosine similarity:
CREATE INDEX "Persona_embedding_idx" ON "Persona"
  USING hnsw ("embedding" halfvec_cosine_ops)
  WITH (m = 16, ef_construction = 64);
```

Check your original migrations to find what index method and parameters were used — copy those exactly. The parameters (`m`, `ef_construction`) affect query performance and should match what production is using.

**Other extensions**: If you use PostGIS, TimescaleDB, or other extensions, similarly check for any special index types (`GIST`, `BRIN`, etc.) that Prisma may have flattened.

### Step 5: Dev environment only — clear migration history

If you're working in development (where `migrate dev` is used), the database still has records of the old migrations in `_prisma_migrations`. Since those files no longer exist, `migrate dev` will complain about consistency. Clear the table:

```sql
-- Run against your dev/shadow database:
DELETE FROM "_prisma_migrations";
```

**Skip this for production.** Production uses `migrate deploy`, which only applies pending migrations and doesn't check consistency against existing records.

### Step 6: Mark migration as applied on all environments

This prevents Prisma from trying to run the init migration on databases that already have the schema:

```bash
# Run on every environment: dev, staging, production
npx prisma migrate resolve --applied "${TIMESTAMP}_init"
```

On production, run this before any other deployment step. On CI/CD, add it to your deploy pipeline before `migrate deploy`.

### Step 7: Verify

```bash
# Should show only your new init migration
npx prisma migrate status
```

A healthy output shows the new migration as "Applied" with no pending or failed migrations.

## Full script (copy-paste for dev environments)

```bash
#!/bin/bash
set -e

# 1. Delete old migrations
find ./prisma/migrations -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +

# 2. Create init directory
TIMESTAMP=$(date -u +%Y%m%d%H%M%S)
MIGRATION_DIR="./prisma/migrations/${TIMESTAMP}_init"
mkdir -p "$MIGRATION_DIR"

# 3. Generate squashed SQL
npx prisma migrate diff \
  --from-empty \
  --to-schema-datamodel ./prisma/schema.prisma \
  --script > "$MIGRATION_DIR/migration.sql"

echo "Generated: $MIGRATION_DIR/migration.sql"
echo ""
echo "IMPORTANT: Review migration.sql for any extension-specific indexes"
echo "(pgvector HNSW, PostGIS GIST, etc.) that need manual correction."
echo ""

# 4. Clear migration history (dev only)
echo "Run this against your dev DB:"
echo "  DELETE FROM \"_prisma_migrations\";"
echo ""

# 5. Mark as applied
echo "Then run:"
echo "  npx prisma migrate resolve --applied ${TIMESTAMP}_init"
```

## Troubleshooting

**`migrate dev` fails with "drift detected"** — You forgot to clear `_prisma_migrations`. Run the DELETE query, then retry.

**`migrate deploy` tries to run the init migration on prod** — You forgot to run `migrate resolve --applied`. Run it now; it's safe.

**Index errors on first deploy** — You likely have an extension-specific index that needs manual correction (see Step 4). Open the migration.sql, find the index, and fix the `USING` clause.

**Shadow database errors during `migrate diff`** — Ensure `SHADOW_DATABASE_URL` is set in your `.env` and the shadow DB exists. Create it with `createdb <shadow_db_name>` if needed.
