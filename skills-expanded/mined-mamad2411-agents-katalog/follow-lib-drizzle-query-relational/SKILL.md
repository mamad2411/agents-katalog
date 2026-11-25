---
name: follow-lib-drizzle-query-relational
description: Drizzle relational queries — db.query API, with/columns/extras, nested selects, joins vs RQB
argument-hint: "[scope]"
related:
  - follow-lib-drizzle
  - run-test
  - resolve-errors
---

## Goal

Use the Drizzle Relational Query Builder (RQB) — `db.query.<table>` API, `with`/`columns`/`extras`, nested relations, pagination

## Scope

`db.query` API (schema-first nested fetching) vs SQL-style `select().from().leftJoin()` — selection strategies, N+1 avoidance, pagination

## Execute

### 1. RQB Basics

```ts
const db = drizzle(client, { schema })   // schema required for db.query API

await db.query.users.findMany()
await db.query.users.findFirst({ where: eq(users.email, email) })
await db.query.users.findMany({
  where: and(eq(users.active, true), gt(users.createdAt, cutoff)),
  orderBy: [desc(users.createdAt)],
  limit: 20, offset: 40,
})
```

### 2. Selection And Relations

```ts
await db.query.users.findMany({
  columns: { id: true, email: true },          // pick cols (false = exclude)
  extras: { lowerEmail: sql`lower(${users.email})`.as('lower_email') },
  with: {
    posts: {
      columns: { title: true },
      with: { comments: { limit: 5 } },        // nested
      orderBy: [desc(posts.createdAt)],
    },
  },
})
```

- `with` = auto-join + nested structure — RQB generates separate optimized queries, not N+1
- `columns`/`where`/`orderBy`/`limit`/`offset` usable in nested levels
- `extras` — computed SQL fields into the result type

### 3. When To Use SQL-Style Instead

```ts
// joins manual, aggregations, unions, subqueries → select() API
await db.select({ u: users, count: count(posts.id) })
  .from(users).leftJoin(posts, eq(posts.authorId, users.id))
  .groupBy(users.id)
```

- RQB: entity graphs, nested fetching; `select()`: aggregations/reporting/complex joins/unions
- `count()`, `avg()`, `sum()`, `sql<>` raw expressions, `getViewSelectedFields`

### 4. Pagination Patterns

- Offset: `limit`+`offset` (simple); cursor: `where(gt(id, cursor))` + `limit` + orderBy (scalable)
- RQB `limit` in `with` levels = per-parent limit (v0.31+ `limit` semantics — check the docs version)

## Rules

- `db.query` requires `drizzle(client, { schema })` — no schema → RQB unusable
- `with` requires complete `relations()` in the schema — no relations → error
- Choose RQB vs select(): nested entity graphs → RQB; manual aggregations/joins → `select()`
- `extras` SQL must be parameterized — the `sql` template is safe, never string concat

## Expected Outcome

- RQB nested queries work against the schema relations
- Know the boundary between RQB vs SQL-style selection
