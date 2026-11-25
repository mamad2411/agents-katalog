---
id: "database.architecture-and-modeling"
name: "Database Architecture & Data Modeling"
version: "1.2.0"
domain: "database"
description: "Architect high-performance relational and document schemas, deterministic zero-downtime migrations, B-Tree/GIN indexing strategies, and ACID transaction boundaries."
triggers:
  - "Designing database schemas, tables, relationships, or migrations"
  - "Writing complex SQL queries, transactions, or indexing strategies"
  - "Refactoring existing database models or optimizing query latency"
  - "Implementing caching layers, read replicas, or partitioning strategies"
prerequisites:
  - "architecture.system-design"
risk_profile: "high"
---

# Database Architecture & Data Modeling

## Overview
This skill encodes the expertise of a Lead Database Architect and Principal Data Engineer. It ensures database schemas are normalized, query plans are optimized, data integrity is guaranteed at the database engine level, and all schema evolutions follow zero-downtime expand-contract paradigms.

## 🎯 Token Conservation & High-Yield Heuristics
1. **Schema DDL First**: Write declarative schema definitions (SQL DDL / Prisma / Drizzle / TypeORM) with explicit types, constraints, and defaults. Avoid conversational speculation about database shapes.
2. **Deterministic Index Definitions**: State index types (B-Tree, GIN, Hash) and explain index column ordering ($(\text{filter}, \text{sort})$) directly in code comments.
3. **Prepared Statements**: Never concatenate SQL strings. Always use parameterized queries or type-safe query builders to ensure security and plan caching.

## 📐 Core Engineering Directives

### 1. Relational Modeling & Data Integrity
- **Third Normal Form (3NF) Baseline**: Normalize entities to 3NF to prevent update anomalies and duplicate storage. Only introduce deliberate denormalization when backed by empirical read performance benchmarks.
- **Engine-Level Constraints**: Enforce data integrity in the database engine, not merely in application code. Use `NOT NULL`, `FOREIGN KEY ... ON DELETE RESTRICT/CASCADE`, `CHECK` constraints, and `UNIQUE` indexes.
- **Primary Keys**: Use immutable, collision-resistant identifiers: UUIDv7 (time-ordered, index-friendly) or standard auto-incrementing BigInt keys. Avoid raw UUIDv4 for high-throughput clustered indexes due to B-Tree page fragmentation.

### 2. Indexing Strategy & Query Optimization
- **Index Selectivity Rule**: Index columns used in `WHERE`, `JOIN`, and `ORDER BY` clauses with high cardinality. Avoid indexing low-cardinality columns (e.g. boolean flags) unless part of a composite or partial index.
- **Leftmost Prefix Rule**: For composite indexes on `(A, B, C)`, queries filtering on `A` or `(A, B)` utilize the index; queries filtering solely on `B` or `C` cannot utilize the B-Tree index.
- **Covering Indexes**: Use `INCLUDE` columns (in PostgreSQL) to satisfy read queries directly from index leaf pages without table heap fetches (`Index Only Scan`).
- **Query Plan Verification**: Verify queries with `EXPLAIN (ANALYZE, BUFFERS)` (PostgreSQL) or `EXPLAIN ANALYZE` (MySQL). Eliminate sequential scans on large tables ($> 10{,}000$ rows).

### 3. Concurrency & Transaction Isolation
- **Short-Lived Transactions**: Keep database transactions as short as possible. Never perform external network calls, file I/O, or CPU-intensive tasks inside a database transaction block.
- **Optimistic Locking**: For concurrent updates on frequently modified entities (e.g. inventory balances), use version numbers (`version INT`) with conditional updates (`WHERE id = :id AND version = :version`).
- **Deadlock Prevention**: Always acquire locks on multiple rows or tables in a globally consistent order (e.g. sorted by ID ascending).

### 4. Zero-Downtime Migration Lifecycle (Expand-Contract)
Never execute breaking schema changes (renaming columns, removing columns, altering types) in a single deployment:
1. **Phase 1 (Expand)**: Add the new column/table as nullable or with a safe default. Deploy code that writes to both old and new columns, reading from the old.
2. **Phase 2 (Backfill)**: Run an asynchronous background migration to copy existing data from old columns to new columns in batches.
3. **Phase 3 (Switch)**: Deploy code that reads and writes strictly to the new column.
4. **Phase 4 (Contract)**: Drop the old column/table in a subsequent maintenance deployment once verified.

## 🛑 Anti-Rationalization Matrix

| Agent Excuse / Shortcut | Database Reality | Mandatory Action |
|---|---|---|
| *"I'll just rename this column in the production migration directly."* | Causes downtime, breaks active application instances, and fails rolling deployments. | Use the 4-phase Expand-Contract pattern with backward compatibility. |
| *"I don't need a foreign key constraint; the ORM handles it."* | Data drift, orphan records, and corrupt states inevitably occur during manual updates or batch operations. | Define foreign key constraints at the SQL DDL level with explicit delete rules. |
| *"I'll use `SELECT *` in queries to get all fields."* | Wastes network bandwidth, consumes memory, breaks covering index scans, and risks payload leakage. | Select only the exact columns required by the calling application layer. |
| *"I don't need indexes yet because the development database is small."* | Small test databases hide $O(N)$ sequential scans that cause catastrophic failure in production under load. | Add indexes during schema definition according to access patterns. |

## ✅ Database Verification Checklist
- [ ] Foreign keys and uniqueness constraints defined at the engine level.
- [ ] No sequential scans on high-traffic queries verified via `EXPLAIN ANALYZE`.
- [ ] UUIDv7 or BigInt primary keys utilized for indexed tables.
- [ ] All migrations are reversible (`down` script provided) and non-blocking (`CREATE INDEX CONCURRENTLY` in PostgreSQL).
- [ ] Zero raw string concatenation in SQL queries; 100% parameterized inputs.

