---
name: database-optimization-pro
description: Database performance optimization — indexes, query tuning, connection pooling, partitioning
triggers: [database optimization, SQL optimization, indexes, query performance, connection pool]
---

# SKILL: Database Optimization Pro

## Indexing Strategies

```sql
-- ❌ Slow: Full table scan
SELECT * FROM users WHERE email = 'user@example.com';

-- ✅ Fast: Index on email
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Good for: WHERE user_id = ? AND created_at > ?
-- Bad for: WHERE created_at > ? (doesn't use index)

-- Partial index (smaller, faster)
CREATE INDEX idx_active_users ON users(id) WHERE status = 'active';
```

## Query Optimization

```sql
-- ❌ SELECT * (fetches unnecessary data)
SELECT * FROM users WHERE id = 1;

-- ✅ Select only needed columns
SELECT id, name, email FROM users WHERE id = 1;

-- ❌ N+1 query problem
SELECT * FROM posts;
-- Then for each post:
SELECT * FROM users WHERE id = post.author_id;

-- ✅ JOIN (1 query instead of N+1)
SELECT posts.*, users.name 
FROM posts 
JOIN users ON posts.author_id = users.id;

-- Use EXPLAIN to analyze
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
```

## Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Connection pool (reuse connections)
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    poolclass=QueuePool,
    pool_size=20,        # Normal connections
    max_overflow=10,     # Extra connections under load
    pool_timeout=30,     # Wait time for connection
    pool_recycle=3600    # Recycle connections after 1 hour
)
```

## Partitioning

```sql
-- Partition large table by date
CREATE TABLE orders (
    id SERIAL,
    user_id INT,
    created_at DATE,
    total DECIMAL
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Queries automatically use correct partition
SELECT * FROM orders WHERE created_at >= '2024-02-01';
```

## Quality Checks
- [ ] Indexes on frequently queried columns
- [ ] Query execution plans analyzed (EXPLAIN)
- [ ] Connection pooling configured
- [ ] N+1 queries eliminated
- [ ] Slow query log enabled
- [ ] Database monitoring (query times)
- [ ] Partitioning for large tables
- [ ] Regular VACUUM/ANALYZE (Postgres)
