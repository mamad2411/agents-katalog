---
name: sqlite-conventions
description:
  This skill should be used when working on SQLite databases, writing SQL schemas, configuring
  PRAGMAs, using FTS5, or designing embedded database schemas.
version: 0.1.0
---

# SQLite Conventions

These are comprehensive conventions for SQLite database development, covering PRAGMA configuration,
type affinity, STRICT tables, schema design, and SQLite-specific features. Following these
conventions ensures optimal performance, data integrity, and portability across SQLite 3.40+
environments.

## Existing Repository Compatibility

When working with existing SQLite databases and projects, always respect established conventions and
patterns before applying these preferences.

- **Audit before changing**: Review existing PRAGMA configuration, table definitions, and migration
  patterns to understand the project's current state and historical decisions.
- **WAL mode caution**: If the project doesn't use WAL mode, understand why before enabling it. Some
  embedded platforms have constraints (network filesystems, specific OS requirements).
- **STRICT tables**: If existing tables don't use STRICT, don't add STRICT to new related tables
  without understanding the implications. Mixed STRICT/non-STRICT tables in the same database are
  valid but may confuse developers.
- **AUTOINCREMENT usage**: If the project uses AUTOINCREMENT consistently, follow that pattern for
  new tables even though plain INTEGER PRIMARY KEY is usually sufficient.
- **Date format**: If the project stores dates as Unix timestamps (INTEGER), continue that pattern
  for consistency. ISO-8601 TEXT is preferred for new projects but consistency within a project is
  more important.
- **Backward compatibility**: When suggesting improvements, provide migration paths and ensure
  changes don't break existing application code. SQLite schema changes are particularly impactful
  because ALTER TABLE support is limited.

## PRAGMA Configuration

PRAGMAs configure SQLite behavior. Some are per-database (persisted), most are per-connection (must
be set on every new connection).

### Required PRAGMAs (Set on Every Connection)

```sql
-- CORRECT: Complete per-connection PRAGMA setup
PRAGMA journal_mode = WAL;          -- Per-database, persisted after first set
PRAGMA foreign_keys = ON;           -- Per-connection, OFF by default
PRAGMA busy_timeout = 5000;         -- Per-connection, 0ms by default
PRAGMA synchronous = NORMAL;        -- Per-connection, FULL by default (safe with WAL)
PRAGMA cache_size = -64000;         -- Per-connection, negative = KB (64MB)
PRAGMA journal_size_limit = 67108864; -- Per-database, limit WAL growth (64MB)
PRAGMA temp_store = MEMORY;         -- Per-connection, use memory for temp tables
```

```sql
-- WRONG: Opening connection without PRAGMAs
-- Defaults: DELETE journal mode, foreign_keys OFF, busy_timeout 0,
-- synchronous FULL, small cache. Every default is suboptimal.
```

### Per-Database vs Per-Connection

**Per-database** (persisted, set once):

- `journal_mode`: WAL vs DELETE. Once set to WAL, persists until changed.
- `page_size`: Set before first table creation. Cannot change without VACUUM.
- `auto_vacuum`: FULL, INCREMENTAL, or NONE. Set before first table.
- `journal_size_limit`: Limits WAL file growth.

**Per-connection** (must set on every new connection):

- `foreign_keys`: OFF by default — always set to ON.
- `busy_timeout`: 0 by default — always set to at least 5000ms.
- `synchronous`: FULL by default — NORMAL is safe with WAL and faster.
- `cache_size`: Varies — increase for read-heavy workloads.
- `temp_store`: DEFAULT (file) — MEMORY is faster.

### WAL Mode

WAL (Write-Ahead Logging) is essential for concurrent access:

- Multiple readers can operate simultaneously without blocking.
- One writer can operate without blocking readers.
- Writes go to a WAL file and are periodically checkpointed to the main database.
- Requires local filesystem — does **not** work on network filesystems (NFS, SMB, CIFS).

```sql
-- CORRECT: Enable WAL mode
PRAGMA journal_mode = WAL;

-- CORRECT: Manual checkpoint (rarely needed — auto-checkpoint handles this)
PRAGMA wal_checkpoint(PASSIVE);    -- Non-blocking checkpoint
PRAGMA wal_checkpoint(TRUNCATE);   -- Checkpoint and reset WAL file
```

```sql
-- WRONG: Using DELETE journal mode for concurrent access
PRAGMA journal_mode = DELETE;
-- DELETE mode blocks all readers during writes and is significantly slower
-- for concurrent workloads. Only use for single-connection scenarios or
-- network filesystem constraints.
```

### Foreign Keys

```sql
-- CORRECT: Always enable foreign key enforcement
PRAGMA foreign_keys = ON;

-- Verify it's enabled
PRAGMA foreign_keys;  -- Should return 1

-- Check for existing violations
PRAGMA foreign_key_check;
```

```sql
-- WRONG: Relying on default (OFF)
-- SQLite defaults to foreign_keys = OFF for backwards compatibility.
-- Without this PRAGMA, foreign key constraints are parsed but NOT enforced.
-- This means invalid references will be silently accepted.
```

## Type Affinity Rules

SQLite uses type affinity rather than strict typing. Any column can store any type unless STRICT is
used.

### The Five Affinities

| Affinity | Stores as           | Column Type Keywords            |
| -------- | ------------------- | ------------------------------- |
| TEXT     | Text string         | CHAR, CLOB, TEXT, VARCHAR       |
| NUMERIC  | Integer, real, text | NUMERIC, DECIMAL, BOOLEAN, DATE |
| INTEGER  | Integer             | INT, INTEGER, TINYINT, BIGINT   |
| REAL     | Floating point      | REAL, DOUBLE, FLOAT             |
| BLOB     | Raw bytes           | BLOB, or no type specified      |

### STRICT Tables (SQLite 3.37+)

STRICT tables enforce column types at insertion time. Allowed types: INTEGER, REAL, TEXT, BLOB, ANY.

```sql
-- CORRECT: STRICT table with enforced types
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    total_cents INTEGER NOT NULL CHECK (total_cents >= 0),
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
) STRICT;
```

```sql
-- WRONG: Non-STRICT table where type safety matters
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    total_cents INTEGER,  -- Without STRICT, text '100' would be stored as text
    customer_id INTEGER   -- '42' (text) would be stored without conversion
);
-- INSERT INTO orders VALUES (1, 'not a number', 'not an id');
-- This succeeds silently in non-STRICT mode!
```

**When to use STRICT**:

- All new tables in new projects (default choice)
- Tables with numeric columns where type safety matters
- Tables in applications where data integrity is critical

**When STRICT may not be appropriate**:

- Legacy databases where existing data may have mixed types
- Tables that need type flexibility (rare)
- Target environments with SQLite < 3.37

### Date and Time Storage

SQLite has no native date/time type. Use TEXT in ISO-8601 format:

```sql
-- CORRECT: ISO-8601 text dates
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    event_date TEXT NOT NULL,           -- '2024-03-15'
    starts_at TEXT NOT NULL,            -- '2024-03-15T09:00:00.000Z'
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
) STRICT;

-- Date arithmetic using SQLite date functions
SELECT title FROM events
WHERE date(event_date) BETWEEN date('now') AND date('now', '+7 days');

-- Formatting
SELECT title, strftime('%Y-%m-%d %H:%M', starts_at) AS formatted
FROM events;
```

```sql
-- WRONG: Unix timestamps
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    event_date INTEGER  -- 1710460800 — not human-readable, harder to debug
);
-- Unix timestamps work but are harder to read in queries, require conversion
-- for display, and don't sort naturally as text. ISO-8601 TEXT is preferred.
```

```sql
-- WRONG: Non-standard date formats
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    event_date TEXT  -- '03/15/2024' — ambiguous (US) or '15/03/2024' (EU)
);
-- Non-ISO formats are ambiguous, don't sort correctly, and don't work with
-- SQLite date functions. Always use ISO-8601.
```

### Boolean Storage

```sql
-- CORRECT: INTEGER booleans with CHECK constraint
CREATE TABLE features (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    is_enabled INTEGER NOT NULL DEFAULT 0 CHECK (is_enabled IN (0, 1))
) STRICT;

-- Query with boolean logic
SELECT name FROM features WHERE is_enabled = 1;
SELECT name FROM features WHERE NOT is_enabled;  -- SQLite treats 0 as false
```

```sql
-- WRONG: TEXT booleans
CREATE TABLE features (
    id INTEGER PRIMARY KEY,
    name TEXT,
    is_enabled TEXT  -- 'true'/'false', 'yes'/'no' — inconsistent, no type safety
);
```

### UUID Storage

```sql
-- CORRECT: TEXT UUID (human-readable, debuggable)
CREATE TABLE resources (
    id TEXT PRIMARY KEY NOT NULL CHECK (
        length(id) = 36 AND
        id GLOB '????????-????-????-????-????????????'
    ),
    name TEXT NOT NULL
) STRICT;

-- CORRECT: BLOB UUID (compact, 16 bytes)
CREATE TABLE resources (
    id BLOB PRIMARY KEY NOT NULL CHECK (length(id) = 16),
    name TEXT NOT NULL
) STRICT;
```

**Choose TEXT when**: Debugging and readability matter, IDs are logged or displayed. **Choose BLOB
when**: Storage efficiency matters, large tables, IDs are opaque.

### Money and Decimal Values

```sql
-- CORRECT: INTEGER cents for monetary values
CREATE TABLE line_items (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0),
    total_cents INTEGER GENERATED ALWAYS AS (quantity * unit_price_cents) STORED
) STRICT;

-- Display as dollars in application code: total_cents / 100.0
```

```sql
-- WRONG: REAL for money
CREATE TABLE line_items (
    id INTEGER PRIMARY KEY,
    price REAL  -- 19.99 + 0.01 might equal 20.000000000000004
);
-- IEEE 754 floating point cannot exactly represent most decimal fractions.
-- Use INTEGER cents or store as TEXT with application-level parsing.
```

## Primary Key Patterns

### INTEGER PRIMARY KEY (Preferred)

```sql
-- CORRECT: INTEGER PRIMARY KEY (rowid alias, auto-increments)
CREATE TABLE items (
    id INTEGER PRIMARY KEY,  -- Alias for rowid, auto-assigned on INSERT
    name TEXT NOT NULL
) STRICT;
```

### Avoid AUTOINCREMENT

```sql
-- CORRECT: Plain INTEGER PRIMARY KEY
CREATE TABLE logs (
    id INTEGER PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
) STRICT;
```

```sql
-- WRONG: Unnecessary AUTOINCREMENT
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL
) STRICT;
-- AUTOINCREMENT prevents rowid reuse but adds overhead:
-- - Creates sqlite_sequence tracking table
-- - Slightly slower inserts
-- - IDs never decrease (even after DELETE)
-- Only use when rowid reuse would cause actual problems (audit trails, external references).
```

## Schema Design Rules

### Naming Conventions

- **Tables**: `snake_case`, lowercase, plural (e.g., `users`, `order_items`)
- **Columns**: `snake_case`, lowercase (e.g., `first_name`, `created_at`)
- **Indexes**: `idx_` prefix with table and columns (e.g., `idx_users_email`)
- **Foreign keys**: Column name ends with `_id` (e.g., `user_id`, `category_id`)
- **Triggers**: Descriptive with table name (e.g., `users_updated_at`)
- **Avoid reserved words**: Don't use `order`, `group`, `index`, `key`, `value`, etc.

### NOT NULL by Default

```sql
-- CORRECT: NOT NULL with defaults where possible
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,             -- Nullable is intentional and documented
    price_cents INTEGER NOT NULL CHECK (price_cents >= 0),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
) STRICT;
```

```sql
-- WRONG: Everything nullable
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,        -- Should be NOT NULL
    price_cents INTEGER  -- Should be NOT NULL with CHECK constraint
);
```

### CHECK Constraints

```sql
-- CORRECT: Domain validation with CHECK constraints
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL CHECK (email LIKE '%@%.%'),
    age INTEGER CHECK (age >= 0 AND age <= 150),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'banned')),
    role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('admin', 'moderator', 'user'))
) STRICT;
```

## Feature Rules

### JSON Functions (SQLite 3.38+)

```sql
-- CORRECT: JSON with generated columns for indexing
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    payload TEXT NOT NULL CHECK (json_valid(payload)),
    event_type TEXT GENERATED ALWAYS AS (json_extract(payload, '$.type')) STORED,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
) STRICT;

CREATE INDEX idx_events_type ON events(event_type);
```

```sql
-- WRONG: json_extract in WHERE without generated column
SELECT * FROM events WHERE json_extract(payload, '$.type') = 'purchase';
-- Full table scan + per-row JSON parsing. Use generated columns for indexed queries.
```

### FTS5 Full-Text Search

```sql
-- CORRECT: External content FTS5 with sync triggers
CREATE VIRTUAL TABLE docs_fts USING fts5(
    title, body,
    content='documents',
    content_rowid='id',
    tokenize='porter unicode61'
);
```

```sql
-- WRONG: LIKE with leading wildcard for text search
SELECT * FROM documents WHERE body LIKE '%search term%';
-- Requires full table scan. Use FTS5 for text search.
```

### WITHOUT ROWID

```sql
-- CORRECT: WITHOUT ROWID for small lookup tables
CREATE TABLE settings (
    key TEXT PRIMARY KEY NOT NULL,
    value TEXT NOT NULL
) STRICT, WITHOUT ROWID;

CREATE TABLE tag_assignments (
    item_id INTEGER NOT NULL REFERENCES items(id),
    tag_id INTEGER NOT NULL REFERENCES tags(id),
    PRIMARY KEY (item_id, tag_id)
) STRICT, WITHOUT ROWID;
```

```sql
-- WRONG: WITHOUT ROWID on large table with INTEGER PRIMARY KEY
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    data TEXT NOT NULL
) STRICT, WITHOUT ROWID;
-- INTEGER PRIMARY KEY is already a rowid alias — WITHOUT ROWID adds overhead
-- by storing data in a B-tree indexed by PK instead of using the optimized rowid.
```

### UPSERT (SQLite 3.24+)

```sql
-- CORRECT: Idempotent upsert
INSERT INTO settings (key, value)
VALUES ('theme', 'dark')
ON CONFLICT (key) DO UPDATE SET value = excluded.value;
```

### Window Functions (SQLite 3.25+)

```sql
-- CORRECT: Window functions for analytics
SELECT
    name, department, salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg
FROM employees;
```

### RETURNING Clause (SQLite 3.35+)

```sql
-- CORRECT: Get inserted data back
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')
RETURNING id, created_at;
```

### Generated Columns (SQLite 3.31+)

```sql
-- CORRECT: Stored generated column for indexing
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    data TEXT NOT NULL CHECK (json_valid(data)),
    customer TEXT GENERATED ALWAYS AS (json_extract(data, '$.customer')) STORED
) STRICT;

CREATE INDEX idx_orders_customer ON orders(customer);
```

## Connection Management Rules

### One Writer, Multiple Readers

- Exactly 1 write connection per application instance
- Multiple read connections (1 per thread/worker)
- All connections must have PRAGMAs configured

### busy_timeout on All Connections

- Set to at least 5000ms (5 seconds)
- Without it, any lock contention returns SQLITE_BUSY immediately
- Application should still handle SQLITE_BUSY for edge cases

### Proper Connection Cleanup

- Close all connections on application shutdown
- Leaked connections hold file locks and prevent checkpointing
- Use try-finally or context managers to ensure cleanup

### BEGIN IMMEDIATE for Write Transactions

```sql
-- CORRECT: Acquire write lock immediately
BEGIN IMMEDIATE;
-- ... write operations ...
COMMIT;
```

```sql
-- WRONG: Deferred transaction (default)
BEGIN;
-- ... read operations ...
INSERT INTO ...;  -- May get SQLITE_BUSY here if another writer started
COMMIT;
-- Deferred transactions don't acquire the write lock until the first write.
-- This can cause unexpected SQLITE_BUSY errors mid-transaction.
```

## Indexing Rules

- Create indexes for columns used in WHERE, JOIN, and ORDER BY clauses
- Composite indexes follow leftmost prefix rule — column order matters
- Partial indexes for filtered queries: `CREATE INDEX ... WHERE condition`
- Expression indexes for computed queries: `CREATE INDEX ... ON table(lower(col))`
- Don't over-index — each index adds write overhead
- A composite index on (a, b) already covers queries on (a) alone
- Use `EXPLAIN QUERY PLAN` to verify index usage

## Compatibility Matrix

| Feature               | Minimum Version |
| --------------------- | --------------- |
| WAL mode              | 3.7.0           |
| FTS5                  | 3.9.0           |
| UPSERT                | 3.24.0          |
| Window functions      | 3.25.0          |
| Generated columns     | 3.31.0          |
| RETURNING clause      | 3.35.0          |
| STRICT tables         | 3.37.0          |
| Built-in JSON         | 3.38.0          |
| RIGHT/FULL OUTER JOIN | 3.39.0          |
| Math functions        | 3.35.0          |

Always check the SQLite version in the target environment before using newer features. Mobile
platforms and embedded systems may ship older versions.
