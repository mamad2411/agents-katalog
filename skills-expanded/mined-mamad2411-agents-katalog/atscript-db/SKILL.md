---
name: atscript-db
description: >-
  Use when working with @atscript/db, @atscript/db-{sqlite,postgres,mysql,mongo},
  @atscript/db-sql-tools, @atscript/moost-db, @atscript/db-client, or .as models
  with @db.* annotations. Covers DbSpace, adapter wiring, table/view CRUD, query
  filters, patch/field/array ops, relations, views, schema sync, engine-specific
  capabilities, BaseDbAdapter subclassing, moost-db REST routes, declarative
  actions, URL query syntax, browser Client, client.action(), and DB validation.
  Scope is DB only; use the atscript skill for .as syntax, @meta.*, @expect.*, asc,
  unplugin, or VSCode.
---

# atscript-db

## Install

```bash
npx skills add moostjs/atscript-db     # this skill (DB layer)
npx skills add moostjs/atscript        # sibling — .as syntax, @meta.*, @expect.*, asc, unplugin
```

## Packages

```
@atscript/db                     core: DbSpace, AtscriptDbTable, AtscriptDbView, schema sync, relations
    ├── @atscript/db-sql-tools   shared SQL builders (WHERE, SELECT, INSERT, aggregation, filter visitor)
    │       ├── @atscript/db-sqlite     better-sqlite3 + FTS5 + collation
    │       ├── @atscript/db-postgres   pg + pgvector + HNSW + CITEXT + FTS
    │       └── @atscript/db-mysql      mysql2 + VECTOR + FULLTEXT + utf8mb4
    ├── @atscript/db-mongo       mongodb (aggregation pipelines, Atlas Search, no SQL layer)
    ├── @atscript/moost-db       Moost HTTP controllers: AsDbController / AsDbReadableController
    └── @atscript/db-client      browser/SSR fetch client over moost-db REST
```

```bash
pnpm add @atscript/core @atscript/typescript @atscript/db
pnpm add @atscript/db-sqlite better-sqlite3                 # pick one adapter
pnpm add @atscript/db-postgres pg
pnpm add @atscript/db-mysql mysql2
pnpm add @atscript/db-mongo mongodb
pnpm add @atscript/moost-db @moostjs/event-http moost       # REST
pnpm add @atscript/db-client                                 # browser/SSR client
```

## Quick start

```atscript
// src/todo.as
@db.table 'todos'
@db.depth.limit 0
export interface Todo {
    @meta.id @db.default.increment
    id: number
    title: string
    @db.default 'false'
    completed?: boolean
    @db.default.now
    createdAt?: number.timestamp
}
```

```ts
import { DbSpace } from "@atscript/db";
import { syncSchema } from "@atscript/db/sync";
import { SqliteAdapter, BetterSqlite3Driver } from "@atscript/db-sqlite";
import { Todo } from "./todo.as";

const db = new DbSpace(() => new SqliteAdapter(new BetterSqlite3Driver("./app.db")));
await syncSchema(db, [Todo]); // idempotent, lock-coordinated
const todos = db.getTable(Todo);

await todos.insertOne({ title: "ship it" }); // { insertedId: 1 }
const open = await todos.findMany({ filter: { completed: false } });
await todos.updateOne({ id: 1, completed: true }); // PK required in payload
await todos.deleteOne(1);
```

## Invariants

| #   | Rule                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **adapter parity** — application code must not branch on adapter type. Every adapter accepts the same filter shape, patch shape, and controls; per-engine features are surfaced through annotations, not API forks.                                                                                                                                                                                                                                                                            |
| 2   | **`@meta.id` is the composite-key marker.** No `@meta.isKey`. Multiple `@meta.id` on different props form a composite PK. Takes no arguments.                                                                                                                                                                                                                                                                                                                                                  |
| 3   | **`@db.depth.limit N` gates nested writes (insert / replace / patch).** Absent or `0` → server rejects nested payloads with HTTP 400 and `/meta` ships shallow FK refs. Set `N ≥ 1` to opt in.                                                                                                                                                                                                                                                                                                 |
| 4   | **MongoDB indexes use the `atscript__` prefix.** `syncIndexes()` only manages indexes with this prefix; consumer-created indexes that start with `atscript__` are treated as managed and may be dropped on drift.                                                                                                                                                                                                                                                                              |
| 5   | **Generated `*.as.d.ts` / `atscript.d.ts` files in a consuming project are produced by `asc`.** Never hand-edit. Regenerate via `npx asc` (or let `unplugin-atscript` do it at bundle time).                                                                                                                                                                                                                                                                                                   |
| 6   | **Schema sync takes a distributed lock.** Multi-pod deployments must configure `podId`, `lockTtlMs`, `waitTimeoutMs` on the `syncSchema()` options; the control table is `__atscript_control`.                                                                                                                                                                                                                                                                                                 |
| 7   | **Third-party `BaseDbAdapter` implementations MUST NOT import any other in-tree adapter.** Shared SQL helpers live in `@atscript/db-sql-tools`. Each adapter is independent.                                                                                                                                                                                                                                                                                                                   |
| 8   | **Navigation relations are lazy.** `@db.rel.to` / `.from` / `.via` fields are `undefined` on read unless requested via `controls.$with`. No N+1 lazy loading.                                                                                                                                                                                                                                                                                                                                  |
| 9   | **`@db.column` has a perf cost.** Any `@db.column` remapping, nested object, or `@db.json` field activates per-row key translation on every read/write/filter. Prefer field names that match physical columns.                                                                                                                                                                                                                                                                                 |
| 10  | **Read responses always carry `preferredId` fields.** The `moost-db` controller silently widens `$select` to include `meta.preferredId` on every row-returning read endpoint (`/query`, `/pages`, `/one`, `/one/:id`, search/vector). Aggregate (`$groupBy`) and count (`$count`) responses are NOT widened. `transformProjection()` overrides cannot suppress preferred-id fields — hide identifiers at the network/authz layer instead.                                                      |
| 11  | **Action identifiers are object-only.** `@DbActionID()` / `@DbActionIDs()` request bodies are JSON objects (single) or arrays of objects (multi) — never scalars. Each object's field set must EXACTLY match one legitimate identification (PK or any `@db.index.unique` group). Strict — unknown fields rejected. Single-field PKs send `{ id: "abc" }`, never bare `"abc"`.                                                                                                                  |
| 12  | **`disabled` requires `requiredFields`.** `@DbAction` / `@DbActions*` predicates must declare every field they read as a literal `requiredFields` tuple. The tuple type-narrows the predicate's row arg (`Pick<FlatOf<TRow>, R[number]>[]`) AND drives server-side projection widening for `@DbActionRow*` injection and the `$actions=true` augmentation. `requiredFields` is server-internal — never on the `/meta` wire. `disabled` without `requiredFields` → action dropped at discovery. |
| 13  | **Per-row action availability is server-evaluated via `?$actions=true`.** Opt-in URL control on `/query`, `/pages`, `/one`. Each returned row gets `$actions: string[]` (row/rows-level action names NOT disabled). Stripped on `$count`/`$groupBy`. `'table'`-level actions never appear. Filters through per-request `applyMetaOverlay()`.                                                                                                                                                   |

## Key imports

```ts
// Core
import { DbSpace, AtscriptDbTable, AtscriptDbView, BaseDbAdapter, DbError } from "@atscript/db";
import { syncSchema, SchemaSync, readStoredSnapshot } from "@atscript/db/sync";
import { dbPlugin } from "@atscript/db/plugin";
import { $inc, $dec, $mul, $replace, $insert, $upsert, $update, $remove } from "@atscript/db/ops";

// Adapters (pick one)
import {
  SqliteAdapter,
  BetterSqlite3Driver,
  createAdapter as sqliteSpace,
} from "@atscript/db-sqlite";
import { PostgresAdapter, PgDriver, createAdapter as pgSpace } from "@atscript/db-postgres";
import { MysqlAdapter, Mysql2Driver, createAdapter as mysqlSpace } from "@atscript/db-mysql";
import { MongoAdapter } from "@atscript/db-mongo";

// HTTP
import {
  AsDbController,
  AsDbReadableController,
  TableController,
  ReadableController,
} from "@atscript/moost-db";

// Browser client
import { Client } from "@atscript/db-client";
```

## References — load only what's needed

| Domain               | File                                                    | When                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| -------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| First contact        | [getting-started.md](references/getting-started.md)     | Install, `atscript.config`, first `.as` model, `DbSpace` wiring, `syncSchema`, first CRUD call                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `@db.*` annotations  | [annotations.md](references/annotations.md)             | `@db.table`, `@db.table.preferredId.uniqueIndex`, `@db.column`, `@db.default*`, indexes, `@db.rel.*`, `@db.json`, `@db.ignore`, `@meta.id`, gate mode                                                                                                                                                                                                                                                                                                                                                               |
| Mongo annotations    | [mongo-annotations.md](references/mongo-annotations.md) | `@db.mongo.*`: collection, capped, search.text/static/dynamic, patch.strategy, array.uniqueItems, primitives                                                                                                                                                                                                                                                                                                                                                                                                        |
| Tables & views       | [tables-and-views.md](references/tables-and-views.md)   | `DbSpace.getTable/getView/get`, lifecycle, `ensureTable`, `syncIndexes`, view kinds (managed/materialized/external)                                                                                                                                                                                                                                                                                                                                                                                                 |
| CRUD                 | [crud.md](references/crud.md)                           | `insertOne/Many`, `replaceOne/Many`, `updateOne/Many`, `deleteOne/Many`, `findOne/Many`, `count`, `bulkUpdate/Replace`, `DbError`                                                                                                                                                                                                                                                                                                                                                                                   |
| Queries              | [queries.md](references/queries.md)                     | Filter operators, `$and` / `$or` / `$not`, projection (`$select`), `$sort`, `$skip` / `$limit` / `$page` / `$size`, `$count`, `$with`, `$groupBy` aggregation                                                                                                                                                                                                                                                                                                                                                       |
| Patch semantics      | [patch.md](references/patch.md)                         | Field ops (`$inc/$dec/$mul`), array ops, `@db.json` handling, `@db.patch.strategy` merge vs replace, `@db.depth.limit` depth gate, Mongo `CollectionPatcher`                                                                                                                                                                                                                                                                                                                                                        |
| Relations            | [relations.md](references/relations.md)                 | `@db.rel.FK/.to/.from/.via`, optional FKs, referential actions, `controls.$with`, fractional ref depth on `/meta`, nested writes                                                                                                                                                                                                                                                                                                                                                                                    |
| Schema sync          | [schema-sync.md](references/schema-sync.md)             | FNV-1a hash, `__atscript_control` store, distributed lock (`podId`, `lockTtlMs`, `waitTimeoutMs`), `@db.sync.method`, `safe` mode, sync hooks                                                                                                                                                                                                                                                                                                                                                                       |
| SQLite specifics     | [adapters-sqlite.md](references/adapters-sqlite.md)     | `BetterSqlite3Driver`, FTS5, `@db.column.collate`, native FKs, in-memory `:memory:`                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| PostgreSQL specifics | [adapters-postgres.md](references/adapters-postgres.md) | `PgDriver`, pgvector + HNSW, CITEXT, `@db.pg.type`, `@db.pg.schema`, `@db.pg.collate`, tsvector FTS                                                                                                                                                                                                                                                                                                                                                                                                                 |
| MySQL specifics      | [adapters-mysql.md](references/adapters-mysql.md)       | `Mysql2Driver`, `@db.mysql.engine/.charset/.collate/.type/.unsigned/.onUpdate`, VECTOR, FULLTEXT, utf8mb4 default                                                                                                                                                                                                                                                                                                                                                                                                   |
| MongoDB specifics    | [adapters-mongo.md](references/adapters-mongo.md)       | `MongoAdapter(db, client?)`, aggregation-pipeline patches, Atlas Search text + vector, `atscript__` index prefix, ObjectId primitive                                                                                                                                                                                                                                                                                                                                                                                |
| Custom adapters      | [creating-adapters.md](references/creating-adapters.md) | `BaseDbAdapter` contract, abstract methods, overridable hooks, `supports*` flags, `@atscript/db-sql-tools` reuse                                                                                                                                                                                                                                                                                                                                                                                                    |
| `moost-db` HTTP      | [moost-db.md](references/moost-db.md)                   | `AsDbController` / `AsDbReadableController` routes, `TableController` / `ReadableController`, `@db.http.path` resolution, value-help endpoints                                                                                                                                                                                                                                                                                                                                                                      |
| Actions              | [actions.md](references/actions.md)                     | `@DbAction` / `@DbActionID*` / `@DbActionRow*` / `@DbActions*` decorators, object-only identifier body (PK or any unique index), row/rows/table actions, `processor: 'backend' \| 'navigate' \| 'custom'`, sync batch `disabled` gate (typed via `requiredFields` tuple, mandatory), `perRow()` helper, `onDisabledRows`, `@DbActionRow*` projection widening, `$actions=true` server-evaluated row availability augmentation, preferred-id navigate substitution, `ActionDisabledError`, `/meta` `actions[]` shape |
| URL query syntax     | [http-query-syntax.md](references/http-query-syntax.md) | URL filter encoding (`field=v`, `!=`, `>`, `<`, `{v1,v2}`, `~=/re/i`, ranges), `$sort`, `$select`, `$with`, `$page`, `$size`                                                                                                                                                                                                                                                                                                                                                                                        |
| Browser client       | [db-client.md](references/db-client.md)                 | `Client<T extends AtscriptClientShape>`, typed CRUD methods with `$with` response narrowing (`ClientResponse<T, Q>`), `client.action<R>(name, id)` object-only identifier contract, filter construction, auth headers, `ClientError` / `ActionDisabledError`, meta + validator caching, preferred-id-driven navigate URLs                                                                                                                                                                                           |
| Validation           | [validation.md](references/validation.md)               | `createDbValidatorPlugin`, `buildDbValidator`, server+client validator, error shape over HTTP, `ValidatorMode`                                                                                                                                                                                                                                                                                                                                                                                                      |
| App-side testing     | [testing.md](references/testing.md)                     | In-memory SQLite (`:memory:`), MongoDB in-memory server, fixture seeding, resetting schema, driving controllers from a test harness                                                                                                                                                                                                                                                                                                                                                                                 |

Reference docs: https://db.atscript.dev.
