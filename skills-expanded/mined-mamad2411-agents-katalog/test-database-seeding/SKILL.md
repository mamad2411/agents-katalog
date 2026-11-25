---
name: test-database-seeding
category: testing
description: Use when a test needs a database - spin up a dedicated, disposable test database (Testcontainers) seeded with known data, never a shared or production database
enabled: false
---
# Test Database Seeding

## Overview

Automated tests need a database that is real (same engine as production), isolated (no shared state), and seeded with known data. The answer is a disposable, per-run database — Testcontainers spins up a real Postgres in a container, migrated and seeded, torn down after.

**Core principle:** Real engine, disposable instance, known seed. Never point tests at a shared dev or production database, and never use an in-memory substitute whose SQL differs from production.

## Why not the alternatives

| Approach | Problem |
|----------|---------|
| Shared dev/staging DB | Flaky: other work mutates it; tests collide and depend on order |
| Production DB | Never — data risk, and tests would mutate real records |
| In-memory (H2/SQLite) | Dialect gaps: queries pass in H2, fail on Postgres → bugs ship |
| Disposable real DB (Testcontainers) | ✅ real engine, isolated, reproducible |

## The Pattern

1. **Start a real DB container** for the suite (Testcontainers): `postgres:<same-major-as-prod>`.
2. **Run the real migrations** against it — the same migration files the app uses, so the schema is production-accurate.
3. **Seed known fixtures**: insert the exact rows the scenario needs (a project, N tasks, a user with a role). Keep fixtures small and explicit — a test asserting "3 tasks" seeds exactly 3.
4. **Isolate per test:** each test either runs in a transaction rolled back at the end, or truncates/reseeds between tests. No test sees another's data.
5. **Point the app/config** at the container's connection string for the run.
6. **Tear down** automatically when the suite ends.

## Worked Example

```java
@Testcontainers
class TaskExportIT {
    @Container static PostgreSQLContainer<?> db =
        new PostgreSQLContainer<>("postgres:16");

    @BeforeAll static void migrate() { Flyway.configure().dataSource(db.getJdbcUrl(),
        db.getUsername(), db.getPassword()).load().migrate(); }   // real migrations

    @BeforeEach void seed() {
        // exactly the rows this scenario needs
        insertProject("p1", "Demo");
        insertTasks("p1", 3);
    }

    @Test void export_returns_all_tasks() {
        var csv = export("p1");
        assertEquals(3, csvRows(csv));   // asserts against the known seed
    }
}
```

Same idea in Go (Testcontainers-Go), Node (testcontainers), etc. — a real Postgres, real migrations, explicit seed.

## Rules

- The container's engine and MAJOR version match production. No dialect gambling.
- Migrations come from the app, not a hand-written schema — a stale test schema hides real migration bugs.
- Seeds are explicit and minimal; assertions reference the seeded values.
- Each test is independent (transaction rollback or reseed) and order-independent.
- Combine with test-doubles-wiremock: real DB, stubbed external HTTP.

## Common Mistakes

- Pointing tests at a shared dev database → collisions and flakiness.
- H2/SQLite instead of the real engine → dialect bugs ship green.
- Hand-maintained test schema that drifts from the real migrations.
- Tests that leave data behind and only pass in a specific order.

## Red Flags

- A test fails when run alone but passes in the suite (or vice versa) → shared/leftover state.
- The test DB schema was created by a script other than the app's migrations.
- Query passes in tests but fails in production → you tested a different engine.
