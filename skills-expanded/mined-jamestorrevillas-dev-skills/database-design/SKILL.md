---
name: database-design
description: Use this skill when designing database schemas, choosing between SQL and NoSQL, optimizing queries, designing indexes, modeling relationships, working with vector databases, or planning data migrations. Trigger on keywords: database, schema, SQL, NoSQL, index, query optimization, data model, migration, ORM, PostgreSQL, MongoDB, Redis, vector database, N+1.
---

# Database Design

## Schema Design Principles

- **Normalize first** — eliminate redundancy, then denormalize only for proven performance needs
- **Name clearly** — `user_id` not `uid`, `created_at` not `ts`
- **Every table needs** — a primary key, `created_at`, `updated_at`
- **Soft deletes** — add `deleted_at` instead of hard deleting rows you might need to recover

---

## Relationship Patterns

| Relationship | Implementation |
|---|---|
| One-to-One | Foreign key on either table + UNIQUE constraint |
| One-to-Many | Foreign key on the "many" side |
| Many-to-Many | Junction/pivot table with two foreign keys |

---

## Indexing Strategy

**Rule:** Index columns you filter, sort, or join on frequently.

```sql
-- Index for common query patterns
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
CREATE INDEX idx_posts_created ON posts(created_at DESC);

-- Partial index for active records only
CREATE INDEX idx_active_users ON users(email) WHERE deleted_at IS NULL;
```

### When NOT to Over-Index
- Every index slows down writes
- Index columns with low cardinality (boolean, status with 3 values) only if queries are very frequent
- Monitor query performance, add indexes based on actual slow queries

---

## Query Optimization

### N+1 Query Problem
```typescript
// BAD — N+1: 1 query for posts + N queries for each author
const posts = await Post.findAll()
for (const post of posts) {
  const author = await User.findById(post.userId) // N queries!
}

// GOOD — 2 queries total using JOIN or eager loading
const posts = await Post.findAll({ include: [{ model: User }] })
```

### Pagination
```sql
-- Offset pagination (simple but slow for large offsets)
SELECT * FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 100;

-- Cursor pagination (fast for large datasets)
SELECT * FROM posts WHERE created_at < :cursor ORDER BY created_at DESC LIMIT 20;
```

Use cursor pagination for large tables or infinite scroll.

---

## SQL vs NoSQL Cheatsheet

| SQL | NoSQL |
|---|---|
| ACID transactions | High write throughput |
| Complex queries, joins | Flexible/variable schema |
| Data integrity critical | Horizontal scale priority |
| Well-defined schema | Unstructured or nested data |
| PostgreSQL, MySQL | MongoDB, DynamoDB, Cassandra |

**Hybrid:** Use SQL as the source of truth, Redis for caching, Elasticsearch for search.

---

## Vector Databases (AI Use Cases)

For semantic search, RAG, and embeddings:

| DB | Best For |
|---|---|
| pgvector | Existing PostgreSQL stack |
| Pinecone | Managed, production-scale |
| Weaviate | Multi-modal, hybrid search |
| Chroma | Local dev and prototyping |

### Indexing Strategies
- **HNSW** — best recall, higher memory usage
- **IVFFlat** — lower memory, slightly lower recall
- **Product Quantization** — memory-efficient for very large datasets

---

## Migration Best Practices

- **Never drop columns in the same deploy** as removing code that uses them — separate deploys
- **Backward compatible first** — add new column → deploy new code → remove old column
- **Always test migrations** on a copy of production data before running in prod
- **Zero-downtime migrations** — use `NOT NULL DEFAULT` carefully, add constraints after backfill

---

## Redis Use Cases

| Use Case | Pattern |
|---|---|
| Session storage | Key: `session:{id}`, TTL |
| Rate limiting | Increment counter with TTL |
| Caching | Key: `cache:{resource}:{id}`, TTL |
| Pub/Sub | Real-time events between services |
| Job queue | List with LPUSH/BRPOP |
| Leaderboard | Sorted Set (ZADD/ZRANGE) |
