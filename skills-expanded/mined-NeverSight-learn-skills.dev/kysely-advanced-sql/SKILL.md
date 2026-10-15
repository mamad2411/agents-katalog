---
name: kysely-advanced-sql
description: "Kysely advanced query patterns: CTEs (.with/.withRecursive), window functions (.over), CASE expressions, JSON aggregation (jsonArrayFrom/jsonObjectFrom), raw SQL (sql tag), dynamic column/table refs, and streaming. Use for anything beyond basic SELECT/WHERE/JOIN."
---

# Kysely Advanced SQL

Write complex SQL queries using Kysely's type-safe query builder. Covers CTEs, window functions, CASE expressions, JSON operations, raw SQL, dynamic queries, and streaming.

## Decision Tree

| Need | Solution |
|---|---|
| Reuse subquery result | CTE with `.with()` |
| Recursive hierarchy | `.withRecursive()` |
| Rank / running total | Window function with `.over()` |
| Conditional value | `eb.case().when().then().else().end()` |
| JSON aggregation | `jsonArrayFrom` / `jsonObjectFrom` (dialect helpers) |
| JSON traversal | `eb.ref('col', '->').key('prop')` |
| Custom SQL | `sql` tagged template |
| Dynamic column/table | `db.dynamic.ref()` / `db.dynamic.table()` |
| Large result set | `.stream(chunkSize)` |

---

## 1. Common Table Expressions (CTEs)

### Basic CTE

```ts
const result = await db
  .with('active_users', (db) =>
    db.selectFrom('user')
      .where('status', '=', 'active')
      .select(['id', 'name', 'email'])
  )
  .selectFrom('active_users')
  .selectAll()
  .execute()
```

### CTE with Named Columns

```ts
.with('stats(user_id, total)', (db) =>
  db.selectFrom('order')
    .select(['user_id', (eb) => eb.fn.count('id').as('total')])
    .groupBy('user_id')
)
```

### Materialized / Not Materialized

Use the builder callback form as the first argument:

```ts
.with(
  (cte) => cte('expensive_query').materialized(),
  (db) => db.selectFrom('large_table').select(['id', 'value']).where('value', '>', 1000)
)

// Not materialized:
.with(
  (cte) => cte('cheap_query').notMaterialized(),
  (db) => db.selectFrom('small_table').select(['id', 'name'])
)
```

### Recursive CTE

Build org chart / tree traversal. The expression callback receives a `db` that includes the CTE itself for self-reference. Use `unionAll` to connect the base case and recursive step:

```ts
const result = await db
  .withRecursive('org_tree', (db) =>
    db.selectFrom('employee')
      .where('manager_id', 'is', null)
      .select(['id', 'name', 'manager_id', sql<number>`0`.as('depth')])
      .unionAll(
        db.selectFrom('employee')
          .innerJoin('org_tree', 'org_tree.id', 'employee.manager_id')
          .select([
            'employee.id',
            'employee.name',
            'employee.manager_id',
            sql<number>`org_tree.depth + 1`.as('depth'),
          ])
      )
  )
  .selectFrom('org_tree')
  .selectAll()
  .orderBy('depth')
  .execute()
```

### CTE with Insert

```ts
const result = await db
  .with('new_order', (db) =>
    db.insertInto('order')
      .values({ customer_id: 1, total: 99.99 })
      .returning(['id', 'customer_id', 'total'])
  )
  .selectFrom('new_order')
  .innerJoin('customer', 'customer.id', 'new_order.customer_id')
  .select(['new_order.id', 'customer.name', 'new_order.total'])
  .execute()
```

---

## 2. Window Functions

### Empty Window (entire result set)

```ts
.select([
  'id', 'amount',
  (eb) => eb.fn.sum<number>('amount').over().as('running_total'),
])
```

### Partition and Order

```ts
.select([
  'department', 'employee_id', 'amount',
  (eb) => eb.fn.sum<number>('amount')
    .over((ob) => ob.partitionBy('department').orderBy('created_at'))
    .as('dept_running_total'),
])
```

### Aggregates as Window Functions

```ts
.select([
  'id',
  (eb) => eb.fn.count<number>('id')
    .over((ob) => ob.partitionBy('category'))
    .as('category_count'),
  (eb) => eb.fn.avg<number>('price')
    .over((ob) => ob.partitionBy('category'))
    .as('avg_price'),
])
```

### Custom Window Functions (row_number, rank, etc.)

Use `fn.agg` for window functions not built into the `fn` module:

```ts
.select([
  'name',
  'score',
  (eb) => eb.fn.agg<number>('row_number')
    .over((ob) => ob.orderBy('score', 'desc'))
    .as('rank'),
  (eb) => eb.fn.agg<number>('rank')
    .over((ob) => ob
      .partitionBy('department')
      .orderBy('score', 'desc')
    )
    .as('dept_rank'),
  (eb) => eb.fn.agg<number>('dense_rank')
    .over((ob) => ob.orderBy('score', 'desc'))
    .as('dense_rank'),
])
```

### Frame Specs (ROWS BETWEEN)

Not built into the fluent API. Use `sql` tag:

```ts
.select([
  'date',
  'revenue',
  sql<number>`sum(revenue) over (
    order by date
    rows between 6 preceding and current row
  )`.as('seven_day_total'),
])
```

---

## 3. CASE Expressions

### Searched CASE

```ts
.select((eb) => [
  'name', 'age',
  eb.case()
    .when('age', '<', 18).then('minor')
    .when('age', '<', 65).then('adult')
    .else('senior')
    .end()
    .as('age_group'),
])
```

### Simple CASE (switching on a column)

```ts
.select((eb) => [
  'status',
  eb.case('status')
    .when('A').then('Active')
    .when('I').then('Inactive')
    .when('D').then('Deleted')
    .else('Unknown')
    .end()
    .as('status_label'),
])
```

### CASE in WHERE / ORDER BY

```ts
.where((eb) => eb.case()
  .when('role', '=', 'admin').then(sql<boolean>`true`)
  .else(sql<boolean>`false`)
  .end()
)

.orderBy((eb) => eb.case()
  .when('priority', '=', 'high').then(1)
  .when('priority', '=', 'medium').then(2)
  .else(3)
  .end()
)
```

### CASE Without else

Omitting `.else()` makes the result type nullable (`T | null`).

---

## 4. JSON Operations

### JSON Aggregation (dialect-specific helpers)

Import from the appropriate dialect helper:

```ts
// PostgreSQL
import { jsonArrayFrom, jsonObjectFrom } from 'kysely/helpers/postgres'

// MySQL
import { jsonArrayFrom, jsonObjectFrom } from 'kysely/helpers/mysql'

// SQLite
import { jsonArrayFrom, jsonObjectFrom } from 'kysely/helpers/sqlite'

// MSSQL
import { jsonArrayFrom, jsonObjectFrom } from 'kysely/helpers/mssql'
```

#### jsonArrayFrom — nested array of related rows

```ts
db.selectFrom('person')
  .select((eb) => [
    'id', 'name',
    jsonArrayFrom(
      eb.selectFrom('pet')
        .select(['pet.id', 'pet.name', 'pet.species'])
        .whereRef('pet.owner_id', '=', 'person.id')
    ).as('pets'),
  ])
```

#### jsonObjectFrom — single nested object

```ts
db.selectFrom('order')
  .select((eb) => [
    'id', 'total',
    jsonObjectFrom(
      eb.selectFrom('customer')
        .select(['customer.id', 'customer.name', 'customer.email'])
        .whereRef('customer.id', '=', 'order.customer_id')
    ).as('customer'),
  ])
```

> **Note:** MySQL and SQLite require explicit `.select()` — `.selectAll()` is not supported.

### JSON Path Traversal

```ts
db.selectFrom('event')
  .select((eb) => [
    'id',
    eb.ref('metadata', '->').key('category').as('category'),
    eb.ref('metadata', '->>').key('priority').as('priority'),
  ])
```

---

## 5. Raw SQL (`sql` Tag)

Import: `import { sql } from 'kysely'`

### Basic Usage

```ts
const result = await sql<{ id: number; name: string }>`
  SELECT id, name FROM person WHERE age > ${minAge}
`.execute(db)
```

Values interpolated with `${}` are automatically parameterized (safe from injection).

### Helper Functions

| Helper | Purpose | Injection-safe? |
|---|---|---|
| `sql.ref('col')` | Column reference (quoted identifier) | ❌ Validate input |
| `sql.table('t')` | Table reference (quoted identifier) | ❌ Validate input |
| `sql.id('schema', 'table')` | Multi-part identifier quoting | ❌ Validate input |
| `sql.val(value)` | Explicit parameterized value | ✅ |
| `sql.lit(value)` | Literal value (inlined into SQL) | ❌ Never use with user input |
| `sql.raw(str)` | Completely unescaped raw SQL | ❌ Never use with user input |
| `sql.join(arr, sep?)` | Join array with separator | Depends on contents |

### sql.ref — column reference

```ts
const col = 'first_name'  // must be validated/whitelisted
sql`SELECT ${sql.ref(col)} FROM person`
// → SELECT "first_name" FROM person
```

### sql.id — multi-part identifier

```ts
sql`SELECT * FROM ${sql.id('public', 'person')}`
// → SELECT * FROM "public"."person"
```

### sql.lit — literal (inlined, NOT parameterized)

```ts
sql`SELECT * FROM person LIMIT ${sql.lit(10)}`
// → SELECT * FROM person LIMIT 10
```

### sql.join — join array elements

```ts
const columns = ['id', 'name', 'email'].map(c => sql.ref(c))
sql`SELECT ${sql.join(columns, sql`, `)} FROM person`
// → SELECT "id", "name", "email" FROM person
```

### Inline in Query Builder

```ts
db.selectFrom('person')
  .select([
    'id',
    sql<string>`concat(first_name, ' ', last_name)`.as('full_name'),
  ])
  .where(sql<boolean>`age > ${minAge}`)
  .orderBy(sql`random()`)
  .execute()
```

### Typed Results

Always provide a type parameter for type-safe results:

```ts
const result = await sql<{ count: number }>`
  SELECT count(*) as count FROM person
`.execute(db)
// result.rows[0].count is typed as number
```

---

## 6. Dynamic Module

For queries where column or table names are determined at runtime.

### Dynamic Column Reference

```ts
const sortColumn = 'created_at'  // MUST validate against whitelist
const allowedColumns = ['created_at', 'name', 'email'] as const
if (!allowedColumns.includes(sortColumn)) throw new Error('Invalid sort column')

db.selectFrom('person')
  .selectAll()
  .orderBy(db.dynamic.ref(sortColumn))
```

### Dynamic Table Reference

```ts
const tableName = 'person'  // MUST validate against whitelist
const allowedTables = ['person', 'pet', 'order'] as const
if (!allowedTables.includes(tableName)) throw new Error('Invalid table')

db.selectFrom(db.dynamic.table(tableName)).selectAll()
```

> **Security:** Always whitelist user input before passing to `db.dynamic.ref()` or `db.dynamic.table()`. These bypass type checking and do NOT sanitize input.

---

## 7. Streaming

Process large result sets without loading everything into memory.

```ts
for await (const row of db.selectFrom('large_table').selectAll().stream(100)) {
  await processRow(row)
}

// Early break releases connection automatically
for await (const row of query.stream(100)) {
  if (row.id > 1000) break
}
```

- **PostgreSQL**: `chunkSize` controls cursor fetch size (true server-side streaming)
- **MySQL/SQLite/MSSQL**: All rows fetched at once, yielded in chunks (no memory benefit)
- Default chunk size: `100`

---

## 8. Common Pitfalls

### Injection Risks

```ts
// ❌ DANGEROUS — user input directly in sql.ref
sql`SELECT ${sql.ref(userInput)} FROM person`

// ✅ SAFE — whitelist first
const col = allowedCols.includes(userInput) ? userInput : 'id'
sql`SELECT ${sql.ref(col)} FROM person`

// ❌ DANGEROUS — sql.lit with user input
sql`LIMIT ${sql.lit(userInput)}`

// ✅ SAFE — sql.val parameterizes the value
sql`WHERE age > ${sql.val(userInput)}`

// ✅ SAFE — direct interpolation auto-parameterizes
sql`WHERE age > ${userInput}`
```

### Recursive CTE Requires UNION ALL

The recursive step must explicitly use `.unionAll()`:

```ts
// ❌ Won't recurse — missing unionAll
.withRecursive('tree', (db) =>
  db.selectFrom('node').where('parent_id', 'is', null).select(['id', 'parent_id'])
)

// ✅ Correct — base case + recursive step joined with unionAll
.withRecursive('tree', (db) =>
  db.selectFrom('node').where('parent_id', 'is', null).select(['id', 'parent_id'])
    .unionAll(
      db.selectFrom('node')
        .innerJoin('tree', 'tree.id', 'node.parent_id')
        .select(['node.id', 'node.parent_id'])
    )
)
```

### Forgetting Type Parameter on sql Tag

```ts
// ❌ Result typed as unknown
const r = await sql`SELECT count(*) as c FROM person`.execute(db)
r.rows[0].c  // unknown

// ✅ Properly typed
const r = await sql<{ c: number }>`SELECT count(*) as c FROM person`.execute(db)
r.rows[0].c  // number
```

### Window Frame Specs

The fluent `.over()` builder supports `partitionBy` and `orderBy` but not frame clauses (`ROWS BETWEEN`, `RANGE BETWEEN`). Use the `sql` tag for frame specs.

### CASE Without else

Omitting `.else()` makes the result type nullable. Add `.else()` if you need a non-null guarantee.
