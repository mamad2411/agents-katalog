---
name: kysely-dialect-portability
description: "Kysely cross-dialect portability: dialect setup (PostgresDialect, MysqlDialect, etc.), feature capability matrix, JSON helper import differences, plugins (CamelCase, ParseJSON, DeduplicateJoins), and portable fallback patterns. Use when targeting multiple databases or setting up a Kysely dialect instance."
---

# Kysely Dialect Portability

Write Kysely code that works across PostgreSQL, MySQL, SQLite, and MSSQL by understanding dialect-specific feature gaps, JSON helper differences, plugin requirements, and portable fallback patterns.

## Capability Matrix

| Feature | PostgreSQL | MySQL | SQLite | MSSQL |
|---|---|---|---|---|
| RETURNING clause | ✅ | ❌ | ✅ | ❌ |
| OUTPUT clause | ❌ | ❌ | ❌ | ✅ |
| ON CONFLICT (upsert) | ✅ | ❌ | ✅ | ❌ |
| ON DUPLICATE KEY UPDATE | ❌ | ✅ | ❌ | ❌ |
| MERGE statement | ✅ (15+) | ❌ | ❌ | ✅ |
| Transactional DDL | ✅ | ❌ | ❌ | ✅ |
| CREATE IF NOT EXISTS | ✅ | ✅ | ✅ | ❌ |
| DISTINCT ON | ✅ | ❌ | ❌ | ❌ |
| LATERAL joins | ✅ | ✅ | ❌ | ❌ |
| CROSS/OUTER APPLY | ❌ | ❌ | ❌ | ✅ |
| LIMIT on UPDATE/DELETE | ❌ | ✅ | ✅ | ❌ |
| TOP clause | ❌ | ❌ | ❌ | ✅ |
| JSON helpers (jsonArrayFrom etc.) | ✅ json_agg | ✅ json_arrayagg | ✅ json_group_array | ✅ FOR JSON PATH |

## Dialect Setup

### PostgreSQL — pg driver

```ts
import { Kysely, PostgresDialect } from 'kysely'
import { Pool } from 'pg'

const db = new Kysely<Database>({
  dialect: new PostgresDialect({
    pool: new Pool({ connectionString: 'postgres://localhost:5432/mydb' }),
  }),
})
```

### MySQL — mysql2 driver

```ts
import { Kysely, MysqlDialect } from 'kysely'
import { createPool } from 'mysql2'

const db = new Kysely<Database>({
  dialect: new MysqlDialect({
    pool: createPool({ uri: 'mysql://localhost:3306/mydb' }),
  }),
})
```

### SQLite — better-sqlite3 driver

```ts
import { Kysely, SqliteDialect, ParseJSONResultsPlugin } from 'kysely'
import Database from 'better-sqlite3'

const db = new Kysely<Database>({
  dialect: new SqliteDialect({
    database: new Database('mydb.sqlite'),
  }),
  plugins: [new ParseJSONResultsPlugin()], // Required for JSON helpers
})
```

### MSSQL — tedious + tarn drivers

```ts
import { Kysely, MssqlDialect, ParseJSONResultsPlugin } from 'kysely'
import * as Tarn from 'tarn'
import * as Tedious from 'tedious'

const db = new Kysely<Database>({
  dialect: new MssqlDialect({
    tarn: { ...Tarn, options: { min: 0, max: 10 } },
    tedious: {
      ...Tedious,
      connectionFactory: () =>
        new Tedious.Connection({
          authentication: {
            options: { password: 'password', userName: 'sa' },
            type: 'default',
          },
          options: { database: 'mydb', port: 1433, trustServerCertificate: true },
          server: 'localhost',
        }),
    },
  }),
  plugins: [new ParseJSONResultsPlugin()], // Required for JSON helpers
})
```

## JSON Helper Differences

Each dialect has its own `jsonArrayFrom`, `jsonObjectFrom`, and `jsonBuildObject` with different import paths and SQL generation.

### Import paths

```ts
import { jsonArrayFrom, jsonObjectFrom, jsonBuildObject } from 'kysely/helpers/postgres'
import { jsonArrayFrom, jsonObjectFrom, jsonBuildObject } from 'kysely/helpers/mysql'
import { jsonArrayFrom, jsonObjectFrom, jsonBuildObject } from 'kysely/helpers/sqlite'
import { jsonArrayFrom, jsonObjectFrom, jsonBuildObject } from 'kysely/helpers/mssql'
```

### Generated SQL per dialect

**jsonArrayFrom** — aggregates a subquery into a JSON array:

| Dialect | Generated SQL pattern |
|---|---|
| PostgreSQL | `(select coalesce(json_agg(agg), '[]') from (...) as agg)` |
| MySQL | `(select cast(coalesce(json_arrayagg(json_object('col', agg.col, ...)), '[]') as json) from (...) as agg)` |
| SQLite | `(select coalesce(json_group_array(json_object('col', agg.col, ...)), '[]') from (...) as agg)` |
| MSSQL | `coalesce((select * from (...) as agg for json path, include_null_values), '[]')` |

**jsonObjectFrom** — turns a single-row subquery into a JSON object:

| Dialect | Generated SQL pattern |
|---|---|
| PostgreSQL | `(select to_json(obj) from (...) as obj)` |
| MySQL | `(select json_object('col', obj.col, ...) from (...) as obj)` |
| SQLite | `(select json_object('col', obj.col, ...) from (...) as obj)` |
| MSSQL | `(select * from (...) as agg for json path, include_null_values, without_array_wrapper)` |

### Critical caveats

- **MySQL and SQLite require explicit column selection.** `selectAll()` is NOT allowed in subqueries passed to `jsonArrayFrom`/`jsonObjectFrom`. These dialects must enumerate columns in `json_object(...)` calls and cannot introspect `*`.
- **PostgreSQL allows `selectAll()`** because it uses `json_agg(agg)` which wraps the entire row.
- **MSSQL allows `selectAll()`** because it uses `FOR JSON PATH` which serializes all columns.
- **SQLite and MSSQL require `ParseJSONResultsPlugin`** — without it, nested JSON is returned as strings, not parsed objects/arrays.
- **PostgreSQL's built-in driver auto-parses JSON** — no plugin needed unless using a third-party driver.
- **MySQL's built-in driver auto-parses JSON** — no plugin needed unless using a third-party driver.

### Usage example (portable pattern)

```ts
// Pick the right import for your dialect:
// import { jsonArrayFrom } from 'kysely/helpers/postgres'
// import { jsonArrayFrom } from 'kysely/helpers/mysql'

const result = await db
  .selectFrom('person')
  .select((eb) => [
    'id',
    jsonArrayFrom(
      eb
        .selectFrom('pet')
        .select(['pet.id as pet_id', 'pet.name']) // Always use explicit selects for portability
        .whereRef('pet.owner_id', '=', 'person.id')
        .orderBy('pet.name'),
    ).as('pets'),
  ])
  .execute()
```

## Plugin System

### CamelCasePlugin — snake_case DB ↔ camelCase TypeScript

Maps between database snake_case column/table names and TypeScript camelCase properties. Define your `Database` interface in camelCase; the plugin translates automatically.

```ts
import { Kysely, CamelCasePlugin } from 'kysely'

const db = new Kysely<Database>({
  dialect,
  plugins: [new CamelCasePlugin()],
})

// DB column: first_name → TS property: firstName
await db.selectFrom('person').select('firstName').execute()
// Generates: SELECT "first_name" FROM "person"
```

### ParseJSONResultsPlugin — parse JSON strings into objects

**Required for SQLite and MSSQL.** These dialects return JSON columns as strings. The plugin walks result rows and parses any valid JSON string values into JavaScript objects/arrays.

```ts
import { Kysely, ParseJSONResultsPlugin } from 'kysely'

const db = new Kysely<Database>({
  dialect,
  plugins: [new ParseJSONResultsPlugin()],
})
```

### DeduplicateJoinsPlugin — safe join composition

Prevents duplicate joins when composing queries from reusable functions that may each add the same join. Safe to use globally.

```ts
import { Kysely, DeduplicateJoinsPlugin } from 'kysely'

const db = new Kysely<Database>({
  dialect,
  plugins: [new DeduplicateJoinsPlugin()],
})
```

### WithSchemaPlugin — multi-schema databases

Set a default schema for all queries. Available via `db.withSchema()` (preferred) or the plugin directly.

```ts
// Preferred: instance method
const tenantDb = db.withSchema('tenant_42')
await tenantDb.selectFrom('users').selectAll().execute()
// Generates: SELECT * FROM "tenant_42"."users"
```

### HandleEmptyInListsPlugin — empty IN () safety

Handles empty arrays in `WHERE col IN (...)` clauses, which is invalid SQL in most dialects. With the plugin, an empty list produces a `WHERE 1 = 0` (always false) condition instead of a syntax error.

```ts
import { Kysely, HandleEmptyInListsPlugin } from 'kysely'

const db = new Kysely<Database>({
  dialect,
  plugins: [new HandleEmptyInListsPlugin()],
})

const ids: string[] = []
await db.selectFrom('person').where('id', 'in', ids).selectAll().execute()
// Without plugin: SQL error (empty IN list)
// With plugin: SELECT * FROM "person" WHERE 1 = 0
```

### Plugin interface

All plugins implement the `KyselyPlugin` interface with two hooks:

```ts
interface KyselyPlugin {
  // Called before query execution. Transform the query's operation node tree.
  transformQuery(args: PluginTransformQueryArgs): RootOperationNode

  // Called after query execution. Transform the result rows.
  transformResult(args: PluginTransformResultArgs): Promise<QueryResult<UnknownRow>>
}
```

Use `WeakMap` with `args.queryId` to pass data between `transformQuery` and `transformResult` (not every `transformQuery` call is matched by a `transformResult`).

## Portable Fallback Patterns

### Getting the inserted row

**PostgreSQL / SQLite** — use `.returning()`:

```ts
const row = await db
  .insertInto('person')
  .values({ first_name: 'Alice', last_name: 'Smith' })
  .returning(['id', 'first_name', 'created_at'])
  .executeTakeFirstOrThrow()
```

**MSSQL** — use `.output()`:

```ts
const row = await db
  .insertInto('person')
  .values({ first_name: 'Alice', last_name: 'Smith' })
  .output(['inserted.id', 'inserted.first_name', 'inserted.created_at'])
  .executeTakeFirstOrThrow()
```

**MySQL** — no RETURNING; use a separate SELECT after insert:

```ts
const result = await db
  .insertInto('person')
  .values({ first_name: 'Alice', last_name: 'Smith' })
  .executeTakeFirstOrThrow()

const row = await db
  .selectFrom('person')
  .where('id', '=', Number(result.insertId))
  .select(['id', 'first_name', 'created_at'])
  .executeTakeFirstOrThrow()
```

### Upsert (insert or update on conflict)

**PostgreSQL / SQLite** — `onConflict`:

```ts
await db
  .insertInto('person')
  .values({ id: 1, first_name: 'Alice', last_name: 'Smith' })
  .onConflict((oc) =>
    oc.column('id').doUpdateSet({ first_name: 'Alice', last_name: 'Smith' }),
  )
  .execute()
```

**MySQL** — `onDuplicateKeyUpdate`:

```ts
await db
  .insertInto('person')
  .values({ id: 1, first_name: 'Alice', last_name: 'Smith' })
  .onDuplicateKeyUpdate({ first_name: 'Alice', last_name: 'Smith' })
  .execute()
```

**MSSQL / PostgreSQL 15+** — `mergeInto`:

```ts
await db
  .mergeInto('person as target')
  .using(
    db.selectFrom(sql`(values (1, 'Alice', 'Smith'))`.as<'source'>(sql`source(id, first_name, last_name)`)).selectAll(),
    'target.id',
    'source.id',
  )
  .whenMatched()
  .thenUpdateSet({ first_name: sql`source.first_name` })
  .whenNotMatched()
  .thenInsertValues({ id: sql`source.id`, first_name: sql`source.first_name`, last_name: sql`source.last_name` })
  .execute()
```

### Pagination

**Universal** — `limit` / `offset` (works on all dialects):

```ts
await db.selectFrom('person').selectAll().limit(10).offset(20).execute()
```

**MSSQL** — also supports `top`:

```ts
await db.selectFrom('person').selectAll().top(10).execute()
```

**PostgreSQL / MSSQL** — also support `fetch` (SQL standard):

```ts
await db.selectFrom('person').selectAll().offset(20).fetch(10).execute()
```

## Adapter Feature Flags

The `DialectAdapter` interface exposes feature flags that Kysely uses internally (especially for migrations). These are useful when writing dialect-agnostic utilities:

| Flag | PostgreSQL | MySQL | SQLite | MSSQL |
|---|---|---|---|---|
| `supportsReturning` | `true` | `false` | `true` | `false` |
| `supportsOutput` | `false` | `false` | `false` | `true` |
| `supportsTransactionalDdl` | `true` | `false` | `false` | `true` |
| `supportsCreateIfNotExists` | `true` | `true` | `true` | `false` |

### Migration lock strategies per dialect

| Dialect | Lock mechanism | Auto-released? |
|---|---|---|
| PostgreSQL | `pg_advisory_xact_lock` (transaction-level advisory lock) | Yes, at transaction end |
| MySQL | `get_lock` / `release_lock` (session-level named lock, 1h timeout) | Explicit release; also on session end |
| SQLite | Single connection reserved by migration system (no-op) | N/A |
| MSSQL | `sp_getapplock` (transaction-level exclusive lock on migration table) | Yes, at transaction end |

### Implications for migrations

- **Transactional DDL (PG, MSSQL):** Migrations run inside a transaction. If a migration fails, all DDL changes are rolled back.
- **Non-transactional DDL (MySQL, SQLite):** Migrations run on a single connection without a wrapping transaction. A failed migration may leave the database in a partially migrated state. Write idempotent migration steps.
- **No CREATE IF NOT EXISTS (MSSQL):** Kysely's internal migration tables/schemas are created without `IF NOT EXISTS`. This is safe because MSSQL supports transactional DDL, so the creation is wrapped in a transaction with proper error handling.
