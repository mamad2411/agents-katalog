---
name: database-testing
description: Sets up fast, isolated tests against a real database engine - Testcontainers or CI service containers, per-test isolation (rollback, truncate, template databases), factories instead of large fixtures, migration tests, and tests for constraints, triggers, queries and query counts. Use when writing tests that touch a database, replacing an in-memory or SQLite test database, fixing slow or order-dependent database tests, or adding tests for migrations.
license: MIT
---

# Database Testing

Test against the same database engine and major version that production runs. In-memory substitutes (SQLite standing in for PostgreSQL, H2 for MySQL, ORM in-memory providers) accept queries production rejects and reject ones it accepts, and they don't enforce the same constraints, types or locking. Tests that pass on them prove little about the real system.

## When to use

- Writing integration tests for repositories, queries, ORM mappings or database logic.
- Moving off an in-memory or SQLite test database.
- Database tests are slow, flaky, or fail when run in a different order or in parallel.
- Adding a safety net for schema migrations.

Not for: unit tests of pure logic (no database at all; see test-strategy), load testing, or tuning production queries (sql-optimization).

## Workflow

1. **Match production**: same engine, same major version, same extensions. Pin the image tag (for example `postgres:16-alpine` if production is PostgreSQL 16).
2. **Provide the database** with Testcontainers in the test code, or a service container in CI. Examples per stack: [references/setup-examples.md](references/setup-examples.md).
3. **Build the schema with the real migrations**, not the ORM's "create all tables" shortcut, so the tests also prove the migrations work.
4. **Choose an isolation strategy** (table below) so every test starts from a known state and tests can run in any order.
5. **Create data per test with factories**, only what the test needs.
6. **Add migration tests and query-count assertions** for risky paths.
7. **Add a guard** so the test suite refuses to run against anything but a local or test database.

## Providing a real database

| Option | Good for | Notes |
|---|---|---|
| Testcontainers (Java, .NET, Go, Node, Python and others) | Tests that start their own database anywhere Docker runs | Start one container per test session or worker, not per test |
| CI service containers (GitHub Actions `services:`, GitLab `services:`) | Simple pipelines | Local runs need a matching local setup (compose file) |
| `docker compose` with a test profile | Teams that also run the app locally in Docker | Keep it separate from the dev database |
| Managed cloud test instance | Features you can't run in a container | Never share it with other environments |

Speed settings for **throwaway test PostgreSQL only** (they trade crash safety for speed): start the server with `-c fsync=off -c synchronous_commit=off -c full_page_writes=off`, and optionally keep the data directory on tmpfs. Never use these settings on any database that holds real data.

## Isolation strategies

| Strategy | How | Speed | Limits |
|---|---|---|---|
| Transaction rollback per test | Open a transaction before the test, roll back after (Django `TestCase`, Rails transactional tests, Spring `@Transactional` tests) | Fastest | Code under test can't commit or use other connections; misses commit-time behavior (deferred constraints, triggers on commit, `on_commit` hooks) |
| Truncate between tests | `TRUNCATE t1, t2 ... RESTART IDENTITY CASCADE` (PostgreSQL) after each test or class | Fast enough for most suites | Order of tables and foreign keys matters on some engines; reference data must be re-seeded |
| Template database per test or worker | Migrate once into `app_template`, then `CREATE DATABASE test_n TEMPLATE app_template` (PostgreSQL) | Fast clones | The template must have no open connections while cloning |
| Database or schema per parallel worker | Name it after the worker id (`app_test_gw3`) | Enables parallel runs | Combine with one of the strategies above inside each worker |
| Fresh container per test class | New container each time | Slow | Only for tests that change server-level settings |

Default: rollback per test for repository-level tests, truncate or template for tests that exercise code which commits, plus one database per worker when running in parallel.

## Test data

- **Factories or builders per test** (for example factory_boy, FactoryBot, Bogus, or plain builder functions). Each test creates exactly the rows it asserts on, with defaults for everything else.
- **Small, named reference data** (countries, plans) can be seeded once by a migration or a seed script that is part of the test setup.
- **No production dumps.** They contain personal data (see data-privacy-retention), are slow to load, and make tests depend on data nobody understands.
- **Don't depend on generated IDs, row order without `ORDER BY`, or the current time.** Use the IDs returned by the insert, add explicit ordering, and inject a fixed clock.

## Migration tests

1. **From empty**: apply every migration to an empty database and run the suite. Then check that the ORM's model and the migrated schema agree, using the tool's check command where it exists (for example `python manage.py makemigrations --check --dry-run`, `alembic check`, `prisma migrate diff`; check the docs for your tool).
2. **Upgrade from the last release**: restore the previous release's schema (and a little representative data), apply only the new migrations, and run smoke tests. This catches migrations that only work on an empty database.
3. **Down migrations**, if the project uses them: run up, down, up again.
4. **Data migrations and backfills**: test them with edge-case rows (NULLs, empty strings, duplicates, very long values, legacy formats), and assert the result, not only "no error".
5. **Slow migrations**: test duration and locking on a production-sized copy outside the unit test suite (see the database-migrations skill).

## What to test in the database itself

- **Constraints**: insert a duplicate and assert the unique violation; insert an orphan and assert the foreign key error; check CHECK constraints at their edges.
- **Triggers, functions, row-level security**: test as the role the application uses, with tenant settings applied exactly as the application sets them (for example `SET LOCAL app.tenant_id = '<tenant uuid>'` inside the test transaction, matching the policy in the database-schema-design skill), and assert that other tenants' rows are invisible.
- **Tricky queries**: time zones and daylight saving boundaries, NULL handling, pagination stability with ties, case sensitivity and collation.
- **Concurrency**: open two connections and assert that the lock or optimistic version check behaves as designed (two transactions decrementing the same stock must not both succeed).
- **Query counts**: assert the number of statements a code path runs, to stop N+1 regressions (see orm-patterns).

## Safety guard

Add a check that runs before any test touches the database and fails the run unless the target is clearly a test database, for example:

- the host is `localhost`, a container host, or a CI service name, and
- the database name ends in `_test`, and
- an explicit environment variable such as `APP_ENV=test` is set.

Tests truncate and drop tables. **Never point a test suite at a shared, staging or production database**, and stop and ask the user if the configured database looks like one.

## Anti-patterns

- **In-memory or SQLite substitutes** for a different production engine.
- **Schema built by the ORM's "create all"** instead of the migrations.
- **One giant shared fixture** that every test depends on and nobody can change.
- **Tests that depend on each other** or on run order (test B relies on rows from test A).
- **Asserting on auto-increment IDs** or unordered result order.
- **Restarting the database container for every test.**
- **Sleeping** to wait for the database instead of a readiness check (Testcontainers wait strategies, `pg_isready`, CI health checks).

## Done when

- Tests run against the production engine and major version, with the schema built from migrations.
- Each test creates its own data and passes in any order, alone, and in parallel.
- Migrations are tested from empty and as an upgrade from the previous release.
- Constraints, permissions and critical queries have direct tests; key paths have query-count assertions.
- The suite refuses to run against non-test databases.
- The database portion of the suite runs fast enough that developers run it before pushing.

## References

- [references/setup-examples.md](references/setup-examples.md) — read when wiring up the database for tests: Testcontainers in Java/Spring, Python, Node, .NET and Go, a GitHub Actions service container, and template-database and truncate helpers.
