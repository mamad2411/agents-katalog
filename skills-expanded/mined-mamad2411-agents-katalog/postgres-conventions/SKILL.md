---
name: postgres-conventions
description:
  This skill should be used when working on PostgreSQL databases, writing SQL schemas, creating
  tables, designing database architecture, or reviewing PostgreSQL code.
version: 0.1.0
---

# PostgreSQL Conventions

These are comprehensive conventions for PostgreSQL database development, covering schema design,
indexing strategies, data type selection, and query patterns. Following these conventions ensures
optimal performance, data integrity, and maintainability across PostgreSQL 15+ environments.

## Existing Repository Compatibility

When working with existing PostgreSQL databases and projects, always respect established conventions
and patterns before applying these preferences.

- **Audit before changing**: Review existing table definitions, data types, and index choices to
  understand the project's current state and historical decisions.
- **Serial column compatibility**: If the project uses `serial` / `bigserial` columns, understand
  they are legacy. Do not convert to identity columns without coordinating with the team, as it
  requires careful migration and may affect sequences used by application code.
- **Timezone handling**: If the project uses `timestamp` (without time zone), document the
  limitation but do not change without understanding how the application handles timezone
  conversions. Migration to `timestamptz` requires a table rewrite and application changes.
- **Collation consistency**: Mixed collations across columns can cause implicit conversions and
  prevent index usage. Document inconsistencies but plan migrations carefully.
- **Extension dependencies**: If the project relies on specific extension versions, coordinate
  upgrades with the team. Extension updates may change behavior or require data migration.
- **Backward compatibility**: When suggesting improvements, provide migration paths and rollback
  procedures for production systems.

**These conventions apply primarily to new schemas, new tables, and scaffold output. For existing
systems, propose changes through proper change management processes.**

## Schema Design Rules

### Naming Conventions

All identifiers must use lowercase `snake_case`. Never use quoted identifiers, camelCase,
PascalCase, or UPPERCASE names.

```sql
-- CORRECT: snake_case everywhere
CREATE TABLE user_accounts (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    email_address text NOT NULL UNIQUE,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

-- WRONG: camelCase (requires quoting, error-prone)
CREATE TABLE "userAccounts" (
    "firstName" text,
    "lastName" text,
    "emailAddress" text
);

-- WRONG: Mixed case without quotes (PostgreSQL folds to lowercase anyway)
CREATE TABLE UserAccounts (
    FirstName text  -- Becomes "firstname", not what you intended
);
```

### Table Naming Rules

- Use **plural nouns** for tables: `users`, `orders`, `products`
- Use **singular nouns** for enum/lookup tables: `order_status`, `priority`
- Use **verb_noun** for junction tables: `user_roles`, `order_items`
- Never prefix tables with `tbl_` or similar Hungarian notation

```sql
-- CORRECT: Plural table names
CREATE TABLE users (...);
CREATE TABLE orders (...);
CREATE TABLE order_items (...);

-- WRONG: Singular table names (inconsistent with SQL convention)
CREATE TABLE user (...);       -- Also a reserved word!
CREATE TABLE order (...);      -- Also a reserved word!
CREATE TABLE order_item (...);

-- WRONG: Hungarian notation
CREATE TABLE tbl_users (...);
CREATE TABLE t_orders (...);
```

### Constraint and Index Naming

Always name constraints and indexes explicitly using standard prefixes.

```sql
-- CORRECT: Named constraints with standard prefixes
CREATE TABLE orders (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id bigint NOT NULL,
    product_id bigint NOT NULL,
    quantity integer NOT NULL,
    unit_price numeric(15, 2) NOT NULL,
    total_amount numeric(15, 2) GENERATED ALWAYS AS (
        quantity * unit_price
    ) STORED,
    status text NOT NULL DEFAULT 'pending',
    created_at timestamptz NOT NULL DEFAULT now(),

    CONSTRAINT fk_orders_customer_id
        FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_orders_product_id
        FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT chk_orders_quantity_positive
        CHECK (quantity > 0),
    CONSTRAINT chk_orders_unit_price_positive
        CHECK (unit_price > 0),
    CONSTRAINT chk_orders_status_valid
        CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled'))
);

CREATE INDEX idx_orders_customer_id ON orders (customer_id);
CREATE INDEX idx_orders_product_id ON orders (product_id);
CREATE INDEX idx_orders_status ON orders (status) WHERE status != 'delivered';
CREATE UNIQUE INDEX uq_orders_customer_product ON orders (customer_id, product_id)
    WHERE status = 'pending';

-- WRONG: Unnamed constraints (auto-generated names are hard to reference)
CREATE TABLE orders (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id bigint REFERENCES customers(id),  -- Auto-named FK
    quantity integer CHECK (quantity > 0)           -- Auto-named CHECK
);

CREATE INDEX ON orders (customer_id);  -- Auto-named index
```

Naming prefix conventions:

| Prefix  | Usage                | Example                         |
| ------- | -------------------- | ------------------------------- |
| `pk_`   | Primary key          | `pk_orders`                     |
| `fk_`   | Foreign key          | `fk_orders_customer_id`         |
| `idx_`  | Index                | `idx_orders_customer_id`        |
| `uq_`   | Unique constraint    | `uq_users_email`                |
| `chk_`  | Check constraint     | `chk_orders_quantity_positive`  |
| `excl_` | Exclusion constraint | `excl_reservations_room_during` |
| `trg_`  | Trigger              | `trg_orders_updated_at`         |

### Timestamp Columns

Every mutable table should have `created_at` and `updated_at` columns.

```sql
-- CORRECT: Timestamp columns with defaults
CREATE TABLE orders (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- ... other columns ...
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

-- Auto-update updated_at with trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS trigger AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- WRONG: Missing timestamps
CREATE TABLE orders (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id bigint NOT NULL
    -- No created_at, no updated_at
);

-- WRONG: Using timestamp instead of timestamptz
CREATE TABLE orders (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at timestamp NOT NULL DEFAULT now()  -- Missing timezone!
);
```

## Data Type Rules

### Primary Keys: Identity Columns

Always use `bigint GENERATED ALWAYS AS IDENTITY` for primary keys. Never use `serial` or `bigserial`
(legacy syntax). Use `uuid` only when there is a specific need for distributed ID generation.

```sql
-- CORRECT: Identity column (PostgreSQL 10+, SQL standard)
CREATE TABLE users (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY
);

-- CORRECT: UUID primary key (for distributed systems)
CREATE TABLE distributed_events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid()
);

-- WRONG: serial (legacy, creates implicit sequence with different ownership)
CREATE TABLE users (
    id serial PRIMARY KEY
);

-- WRONG: bigserial (legacy)
CREATE TABLE users (
    id bigserial PRIMARY KEY
);

-- WRONG: integer identity (will overflow on high-traffic tables)
CREATE TABLE users (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY
    -- integer max: 2,147,483,647 -- seems large but high-traffic tables hit this
);
```

### Text Types: Always `text`

Use `text` for all string columns. Use `varchar(n)` only when you have a genuine business
requirement for maximum length enforcement. Never use `char(n)`.

```sql
-- CORRECT: text for all string columns
CREATE TABLE products (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    description text,
    sku text NOT NULL UNIQUE
);

-- CORRECT: varchar(n) when length limit is a business rule
CREATE TABLE countries (
    code varchar(3) PRIMARY KEY,  -- ISO 3166-1 alpha-3 code, always 3 chars
    name text NOT NULL
);

-- WRONG: varchar(255) cargo cult
CREATE TABLE products (
    name varchar(255) NOT NULL,        -- Why 255? No business reason.
    description varchar(1000)           -- Arbitrary limit
);

-- WRONG: char(n) (pads with spaces, wastes storage, confusing equality)
CREATE TABLE products (
    sku char(10) NOT NULL  -- Padded with spaces: 'ABC       '
);
```

### Numeric Types: `numeric` for Money

Never use `float`, `real`, or `double precision` for monetary values or any value requiring exact
decimal representation. Use `numeric(precision, scale)`.

```sql
-- CORRECT: numeric for money
CREATE TABLE line_items (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    quantity integer NOT NULL CHECK (quantity > 0),
    unit_price numeric(15, 2) NOT NULL CHECK (unit_price >= 0),
    tax_rate numeric(5, 4) NOT NULL DEFAULT 0.0000,
    total numeric(15, 2) GENERATED ALWAYS AS (
        quantity * unit_price * (1 + tax_rate)
    ) STORED
);

-- CORRECT: integer for cents (avoids decimal arithmetic entirely)
CREATE TABLE transactions (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    amount_cents bigint NOT NULL CHECK (amount_cents > 0),
    currency text NOT NULL DEFAULT 'USD'
);

-- WRONG: float for money (introduces rounding errors)
CREATE TABLE bad_line_items (
    unit_price float NOT NULL,    -- 0.1 + 0.2 != 0.3 in float
    total double precision        -- Same problem
);

-- WRONG: money type (locale-dependent, limited precision, poor portability)
CREATE TABLE bad_transactions (
    amount money NOT NULL  -- Don't use the money type
);
```

### Boolean Type

Use `boolean` for true/false values. Never use integer (0/1) or text ('Y'/'N').

```sql
-- CORRECT: boolean type
CREATE TABLE users (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    is_active boolean NOT NULL DEFAULT true,
    email_verified boolean NOT NULL DEFAULT false,
    is_admin boolean NOT NULL DEFAULT false
);

-- WRONG: integer for boolean
CREATE TABLE bad_users (
    is_active integer NOT NULL DEFAULT 1,   -- 0/1 is not boolean
    email_verified int DEFAULT 0             -- Allows values like 42
);

-- WRONG: text for boolean
CREATE TABLE bad_users (
    is_active text NOT NULL DEFAULT 'Y'  -- Allows 'Y', 'y', 'yes', 'YES', ...
);
```

### Timestamp Type: Always `timestamptz`

Use `timestamptz` (timestamp with time zone) for all temporal data. Never use `timestamp` (without
time zone) unless you have a specific reason (rare).

```sql
-- CORRECT: timestamptz for all time columns
CREATE TABLE events (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_time timestamptz NOT NULL DEFAULT now(),
    scheduled_at timestamptz,
    completed_at timestamptz
);

-- CORRECT: date for date-only values (no time component)
CREATE TABLE holidays (
    holiday_date date NOT NULL PRIMARY KEY,
    name text NOT NULL
);

-- WRONG: timestamp without time zone
CREATE TABLE bad_events (
    event_time timestamp NOT NULL DEFAULT now()
    -- Loses timezone information, ambiguous interpretation
);

-- WRONG: integer/bigint for Unix timestamps
CREATE TABLE bad_events (
    event_time bigint NOT NULL  -- Epoch seconds: loses readability, no timezone
);
```

### JSON Type: Always `jsonb`

Use `jsonb` for all JSON data. Never use `json` (stored as text, cannot be indexed efficiently,
slower for most operations).

```sql
-- CORRECT: jsonb for flexible metadata
CREATE TABLE products (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    attributes jsonb NOT NULL DEFAULT '{}',
    tags jsonb NOT NULL DEFAULT '[]'
);

-- Index specific jsonb paths
CREATE INDEX idx_products_category ON products USING btree ((attributes->>'category'));
CREATE INDEX idx_products_attributes ON products USING gin (attributes);
CREATE INDEX idx_products_tags ON products USING gin (tags jsonb_path_ops);

-- WRONG: json type (slower, cannot be indexed with GIN)
CREATE TABLE bad_products (
    attributes json NOT NULL DEFAULT '{}'
);

-- WRONG: Storing structured data as text
CREATE TABLE bad_products (
    attributes text  -- Requires manual JSON parsing
);
```

### Network Types

Use PostgreSQL's built-in network types for IP addresses and network ranges.

```sql
-- CORRECT: inet for IP addresses
CREATE TABLE access_log (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    client_ip inet NOT NULL,
    request_path text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

-- CORRECT: cidr for network ranges
CREATE TABLE allowed_networks (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    network cidr NOT NULL,
    description text
);

-- Query: Find log entries from a specific subnet
SELECT * FROM access_log
WHERE client_ip << '192.168.1.0/24'::cidr;

-- WRONG: text for IP addresses
CREATE TABLE bad_access_log (
    client_ip text NOT NULL  -- No validation, no subnet queries
);
```

### Array Types

Use PostgreSQL arrays for ordered lists of simple values. For complex collections, use a separate
table.

```sql
-- CORRECT: Array for simple tag lists
CREATE TABLE articles (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title text NOT NULL,
    tags text[] NOT NULL DEFAULT '{}',
    scores integer[] DEFAULT '{}'
);

-- GIN index for array contains queries
CREATE INDEX idx_articles_tags ON articles USING gin (tags);

-- Query: Articles with specific tag
SELECT * FROM articles WHERE tags @> ARRAY['postgresql'];

-- Query: Articles with any of these tags
SELECT * FROM articles WHERE tags && ARRAY['postgresql', 'database'];

-- WRONG: Comma-separated strings
CREATE TABLE bad_articles (
    tags text  -- 'postgresql,database,sql' -- Can't index or query efficiently
);

-- WRONG: Arrays for complex objects (use a join table instead)
CREATE TABLE bad_orders (
    item_names text[],  -- Loses item_id, price, quantity relationships
    item_prices numeric[]
);
```

## Index Rules

### B-tree (Default)

B-tree is the default index type. Use for equality and range queries on scalar types.

```sql
-- CORRECT: B-tree for equality and range
CREATE INDEX idx_orders_created_at ON orders (created_at);
CREATE INDEX idx_users_email ON users (email);

-- CORRECT: Composite index (column order matters!)
-- Supports: WHERE status = 'active' AND created_at > '2025-01-01'
-- Supports: WHERE status = 'active' (leftmost prefix)
-- Does NOT support: WHERE created_at > '2025-01-01' alone (efficiently)
CREATE INDEX idx_orders_status_created ON orders (status, created_at);

-- CORRECT: Covering index (INCLUDE columns stored in leaf pages, PG 11+)
CREATE INDEX idx_orders_status_covering ON orders (status)
    INCLUDE (customer_id, total_amount);
-- Index-only scan: no heap fetches for covered columns
```

### Partial Indexes

Create indexes that cover only a subset of rows. Dramatically smaller and faster for targeted
queries.

```sql
-- CORRECT: Partial index for active records only
CREATE INDEX idx_orders_pending ON orders (created_at)
    WHERE status = 'pending';

-- CORRECT: Partial index for non-null values
CREATE INDEX idx_users_phone ON users (phone)
    WHERE phone IS NOT NULL;

-- CORRECT: Partial unique index (unique only within a subset)
CREATE UNIQUE INDEX uq_users_active_email ON users (email)
    WHERE deleted_at IS NULL;

-- Query that benefits from partial index
SELECT * FROM orders WHERE status = 'pending' ORDER BY created_at;
-- Uses idx_orders_pending (much smaller than full index)
```

### Expression Indexes

Index computed expressions for queries that filter on transformations.

```sql
-- CORRECT: Expression index for case-insensitive search
CREATE INDEX idx_users_email_lower ON users (lower(email));

-- Query that uses it
SELECT * FROM users WHERE lower(email) = lower('User@Example.com');

-- CORRECT: Expression index on jsonb path
CREATE INDEX idx_products_category ON products ((attributes->>'category'));

-- CORRECT: Expression index for date extraction
CREATE INDEX idx_orders_year_month ON orders (
    date_trunc('month', created_at)
);
```

### GIN Indexes

GIN (Generalized Inverted Index) is optimal for multi-valued types: arrays, jsonb, full-text search,
and trigram matching.

```sql
-- CORRECT: GIN for jsonb containment
CREATE INDEX idx_products_attributes ON products USING gin (attributes);
-- Supports: WHERE attributes @> '{"color": "red"}'

-- CORRECT: GIN with jsonb_path_ops (smaller, supports @> only)
CREATE INDEX idx_products_attrs_path ON products
    USING gin (attributes jsonb_path_ops);

-- CORRECT: GIN for array containment
CREATE INDEX idx_articles_tags ON articles USING gin (tags);
-- Supports: WHERE tags @> ARRAY['postgresql']

-- CORRECT: GIN for full-text search
CREATE INDEX idx_articles_search ON articles USING gin (search_vector);
-- Supports: WHERE search_vector @@ to_tsquery('postgresql & database')
```

### GiST Indexes

GiST (Generalized Search Tree) supports spatial data, range types, and nearest-neighbor queries.

```sql
-- CORRECT: GiST for range types
CREATE INDEX idx_reservations_during ON reservations USING gist (during);
-- Supports: WHERE during && '[2025-03-01, 2025-03-05)'::tstzrange

-- CORRECT: GiST for spatial data (PostGIS)
CREATE INDEX idx_locations_coords ON locations USING gist (coords);

-- CORRECT: GiST for exclusion constraints
ALTER TABLE reservations ADD CONSTRAINT excl_reservations_room_during
    EXCLUDE USING gist (room_id WITH =, during WITH &&);
```

### BRIN Indexes

BRIN (Block Range Index) is extremely compact and efficient for naturally ordered data (e.g.,
time-series, append-only logs). Tiny index size but only useful when physical row order correlates
with column values.

```sql
-- CORRECT: BRIN for time-series data (naturally ordered by insert time)
CREATE INDEX idx_events_created_brin ON events
    USING brin (created_at) WITH (pages_per_range = 32);

-- CORRECT: BRIN for append-only log tables
CREATE INDEX idx_audit_log_id_brin ON audit_log
    USING brin (id) WITH (pages_per_range = 64);

-- WRONG: BRIN on randomly-ordered column (poor correlation, useless index)
CREATE INDEX idx_users_email_brin ON users USING brin (email);
```

### Hash Indexes

Hash indexes support only equality comparisons. Useful for large values where B-tree overhead is
significant. PostgreSQL 10+ makes hash indexes WAL-logged and crash-safe.

```sql
-- CORRECT: Hash index for equality-only lookups on large values
CREATE INDEX idx_sessions_token_hash ON sessions USING hash (session_token);
-- Only supports: WHERE session_token = 'abc123...'

-- B-tree is almost always better unless the indexed values are very large
-- and you only ever do equality checks
```

## Query Pattern Rules

### Common Table Expressions (CTEs)

PostgreSQL 12+ does not fence CTEs by default (they may be inlined). Use `MATERIALIZED` or
`NOT MATERIALIZED` hints when you need explicit control.

```sql
-- CORRECT: Let the optimizer decide (PostgreSQL 12+ default)
WITH active_users AS (
    SELECT id, email FROM users WHERE is_active = true
)
SELECT au.email, count(o.id) AS order_count
FROM active_users au
JOIN orders o ON o.user_id = au.id
GROUP BY au.email;

-- CORRECT: Force materialization (when CTE is referenced multiple times)
WITH MATERIALIZED user_stats AS (
    SELECT user_id, count(*) AS order_count, sum(total) AS total_spent
    FROM orders
    GROUP BY user_id
)
SELECT * FROM user_stats WHERE order_count > 10
UNION ALL
SELECT * FROM user_stats WHERE total_spent > 1000;

-- CORRECT: Prevent materialization (when optimizer doesn't push predicates)
WITH NOT MATERIALIZED recent_orders AS (
    SELECT * FROM orders WHERE created_at > now() - interval '30 days'
)
SELECT * FROM recent_orders WHERE customer_id = 42;
-- Predicate on customer_id is pushed into the CTE scan
```

### Pagination

Use keyset pagination for consistent performance on large datasets. Avoid OFFSET for deep
pagination.

```sql
-- CORRECT: Keyset pagination (constant performance regardless of page depth)
SELECT id, name, created_at
FROM products
WHERE (created_at, id) < ($last_created_at, $last_id)
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- WRONG: OFFSET pagination (scans and discards rows, slower for deep pages)
SELECT id, name, created_at
FROM products
ORDER BY created_at DESC
OFFSET 10000 LIMIT 20;
-- Must scan 10020 rows and discard 10000
```

### Bulk Operations

Use batch operations for large data modifications. Never update millions of rows in a single
transaction.

```sql
-- CORRECT: Batch update with controlled transaction size
DO $$
DECLARE
    batch_size constant integer := 5000;
    rows_affected integer;
BEGIN
    LOOP
        UPDATE users
        SET status = 'inactive'
        WHERE id IN (
            SELECT id FROM users
            WHERE last_login_at < now() - interval '1 year'
              AND status = 'active'
            LIMIT batch_size
            FOR UPDATE SKIP LOCKED
        );
        GET DIAGNOSTICS rows_affected = ROW_COUNT;
        RAISE NOTICE 'Updated % rows', rows_affected;
        COMMIT;
        EXIT WHEN rows_affected < batch_size;
        PERFORM pg_sleep(0.1);  -- Brief pause to reduce lock contention
    END LOOP;
END $$;

-- WRONG: Single massive UPDATE (locks entire table, bloats WAL, blocks VACUUM)
UPDATE users SET status = 'inactive'
WHERE last_login_at < now() - interval '1 year';
```

### UPSERT Pattern

Use `INSERT ... ON CONFLICT` for atomic upsert operations.

```sql
-- CORRECT: Upsert with ON CONFLICT
INSERT INTO product_inventory (product_id, warehouse_id, quantity, updated_at)
VALUES ($1, $2, $3, now())
ON CONFLICT (product_id, warehouse_id)
DO UPDATE SET
    quantity = EXCLUDED.quantity,
    updated_at = EXCLUDED.updated_at;

-- CORRECT: Upsert with DO NOTHING (ignore duplicates)
INSERT INTO user_logins (user_id, login_date)
VALUES ($1, current_date)
ON CONFLICT (user_id, login_date) DO NOTHING;

-- WRONG: Check-then-insert (race condition)
-- SELECT count(*) FROM products WHERE sku = $1;
-- IF count = 0 THEN INSERT ... END IF;
-- Another session can insert between SELECT and INSERT
```

### Window Functions

Use window functions for ranking, running totals, and row comparisons without self-joins.

```sql
-- CORRECT: Running total with window function
SELECT order_date,
       amount,
       sum(amount) OVER (ORDER BY order_date) AS running_total,
       avg(amount) OVER (
           ORDER BY order_date
           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ) AS moving_avg_7d
FROM daily_revenue;

-- CORRECT: Row numbering for deduplication
DELETE FROM users
WHERE id IN (
    SELECT id FROM (
        SELECT id, ROW_NUMBER() OVER (
            PARTITION BY email ORDER BY created_at DESC
        ) AS rn
        FROM users
    ) dupes
    WHERE rn > 1
);
```

## Anti-Pattern Summary

| Anti-Pattern           | Correct Approach                             |
| ---------------------- | -------------------------------------------- |
| `serial` / `bigserial` | `bigint GENERATED ALWAYS AS IDENTITY`        |
| `varchar(255)`         | `text`                                       |
| `float` for money      | `numeric(p, s)`                              |
| `timestamp`            | `timestamptz`                                |
| `json`                 | `jsonb`                                      |
| `integer` for boolean  | `boolean`                                    |
| `char(n)`              | `text`                                       |
| Unnamed constraints    | `fk_`, `idx_`, `chk_`, `uq_` prefixes        |
| OFFSET pagination      | Keyset pagination                            |
| Single massive UPDATE  | Batched updates with LIMIT                   |
| EAV tables             | `jsonb` columns or proper normalization      |
| Polymorphic FK         | Separate nullable FKs with CHECK             |
| Missing `created_at`   | Always include `created_at` and `updated_at` |
| camelCase identifiers  | `snake_case` identifiers                     |
