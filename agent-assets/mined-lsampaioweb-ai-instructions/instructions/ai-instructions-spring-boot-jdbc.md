---
description: "Spring Boot JDBC contract for JdbcClient, externalized SQL, transactions, generated keys, and DBA-owned DDL."
applyTo: "**/*Repository*.java, **/db/**/*.java, **/sql/**, **/application*.yml, **/application*.yaml, **/pom.xml"
---

# Spring Boot JDBC Contract

These rules apply to real applications that use relational databases through
Spring JDBC. Architecture already forbids JPA; this file owns how JDBC is done.

Exception handling, i18n, packaging, and pom coordinate rules stay in their own
instruction files. Do not restate those contracts here.

## Dependencies

- Use `spring-boot-starter-jdbc` plus the matching JDBC driver (for example
  `org.postgresql:postgresql`) and an explicit `com.zaxxer:HikariCP` runtime
  dependency. Dependency comments, ordering, and the JPA ban are owned by the pom
  contract.

## Access API

- Use Spring `JdbcClient` for ordinary reads and writes.
- Use `NamedParameterJdbcTemplate` only when you need APIs `JdbcClient` does not
  cover cleanly (for example multi-row `batchUpdate`).
- Keep `JdbcClient` and JDBC templates inside repository implementations
  (architecture contract).
- Prefer the Boot-provided `JdbcClient` bean. Load SQL with `@PropertySource` on
  a dedicated config class; do not recreate `JdbcClient` unless auto-config is
  disabled.

## SQL location and shape

- Store DML statements in `classpath:sql/{feature}.xml` (Java properties DTD)
  and bind them to a feature `@ConfigurationProperties` record
  (for example `sql.users.find-by-id`).
- Use named parameters only (`:id`, `:name`). Do not use `?` placeholders in new
  SQL.
- Keep domain models as plain records with no JDBC or ORM annotations.
- Do not bury SQL strings as Java constants in real applications.

## Generated keys and updates (PostgreSQL)

- When an insert must return the new row, use `INSERT … RETURNING …` and map the
  result with `JdbcClient` (`.query(…).single()`). Do not invent primary keys in
  Java.
- Prefer `RETURNING` on updates when the caller needs the persisted row.

## Lookups, paging, and dynamic SQL

- Single-row repository lookups return `Optional`. The service turns empty into
  a feature `AppException` (exception contract). Do not return `null` from
  repositories.
- Unbounded collection reads that page in SQL use `COUNT` plus `LIMIT`/`OFFSET`
  (or the database equivalent) with Spring `Pageable`/`Page`.
- When building dynamic `ORDER BY`, allowlist column names. Never concatenate
  raw client sort fields into SQL.

## Transactions

- Put `@Transactional` on the service implementation, never on the repository.
- Use `@Transactional(readOnly = true)` for read-only service methods.

## Failures

- Unexpected JDBC or infrastructure failures become a shared `DatabaseException`
  that extends `AppException` with status `500` and an i18n message key.
- Expected misses and business rule failures stay feature exceptions
  (`UserNotFoundException`, `InsufficientBalanceException`, and so on).

## Datasource configuration

- Bind URL, username, and password from environment variables (configuration
  contract for secrets).
- Configure Hikari pool settings in `application.yml` (`maximum-pool-size`,
  `minimum-idle`, timeouts).

## Schema and privileges (DDL vs DML)

- The application database user has **DML only**. It must not create, alter, or
  drop schema objects.
- Keep DDL scripts in the repository under `sql/db/` (or an equivalent folder)
  so they are versioned in git for DBAs. DBAs apply those scripts through the
  PostgreSQL client or their change process.
- Never run DDL from the application at startup or runtime.
- Never use `spring.sql.init`, Flyway, Liquibase, or any in-app migration runner.

## Forbidden

- Never put SQL string constants in Java for real-app DML (use `classpath:sql`).
- Never use positional `?` placeholders in new SQL.
- Never put `@Transactional` on a repository.
- Never return `null` from a single-row repository lookup.
- Never concatenate unvalidated client input into SQL (including `ORDER BY`).
- Never enable `spring.sql.init`, Flyway, or Liquibase.
- Never grant or rely on DDL privileges for the application database user.
- Never invent primary keys in Java when the database can return them.
