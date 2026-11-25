---
name: db-optimizer
description: Optimize database queries — EXPLAIN analysis, index recommendations, query rewriting, connection pooling, N+1 detection. Supports PostgreSQL with TypeORM/Prisma and Django ORM. Use when the user says "slow query", "optimize queries", "EXPLAIN ANALYZE", "N+1 problem", "database performance", "index recommendations", or needs to tune database performance.
allowed-tools: Read, Bash, Grep, Glob
---

# Database Optimizer Skill

Optimize PostgreSQL queries across NestJS (TypeORM/Prisma) and Python (Django ORM) services.

## When to Use
- API response times exceed the 50ms p95 target for database queries
- EXPLAIN ANALYZE shows sequential scans on large tables
- N+1 query patterns detected in ORM code
- Connection pool exhaustion under load

## EXPLAIN ANALYZE Patterns

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.id, u.name, COUNT(o.id) AS order_count
FROM users u LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2025-01-01'
GROUP BY u.id, u.name ORDER BY order_count DESC LIMIT 20;
```

**Red flags:** `Seq Scan` on 10k+ rows, `Nested Loop` with high row estimates, `Sort` with external disk merge, high `Rows Removed by Filter`.

## Index Strategy

```sql
-- B-tree: equality and range queries (default)
CREATE INDEX idx_orders_user_id ON orders (user_id);
CREATE INDEX idx_orders_user_status ON orders (user_id, status);  -- composite

-- Partial: filter subset of rows
CREATE INDEX idx_orders_active ON orders (user_id, created_at) WHERE status = 'active';

-- GIN: JSONB and full-text search
CREATE INDEX idx_metadata_gin ON documents USING GIN (metadata);
CREATE INDEX idx_docs_search ON documents USING GIN (to_tsvector('english', content));

-- GiST: geospatial
CREATE INDEX idx_locations_geo ON locations USING GiST (coordinates);
```

## N+1 Detection and Fixes

### Prisma (NestJS Core Service)
```typescript
// BAD: N+1
const users = await prisma.user.findMany();
for (const user of users) {
  const orders = await prisma.order.findMany({ where: { userId: user.id } });
}

// GOOD: eager load
const users = await prisma.user.findMany({
  include: { orders: true },
});
```

### TypeORM (NestJS Core Service)
```typescript
// BAD: lazy loading triggers N+1
const users = await userRepo.find();
users.forEach(u => console.log(u.orders));

// GOOD: explicit join
const users = await userRepo.createQueryBuilder('user')
  .leftJoinAndSelect('user.orders', 'order')
  .where('user.isActive = :active', { active: true })
  .getMany();
```

### Django ORM (AI Service)
```python
# BAD: N+1 on ForeignKey
tasks = Task.objects.all()
for task in tasks:
    print(task.user.name)

# GOOD: select_related for FK (single JOIN), prefetch_related for M2M
tasks = Task.objects.select_related('user').all()
users = User.objects.prefetch_related('tasks').all()
```

## Connection Pooling (PgBouncer)

```ini
[pgbouncer]
pool_mode = transaction
default_pool_size = 20
max_client_conn = 200
reserve_pool_size = 5
```

Point services at PgBouncer (port 6432), not PostgreSQL directly.

## Common Slow Query Fixes

| Problem | Fix |
|---------|-----|
| Seq Scan on large table | Add B-tree index on filter/join columns |
| `SELECT *` | Use `select` (Prisma) or `.only()` (Django) |
| No LIMIT | Always paginate; use cursor for deep pages |
| Leading wildcard LIKE '%x' | Use GIN trigram index or full-text search |
| Slow COUNT(*) | Use approximate count or cached counter |

## Anti-Patterns
- **Never add indexes blindly** -- verify need with EXPLAIN first
- **Never use OFFSET for deep pagination** -- use cursor-based pagination
- **Never run EXPLAIN without ANALYZE** -- estimated plans hide actual row counts
- **Never set pool_mode=session** with PgBouncer -- negates pooling benefits

## Checklist
- [ ] All queries under 50ms at p95 (verified with EXPLAIN ANALYZE)
- [ ] No N+1 patterns: ORM queries use eager loading or joins
- [ ] Composite indexes match WHERE clause column order
- [ ] Partial indexes used for filtered queries
- [ ] Connection pooling configured with transaction mode
- [ ] Pagination uses cursor-based approach for large datasets
- [ ] `SELECT *` replaced with explicit column selection in hot paths
