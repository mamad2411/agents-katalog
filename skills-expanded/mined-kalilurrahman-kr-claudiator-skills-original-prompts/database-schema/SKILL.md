---
name: database-schema
description: Design a normalized database schema with tables, relationships, indexes, and constraints. Outputs SQL DDL and ER diagram description.
argument-hint: [data requirements and relationships]
allowed-tools: Read, Write, Bash
---

# Database Schema Design

Design a production-ready database schema from data requirements. Every table, column, constraint, and index must be specified with enough detail to create the database and support expected queries.

## Process

1. **Identify entities.** Parse requirements to extract core business objects.
2. **Define relationships.** One-to-many, many-to-many, one-to-one.
3. **Normalize to 3NF.** Eliminate redundancy unless denormalization is justified.
4. **Choose data types.** Match business requirements (VARCHAR vs TEXT, INT vs BIGINT, TIMESTAMP vs DATE).
5. **Add constraints.** Primary keys, foreign keys, unique constraints, check constraints, NOT NULL.
6. **Design indexes.** Based on expected query patterns (WHERE, JOIN, ORDER BY clauses).
7. **Plan partitioning.** If scale requires it (time-based, hash-based).
8. **Document migrations.** How to evolve schema without downtime.
9. **Generate SQL DDL.** PostgreSQL syntax by default, flag if other RDBMS needed.

## Output Format

### Schema Overview
- **Database:** PostgreSQL 15+
- **Total Tables:** 8
- **Normalization:** 3NF with denormalization for read-heavy tables
- **Partitioning:** Time-based on events table

### Entity Relationship Summary
```
User (1) ----< (N) Order
Order (1) ----< (N) OrderItem
Product (1) ----< (N) OrderItem
User (1) ----< (N) Address
```

### Tables

#### users
**Purpose:** Core user accounts

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | User identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email (login) |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt hash |
| name | VARCHAR(100) | NOT NULL | Display name |
| status | VARCHAR(20) | NOT NULL, CHECK | active, suspended, deleted |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Account creation |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last modification |

**Indexes:**
- `idx_users_email` — UNIQUE (email) — Login lookups
- `idx_users_status` — (status) — Active user queries
- `idx_users_created` — (created_at DESC) — Recent signups

**SQL DDL:**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active' 
        CHECK (status IN ('active', 'suspended', 'deleted')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status) WHERE status = 'active';
CREATE INDEX idx_users_created ON users(created_at DESC);
```

#### orders
**Purpose:** Purchase orders

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BIGSERIAL | PRIMARY KEY | Order ID |
| user_id | UUID | FOREIGN KEY, NOT NULL | References users(id) |
| status | VARCHAR(20) | NOT NULL, CHECK | pending, paid, shipped, cancelled |
| total_amount | DECIMAL(10,2) | NOT NULL, CHECK >= 0 | Total order value |
| currency | CHAR(3) | NOT NULL, DEFAULT 'USD' | ISO 4217 code |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Order placed |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last status change |

**Indexes:**
- `idx_orders_user_created` — (user_id, created_at DESC) — User order history
- `idx_orders_status` — (status) WHERE status IN ('pending', 'paid') — Active orders

**SQL DDL:**
```sql
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'paid', 'shipped', 'cancelled')),
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    currency CHAR(3) NOT NULL DEFAULT 'USD',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);
CREATE INDEX idx_orders_status ON orders(status) 
    WHERE status IN ('pending', 'paid');
```

#### products
**Purpose:** Product catalog

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BIGSERIAL | PRIMARY KEY | Product ID |
| sku | VARCHAR(50) | UNIQUE, NOT NULL | Stock keeping unit |
| name | VARCHAR(200) | NOT NULL | Product name |
| description | TEXT | NULL | Product description |
| price | DECIMAL(10,2) | NOT NULL, CHECK > 0 | Current price |
| stock | INT | NOT NULL, DEFAULT 0, CHECK >= 0 | Available inventory |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | In catalog |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Added to catalog |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last modified |

**Indexes:**
- `idx_products_sku` — UNIQUE (sku) — SKU lookups
- `idx_products_active` — (is_active) WHERE is_active = TRUE — Active products only

**SQL DDL:**
```sql
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_active ON products(is_active) WHERE is_active = TRUE;
```

#### order_items
**Purpose:** Line items in orders (many-to-many resolver)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BIGSERIAL | PRIMARY KEY | Line item ID |
| order_id | BIGINT | FOREIGN KEY, NOT NULL | References orders(id) |
| product_id | BIGINT | FOREIGN KEY, NOT NULL | References products(id) |
| quantity | INT | NOT NULL, CHECK > 0 | Items ordered |
| unit_price | DECIMAL(10,2) | NOT NULL, CHECK > 0 | Price at time of order |
| subtotal | DECIMAL(10,2) | NOT NULL, CHECK >= 0 | quantity * unit_price |

**Indexes:**
- `idx_order_items_order` — (order_id) — Fetch order details
- `idx_order_items_product` — (product_id) — Product sales analytics

**SQL DDL:**
```sql
CREATE TABLE order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price > 0),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0)
);

CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
```

### Migration Strategy

**Adding new column (backward compatible):**
```sql
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
```

**Changing column type (requires downtime or dual-write):**
1. Add new column: `ALTER TABLE users ADD COLUMN email_new TEXT;`
2. Backfill data: `UPDATE users SET email_new = email;`
3. Switch application to use new column
4. Drop old column: `ALTER TABLE users DROP COLUMN email;`
5. Rename: `ALTER TABLE users RENAME COLUMN email_new TO email;`

**Adding foreign key to existing table:**
```sql
-- Add column first
ALTER TABLE orders ADD COLUMN shipping_address_id BIGINT;
-- Backfill data
UPDATE orders SET shipping_address_id = ...;
-- Add constraint
ALTER TABLE orders ADD CONSTRAINT fk_shipping_address 
    FOREIGN KEY (shipping_address_id) REFERENCES addresses(id);
```

## Rules

- Always use UUID for user-facing IDs (non-sequential, harder to enumerate).
- Use BIGSERIAL for internal IDs when UUID overhead is too high.
- Every table must have `created_at` and `updated_at` timestamps.
- Foreign keys must specify ON DELETE behavior (CASCADE, RESTRICT, SET NULL).
- Add CHECK constraints for enum-like columns (status, type, etc.).
- Indexes are mandatory for foreign keys and WHERE clause columns.
- Use DECIMAL for money, never FLOAT or DOUBLE.
- Timestamps must include timezone (TIMESTAMPTZ in PostgreSQL).
- If requirements mention "millions of rows", add partitioning strategy.
- Document why denormalization is used if schema is not 3NF.
- Generate full SQL DDL that can be executed to create schema.
