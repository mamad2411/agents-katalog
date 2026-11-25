---
name: database-architect
description: Design scalable relational and distributed database architectures, schema migrations, indexing strategies, and query optimization. Enforces ACID compliance, data integrity, and connection pooling.
---

# Database Architect Skill

## Purpose
Directs relational schema modeling (PostgreSQL), index design (B-tree, GIN, BRIN), transactional integrity, and zero-downtime migrations.

## When to Use
- Designing relational schemas, foreign key relationships, and check constraints.
- Writing migration scripts with rollback paths (e.g. `sqlx`, Flyway, Alembic).
- Analyzing slow query execution plans (`EXPLAIN (ANALYZE, BUFFERS)`).

## Engineering Workflow
1. **Schema Design**: Normalize to 3NF for OLTP; apply appropriate indexing for high-frequency queries.
2. **Migrations**: Write idempotent migrations that support backward-compatible releases.
3. **Verification**:
   - Verify query plans eliminate sequential scans on large tables.
   - Test transactions under concurrent access with appropriate isolation levels (`READ COMMITTED`, `SERIALIZABLE`).

