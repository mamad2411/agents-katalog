---

name: cosmosdb-mongodb
description: >
  Best practices for Azure Cosmos DB for MongoDB (RU-based). Use this skill when:
  (1) creating or modifying database indexes,
  (2) writing database migrations,
  (3) designing queries against CosmosDB,
  (4) troubleshooting query performance or index errors.
metadata:
  version: "1.0.0"

---

# Azure Cosmos DB for MongoDB (RU-based) Best Practices

## Indexing Strategy

### Prefer Single-Field Indexes for Equality Filters

Cosmos DB uses **index intersection** for multi-property equality filters. Create single-field indexes on each filtered field rather than large compound indexes:

```typescript
// ✅ GOOD — single-field indexes, Cosmos intersects them for queries with multiple filters
await col.createIndex({ "run.status": 1 });
await col.createIndex({ workerType: 1 });
await col.createIndex({ deletedAt: 1 });

// ❌ BAD — large compound index may be silently ignored by Cosmos DB
await col.createIndex({ "run.status": 1, workerType: 1, deletedAt: 1, priority: -1, createdAt: 1 });
```

### Use 2-Field Compound Indexes for ORDER BY

Cosmos DB requires a compound index that matches the sort fields. Keep it to **2 fields maximum** for reliability:

```typescript
// ✅ GOOD — 2-field compound for sort, single-field indexes handle the WHERE clause
await col.createIndex({ priority: -1, createdAt: 1 });

// ✅ GOOD — selective filter + sort field compound
await col.createIndex({ "run.postProcessorStatus": 1, updatedAt: -1 });
```

### Large Compound Indexes May Be Silently Dropped

Cosmos DB (RU-based) **silently drops compound indexes** it cannot support — `createIndex()` succeeds but the index is never created. This leads to runtime errors like:

```
"The order by query does not have a corresponding composite index that it can be served from."
```

**Always verify** that your index was actually created:

```javascript
db.collection.getIndexes()
```

### Index Pattern for Polling Queries

For queries that combine equality filters with a sort (e.g., scheduler dispatchers), use this pattern:

1. Single-field indexes on each equality filter field (from migration 009)
2. A focused 2-field compound index: `{ mostSelectiveFilterField: 1, sortField: -1 }`

## Migration Best Practices

### Structure

Migrations live in `packages/db-migrations/src/migrations/` and implement `MigrationInterface` from `mongo-migrate-ts`:

```typescript
import type { Db } from "mongodb";
import type { MigrationInterface } from "mongo-migrate-ts";

export class MyMigration implements MigrationInterface {
  async up(db: Db): Promise<void> { /* ... */ }
  async down(db: Db): Promise<void> { /* ... */ }
}
```

### Always Wrap Index Operations in try/catch

Index creation or deletion may fail if the index already exists or doesn't exist. Never let this crash the migration:

```typescript
try {
  await col.createIndex({ field: 1 });
  console.log("[NNN] Created index on field");
} catch (err: any) {
  console.log(`[NNN] Index already exists or couldn't be created: ${err.message ?? err}`);
}
```

### Register in required-migrations.ts

Every new migration must be added to `packages/db-migrations/src/required-migrations.ts`. The API readiness probe checks that all required migrations have been applied.

### down() Should Be Safe but Not Destructive

Dropping indexes in `down()` can be destructive in production. Prefer a log-only approach:

```typescript
async down(db: Db): Promise<void> {
  console.log("[NNN-down] Skipping index drop — indexes should be dropped manually if needed");
}
```

## Features NOT Supported or Limited

These MongoDB features do **not** work reliably in Cosmos DB for MongoDB (RU-based):

| Feature | Status |
|---------|--------|
| Large compound indexes (5+ fields) | May be silently ignored |
| `$text` / text indexes | Not supported |
| Certain aggregation stages | Partial support — test each one |
| Change streams (resume after) | Limited compared to native MongoDB |
| Transactions (multi-document) | Supported only on API version 4.0+ with limitations |

## RU Cost Awareness

- Every index increases write RU cost (each insert/update/delete must update all indexes)
- Keep the total number of indexes reasonable — add indexes only for queries that actually run
- Compound indexes cost more RUs per write than single-field indexes
