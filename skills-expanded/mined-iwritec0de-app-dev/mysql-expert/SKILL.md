---
name: mysql-expert
description: >-
  This skill should be used when the user asks to "write a MySQL query", "configure
  my.cnf", "choose a storage engine", "tune MySQL performance", "set up MySQL
  replication", or mentions "mysql", "mariadb", "innodb", "my.cnf", "mysqldump",
  "mysql replication", "mysql tuning", "mysql index", "mysql json", "charset",
  "collation". Provides MySQL/MariaDB-specific expertise for SQL, storage engines,
  types, configuration, and tuning.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# MySQL Expert Skill

You are a MySQL/MariaDB expert specializing in InnoDB, query optimization, and database administration.

## Critical Rules

- **Always use InnoDB** — the only engine with ACID transactions, row-level locking, and crash recovery
- **Use utf8mb4, not utf8** — MySQL's `utf8` is broken (3-byte, no emoji); `utf8mb4` is true UTF-8
- **Define explicit PRIMARY KEYs** — InnoDB clusters data on PK; implicit keys waste space
- **Use EXPLAIN** — verify query plans before and after optimization
- **Use prepared statements** — for security (SQL injection) and performance (plan caching)
- **Don't use query cache** — removed in MySQL 8.0; use application-level caching instead
- **Collation matters** — use `utf8mb4_unicode_ci` for case-insensitive, `utf8mb4_bin` for exact

## Storage Engines

| Engine | Use Case | Notes |
|--------|----------|-------|
| InnoDB | Everything (default) | ACID, row locks, crash recovery, FK support |
| MEMORY | Temporary lookup tables | Lost on restart, table-level locks |
| MyISAM | Legacy only | No transactions, no FK, table locks — avoid |

## MySQL-Specific Types

| Type | Use Case | Example |
|------|----------|---------|
| `JSON` | Flexible data (MySQL 5.7+) | `data->>'$.name'`, `JSON_EXTRACT()` |
| `ENUM` | Fixed small sets | `ENUM('active','inactive','deleted')` |
| `SET` | Multiple choice from fixed set | `SET('read','write','admin')` |
| Generated columns | Derived/computed data | `GENERATED ALWAYS AS (price * qty) STORED` |
| `BINARY(16)` | UUID storage (compact) | `UUID_TO_BIN(UUID(), 1)` for ordered UUIDs |

## Advanced SQL (MySQL 8.0+)

```sql
-- Common Table Expression
WITH monthly AS (
  SELECT DATE_FORMAT(created_at, '%Y-%m') AS month, SUM(total) AS revenue
  FROM orders GROUP BY month
) SELECT * FROM monthly WHERE revenue > 10000;

-- Window function
SELECT name, salary, RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;

-- JSON query
SELECT * FROM products WHERE data->>'$.category' = 'electronics';

-- Full-text search
SELECT *, MATCH(title, body) AGAINST('database optimization' IN BOOLEAN MODE) AS relevance
FROM articles WHERE MATCH(title, body) AGAINST('database optimization' IN BOOLEAN MODE);
```

Read `reference/advanced-sql.md` for CTEs, JSON functions, partitioning, and generated columns.

## Configuration

Key `my.cnf` settings:

| Setting | Default | Recommendation |
|---------|---------|---------------|
| `innodb_buffer_pool_size` | 128MB | 70-80% of RAM |
| `innodb_log_file_size` | 48MB | 1-2GB |
| `innodb_flush_log_at_trx_commit` | 1 | 1 (safe) or 2 (faster, slight risk) |
| `max_connections` | 151 | Based on workload + pool size |
| `slow_query_log` | OFF | ON (always in production) |
| `long_query_time` | 10 | 1 (catch more slow queries) |

Read `reference/tuning.md` for InnoDB tuning, buffer pool sizing, and monitoring.

## Replication

- **Source-Replica** — async replication for read scaling and backups
- **GTID replication** — recommended; simplifies failover (`gtid_mode=ON`)
- **Group Replication** — multi-primary for HA (MySQL 8.0+)
- **Read replicas** — route reads to replicas, writes to source

Read `reference/administration.md` for replication setup, backup strategies, and user management.

## Anti-Patterns

- **Don't use `utf8`** — use `utf8mb4` for full Unicode support
- **Don't skip PRIMARY KEY** — InnoDB generates a hidden 6-byte key, wasting space
- **Don't use MyISAM** — for any transactional or concurrent workload
- **Don't rely on query cache** — deprecated and removed; use Redis/Memcached
- **Don't use `SELECT *` in production** — fetch only needed columns
- **Don't store large BLOBs in InnoDB** — use file storage + path references

## Related

- `reference/advanced-sql.md` — CTEs, window functions, JSON, full-text, partitioning
- `reference/administration.md` — Backups, replication, user management, SSL
- `reference/tuning.md` — InnoDB tuning, buffer pool, slow query analysis
