---
name: follow-lib-drizzle-define-schema
description: Drizzle schema design — pg/mysql/sqlite tables, columns, indexes, relations, enums, types
argument-hint: "[dialect]"
related:
  - follow-lib-drizzle
  - run-typecheck
  - resolve-errors
---

## Goal

Write a complete Drizzle schema — table/column definitions per dialect, relations, indexes, enums, custom types

## Scope

schema authoring — `pgTable`/`mysqlTable`/`sqliteTable`, column builders, `relations()`, indexes/constraints; schema migrations → `migrate-schema`/`use-drizzle-kit`

## Execute

### 1. Dialect Table Builders

```ts
import { pgTable, serial, text, integer, timestamp, boolean, uuid, jsonb, index, uniqueIndex } from 'drizzle-orm/pg-core'
// mysql-core: mysqlTable, int, varchar, datetime, json, ...
// sqlite-core: sqliteTable, integer, text, blob, real, ...

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: text('email').notNull().unique(),
  name: text('name'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
})
```

### 2. Columns And Constraints

- `.primaryKey()`, `.notNull()`, `.unique()`, `.default()`, `.defaultNow()`, `.defaultRandom()`
- `.references(() => users.id, { onDelete: 'cascade' })` — FK
- `.array()` (pg), `jsonb`/`json`, `customType` for unsupported types
- Composite: `primaryKey({ columns: [a, b] })`, `unique().on(a, b)`, `check()` constraints in the callback arg

### 3. Indexes And Config Callback

```ts
export const posts = pgTable('posts', { ... }, (t) => [
  index('posts_author_idx').on(t.authorId),
  uniqueIndex('posts_slug_idx').on(t.slug),
])
```

- v0.36+: callback returns an array (object syntax deprecated)
- `pgEnum('status', ['a','b'])`, sequences, views (`pgView`), materialized views

### 4. Relations

```ts
export const usersRelations = relations(users, ({ many }) => ({ posts: many(posts) }))
export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, { fields: [posts.authorId], references: [users.id] }),
}))
```

- `relations()` = for relational queries (`db.query.*.findMany({ with: ... })`) — not a DB-level constraint
- `one`/`many` + `relationName` when ambiguous (self/multiple FKs to the same table)

### 5. Schema Organization

- `src/db/schema/*.ts` per domain → `src/db/schema/index.ts` barrel — drizzle-kit `schema` points at the barrel
- Infer types: `typeof users.$inferSelect`, `$inferInsert` — don't write duplicate interfaces

## Rules

- Column builders must match the dialect (`pg-core` vs `mysql-core` vs `sqlite-core`) — never mix
- `relations()` ≠ FK — FK needs `.references()`; relations are used with the query API
- Indexes/unique/checks in the callback arg as an array syntax (v0.36+)
- Use `$inferSelect`/`$inferInsert` — the schema is the single source of truth for types

## Expected Outcome

- Schema typed per dialect with complete tables/relations/indexes
- `$infer*` types used in the codebase — no manual interfaces
