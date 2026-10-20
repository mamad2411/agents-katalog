---
name: sql-oracle
description: "Applies when writing or reviewing Oracle SQL and PL/SQL. Covers NUMBER/VARCHAR2, MERGE, bulk operations, partitioning, and SQL Plan Management."
---

# Oracle

## Data types

1. **`NUMBER(p,s)` with explicit precision.** `NUMBER(10)` for integers, `NUMBER(19,4)` for money. Unqualified `NUMBER` hides intent.
2. **`VARCHAR2` over `CHAR`.** `CHAR` pads with spaces, wastes storage, causes comparison surprises.
3. **`TIMESTAMP WITH TIME ZONE`** for cross-timezone temporal data. `TIMESTAMP WITH LOCAL TIME ZONE` for auto-conversion to session timezone.
4. **`CLOB`/`BLOB` for large objects**, not `LONG` (deprecated, one per table, no indexing).
5. **Oracle `DATE` includes a time component** (unlike SQL standard). Use `TIMESTAMP` when you need sub-second precision.

## Sequences and upsert

6. **`GENERATED ALWAYS AS IDENTITY`** (12c+) for auto-increment PKs. Falls back to `SEQUENCE` objects for cross-table sharing.
7. **`MERGE` for upserts:**
   ```sql
   MERGE INTO inventory tgt
   USING (SELECT 101 AS product_id, 5 AS qty FROM dual) src
   ON (tgt.product_id = src.product_id)
   WHEN MATCHED THEN UPDATE SET tgt.qty = tgt.qty + src.qty
   WHEN NOT MATCHED THEN INSERT (product_id, qty) VALUES (src.product_id, src.qty);
   ```
8. **Recursive CTEs** (11gR2+) over `CONNECT BY` for portability. Include a depth counter for termination.

## Indexes

9. **Bitmap indexes** for low-cardinality columns in read-heavy/warehouse workloads. Never on OLTP tables — severe lock contention.
10. **Function-based indexes:** `CREATE INDEX ix_upper_email ON users (UPPER(email))`.
11. **Index-organized tables (IOT)** for lookup tables always accessed by PK.
12. **Invisible indexes (12c+):** `ALTER INDEX ix_name INVISIBLE` to test dropping without committing.

## PL/SQL performance

13. **`FORALL` for bulk DML.** Sends all DML as a single round-trip:
    ```sql
    FORALL i IN 1..ids.COUNT
      DELETE FROM orders WHERE id = ids(i);
    ```
14. **`BULK COLLECT ... LIMIT`** for batch fetching. Control memory with `LIMIT 1000`.
15. **Use packages** over standalone procedures. Shared state, reduced hard parsing, information hiding.

## Partitioning

16. **Range-partition by date** for time-series. Enables partition pruning and fast `DROP PARTITION`.
17. **List partitioning** for categories (region, status). **Hash partitioning** for even distribution.
18. **Local indexes** (one per partition) over global indexes for partitioned tables.

## Hints and plans

19. **Use hints sparingly and document why.** Prefer SQL Plan Baselines (`DBMS_SPM`) for plan stability.
20. **`DBMS_STATS.GATHER_TABLE_STATS`** after large data changes. Stale statistics are the #1 cause of bad plans.

## Oracle pitfalls

21. **Bind variable peeking:** first bind value determines the plan. Adaptive Cursor Sharing (11g+) mitigates; `CURSOR_SHARING = FORCE` as last resort.
22. **Implicit DATE conversion:** `WHERE date_col = '2025-01-01'` depends on `NLS_DATE_FORMAT`. Always use `DATE '2025-01-01'` or `TO_DATE('2025-01-01', 'YYYY-MM-DD')`.
23. **Empty string is NULL in Oracle.** `'' IS NULL` is TRUE. Non-standard; plan for this when porting.
24. **`ROWNUM` filters before `ORDER BY`.** Wrap in subquery: `SELECT * FROM (SELECT ... ORDER BY col) WHERE ROWNUM <= 10`. Or use `FETCH FIRST N ROWS ONLY` (12c+).
25. **`FOR UPDATE SKIP LOCKED`** (11g+) for job-queue patterns.

## Sources

- https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/
- https://docs.oracle.com/en/database/oracle/oracle-database/23/tgsql/
