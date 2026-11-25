---
name: oracle-database
description: Use when working on Oracle Database, Oracle SQL, PL/SQL, schema migrations, packages, procedures, functions, triggers, indexes, partitions, sequences, locks, JDBC/ODP.NET/oracledb connectivity, or Oracle-specific query behavior.
category: database
---

# Oracle Database

Use this skill when a service owns or touches Oracle Database behavior, not just generic SQL.

## Activation evidence

Apply this skill when any of these signals exist:

- Files use extensions such as .sql, .pls, .pks, .pkb, .prc, .fnc, .trg.
- Code imports or configures Oracle drivers such as oracledb, cx_Oracle, JDBC thin URLs, OracleDataSource, ODP.NET, or managed Oracle clients.
- Migrations mention Oracle, Liquibase/Flyway Oracle dialects, CREATE OR REPLACE, packages, procedures, functions, sequences, synonyms, materialized views, partitions, or tablespaces.
- Task text mentions PL/SQL, Oracle SQL, Oracle Database, RAC, ASM, Data Guard, AWR, explain plan, dbms_xplan, dbms_scheduler, or Oracle locking/performance behavior.

## Operating rules

- Do not assume PostgreSQL, MySQL, or SQL Server syntax works in Oracle.
- Preserve transaction boundaries, isolation assumptions, locking behavior, and commit/rollback ownership.
- Prefer bind variables and parameterized execution. Do not concatenate user input into SQL.
- Treat empty string and NULL behavior carefully because Oracle treats empty string as NULL in many SQL contexts.
- Handle pagination, sequences, identity columns, MERGE, date/time functions, CLOB/BLOB handling, and case sensitivity using Oracle-specific semantics.
- For schema changes, document compatibility, rollback path, data backfill strategy, lock risk, index impact, and deployment order.
- For query tuning, consider explain plans, index selectivity, histograms/statistics, bind peeking, partitions, join order, cardinality, and execution-plan regressions.
- For PL/SQL changes, keep package spec/body compatibility, explicit exception handling, bulk collect/forall for bulk operations, deterministic/idempotent DDL where possible, and clear error propagation.

## Expected output from coder agents

When a coder agent uses this skill, its implementation notes must include:

- Oracle objects changed: tables, views, packages, procedures, functions, triggers, indexes, sequences, grants, synonyms.
- Runtime code changed: repository/DAO/service files and driver configuration.
- Migration/deployment notes: ordering, rollback, data migration, lock risk, and environment assumptions.
- Manual or automated verification performed against Oracle behavior, or a clear reason why Oracle execution was not available.

## Skill composition

Use this skill together with complementary skills rather than alone:

- Pair with query-expert for query correctness and SQL review.
- Pair with database-architect for schema/data-model design.
- Pair with database-optimizer for performance-sensitive SQL or indexing work.
- Pair with discover-database during onboarding to detect database ownership and dialect.
- Pair with oracle-cloud only when OCI infrastructure, networking, managed database, deployment, or cloud operations are in scope.
- Pair with java-architect, spring-boot-engineer, aspnet-core, nodejs-backend-patterns, fastapi-python, or other language/framework skills based on the service runtime.
