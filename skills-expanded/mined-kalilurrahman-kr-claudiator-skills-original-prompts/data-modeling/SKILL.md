---
name: data-modeling
description: Design data models for relational and NoSQL databases. Outputs entity relationships, normalization, denormalization strategies, and schema evolution.
argument-hint: [data domain, access patterns, consistency requirements]
allowed-tools: Read, Write, Bash
---

# Data Modeling

Design database schemas for applications. Not ad-hoc tables — normalized models, access pattern optimization, and schema evolution strategies.

## Process

1. **Understand domain.** Entities, relationships, business rules.
2. **Identify access patterns.** Read-heavy vs write-heavy, query types.
3. **Choose model type.** Relational (normalized), document (denormalized), graph, key-value.
4. **Design schema.** Tables/collections, relationships, indexes.
5. **Normalize/denormalize.** Balance redundancy vs query performance.
6. **Plan evolution.** Schema migrations, backward compatibility.
7. **Optimize for queries.** Indexes, materialized views, caching.

## Output Format

### Data Model: [Domain Name]

**Database:** PostgreSQL  
**Entities:** Users, Orders, Products, Payments  
**Relationships:** One-to-many (User→Orders), Many-to-many (Orders↔Products)  
**Normalization:** 3NF with selective denormalization  
**Indexes:** 12 (query optimization)

---

## Relational Model (SQL)

### Entity Relationship Diagram

```
┌─────────────┐
│    Users    │
├─────────────┤
│ id (PK)     │
│ email       │
│ name        │
│ created_at  │
└──────┬──────┘
       │ 1
       │
       │ N
┌──────▼──────┐
│   Orders    │
├─────────────┤
│ id (PK)     │
│ user_id (FK)│
│ total       │
│ status      │
│ created_at  │
└──────┬──────┘
       │ N
       │
       │ M
┌──────▼──────────┐      ┌─────────────┐
│  Order_Items    │  N   │  Products   │
├─────────────────┤──────├─────────────┤
│ id (PK)         │  M   │ id (PK)     │
│ order_id (FK)   │      │ name        │
│ product_id (FK) │      │ price       │
│ quantity        │      │ stock       │
│ price_at_time   │      │ created_at  │
└─────────────────┘      └─────────────┘
```

### DDL (PostgreSQL)

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    category_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    total DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price_at_time DECIMAL(10, 2) NOT NULL,  -- Snapshot of product price
    UNIQUE(order_id, product_id)  -- Can't add same product twice
);

-- Indexes for performance
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
```

---

## Normalization Forms

### 1NF (First Normal Form)
- Atomic values (no arrays/lists)
- Each column contains single value
- Each row unique

#### ❌ Not 1NF
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    products VARCHAR(255)  -- "123,456,789" BAD!
);
```

#### ✅ 1NF
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER
);

CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER
);
```

### 2NF (Second Normal Form)
- 1NF + No partial dependencies
- Non-key columns depend on entire primary key

#### ❌ Not 2NF
```sql
CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    product_name VARCHAR(255),  -- Depends only on product_id, not (order_id, product_id)
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);
```

#### ✅ 2NF
```sql
CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)  -- Moved to products table
);
```

### 3NF (Third Normal Form)
- 2NF + No transitive dependencies
- Non-key columns depend only on primary key

#### ❌ Not 3NF
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    city VARCHAR(255),
    country VARCHAR(255),  -- Depends on city (transitive)
    zipcode VARCHAR(10)    -- Depends on city (transitive)
);
```

#### ✅ 3NF
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    address_id INTEGER REFERENCES addresses(id)
);

CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    city VARCHAR(255),
    country VARCHAR(255),
    zipcode VARCHAR(10)
);
```

---

## Denormalization for Performance

### When to Denormalize

**Scenario:** Displaying order with user name requires JOIN

```sql
-- Normalized (JOIN required)
SELECT o.id, o.total, u.name
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.id = 123;
```

**Denormalized:**

```sql
ALTER TABLE orders ADD COLUMN user_name VARCHAR(255);

-- Query without JOIN (faster)
SELECT id, total, user_name
FROM orders
WHERE id = 123;
```

**Trade-off:**
- ✅ Faster reads (no JOIN)
- ❌ Slower writes (update user_name in orders when user changes name)
- ❌ Data redundancy

### Materialized View (Denormalization Alternative)

```sql
CREATE MATERIALIZED VIEW order_summary AS
SELECT 
    o.id,
    o.total,
    o.status,
    u.name AS user_name,
    u.email AS user_email,
    COUNT(oi.id) AS item_count
FROM orders o
JOIN users u ON o.user_id = u.id
LEFT JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, u.id;

-- Refresh periodically
REFRESH MATERIALIZED VIEW order_summary;

-- Query (fast)
SELECT * FROM order_summary WHERE id = 123;
```

---

## Document Model (NoSQL)

### MongoDB Schema

```javascript
// users collection
{
  _id: ObjectId("507f1f77bcf86cd799439011"),
  email: "user@example.com",
  name: "John Doe",
  created_at: ISODate("2024-03-21T10:00:00Z")
}

// orders collection (embedded items)
{
  _id: ObjectId("507f191e810c19729de860ea"),
  user: {
    id: ObjectId("507f1f77bcf86cd799439011"),
    name: "John Doe",  // Denormalized
    email: "user@example.com"
  },
  items: [
    {
      product_id: ObjectId("507f191e810c19729de860eb"),
      product_name: "Laptop",  // Denormalized
      quantity: 1,
      price: 999.99
    },
    {
      product_id: ObjectId("507f191e810c19729de860ec"),
      product_name: "Mouse",
      quantity: 2,
      price: 29.99
    }
  ],
  total: 1059.97,
  status: "completed",
  created_at: ISODate("2024-03-21T10:30:00Z")
}
```

**Advantages:**
- Single document fetch (no joins)
- Schema flexibility

**Disadvantages:**
- Data duplication (user name in every order)
- Update anomalies (user changes name)

---

## Access Pattern-Driven Design

### Example: Social Media App

**Access Patterns:**
1. Show user profile (read-heavy)
2. List user's posts (read-heavy)
3. Show post with comments (read-heavy)
4. Show home feed (read-heavy, complex)

### Option 1: Normalized (SQL)

```sql
CREATE TABLE users (id, name, bio);
CREATE TABLE posts (id, user_id, content, created_at);
CREATE TABLE comments (id, post_id, user_id, content);
CREATE TABLE follows (follower_id, followee_id);

-- Home feed query (complex, multiple JOINs)
SELECT p.*, u.name, COUNT(c.id) AS comment_count
FROM posts p
JOIN users u ON p.user_id = u.id
LEFT JOIN comments c ON p.id = c.post_id
WHERE p.user_id IN (
  SELECT followee_id FROM follows WHERE follower_id = 123
)
GROUP BY p.id
ORDER BY p.created_at DESC
LIMIT 20;
```

### Option 2: Denormalized (NoSQL)

```javascript
// Denormalized for feed performance
{
  _id: ObjectId("..."),
  author: {
    id: "user123",
    name: "John Doe",
    avatar: "https://..."
  },
  content: "Hello world!",
  comments_count: 42,
  likes_count: 100,
  created_at: ISODate("..."),
  
  // Embedded top comments
  top_comments: [
    {
      author: {id: "user456", name: "Jane"},
      content: "Great post!",
      created_at: ISODate("...")
    }
  ]
}
```

**Trade-off:**
- ✅ Feed loads fast (one query)
- ❌ Author name update requires updating all posts

---

## Schema Evolution

### Backward-Compatible Migrations

```sql
-- Add column with default (safe)
ALTER TABLE users ADD COLUMN phone VARCHAR(20) DEFAULT NULL;

-- Add NOT NULL column (unsafe, requires data)
-- Step 1: Add nullable
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT NULL;

-- Step 2: Backfill data
UPDATE users SET status = 'active' WHERE status IS NULL;

-- Step 3: Add NOT NULL constraint
ALTER TABLE users ALTER COLUMN status SET NOT NULL;
```

### Versioned Schema (API Evolution)

```javascript
// V1: Single name field
{
  id: 1,
  name: "John Doe",
  email: "john@example.com"
}

// V2: Split name into first/last
{
  id: 1,
  first_name: "John",
  last_name: "Doe",
  email: "john@example.com",
  
  // Keep old field for backward compat
  name: "John Doe"  // Computed from first_name + last_name
}
```

---

## Graph Model (Neo4j)

```cypher
// Create nodes
CREATE (u1:User {id: '1', name: 'Alice'})
CREATE (u2:User {id: '2', name: 'Bob'})
CREATE (p1:Product {id: '1', name: 'Laptop'})

// Create relationships
CREATE (u1)-[:FOLLOWS]->(u2)
CREATE (u1)-[:PURCHASED]->(p1)

// Query: Find friends who purchased same product
MATCH (me:User {id: '1'})-[:FOLLOWS]->(friend:User)
-[:PURCHASED]->(product:Product)<-[:PURCHASED]-(me)
RETURN friend.name, product.name
```

**Use cases:** Social networks, recommendation engines, fraud detection

---

## Time-Series Model

```sql
-- Wide table (one row per metric per hour)
CREATE TABLE metrics (
    timestamp TIMESTAMPTZ NOT NULL,
    server_id INTEGER NOT NULL,
    cpu_usage REAL,
    memory_usage REAL,
    disk_usage REAL,
    PRIMARY KEY (timestamp, server_id)
);

-- Partition by time (TimescaleDB)
SELECT create_hypertable('metrics', 'timestamp');

-- Efficient time-range queries
SELECT AVG(cpu_usage)
FROM metrics
WHERE timestamp >= NOW() - INTERVAL '24 hours'
  AND server_id = 123;
```

---

## Indexing Strategy

```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Covers query: WHERE user_id = X AND status = Y
-- Also covers: WHERE user_id = X
-- Does NOT cover: WHERE status = Y (status not first)

-- Partial index (smaller, faster)
CREATE INDEX idx_orders_pending ON orders(user_id)
WHERE status = 'pending';

-- Full-text search index
CREATE INDEX idx_products_search ON products
USING gin(to_tsvector('english', name || ' ' || description));
```

## Rules

- Normalize to 3NF first, denormalize for performance — start correct, optimize later.
- Access patterns drive schema design — optimize for most frequent queries.
- Foreign keys enforce referential integrity — prevents orphaned records.
- Index foreign keys always — joins on unindexed columns are slow.
- Composite indexes ordered by selectivity — most selective column first.
- Denormalize read-heavy data — user names, product titles in orders.
- Price snapshots for historical accuracy — store price_at_time in order_items.
- UUID for distributed systems — auto-increment IDs cause collisions in multi-region.
- Schema migrations backward compatible — add columns nullable, backfill, then add constraints.
- NoSQL for flexible schemas and horizontal scaling — SQL for complex queries and ACID transactions.
