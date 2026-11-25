---
name: sql-mysql
description: "Applies when writing or reviewing MySQL queries and schemas. Covers InnoDB, utf8mb4, AUTO_INCREMENT, ON DUPLICATE KEY, covering indexes, and ONLY_FULL_GROUP_BY."
---

# MySQL

## Storage and character sets

1. **Always InnoDB.** MyISAM lacks transactions, row-level locking, crash recovery. No valid production use.
2. **`utf8mb4` everywhere.** `CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci` (MySQL 8) or `utf8mb4_unicode_ci` (MySQL 5.7). MySQL's `utf8` is 3-byte only — cannot store emoji.
3. **`innodb_file_per_table = ON`** (default since 5.6.6) for per-table tablespace management.

## Keys and upsert

4. **`BIGINT AUTO_INCREMENT` for PKs.** `INT` maxes at ~2.1B. UUIDs as PKs cause random I/O on clustered indexes — store as `BINARY(16)` with a `BIGINT AUTO_INCREMENT` PK and a unique index on the UUID.
5. **`ON DUPLICATE KEY UPDATE` for upserts:**
   ```sql
   INSERT INTO inventory (product_id, qty) VALUES (101, 5)
   ON DUPLICATE KEY UPDATE qty = qty + VALUES(qty);
   ```
6. **`LAST_INSERT_ID()`** immediately after INSERT on the same connection. Connection-safe, no transaction needed.

## Indexes

7. **Composite indexes follow leftmost-prefix rule.** `(a, b, c)` serves queries on `(a)`, `(a, b)`, `(a, b, c)` but not `(b)` or `(c)` alone.
8. **Covering indexes** — include all SELECT columns in the index for "index-only" scans. Check `EXPLAIN` for `Using index`.
9. **Avoid `FORCE INDEX` / `USE INDEX`.** Hints become wrong as data changes.
10. **`FULLTEXT` indexes for text search.** `LIKE '%term%'` cannot use B-tree indexes. Use `MATCH ... AGAINST`.
11. **Invisible indexes (8.0+):** `ALTER INDEX ix_name INVISIBLE` to test impact before dropping.

## JSON and generated columns

12. **`JSON` columns for semi-structured data.** For indexed fields, add a generated column:
    ```sql
    ALTER TABLE orders
      ADD customer_email VARCHAR(255)
        GENERATED ALWAYS AS (metadata->>'$.email') STORED,
      ADD INDEX ix_orders_email (customer_email);
    ```

## MySQL pitfalls

13. **`ONLY_FULL_GROUP_BY` must be enabled** (default 5.7.5+). Without it, non-aggregated columns return indeterminate values.
14. **Implicit type conversion kills indexes.** `WHERE varchar_col = 12345` converts every row. Match types.
15. **`LIMIT` with large offsets is slow.** Use keyset pagination: `WHERE id > :last_id ORDER BY id LIMIT :n`.
16. **`COUNT(*)` on InnoDB is a full scan.** For approximate counts, use `information_schema.TABLES.TABLE_ROWS`.
17. **`ENUM` values are painful to alter.** Appending is instant in MySQL 8; inserting in the middle requires a rebuild. Prefer `CHECK` constraints or lookup tables.
18. **GTID-based replication:** avoid non-deterministic statements (`INSERT ... SELECT` without `ORDER BY`).

## Sources

- https://dev.mysql.com/doc/refman/8.0/en/optimization.html
- https://dev.mysql.com/doc/refman/8.0/en/innodb-index-types.html
