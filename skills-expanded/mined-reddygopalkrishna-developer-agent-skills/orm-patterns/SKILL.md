---
name: orm-patterns
description: Writes efficient, correct data access code with ORMs (Prisma, Hibernate/JPA, EF Core, SQLAlchemy, Django ORM, ActiveRecord) - finding and fixing N+1 queries, eager vs lazy loading, transaction boundaries, bulk operations, safe raw SQL and optimistic locking. Use when writing or reviewing ORM queries, when an endpoint issues too many queries, on LazyInitializationException or detached-entity errors, or when choosing between ORM and raw SQL.
license: MIT
---

# ORM Patterns

An ORM hides the SQL, not the cost of it. Before judging any ORM code, look at the SQL it actually sends and how many statements one request runs. Most ORM performance bugs are a loop that issues one query per row (N+1), loading far more columns or rows than needed, or a transaction held open across slow work.

## When to use

- Writing or reviewing repository/model code that loads related data.
- An endpoint or job is slow and the logs show many similar queries.
- Errors such as `LazyInitializationException`, "detached instance", `MissingGreenlet` (SQLAlchemy async), or unexpected extra queries in templates and serializers.
- Bulk imports, mass updates, concurrent edits to the same record.

Not for: reading query plans and designing indexes (use sql-optimization), schema migrations (use database-migrations), pool and server tuning (use postgres-operations).

## Workflow

1. **Turn on SQL logging in development** (one line per ORM in [references/orm-cheatsheet.md](references/orm-cheatsheet.md)) and run the code path once.
2. **Count the statements.** The same query repeated with different IDs is an N+1. A request that runs more than a handful of queries needs a reason.
3. **Fix the loading strategy** for that code path (table below), not globally.
4. **Select only what you need.** Project to the columns or DTO the caller uses; skip change tracking for read-only paths.
5. **Lock it in with a test** that asserts the query count for the code path, so the N+1 cannot come back silently.
6. **Check the SQL again**, and for heavy queries hand the final SQL to the sql-optimization skill to check the plan.

## N+1: detect and fix

```text
orders = Order.all()            -- 1 query
for order in orders:
    print(order.customer.name)  -- +1 query per order  => N+1
```

| ORM | Load a single related object (many-to-one) | Load a collection (one-to-many) | Stop silent lazy loads |
|---|---|---|---|
| Prisma | `include: { customer: true }` | `include: { items: true }` | No lazy loading; relations load only when included |
| Hibernate / JPA | `JOIN FETCH o.customer` or `@EntityGraph` | `JOIN FETCH` (one collection per query) or batch fetching (`@BatchSize`, `hibernate.default_batch_fetch_size`) | Keep associations `LAZY`; disable open-session-in-view |
| EF Core | `.Include(o => o.Customer)` | `.Include(o => o.Items)` plus `.AsSplitQuery()` for several collections | Don't enable lazy-loading proxies |
| SQLAlchemy | `joinedload(Order.customer)` | `selectinload(Order.items)` | `raiseload("*")` or `lazy="raise"` on relationships |
| Django | `select_related("customer")` | `prefetch_related("items")` | Assert query counts in tests |
| ActiveRecord | `includes(:customer)` / `eager_load` | `includes(:items)` / `preload` | `strict_loading` |

Rules of thumb:

- **JOIN for to-one, separate IN-query for to-many.** Joining a collection multiplies rows (one row per child), and joining two collections multiplies them together (a cartesian explosion). Use the "select in" / "prefetch" / "split query" strategy for collections.
- **Never paginate a query that joins a collection.** The limit applies to joined rows, so the ORM either returns wrong pages or (Hibernate) paginates in memory. Page the parent IDs first, then load children for those IDs.
- **Serializers and templates trigger lazy loads too.** Load everything the response needs before rendering, then fail fast on any lazy load.

## Read paths

- Project to what the caller needs: `select` (Prisma), DTO/constructor queries (JPA), `.Select(...)` (EF Core), `load_only` or selecting columns (SQLAlchemy), `.only()` / `.values()` (Django), `.select(...)` / `pluck` (ActiveRecord).
- Turn off change tracking for read-only work: `AsNoTracking()` (EF Core), `@Transactional(readOnly = true)` or read-only query hints (Hibernate).
- Iterate large result sets in batches or streams (`find_each`, `iterator()`, `yield_per`, keyset pagination). Never load a whole large table into memory.
- `count()` or `exists()` instead of loading rows to check emptiness.

## Write paths

| Task | Do | Avoid |
|---|---|---|
| Insert many rows | Bulk insert (`createMany`, `bulk_create`, `insert_all`, batched `SaveChanges`, JDBC batching) | One `save()` per row in a loop |
| Update many rows by a condition | Set-based update (`updateMany`, `QuerySet.update()`, `ExecuteUpdate`, `update_all`, SQLAlchemy `update()`) | Load every row, change it, save it |
| Increment a counter | Atomic expression (`F("count") + 1`, `{ increment: 1 }`, SQL `SET n = n + 1`) | Read, add in code, write back (lost updates) |
| Upsert | The ORM's upsert / `ON CONFLICT` support | Select-then-insert (races under concurrency) |

Set-based updates usually skip model callbacks, validations and in-memory state. Check what the code relied on before switching.

## Transactions

- **Keep transactions short.** Open them around the database work only. No HTTP calls, emails, message publishing, file uploads or user waits inside a transaction: they hold locks and connections, and they can't be rolled back anyway.
- For "save and then notify", write an outbox row in the same transaction and publish afterwards (see the resilience-patterns skill).
- Know your ORM's default: some wrap each request in a transaction, some autocommit each statement. Make the boundary explicit in services that do several writes.
- Don't catch and swallow database exceptions inside a transaction and keep going; on PostgreSQL the transaction is aborted and every following statement fails.

## Concurrency: optimistic locking

When two users can edit the same record, add a version column so the second writer gets a conflict instead of silently overwriting:

| ORM | Mechanism | Conflict error |
|---|---|---|
| JPA / Hibernate | `@Version` field | `OptimisticLockException` |
| EF Core | `[ConcurrencyCheck]` or a `[Timestamp]` / row version property | `DbUpdateConcurrencyException` |
| ActiveRecord | `lock_version` column | `ActiveRecord::StaleObjectError` |
| Django, SQLAlchemy, Prisma | `UPDATE ... WHERE id = ? AND version = ?` and check the affected row count (SQLAlchemy also has `version_id_col`) | Your own error when 0 rows changed |

Return the conflict to the caller (HTTP 409 or 412) so they can reload; don't retry blindly. Use pessimistic locks (`SELECT ... FOR UPDATE`) only for short critical sections such as reserving stock (see the concurrency-patterns skill).

## Raw SQL safely

Raw SQL is fine when the ORM produces a bad query; keep it parameterized:

- Prisma: `` prisma.$queryRaw`SELECT ... WHERE id = ${id}` `` is parameterized. `$queryRawUnsafe` with string building is not.
- EF Core: `FromSql($"... {id}")` / `FromSqlInterpolated` are parameterized. `FromSqlRaw` with concatenated strings is not.
- SQLAlchemy: `text("... WHERE id = :id")` with `{"id": id}`.
- Django: `Model.objects.raw("... WHERE id = %s", [id])` or `cursor.execute(sql, [id])`. Never f-strings.
- JPA: named or positional parameters (`:id`, `?1`), never concatenation.
- ActiveRecord: `where("name = ?", name)`.

Identifiers (table or column names, sort direction) cannot be parameters: map user input to an allowlist.

## Migrations generated by the ORM

Always print and read the SQL before it ships (`prisma migrate dev --create-only`, `dotnet ef migrations script`, `python manage.py sqlmigrate`, `alembic upgrade head --sql`, Rails `db:migrate` output or `structure.sql` diff). Generated migrations can drop and recreate columns on a rename or lock big tables. Apply the database-migrations skill.

## Anti-patterns

- **Making associations eager globally** to fix one N+1. Every other query now loads data it doesn't need. Fix the loading per query.
- **Open session in view** (Spring's `spring.jpa.open-in-view`, enabled by default) hiding lazy loads during rendering. Disable it and load data explicitly in the service.
- **Fetching entities to return a count or a few fields.**
- **Save in a loop** for bulk work.
- **Read-modify-write** for counters and balances.
- **Network calls inside transactions.**
- **Trusting the ORM's migration diff** without reading the SQL.
- **Unparameterized raw SQL** "just for this one admin query".

## Done when

- SQL logging shows a fixed, small number of queries for the code path, independent of the number of rows.
- A test asserts that query count.
- Read paths select only needed columns; read-only paths skip change tracking.
- Bulk and counter writes are set-based or atomic.
- Transactions contain only database work; concurrent edits are protected by a version check or a deliberate lock.
- Any raw SQL is parameterized.

## References

- [references/orm-cheatsheet.md](references/orm-cheatsheet.md) — read for the exact syntax per ORM: SQL logging, eager loading, projections, bulk writes, query-count assertions and pool settings.
