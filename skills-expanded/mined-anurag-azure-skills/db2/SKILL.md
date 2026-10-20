---
name: "db2"
description: "IBM Db2 (LUW/z) database usage: SQL dialect, data types, identity/sequences, FETCH FIRST pagination, isolation/locking, db2jcc driver config, and Db2-correct DDL for Flyway migrations."
version: 1
created: "2026-06-09T03:34:24+05:30"
updated: "2026-06-26"
---
## When to Use
Use when tsa.technology.database.vendor = DB2 (or the legacy schema is Db2, e.g. OCP_* tables). Activate for relational persistence whose target engine is IBM Db2, especially when migrating legacy Db2 SQL/DDL and preserving an existing Db2 schema unchanged. Resolve language/framework from the TSA; this skill governs Db2-specific SQL/DDL/driver concerns that JPA does NOT abstract.

## Procedure
1. **Driver & connection**: Use the IBM driver `com.ibm.db2.jcc.DB2Driver` with a `jdbc:db2://host:50000/DBNAME` URL. Set `currentSchema` to the target schema/qualifier. Configure HikariCP (pool size, connectionTimeout, validation query `SELECT 1 FROM SYSIBM.SYSDUMMY1`). Externalize all of this; never hardcode.
2. **Hibernate dialect**: Set the JPA dialect to the matching Db2 dialect (e.g. `org.hibernate.dialect.DB2Dialect`/`DB2LUWDialect` for the target Db2 version) so generated SQL is Db2-correct.
3. **Data types**: Map to Db2 types — `VARCHAR(n)`, `CHAR(n)`, `CLOB`, `BLOB`, `DECIMAL(p,s)`, `INTEGER`/`BIGINT`, `TIMESTAMP`, `DATE`. There is no native JSONB; store JSON as `VARCHAR`/`CLOB` and use Db2 JSON functions (`JSON_VALUE`, `JSON_TABLE`) only where the Db2 version supports them.
4. **Identity & keys**: Use `GENERATED ALWAYS AS IDENTITY` or `SEQUENCE` objects (`NEXT VALUE FOR seq`). Do NOT assume Postgres `SERIAL` or MySQL `AUTO_INCREMENT`. Preserve legacy `OCP_*` key strategies when migrating.
5. **Pagination**: Use `FETCH FIRST n ROWS ONLY` (optionally `OFFSET n ROWS FETCH NEXT m ROWS ONLY`). Do NOT use `LIMIT/OFFSET` (Postgres/MySQL) — it is invalid Db2 SQL.
6. **Upsert / set ops**: Use `MERGE INTO ... USING ...` for upserts. Use `VALUES`/common-table-expressions for set-based work. Reference the catalog via `SYSCAT.*` / `SYSIBM.*` (e.g. dummy table `SYSIBM.SYSDUMMY1`).
7. **Isolation & locking**: Default isolation is Cursor Stability (CS). Choose deliberately (UR/CS/RS/RR); keep transactions short. Be aware of lock escalation and use `FOR READ ONLY` / `WITH UR` on read-only queries where appropriate to reduce contention.
8. **Migrations (Flyway)**: Write Db2-dialect DDL in the Flyway scripts (correct types, `GENERATED AS IDENTITY`, no Postgres-only constructs). Qualify objects with the schema. Keep DDL forward-only; large data operations separate from DDL. Validate that scripts run against the target Db2 version.
9. **Native queries / legacy SQL**: When migrating legacy Db2 SQL, preserve Db2 syntax/functions; translate only what the target Db2 version no longer supports. Prefer JPQL/Criteria for portable CRUD and reserve native Db2 SQL for vendor-specific needs.
10. **Maintenance awareness**: Generated schemas should be RUNSTATS/REORG-friendly; avoid designs that force frequent reorgs. Index for actual access patterns.

## Patterns
- Db2 identity columns / sequences (`GENERATED AS IDENTITY`, `NEXT VALUE FOR`)
- `FETCH FIRST n ROWS ONLY` (and OFFSET ... FETCH NEXT) for paging
- `MERGE INTO` for upserts
- `SYSIBM.SYSDUMMY1` for single-row selects; `SYSCAT.*` for catalog lookups
- Schema/qualifier set via `currentSchema`; objects fully qualified in DDL
- Hibernate DB2Dialect so ORM emits Db2-valid SQL
- `WITH UR` / `FOR READ ONLY` on read-heavy queries to cut locking

## Anti-Patterns
- Using `LIMIT/OFFSET` (Postgres/MySQL) — invalid in Db2
- `SERIAL` / `AUTO_INCREMENT` instead of Db2 identity/sequence
- Assuming `JSONB`/GIN indexes exist (they do not in Db2)
- Postgres/MySQL-only functions or types in DDL/native SQL
- Hardcoded Db2 URL/credentials instead of vault + externalized config
- Long-running transactions that trigger lock escalation
- Wrong/absent Hibernate dialect (ORM then emits non-Db2 SQL)
- Editing an already-applied Flyway migration (checksum break)

## Tool Selection
- Generic: read_file, write_file, command_line, skills
- Intended (roadmap): db2_ddl_generator, db2_sql_dialect_validator, legacy_db2_sql_translator

## Validation Rules
- All DDL/native SQL uses Db2 dialect (FETCH FIRST, identity/sequence, Db2 types)
- No `LIMIT/OFFSET`, `SERIAL`, `JSONB`, or other non-Db2 constructs present
- Hibernate dialect set to a Db2 dialect matching the target version
- Connection uses db2jcc driver + externalized URL/credentials + currentSchema
- Flyway scripts validated to apply on the target Db2 version
- Legacy Db2 schema (e.g. OCP_*) semantics preserved per the migration spec

## RAG Sources
- ibm-db2-sql-reference
- ibm-db2-knowledge-center
- hibernate-db2-dialect-docs
- flyway-db2-support
- tsa.technology.database (vendor=DB2) + legacy schema artifacts
