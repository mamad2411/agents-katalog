---
name: postgres-patterns
description: PostgreSQL database patterns for query optimization, schema design, indexing, GORM integration, and security.
---

# PostgreSQL Patterns

PostgreSQL best practices quick reference, tailored for GORM-based Go applications and Docker-based local development.

## When to Activate

- Writing SQL queries or migrations
- Designing database schemas
- Troubleshooting slow queries
- Configuring connection pooling
- Working with GORM models

## Quick Reference

### Index Cheat Sheet

| Query Pattern | Index Type | Example |
|--------------|------------|---------|
| `WHERE col = value` | B-tree (default) | `CREATE INDEX idx ON t (col)` |
| `WHERE col > value` | B-tree | `CREATE INDEX idx ON t (col)` |
| `WHERE a = x AND b > y` | Composite | `CREATE INDEX idx ON t (a, b)` |
| `WHERE jsonb @> '{}'` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| `WHERE tsv @@ query` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| Time-series ranges | BRIN | `CREATE INDEX idx ON t USING brin (col)` |

### Data Type Quick Reference

| Use Case | Correct Type | Avoid |
|----------|-------------|-------|
| ID | `bigint` / `bigserial` | `int`, random UUID |
| Strings | `text` | `varchar(255)` |
| Timestamps | `timestamptz` | `timestamp` |
| Money | `numeric(10,2)` | `float` |
| Flags | `boolean` | `varchar`, `int` |

### Common Patterns

**Composite Index Ordering:**
```sql
-- Equality columns first, then range columns
CREATE INDEX idx ON orders (status, created_at);
-- Works for: WHERE status = 'pending' AND created_at > '2024-01-01'
```

**Covering Index:**
```sql
CREATE INDEX idx ON users (email) INCLUDE (name, created_at);
-- Avoids table lookup for SELECT email, name, created_at
```

**Partial Index:**
```sql
CREATE INDEX idx ON users (email) WHERE deleted_at IS NULL;
-- Smaller index, only includes active users
```

**UPSERT:**
```sql
INSERT INTO settings (user_id, key, value)
VALUES (123, 'theme', 'dark')
ON CONFLICT (user_id, key)
DO UPDATE SET value = EXCLUDED.value;
```

**Cursor Pagination:**
```sql
SELECT * FROM products WHERE id > $last_id ORDER BY id LIMIT 20;
-- O(1) vs OFFSET which is O(n)
```

**Queue Processing with SKIP LOCKED:**
```sql
UPDATE jobs SET status = 'processing'
WHERE id = (
  SELECT id FROM jobs WHERE status = 'pending'
  ORDER BY created_at LIMIT 1
  FOR UPDATE SKIP LOCKED
) RETURNING *;
```

## GORM-Specific Patterns

### Auto Migration

```go
func AutoMigrate(db *gorm.DB) error {
    return db.AutoMigrate(
        &User{},
        &Asset{},
        &AssetPrice{},
        &ExchangeRate{},
    )
}
```

### Scopes for Reusable Queries

```go
func ActiveUsers(db *gorm.DB) *gorm.DB {
    return db.Where("deleted_at IS NULL AND active = ?", true)
}

func Paginate(page, limit int) func(db *gorm.DB) *gorm.DB {
    return func(db *gorm.DB) *gorm.DB {
        offset := (page - 1) * limit
        return db.Offset(offset).Limit(limit)
    }
}

func DateRange(start, end time.Time) func(db *gorm.DB) *gorm.DB {
    return func(db *gorm.DB) *gorm.DB {
        return db.Where("created_at BETWEEN ? AND ?", start, end)
    }
}

// Usage
db.Scopes(ActiveUsers, Paginate(1, 20)).Find(&users)
```

### Preloading Associations

```go
// Eager loading to avoid N+1
db.Preload("Assets").Preload("Assets.Prices").Find(&users)

// Conditional preloading
db.Preload("Assets", "currency = ?", "USD").Find(&users)

// Nested preloading with custom query
db.Preload("Assets", func(db *gorm.DB) *gorm.DB {
    return db.Order("created_at DESC").Limit(5)
}).Find(&users)
```

### Transaction Patterns

```go
func TransferAsset(db *gorm.DB, fromID, toID uint, assetID uint) error {
    return db.Transaction(func(tx *gorm.DB) error {
        var asset Asset
        if err := tx.Clauses(clause.Locking{Strength: "UPDATE"}).
            First(&asset, assetID).Error; err != nil {
            return fmt.Errorf("find asset: %w", err)
        }

        if asset.UserID != fromID {
            return errors.New("asset does not belong to sender")
        }

        asset.UserID = toID
        if err := tx.Save(&asset).Error; err != nil {
            return fmt.Errorf("transfer asset: %w", err)
        }

        return nil
    })
}
```

### Hooks

```go
func (u *User) BeforeCreate(tx *gorm.DB) error {
    hashedPassword, err := bcrypt.GenerateFromPassword(
        []byte(u.Password), bcrypt.DefaultCost,
    )
    if err != nil {
        return err
    }
    u.Password = string(hashedPassword)
    return nil
}
```

## Anti-Pattern Detection

```sql
-- Find foreign keys without indexes
SELECT conrelid::regclass, a.attname
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = 'f'
  AND NOT EXISTS (
    SELECT 1 FROM pg_index i
    WHERE i.indrelid = c.conrelid AND a.attnum = ANY(i.indkey)
  );

-- Find slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC;

-- Check table bloat
SELECT relname, n_dead_tup, last_vacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

## Configuration Template

```sql
-- Connection limits (adjust based on RAM)
ALTER SYSTEM SET max_connections = 100;
ALTER SYSTEM SET work_mem = '8MB';

-- Timeouts
ALTER SYSTEM SET idle_in_transaction_session_timeout = '30s';
ALTER SYSTEM SET statement_timeout = '30s';

-- Monitoring
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Security defaults
REVOKE ALL ON SCHEMA public FROM public;

SELECT pg_reload_conf();
```

## Local Development (Docker)

Connect to the Fusion Labs local PostgreSQL:

```bash
# Connection string
postgresql://devuser:devpassword@localhost:5432/devdb

# psql
psql -h localhost -p 5432 -U devuser -d devdb
```

## Related Skills

- Skill: `gin-patterns` — Gin + GORM integration
- Skill: `golang-patterns` — Go design patterns
- Skill: `docker-patterns` — Docker Compose setup

---

**Remember**: Database design decisions are hard to reverse. Take time to choose the right data types, indexes, and constraints upfront.
