---
name: sql-mssql
description: "Applies when writing or reviewing MS SQL Server T-SQL. Covers NVARCHAR, columnstore indexes, TRY/CATCH, CROSS APPLY, temporal tables, and parameter sniffing."
---

# MS SQL Server (T-SQL)

## Data types

1. **`NVARCHAR` for user-facing text.** `VARCHAR` is single-byte — cannot store emoji, CJK, or many international characters. Use `VARCHAR` only for known-ASCII data.
2. **`UNIQUEIDENTIFIER` for UUIDs.** `NEWSEQUENTIALID()` for clustered PKs (ordered, less fragmentation). `NEWID()` for random.
3. **`DATETIME2` over `DATETIME`.** Higher precision, wider range. `DATETIMEOFFSET` for timezone-aware timestamps.
4. **`DECIMAL(p,s)` for money**, never `FLOAT` or `REAL`.

## Identity, sequences, and OUTPUT

5. **`IDENTITY` for auto-increment PKs.** `SEQUENCE` for cross-table sharing or pre-allocation.
6. **`OUTPUT` clause** instead of separate SELECT after mutations:
   ```sql
   INSERT INTO orders (customer_id, total)
   OUTPUT inserted.id, inserted.created_at
   VALUES (42, 99.99);
   ```
7. **`MERGE` with `HOLDLOCK`** for upserts (MERGE has had race-condition bugs without it):
   ```sql
   MERGE INTO inventory WITH (HOLDLOCK) AS tgt
   USING (VALUES (101, 5)) AS src (product_id, qty)
   ON tgt.product_id = src.product_id
   WHEN MATCHED THEN UPDATE SET tgt.qty = tgt.qty + src.qty
   WHEN NOT MATCHED THEN INSERT (product_id, qty) VALUES (src.product_id, src.qty);
   ```

## Indexes

8. **Columnstore indexes** for analytical queries on large tables. Non-clustered columnstore coexists with row-store for OLTP+analytics on the same table.
9. **Filtered indexes:** `CREATE INDEX ix_pending ON orders (created_at) WHERE status = 'pending'`.
10. **`INCLUDE` columns** for covering non-clustered indexes without bloating the B-tree key:
    ```sql
    CREATE INDEX ix_orders_customer ON orders (customer_id) INCLUDE (order_date, total);
    ```

## Error handling

11. **`TRY...CATCH` with `SET XACT_ABORT ON`:**
    ```sql
    SET XACT_ABORT ON;
    BEGIN TRY
      BEGIN TRANSACTION;
      -- DML
      COMMIT;
    END TRY
    BEGIN CATCH
      IF @@TRANCOUNT > 0 ROLLBACK;
      THROW;
    END CATCH;
    ```
12. **`THROW` over `RAISERROR`** (2012+). Re-raises the original error correctly.
13. **Check `@@TRANCOUNT` before `ROLLBACK`** in CATCH blocks.

## CROSS APPLY and temporal tables

14. **`CROSS APPLY` / `OUTER APPLY`** instead of correlated subqueries:
    ```sql
    SELECT c.name, latest.order_date
    FROM customer c
    OUTER APPLY (
      SELECT TOP 1 order_date FROM orders o
      WHERE o.customer_id = c.id ORDER BY order_date DESC
    ) latest;
    ```
15. **System-versioned temporal tables** for automatic audit history. Query with `FOR SYSTEM_TIME AS OF`.

## T-SQL pitfalls

16. **Parameter sniffing:** first parameter values determine the plan. Mitigations: `OPTION (RECOMPILE)` for infrequent queries, `OPTION (OPTIMIZE FOR UNKNOWN)`, or Query Store plan forcing.
17. **Implicit conversions kill performance.** `WHERE nvarchar_col = @varchar_param` forces per-row conversion. Match parameter types to column types.
18. **`NOLOCK` is almost never correct.** Reads dirty data, can skip or double-read rows. Use Read Committed Snapshot Isolation (RCSI) instead.
19. **`SELECT TOP N` without `ORDER BY`** returns arbitrary rows.
20. **`@@IDENTITY` crosses scopes (including triggers).** Use `SCOPE_IDENTITY()` or `OUTPUT inserted.id`.
21. **Scalar UDFs execute row-by-row** (before 2019 inlining). Use inline table-valued functions or `CROSS APPLY`.
22. **Enable Query Store** for plan regression detection and plan forcing without hints.

## Sources

- https://learn.microsoft.com/en-us/sql/t-sql/language-reference
- https://learn.microsoft.com/en-us/sql/relational-databases/indexes/columnstore-indexes-overview
