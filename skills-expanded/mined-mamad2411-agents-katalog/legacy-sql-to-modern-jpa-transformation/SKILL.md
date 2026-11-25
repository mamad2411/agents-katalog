---
name: "legacy-sql-to-modern-jpa-transformation"
description: "Transform legacy SQL (stored procedures, views, dynamic SQL, native queries) to modern Spring Data JPA/JPQL with proper schema mapping, parameterization, and type safety. Target datastore, dialect, and migration tool are resolved from the TSA (e.g. DB2 via JPA/Hibernate + Flyway). Use with Database Implementation agents."
version: 2
created: "2026-06-09T03:34:24+05:30"
updated: "2026-06-26"
---
## When to Use
Use this skill when:
- Migrating legacy database access (e.g. IBM WEF / DB2 native SQL, stored procedures, dynamic SQL, cursors) to modern Spring Data JPA repositories.
- A Database agent needs to replace stored procedures / hand-built SQL with JPA repositories + JPQL.
- Converting dynamic SQL strings to type-safe, parameterized JPQL queries.
- Mapping legacy views/functions to JPA entity graphs.
- Creating migrations from legacy DDL using the TSA migration tool.
- **Target architecture is resolved from the TSA:** Spring Data JPA on `tsa.technology.database.vendor` (e.g. DB2) with `tsa.technology.database.migration_tool` migrations (e.g. Flyway). Defer vendor-specific SQL/DDL concerns to the matching DB skill (db2/oracle/postgresql/mongodb).

## Procedure
1. STEP 1: Analyze Legacy SQL Pattern - Identify the legacy pattern (stored procedure, dynamic SQL, view, cursor logic, temp tables). Extract inputs (parameters), outputs (result sets/columns), business logic, joins, filters, sorting. Document the legacy schema: table names, column names, data types, relationships (even if not enforced). For the reset-password migration the legacy engine is **DB2** with the existing `OCP_*` tables — preserve those names/semantics per `tsa.migration`.
2. STEP 2: Design Target Schema - Map legacy tables to the target schema on `tsa.technology.database.vendor`. **Preserve the legacy schema where the TSA requires functional parity** (e.g. DB2 `OCP_*` tables unchanged); add constraints (PRIMARY KEY, FOREIGN KEY, NOT NULL, UNIQUE) only where they do not break parity. Add a tenant-isolation column **only if the TSA declares multi-tenancy** (the reset-password TSA is single-tenant — do NOT add tenant_id). Decide entity relationships (`@ManyToOne`, `@OneToMany`) with `FetchType.LAZY`. Create the schema migration with the TSA migration tool: Flyway `V<n>__<description>.sql` (CREATE/ALTER TABLE, CREATE INDEX, comments) in `src/main/resources/db/migration/`.
3. STEP 3: Create JPA Entities - Map each target table to an `@Entity` with `@Table(name=..., schema=...)` matching the resolved schema/qualifier. Use `@Getter`/`@Setter` (NEVER `@Data` on entities). Add `@Column(name=...)` matching exact DB column names. Use `FetchType.LAZY` on ALL relationships. Use `@EqualsAndHashCode(onlyExplicitlyIncluded = true)` with `@EqualsAndHashCode.Include` on the `@Id`/business key only. Add a tenant column only if the TSA declares tenancy.
4. STEP 4: Transform SQL Logic to JPQL - Convert legacy SELECTs with table joins to JPQL with entity joins (`LEFT JOIN entity.relationship`, not `LEFT JOIN table_name`). Replace dynamic SQL parameters with named JPQL parameters (`:param`). Convert CASE/COALESCE/aggregates to JPQL equivalents, or a native query (vendor dialect) where JPQL is insufficient. Replace cursors/loops with batch queries or `Stream<Entity>`. Convert temp tables to `@Transient` fields or separate queries.
5. STEP 5: Create Repository Interfaces - Extend `JpaRepository<Entity, ID>` for CRUD. Create a `CustomRepository` interface for complex queries (replacing stored procedures) with `CustomRepositoryImpl` using `@PersistenceContext EntityManager`. Use `@Query` (JPQL) for reads, `@Modifying` for writes, `@Param` for named params. Use DTO projections (JPQL constructor expressions) for read-only result sets.
6. STEP 6: Handle Legacy SQL Idioms - String concatenation → `CONCAT()` or Java in the service layer. `ISNULL`/`NVL`/`COALESCE` → JPQL `COALESCE` or Java `Optional`. Date conversions → Java `DateTimeFormatter` in the service layer. Dynamic `ORDER BY` → Spring Data `Pageable`/`Sort`. String-based `IN` clauses → `List<T>` parameters. Stored-proc calls → custom repository method (`@Query` or `@Procedure`). **For vendor-specific paging/upsert use the target dialect** (e.g. DB2 `FETCH FIRST n ROWS ONLY` and `MERGE INTO`, NOT `LIMIT/OFFSET`) — see the db2v2 skill.
7. STEP 7: Map Legacy Data Types to the Target Vendor - Map legacy types to `tsa.technology.database.vendor` types. **For DB2:** `VARCHAR(n)`/`CHAR(n)`, `CLOB` (large text), `BLOB`/`VARBINARY` (binary), `DECIMAL(p,s)` (money), `INTEGER`/`BIGINT`, `TIMESTAMP`, `DATE`; there is no native `JSONB` — store JSON as `VARCHAR`/`CLOB` and use DB2 JSON functions only where supported. Use `GENERATED ALWAYS AS IDENTITY` or a `SEQUENCE` for keys (not `SERIAL`/`AUTO_INCREMENT`). Do not assume Postgres-only types.
8. STEP 8: Create Migration Mapping Documentation - Document legacy→target mapping: legacy_table → target_entity, legacy_sp → repository_method, legacy_column → entity_field. Include performance notes (indexes on FKs and frequent predicates; N+1 prevention with `@EntityGraph`). Add a rollback note. Document any business logic moved from SQL to the Java service layer.

## Pitfalls
- DO NOT use table names in JPQL — use entity names and relationship navigation (e.g. `FROM User u LEFT JOIN u.profile p`, not `FROM ocp_up u LEFT JOIN ...`).
- DO NOT use `FetchType.EAGER` — always `LAZY` to prevent N+1; use explicit fetch joins/`@EntityGraph`.
- DO NOT put `@Data` on `@Entity` classes — use `@Getter`/`@Setter` + `@EqualsAndHashCode(onlyExplicitlyIncluded = true)` to avoid lazy-loading/proxy issues.
- DO NOT silently restructure a legacy schema the TSA requires preserved — for functional-parity migrations (e.g. DB2 `OCP_*`), keep names/semantics; normalize only where parity allows.
- DO NOT add tenant columns/filters unless the TSA declares multi-tenancy.
- DO NOT use string concatenation for SQL parameters — always named parameters (`@Param`) to prevent SQL injection.
- DO NOT push complex business rules into SQL/JPQL — they belong in the Java service layer.
- DO NOT forget indexes on foreign keys and frequent predicates.
- DO NOT use native SQL unless necessary — prefer JPQL for portability/type-safety; reserve native SQL for vendor-specific needs and write it in the target dialect (e.g. DB2).
- DO NOT assume legacy types match the target — map deliberately to the target vendor's types (DB2: see Step 7), not Postgres-only types like `JSONB`/`BYTEA`/`SERIAL`.
- DO NOT use the wrong migration tool — use the TSA tool (e.g. Flyway `V<n>__*.sql`), and never edit an applied migration.
- DO NOT ignore legacy comments/documentation — stored-proc comments often hold business rules not obvious from the SQL.

## Verification
1. Schema migration runs successfully with the TSA migration tool (e.g. `mvn flyway:migrate` / Flyway validate); target DB has all tables/columns/indexes/constraints.
2. Entities compile and map correctly: `mvn clean compile`; no JPA validation errors with `spring.jpa.hibernate.ddl-auto=validate`.
3. JPQL queries return the same results as the legacy SQL: compare row counts, values, and sort order via integration tests with Testcontainers (vendor image per `tsa.technology.database.vendor`, e.g. Db2, or H2 for fast slices).
4. No N+1 queries: enable `spring.jpa.show-sql=true`; confirm a single query (or explicit batch), not N+1 selects.
5. Parameterization prevents SQL injection: test with malicious input (`'; DROP TABLE--`); the parameterized query rejects it safely.
6. Performance: compare legacy vs JPQL execution time; verify indexes are used (vendor `EXPLAIN`).
7. Tenancy (only if declared): if the TSA defines tenancy, queries filter by the tenant key; otherwise no tenant filtering exists.
8. Integration tests: `@DataJpaTest` with Testcontainers for the target vendor; all repository methods verified against expected DTOs.

## RAG Sources
- tsa.technology.database (vendor, access, migration_tool) / tsa.migration / tsa.domain
- jakarta-persistence-spec
- spring-data-jpa-docs
- pair with the db2v2 (or matching vendor) and flywayv2 skills
