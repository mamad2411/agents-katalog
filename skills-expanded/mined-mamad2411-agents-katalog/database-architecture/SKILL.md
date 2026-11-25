---
name: database-architecture
description: |
  Database design, modeling, indexing, and query optimization standards. Apply when designing
  schemas, writing migrations, optimizing slow queries, or planning data architecture.
  Covers PostgreSQL patterns, indexing strategy, partitioning, full-text search, and Redis usage.
---

# Database Architecture Standards

## Schema Design Principles

### Base Model (All Tables)
```python
# Django
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        abstract = True
```

### Naming Conventions
```sql
-- Tables: snake_case plural
users, order_items, product_categories

-- Columns: snake_case
user_id, created_at, is_active, deleted_at

-- Indexes: idx_{table}_{columns}
idx_orders_user_id_status
idx_products_category_id_price

-- Foreign keys: fk_{from_table}_{to_table}
fk_orders_users
```

## Indexing Strategy

### When to Index
```sql
-- Always index:
-- 1. Primary keys (automatic)
-- 2. Foreign keys
-- 3. Fields in WHERE clauses
-- 4. Fields in ORDER BY
-- 5. Fields in JOIN conditions
-- 6. Fields in GROUP BY

-- Composite index: most selective (higher cardinality) column first
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
-- Good for: WHERE user_id = ? AND status = ?
-- Also good for: WHERE user_id = ?  (leftmost prefix rule)
-- NOT good for: WHERE status = ?  (no leftmost prefix)

-- Partial index: index only relevant rows (saves space, faster)
CREATE INDEX idx_orders_pending ON orders(created_at) WHERE status = 'pending';
```

### Query Optimization Checklist
```sql
-- Always EXPLAIN ANALYZE before shipping a query
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;

-- Red flags in EXPLAIN output:
-- Seq Scan on large table → needs index
-- Nested Loop with large row estimates → consider JOIN order
-- Sort with high cost → consider index on ORDER BY column
-- Rows Removed by Filter high → index selectivity issue
```

## PostgreSQL Patterns

### Full-Text Search (Built-in)
```python
# Django
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

def search_products(query: str):
    search_vector = SearchVector('name', weight='A') + SearchVector('description', weight='B')
    search_query = SearchQuery(query, search_type='websearch')
    return Product.objects.annotate(
        rank=SearchRank(search_vector, search_query)
    ).filter(rank__gte=0.1).order_by('-rank')
```

### JSONB for Flexible Attributes
```python
# Use JSONB for truly flexible data, not to avoid schema design
class Product(BaseModel):
    name = models.CharField(max_length=200)
    attributes = models.JSONField(default=dict)  # {"color": "red", "size": "XL"}

# Index JSONB fields that are frequently queried
CREATE INDEX idx_products_color ON products USING gin((attributes->'color'));
```

### Row-Level Security
```sql
-- Enable for multi-tenant apps
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY orders_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

## Redis Patterns

### Cache Keys (Consistent naming)
```python
CACHE_KEYS = {
    "user_profile": "user:{user_id}:profile",
    "product_detail": "product:{product_id}:detail",
    "user_cart": "user:{user_id}:cart",
    "rate_limit": "ratelimit:{ip}:{endpoint}",
    "session": "session:{session_id}",
}

# TTL strategy
TTL = {
    "user_profile": 300,      # 5 min — changes infrequently
    "product_detail": 3600,   # 1 hr — changes on admin action
    "rate_limit": 60,         # 1 min — sliding window
    "session": 86400 * 7,     # 7 days — with refresh
}
```

### Cache Invalidation
```python
def update_product(product_id: str, data: dict):
    product = Product.objects.get(id=product_id)
    product.update(**data)
    # Invalidate immediately after write
    cache.delete(f"product:{product_id}:detail")
    cache.delete_pattern(f"product_list:*")  # Invalidate all list caches
```

## Migration Best Practices
```python
# Every migration: descriptive name, reversible, tested
# 0015_add_soft_delete_to_orders.py

# For large tables: avoid locking operations in single migration
# Split into:
# Step 1: Add column nullable (non-blocking)
# Step 2: Backfill data in batches
# Step 3: Add NOT NULL constraint (after backfill complete)

def backfill_in_batches(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    batch_size = 1000
    orders = Order.objects.filter(deleted_at__isnull=True)
    for i in range(0, orders.count(), batch_size):
        batch = orders[i:i + batch_size]
        Order.objects.bulk_update(batch, ['deleted_at'])
```
