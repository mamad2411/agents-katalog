---
name: relational-database
description: "Unified relational database skill index — covers schema design, SQL queries, JOINs, constraints, indexing, normalization, transactions, migrations, performance tuning, and backup & recovery. Use this as the entry point; it delegates to focused sub-skill files for each domain."
---

# Relational Database Skill

## Overview

This file is the top-level entry point for all relational database topics. It identifies the right sub-skill file based on what the user is trying to accomplish. Each sub-skill file contains clear explanations, examples, and best practices for its domain.

The concepts here apply to all major relational databases (PostgreSQL, MySQL, SQLite, SQL Server) unless noted otherwise.

---

## Sub-Skills Reference

| Domain             | File                                           | When to use                                                                                                        |
| ------------------ | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Schema Design      | [schema-design.md](schema-design.md)           | Designing tables, choosing data types, primary keys, foreign keys, naming conventions                              |
| SQL Queries        | [sql-queries.md](sql-queries.md)               | Writing `SELECT`, `INSERT`, `UPDATE`, `DELETE`; filtering with `WHERE`; grouping with `GROUP BY`; subqueries       |
| JOINs              | [joins.md](joins.md)                           | Combining data from multiple tables using `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL JOIN`, self-joins         |
| Constraints        | [constraints.md](constraints.md)               | Enforcing data integrity with `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`, `CHECK`, `DEFAULT`               |
| Indexing           | [indexing.md](indexing.md)                     | Creating indexes to speed up queries; understanding when indexes help or hurt; composite and partial indexes       |
| Normalization      | [normalization.md](normalization.md)           | Understanding 1NF, 2NF, 3NF; eliminating redundancy; knowing when to denormalize                                   |
| Transactions       | [transactions.md](transactions.md)             | Using `BEGIN`, `COMMIT`, `ROLLBACK`; ACID properties; isolation levels; preventing dirty reads and race conditions |
| Migrations         | [migrations.md](migrations.md)                 | Evolving schema safely with `ALTER TABLE`; adding/removing columns; renaming; zero-downtime strategies             |
| Performance Tuning | [performance-tuning.md](performance-tuning.md) | Reading `EXPLAIN`/`EXPLAIN ANALYZE`; spotting slow queries; query optimization techniques; avoiding N+1 in SQL     |
| Backup & Recovery  | [backup-recovery.md](backup-recovery.md)       | Backing up and restoring databases; `pg_dump`, `mysqldump`; point-in-time recovery; backup strategies              |

---

## Quick Decision Guide

```
What are you trying to do?
│
├── Design a new table or choose a data type?
│   └── → schema-design.md
│
├── Write a SELECT, INSERT, UPDATE, or DELETE query?
│   └── → sql-queries.md
│
├── Combine data from multiple tables?
│   └── → joins.md
│
├── Enforce data rules (uniqueness, not null, foreign keys)?
│   └── → constraints.md
│
├── Speed up slow queries with indexes?
│   └── → indexing.md
│
├── Structure tables to reduce redundancy?
│   └── → normalization.md
│
├── Run multiple operations atomically?
│   └── → transactions.md
│
├── Change an existing table without losing data?
│   └── → migrations.md
│
├── Diagnose and fix slow database queries?
│   └── → performance-tuning.md
│
└── Back up or restore a database?
    └── → backup-recovery.md
```

---

## How to Use This Skill

1. **Identify the goal** using the Quick Decision Guide above.
2. **Load the corresponding sub-skill file** with `read_file` (e.g., `joins.md`).
3. **Follow the patterns and examples** in that file to produce the response.
4. **Load multiple sub-skill files** when the task spans domains — for example, optimizing a slow query typically involves `indexing.md` + `performance-tuning.md`.
