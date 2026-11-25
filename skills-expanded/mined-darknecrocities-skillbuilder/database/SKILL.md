---
name: database
description: Architect, implement, and maintain resilient relational and NoSQL databases, zero-downtime schema migrations (expand/contract), index optimization, and connection pooling.
---

# Database & Datastore Engineering (`/database`)

> **Role**: Principal Database Architect & Data Engineer  
> **Philosophy**: *Data is the foundation. Index intentionally. Migrate without downtime. Guard ACID integrity. Keep transactions micro-short.*

This skill establishes database architecture and operational discipline across PostgreSQL, SQLite, Google Cloud SQL, Spanner, Redis, and vector stores. It enforces relational integrity, non-blocking migrations, composite indexing, and connection pool hygiene.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource Type | Document | Description |
| :--- | :--- | :--- |
| **Reference** | [references/schema-design-and-normalization.md](references/schema-design-and-normalization.md) | Relational constraints, foreign keys, enums, soft deletes vs hard deletes. |
| **Reference** | [references/zero-downtime-migrations.md](references/zero-downtime-migrations.md) | Expand-and-contract migration strategy, non-blocking indexes (`CONCURRENTLY`). |
| **Reference** | [references/indexing-and-query-optimization.md](references/indexing-and-query-optimization.md) | B-tree, GIN indexes, EXPLAIN ANALYZE interpretation, eliminating N+1 queries. |
| **Reference** | [references/connection-pooling-and-transactions.md](references/connection-pooling-and-transactions.md) | PgBouncer configuration, isolation levels, lock minimization. |
| **Reference** | [references/deduplicated-backup-and-deletion-guardrails.md](references/deduplicated-backup-and-deletion-guardrails.md) | Single-slot SHA-256 content-hashed backups (zero spam) and sensitive pre-deletion user disclosures. |
| **Reference** | [references/database-error-catalog.md](references/database-error-catalog.md) | Catalog of database errors: deadlocks, pool exhaustion, lock timeouts. |
| **Template** | [templates/migration_expand_contract.sql](templates/migration_expand_contract.sql) | Production 3-step zero-downtime SQL migration template. |
| **Template** | [templates/drizzle_schema_template.ts](templates/drizzle_schema_template.ts) | Production Drizzle ORM schema with relations, indexes, and timestamps. |
| **Utility** | [scripts/verify_database_hygiene.py](scripts/verify_database_hygiene.py) | CLI auditor checking migrations for missing FK indexes, hazardous locks, and unapproved deletions. |
| **Utility** | [scripts/manage_deduplicated_backup.py](scripts/manage_deduplicated_backup.py) | Multi-agent content-addressable single-slot backup manager and pre-deletion safety gate. |

---

## 2. Zero-Downtime Expand-and-Contract Migrations

```mermaid
flowchart TD
    subgraph Step1["Step 1: Expand (Deploy 1)"]
        A["Add new column/table nullable or with default"]
        B["Deploy code dual-writing to Old and New columns"]
    end
    subgraph Step2["Step 2: Backfill (Async Job)"]
        C["Batch backfill historical records in chunks (e.g. 5,000 rows)"]
        D["Verify checksums and record parity between columns"]
    end
    subgraph Step3["Step 3: Contract (Deploy 2)"]
        E["Switch application to read exclusively from New column"]
        F["Remove Old column writing code"]
        G["Drop Old column via non-blocking migration"]
    end
    Step1 --> Step2 --> Step3
```

### PostgreSQL Migration Guardrails:
1. **Never use `ALTER TABLE ... ADD COLUMN ... DEFAULT <expensive>`** without PG 11+ instant metadata defaults.
2. **Never create indexes synchronously** on production tables:
   ```sql
   -- ❌ HAZARDOUS: Locks table for writes
   CREATE INDEX idx_users_email ON users(email);

   -- ✅ PRODUCTION: Non-blocking background build
   CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
   ```
3. **Always set lock timeouts** before running DDL migrations:
   ```sql
   SET lock_timeout = '3s';
   SET statement_timeout = '15s';
   ```

---

## 3. Index Optimization & N+1 Elimination

### 3.1 Index Types Decision Matrix
- **B-tree (Default)**: Equality (`=`), range (`<`, `>`, `BETWEEN`), sorting (`ORDER BY`).
- **GIN (Generalized Inverted Index)**: `JSONB` document paths, arrays, full-text search (`tsvector`).
- **Partial Index**: High cardinality sub-queries (e.g. `WHERE status = 'unprocessed'`). Saves 90%+ index memory.
- **Composite Index Order**: Equality columns first, range/sort columns second (`(tenant_id, created_at DESC)`).

### 3.2 Eliminating N+1 Query Anti-Patterns
```typescript
// ❌ ANTI-PATTERN: N+1 queries in loop
const users = await db.users.findMany();
for (const user of users) {
  user.posts = await db.posts.findMany({ where: { userId: user.id } }); // N queries!
}

// ✅ PRODUCTION: Single batch join or DataLoader
const usersWithPosts = await db.users.findMany({
  include: { posts: true } // Single JOIN or IN (...) query
});
```

---

## 4. Connection Pool Tuning

Unbounded connections exhaust server RAM and trigger `remaining connection slots are reserved for non-replication superuser connections`.

### Mathematical Pool Sizing Formula:
$$\text{Pool Size} = (\text{CPU Cores} \times 2) + \text{Disk Spindle Count}$$
For a 4-core cloud instance, pool size should be **8 to 12 connections per worker**, never hundreds.

### Safe Session Timeouts:
- `statement_timeout = '5000ms'` (kill runaway queries before consuming all worker threads)
- `idle_in_transaction_session_timeout = '10000ms'` (reclaim idle locked connections)

---

## 5. Deduplicated Single-Slot Backups & Sensitive Deletion Gate

When one or more agents work on PostgreSQL, SQLite, Cloud SQL, or serverless stores simultaneously, they MUST prevent both **unbacked destructive mutations** and **spammy backup duplication** (`*.bak.1`, `*.bak.2`, `backup_copy.sql`):

1. **Idempotent Content-Hashed Single-Slot Backup**:
   - Before running schema migrations or bulk updates, execute `manage_deduplicated_backup.py` to compute the SHA-256 digest of the database or schema state and record it in `.backups/backup_manifest.json`.
   - If the state SHA-256 has not changed since the last snapshot (or a concurrent subagent already backed up the current state), **reuse the canonical slot** (`SKIPPED_DUPLICATE_HASH`) rather than creating redundant backup files.
2. **Sensitive Data & Destructive Operation Gate (Tell the User First)**:
   - Before executing `DROP TABLE`, `DROP COLUMN`, `TRUNCATE`, or unconditioned `DELETE`, the agent MUST **halt and notify the user first** with the target resource, sensitivity tier, row/file impact scope, and verified canonical backup SHA-256 hash.
   - Prefer soft-deletes (`deleted_at TIMESTAMPTZ NULL`) over hard deletions.
   - Once the user explicitly approves a permanent deletion, annotate the SQL script with `-- @user-approved-deletion` and `-- @verified-backup-sha256: <digest>`.

```bash
# 1. Create or reuse a single canonical deduplicated backup (zero duplicate spam)
python3 skills/database/scripts/manage_deduplicated_backup.py --target data/app.sqlite --agent-id track-2a

# 2. Verify pre-deletion safety gate and generate sensitive deletion disclosure
python3 skills/database/scripts/manage_deduplicated_backup.py --target data/app.sqlite --check-deletion

# 3. Audit SQL migration scripts for hazardous locks, unapproved drops, and duplicate backup spam
python3 skills/database/scripts/verify_database_hygiene.py --path migrations/
```
