---
name: kysely-querying
description: "Kysely SELECT queries: joins, WHERE filters, boolean expressions (eb.or/eb.and), aggregates (count/sum/avg), subqueries, ordering, pagination, $if conditionals. NOT for CTEs, window functions, CASE, JSON ops, or raw SQL — use kysely-advanced-sql."
---

# Kysely SELECT Queries, Joins & Expressions

Type-safe query building patterns for Kysely. All builders are **immutable** — every method returns a new instance.

## Decision Tree

| Need | Pattern |
|---|---|
| All columns | `db.selectFrom('t').selectAll()` |
| Specific columns | `.select(['col1', 'col2'])` |
| Filtered rows | `.where('col', '=', value)` |
| Joined tables | `.innerJoin('t2', 't2.fk', 't1.pk')` |
| Complex expressions | `.where((eb) => eb.or([...]))` |
| Aggregates | `.select((eb) => eb.fn.count('id').as('n')).groupBy(...)` |
| Subquery in select | `.select((eb) => eb.selectFrom('t2')...as('alias'))` |
| Subquery in where | `.where('col', 'in', db.selectFrom('t2').select('col'))` |
| No FROM clause | `db.selectNoFrom((eb) => [...])` |

## Canonical Patterns

### Basic SELECT

```ts
// All columns
const rows = await db.selectFrom('person').selectAll().execute()

// Specific columns
const rows = await db.selectFrom('person')
  .select(['id', 'first_name'])
  .execute()

// Table-qualified (important in joins)
const rows = await db.selectFrom('person')
  .select(['person.id', 'person.first_name'])
  .execute()

// Aliased columns — 'col as alias' string syntax
const rows = await db.selectFrom('person')
  .select(['first_name as fn', 'person.last_name as ln'])
  .execute()

// selectAll with table arg (use in joins to avoid ambiguity)
const rows = await db.selectFrom('person')
  .innerJoin('pet', 'pet.owner_id', 'person.id')
  .selectAll('person')  // person.* only
  .execute()
```

### WHERE Clauses

```ts
// Equality
.where('first_name', '=', 'Jennifer')

// Comparison operators: =, !=, <, <=, >, >=, like, in, is, is not
.where('age', '>', 18)
.where('id', 'in', [1, 2, 3])
.where('name', 'like', '%son')

// Null checks
.where('deleted_at', 'is', null)
.where('email', 'is not', null)

// Multiple where calls are ANDed
.where('first_name', '=', 'Jennifer')
.where('age', '>', 40)

// Column-to-column comparison
.whereRef('person.first_name', '=', 'pet.name')
```

### Boolean Composition with ExpressionBuilder

```ts
// OR
.where((eb) => eb.or([
  eb('first_name', '=', 'Jennifer'),
  eb('first_name', '=', 'Arnold'),
]))

// AND (explicit)
.where((eb) => eb.and([
  eb('age', '>', 18),
  eb('age', '<', 65),
]))

// NOT + EXISTS
.where((eb) => eb.not(eb.exists(
  eb.selectFrom('pet')
    .select('pet.id')
    .whereRef('pet.owner_id', '=', 'person.id')
)))

// Object filter shorthand (all equality, ANDed)
.where((eb) => eb.and({
  first_name: 'Jennifer',
  last_name: 'Aniston',
}))

// Chained .or() on expression
.where((eb) =>
  eb('last_name', '=', 'Aniston').or('last_name', '=', 'Stallone')
)

// between
.where((eb) => eb.between('age', 18, 65))
```

### Joins

```ts
// Inner join — simple column references
db.selectFrom('person')
  .innerJoin('pet', 'pet.owner_id', 'person.id')
  .select(['person.id', 'pet.name as pet_name'])

// Left join — joined columns become NULLABLE in output type
db.selectFrom('person')
  .leftJoin('pet', 'pet.owner_id', 'person.id')
  .select(['person.id', 'pet.name'])  // pet.name: string | null

// Right join — left table columns become nullable
// Full join — both sides become nullable

// Cross join — cartesian product, no ON clause
db.selectFrom('person')
  .crossJoin('pet')
  .selectAll()

// Aliased join table
db.selectFrom('person')
  .innerJoin('pet as p', 'p.owner_id', 'person.id')
  .select(['person.id', 'p.name'])

// Complex ON clause with callback
db.selectFrom('person')
  .innerJoin('pet', (join) => join
    .onRef('pet.owner_id', '=', 'person.id')
    .on('pet.name', '=', 'Doggo')
    .on((eb) => eb.or([
      eb('person.age', '>', 18),
      eb('person.age', '<', 100),
    ]))
  )
  .selectAll()

// Subquery join
db.selectFrom('person')
  .innerJoin(
    (eb) => eb.selectFrom('pet')
      .select(['owner_id as owner', 'name'])
      .where('name', '=', 'Doggo')
      .as('doggos'),
    (join) => join.onRef('doggos.owner', '=', 'person.id'),
  )
  .selectAll('doggos')
```

### ExpressionBuilder (eb) in SELECT

```ts
db.selectFrom('person')
  .select(({ eb, selectFrom, or, val, lit, fn, ref }) => [
    'person.id',

    // Correlated subquery
    selectFrom('pet')
      .select('pet.name')
      .whereRef('pet.owner_id', '=', 'person.id')
      .orderBy('pet.name')
      .limit(1)
      .as('first_pet_name'),

    // Boolean expression
    or([
      eb('first_name', '=', 'Jennifer'),
      eb('first_name', '=', 'Arnold'),
    ]).as('is_jennifer_or_arnold'),

    // Aggregate via eb.fn (query-scoped, type-safe)
    fn.count<number>('pet.id').as('pet_count'),

    // Static value / literal
    val('hello').as('greeting'),
    lit(42).as('answer'),

    // Column reference (for use as rhs)
    ref('first_name'),
  ])
  .execute()
```

### Aggregate Functions

```ts
// count, sum, avg, min, max
db.selectFrom('person')
  .select((eb) => eb.fn.count<number>('id').as('total'))
  .executeTakeFirstOrThrow()

// countAll (COUNT(*))
db.selectFrom('person')
  .select((eb) => eb.fn.countAll<number>().as('total'))
  .executeTakeFirstOrThrow()

// distinct inside aggregate
db.selectFrom('person')
  .select((eb) =>
    eb.fn.count<number>('first_name').distinct().as('unique_names')
  )

// filterWhere on aggregate
db.selectFrom('person')
  .select((eb) =>
    eb.fn.count<number>('id')
      .filterWhere('age', '>', 18)
      .as('adult_count')
  )

// Window function with .over()
db.selectFrom('person')
  .select((eb) => [
    'first_name',
    eb.fn.count<number>('id').over(
      (ob) => ob.partitionBy('first_name').orderBy('id')
    ).as('row_num'),
  ])

// Custom aggregate via fn.agg
db.selectFrom('person')
  .select((eb) =>
    eb.fn.agg<string[]>('array_agg', ['first_name']).as('names')
  )

// groupBy + having
db.selectFrom('person')
  .innerJoin('pet', 'pet.owner_id', 'person.id')
  .select((eb) => [
    'person.id',
    eb.fn.count<number>('pet.id').as('pet_count'),
  ])
  .groupBy('person.id')
  .having((eb) => eb.fn.count('pet.id'), '>', 10)
  .execute()
```

### Subqueries

```ts
// In SELECT (correlated)
db.selectFrom('person')
  .selectAll('person')
  .select((eb) =>
    eb.selectFrom('pet')
      .select('name')
      .whereRef('pet.owner_id', '=', 'person.id')
      .limit(1)
      .as('pet_name')
  )

// In WHERE — exists
db.selectFrom('person')
  .selectAll()
  .where((eb) => eb.exists(
    eb.selectFrom('pet')
      .select('pet.id')
      .whereRef('pet.owner_id', '=', 'person.id')
  ))

// In WHERE — in with subquery
db.selectFrom('person')
  .selectAll()
  .where('id', 'in',
    db.selectFrom('pet').select('owner_id')
  )

// selectNoFrom — SELECT without FROM
const result = await db.selectNoFrom((eb) => [
  eb.selectFrom('person')
    .select('id')
    .where('first_name', '=', 'Jennifer')
    .limit(1)
    .as('jennifer_id'),
  eb.selectFrom('pet')
    .select('id')
    .where('name', '=', 'Doggo')
    .limit(1)
    .as('doggo_id'),
]).executeTakeFirstOrThrow()
```

### Ordering, Pagination & Distinct

```ts
// orderBy
.orderBy('first_name', 'asc')
.orderBy('last_name', 'desc')

// Direction-in-string shorthand
.orderBy('first_name asc')

// limit + offset
.limit(10)
.offset(20)

// distinct
db.selectFrom('person').select('first_name').distinct().execute()

// distinctOn (PostgreSQL only)
db.selectFrom('person')
  .innerJoin('pet', 'pet.owner_id', 'person.id')
  .distinctOn('person.id')
  .selectAll('person')
```

### Conditional Queries with $if

```ts
async function getPerson(id: number, withLastName: boolean) {
  return await db.selectFrom('person')
    .select(['id', 'first_name'])
    .$if(withLastName, (qb) => qb.select('last_name'))
    .where('id', '=', id)
    .executeTakeFirstOrThrow()
}
// Return type: { id: number; first_name: string; last_name?: string }
// Selections inside $if become optional in the output type.
```

Prefer plain `if` + reassignment for non-select conditionals:

```ts
let query = db.selectFrom('person').selectAll()
if (firstName) {
  query = query.where('first_name', '=', firstName)
}
```

### Narrowing Types with $narrowType

```ts
import { NotNull } from 'kysely'

const person = await db.selectFrom('person')
  .where('nullable_column', 'is not', null)
  .selectAll()
  .$narrowType<{ nullable_column: NotNull }>()
  .executeTakeFirstOrThrow()
// nullable_column is now non-null in the result type
```

### Execution Methods

| Method | Returns |
|---|---|
| `.execute()` | `Promise<O[]>` — always an array |
| `.executeTakeFirst()` | `Promise<O \| undefined>` |
| `.executeTakeFirstOrThrow()` | `Promise<O>` — throws `NoResultError` if empty |
| `.stream()` | Async iterable of rows |
| `.compile()` | `CompiledQuery` — SQL string + parameters, no execution |

## Common Pitfalls

### 1. Forgetting to capture the return value (immutable builders)

```ts
// ❌ WRONG — .where() return value is discarded
let query = db.selectFrom('person').selectAll()
query.where('id', '=', 1)  // does nothing!

// ✅ CORRECT — reassign
query = query.where('id', '=', 1)
```

### 2. selectAll() without table arg in joins

```ts
// ❌ Ambiguous — selects * from all joined tables
db.selectFrom('person')
  .innerJoin('pet', 'pet.owner_id', 'person.id')
  .selectAll()  // includes both person and pet columns

// ✅ Explicit
  .selectAll('person')  // person.* only
```

### 3. Left join columns not typed as nullable

Left/full join makes the joined table's columns `T | null`. This is enforced by Kysely's type system. If you know a column is non-null after filtering, use `$narrowType`.

### 4. Missing .execute()

The query builder is lazy. Nothing runs until you call `.execute()`, `.executeTakeFirst()`, or `.executeTakeFirstOrThrow()`.

### 5. db.fn vs eb.fn

- `db.fn` — globally available, can reference **any** table in the DB (less safe)
- `eb.fn` — scoped to the current query context, only allows columns in scope (prefer this)

### 6. Aggregate return types

`fn.count()`, `fn.sum()`, `fn.avg()` return `number | string | bigint` by default. Provide a type parameter: `fn.count<number>('id')`. Include `null` when rows might be empty and no `groupBy` is used: `fn.avg<number | null>('price')`.

## Dialect-Specific Features

| Feature | Dialects |
|---|---|
| `distinctOn()` | PostgreSQL |
| `forUpdate()` / `forShare()` | PostgreSQL, MySQL |
| `forKeyShare()` / `forNoKeyUpdate()` | PostgreSQL |
| `innerJoinLateral()` / `leftJoinLateral()` | PostgreSQL, MySQL |
| `crossJoinLateral()` | PostgreSQL |
| `crossApply()` / `outerApply()` | MS SQL Server |
| `top()` | MS SQL Server |
| `fetch()` | PostgreSQL, MS SQL Server |

## Quick Reference

For deeper content, see the `reference/` directory (create files as needed for advanced topics like CTEs, JSON operators, dynamic references, and raw SQL escape hatches).
