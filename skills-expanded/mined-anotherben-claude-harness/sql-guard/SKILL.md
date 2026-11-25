---
name: sql-guard
description: SQL safety checker for database queries and migrations. This skill should be used before writing or modifying any SQL query, database migration, or code that constructs SQL strings. It enforces multi-tenant tenant_id scoping, parameterized queries, correct timestamp types, IF NOT EXISTS guards, and type-safe joins. Invoke this skill when writing INSERT/UPDATE/DELETE statements, creating migrations, modifying database queries, joining tables with mixed ID types, or when any code touches the database layer. Even for "simple SELECT queries", invoke this — tenant_id scoping bugs are silent and ship to production undetected.
---

# SQL Guard

A pre-edit checker for all SQL and database code. These rules have zero automated enforcement but cause the most insidious production bugs — tenant isolation violations, type mismatches, and unsafe query construction.

## Before Writing Any SQL

1. **Read `references/schema.md`** for the authoritative table-by-table tenant_id map, type traps, and REX SKU field mapping. That file is the source of truth for which tables need tenant_id and which don't. (Use Read — this is a reference doc, not code.)

1. **Choose the safest real schema proof surface.** For pre-PR schema/query testing, prefer a local Postgres instance restored from a sanitized clone, approved snapshot, or schema-only dump plus representative fixtures. Do not run proof against production, print credentials, store dumps in the repo, or depend on machine-local paths in committed evidence. If local full-schema proof is unavailable, treat schema/query claims as blocked or explicitly narrowed.

2. **Explore the actual service file** that already queries the tables you are about to use. Column names, join patterns, and scoping conventions vary across this codebase — do not guess from training data:
   - `search_symbols(query="[table-name]")` to find which service files query that table
   - `get_symbol([service-file], [function-name])` to pull the specific query function
   - `get_file_outline([service-file])` to see all query functions in large service files
   - Only use Read for full-file context or before editing

3. **Verify the migration files** for any table you are adding columns to or creating indexes on:
   - `search_text(query="CREATE TABLE [table-name]", path="apps/api/database/migrations/")` to find the right migration
   - `get_symbol([migration-file], [table-name])` to pull the CREATE TABLE block
   - This confirms the actual column types, existing indexes, and constraints

## The Pre-Write Checklist

Run through every item before writing or modifying database code. Skipping even one item has caused production bugs in this codebase.

### 1. Tenant Isolation

**The #1 silent bug.** A missing `tenant_id` WHERE clause leaks data across tenants with zero errors.

- Every `INSERT` into a tenant-scoped table includes `tenant_id` column
- Every `SELECT` / `UPDATE` / `DELETE` on a tenant-scoped table has `WHERE tenant_id = $N` (or joins to a table that does)
- **Check `references/schema.md`** to confirm whether the table has `tenant_id` — don't guess

Tables that commonly trip people up:
- `customers` — has `tenant_id` column but it is NOT scoped in existing queries (ambiguous — match existing patterns)
- `products` — has NO `tenant_id` — do NOT add one
- `call_logs` — HAS `tenant_id` (INTEGER) — easy to forget
- `conversations` — HAS `tenant_id` (INTEGER) — must scope
- `customer_portal_tokens` — HAS `tenant_id` (UUID, not INTEGER like others)

### 2. Parameterized Queries

**The #1 security vulnerability.** Template literals in SQL strings = SQL injection.

- All user-supplied values use `$1`, `$2`, etc. placeholders
- NEVER use template literals (`${value}`) inside SQL strings — not even for "known safe" values
- For `IN` clauses: build placeholder list dynamically, not string concatenation:
  ```javascript
  const placeholders = ids.map((_, i) => `$${i + 1}`).join(', ');
  const result = await pool.query(
    `SELECT * FROM products WHERE id IN (${placeholders})`,
    ids
  );
  ```
- For dynamic column/table names (rare): whitelist against an explicit array of known values, never interpolate

### 3. Timestamp Types

**The Melbourne timezone trap.** This codebase serves an Australian business. The server runs UTC but all business dates are Melbourne time.

- Always use `TIMESTAMPTZ`, never `TIMESTAMP`, in DDL
- Date filtering pattern (the only correct way):
  ```sql
  WHERE created_at >= $1::DATE::TIMESTAMP AT TIME ZONE 'Australia/Melbourne'
    AND created_at < ($1::DATE + INTERVAL '1 day')::TIMESTAMP AT TIME ZONE 'Australia/Melbourne'
  ```
- The `::TIMESTAMP` cast before `AT TIME ZONE` is mandatory — `DATE AT TIME ZONE` without it goes backwards on UTC servers (shifts +10 instead of -10)
- **CURRENT_DATE trap**: `CURRENT_DATE` returns the UTC date, which is wrong for Melbourne after ~2pm AEST. For "today" queries use:
  ```sql
  (CURRENT_TIMESTAMP AT TIME ZONE 'Australia/Melbourne')::date
  ```
  Any code using bare `CURRENT_DATE` for business logic is a bug — it will miss or duplicate records during the UTC/Melbourne date boundary.
- See `references/schema.md` "Melbourne Timezone Pattern" section for the full explanation

### 4. Migration Safety

- `CREATE TABLE IF NOT EXISTS` — always
- `ADD COLUMN IF NOT EXISTS` — wrap in DO block:
  ```sql
  DO $$ BEGIN
    ALTER TABLE orders ADD COLUMN IF NOT EXISTS tracking_number TEXT;
  EXCEPTION WHEN duplicate_column THEN NULL;
  END $$;
  ```
- `CREATE INDEX IF NOT EXISTS` — and NEVER inside a transaction if using `CONCURRENTLY`
- Check next migration number: currently **338** in MEMORY.md — verify with `ls apps/api/database/migrations/ | tail -5`
- Migration file exists does NOT mean it was run. Verify with `\d table_name` on the actual database if uncertain.

**Migration collision handling**: If the next number (338) already exists from another branch, increment to the next available number. Check both `apps/api/database/migrations/` and any open worktrees for pending migrations to avoid collisions.

**Rollback safety**: Every migration should be reversible or at minimum non-destructive:
- `ADD COLUMN` is safe (reversible with `DROP COLUMN`)
- `DROP COLUMN` is NOT reversible — gate behind explicit user confirmation
- `ALTER COLUMN TYPE` may lose data — add a comment noting the original type
- `CREATE INDEX CONCURRENTLY` can fail partway — always use `IF NOT EXISTS` so re-running is safe

**Dev vs production**: Migrations run on the dev database first (`DATABASE_URL` in `.env`). Production migrations are a separate deploy step. Never assume a migration that ran on dev has run on production — check the handover/deploy notes.

### 5. Type-Safe Joins

This codebase has mixed column types that cause silent bugs. The full list is in `references/schema.md` "Type Traps" section. The most dangerous ones:

| Join | Trap | Fix |
|------|------|-----|
| `products.supplier_id` → `suppliers.id` | INTEGER vs UUID | Cast: `supplier_id::text = suppliers.id::text` |
| `shopify_orders.shopify_id` → any VARCHAR | BIGINT vs VARCHAR | Cast: `shopify_id::text` or `$1::bigint` |
| `orders.rex_order_id` → bigint param | VARCHAR vs BIGINT | Cast: `$1::text` |
| `products.retail_express_id` → integer param | VARCHAR vs INTEGER | Cast: `$1::text` or `retail_express_id::int` |

Never rely on implicit PostgreSQL coercion. Always cast explicitly when types differ.

Cast safety is not just type matching:

- Cast untrusted JSON/text/external IDs only after a guard proves the value is non-empty, well-formed, and in range.
- Numeric-looking text outside the destination range, such as `bigint` overflow, must be filtered before `::bigint`; one corrupt payload row must not abort the whole worker query.
- Prefer casting the parameter side, not the indexed column side. `p.id = ANY($1::uuid[])` can use the primary-key index; `p.id::text = ANY($1::text[])` can force scans.
- For every changed SQL cast on a hot path, worker, sync, proof lane, or high-cardinality table, capture query-plan/index evidence or classify the missing proof as a finding.

**Established join patterns in this codebase** (verified from service files):

| From → To | Correct Pattern | Notes |
|-----------|----------------|-------|
| `products` → `suppliers` | `products.rex_supplier_id::text = suppliers.retail_express_id` | NOT via `supplier_id` → `suppliers.id` |
| `orders` → `customers` | `orders.customer_id = customers.id` | Both INTEGER |
| `shopify_orders` → `orders` | `shopify_orders.order_id = orders.id` | Both INTEGER |
| `call_logs` → `customers` | `call_logs.customer_id = customers.id` | Both INTEGER, but call_logs needs tenant_id |

### 6. REX SKU Field Mapping

When working with REX (Retail Express) product data, the SKU fields are misleadingly named. See `references/schema.md` "REX SKU Field Mapping" for the full map. The critical trap:

- REX `supplier_sku` → our `sku` (this is the primary SKU you want)
- REX `sku` (top-level) → usually NULL (do NOT use this)
- REX `supplier_sku2` → our `sku2` (secondary/alternate)

### 7. Batch/Bulk Operations

- Use `unnest()` for bulk inserts (more efficient than VALUES lists for large batches):
  ```sql
  INSERT INTO products (sku, name, price)
  SELECT * FROM unnest($1::text[], $2::text[], $3::numeric[])
  ON CONFLICT (sku) DO UPDATE SET name = EXCLUDED.name, price = EXCLUDED.price;
  ```
- Use `VALUES` lists for small batches (under ~50 rows):
  ```javascript
  const values = items.map((_, i) => `($${i*3+1}, $${i*3+2}, $${i*3+3})`).join(', ');
  const params = items.flatMap(item => [item.sku, item.name, item.price]);
  await pool.query(`INSERT INTO products (sku, name, price) VALUES ${values}`, params);
  ```
- Bound all queries — add `LIMIT` or date windows to prevent unbounded table scans
- For large result sets, use cursor-based pagination (`WHERE id > $last_id ORDER BY id LIMIT $page_size`)

## Post-Write Review Checklist

After writing any SQL query or migration, run through these 8 items. This takes 30 seconds and catches the mistakes that pass code review:

1. **Tenant scoped?** Every tenant-scoped table in the query has `WHERE tenant_id = $N`
2. **Parameterized?** Zero template literals inside SQL strings
3. **Types match safely?** Every JOIN and WHERE comparison uses matching types, casts untrusted values only after malformed/empty/out-of-range guards, and keeps indexed column predicates indexable
4. **Timestamps correct?** `TIMESTAMPTZ` in DDL, `AT TIME ZONE` pattern in queries, no bare `CURRENT_DATE`
5. **Bounded?** Query has `LIMIT`, date window, pagination, or a proof-specific sample set — no unbounded scans in runtime paths or live-proof lanes
6. **Idempotent?** Migration uses `IF NOT EXISTS` / `IF EXISTS` guards
7. **Column names real?** Every column name was verified by reading the actual table's migration or service file
8. **CONCURRENTLY safe?** If using `CREATE INDEX CONCURRENTLY`, it is NOT inside a transaction block
9. **Local full-schema proof safe?** Schema/query changes ran against local restored Postgres or have a documented blocker/narrowed claim; evidence shows no production writes, no secrets, no repo dumps, and cleanup/reset.

## Common Mistakes from Evaluations

These specific mistakes have been observed in A/B testing. They are the highest-probability errors:

| Mistake | Why It Happens | Prevention |
|---------|---------------|------------|
| Adding `WHERE products.tenant_id = $1` | Guessing from table name — products has no tenant_id | Check `references/schema.md` |
| Using `duration` instead of `call_duration_seconds` | Guessing column name from context | Read actual migration/service file |
| Using `created_at` instead of `ring_time` on call_logs | Generic timestamp assumption | Read actual migration/service file |
| Joining `products.supplier_id = suppliers.id` directly | Looks obvious but types mismatch (INT vs UUID) | Check Type Traps table |
| Using bare `CURRENT_DATE` in WHERE clause | Seems correct but wrong after 2pm AEST | Use `(CURRENT_TIMESTAMP AT TIME ZONE 'Australia/Melbourne')::date` |

## Quick Reference: Safe Patterns

```sql
-- Safe INSERT with tenant_id (for tenant-scoped tables)
INSERT INTO call_logs (tenant_id, customer_id, call_duration_seconds)
VALUES ($1, $2, $3)
RETURNING id;

-- Safe date filtering (Melbourne timezone)
WHERE ring_time >= $1::DATE::TIMESTAMP AT TIME ZONE 'Australia/Melbourne'
  AND ring_time < ($1::DATE + INTERVAL '1 day')::TIMESTAMP AT TIME ZONE 'Australia/Melbourne'

-- Safe "today" in Melbourne
WHERE ring_time >= (CURRENT_TIMESTAMP AT TIME ZONE 'Australia/Melbourne')::date::TIMESTAMP AT TIME ZONE 'Australia/Melbourne'

-- Safe bigint comparison
WHERE shopify_id = $1::bigint
-- or against text column:
WHERE rex_order_id = $1::text

-- Safe type-mismatched join (products → suppliers)
WHERE products.rex_supplier_id::text = suppliers.retail_express_id

-- Safe migration column add
DO $$ BEGIN
  ALTER TABLE orders ADD COLUMN IF NOT EXISTS tracking_number TEXT;
EXCEPTION WHEN duplicate_column THEN NULL;
END $$;

-- Safe bulk insert with unnest
INSERT INTO products (sku, name, price)
SELECT * FROM unnest($1::text[], $2::text[], $3::numeric[])
ON CONFLICT (sku) DO UPDATE SET name = EXCLUDED.name, price = EXCLUDED.price;

-- Safe parameterized IN clause
const placeholders = ids.map((_, i) => `$${i + 1}`).join(', ');
const result = await pool.query(
  `SELECT * FROM products WHERE id IN (${placeholders})`,
  ids
);
```
