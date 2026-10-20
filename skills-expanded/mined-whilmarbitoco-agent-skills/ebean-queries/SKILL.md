---
name: ebean-queries
description: >
  Extends agent's knowledge of building Ebean queries: type-safe expression
  lists, fetch paths, raw SQL, named queries, and batch operations.
  Use when writing queries, optimizing N+1 issues, or debugging query results.
compatibility: Java 21+
metadata:
  domain: persistence
  level: intermediate
  stack: [java-21, ebean-15]
  version: "1.0.0"
---

# Ebean Queries

Ebean provides a fluent, type-safe API via expression lists, plus raw SQL
fallbacks, named queries, and batch operations for bulk processing.

## Concepts

- **`ExpressionList<T>`** — chainable query filters with compile-time field reference
- **`fetch()` / `fetchLazy()`** — control eager/lazy loading of relationships
- **`orderBy()`** — sort by entity properties
- **`setMaxRows()` / `setFirstRow()`** — pagination
- **`RawSql`** — raw SQL mapped to entities or DTOs
- **`@NamedQuery`** — pre-defined query for reuse
- **`SqlQuery`** — raw SQL returning `SqlRow` maps
- **`findEach()`** — streaming iteration for batch processing

## Rules

1. Use `ExpressionList` for all standard queries — never string-based JPQL.
2. Control N+1 with explicit `fetch()` and `fetchLazy()` paths.
3. Use `findEach()` (not `findList()`) for processing > 1000 rows.
4. Paginate with `setFirstRow()` + `setMaxRows()` — never load entire tables.
5. Use `RawSql` only for complex aggregations or native SQL features.
6. Use SLF4J parameterized logging for query debugging — not `toString()`.
7. Close cursors from `findEach()` implicitly via try-with-resources.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- ebean-setup — configuration
- ebean-entities — entity mapping
- sqlite-best-practices — SQLite query optimization
