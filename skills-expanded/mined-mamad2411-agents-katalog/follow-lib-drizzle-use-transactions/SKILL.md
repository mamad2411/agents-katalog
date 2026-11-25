---
name: follow-lib-drizzle-use-transactions
description: Drizzle mutations + transactions — insert/update/delete, returning, batch, nested tx, upsert
argument-hint: "[scope]"
related:
  - follow-lib-drizzle
  - run-test
  - resolve-errors
---

## Goal

Write mutations + transactions in Drizzle completely — CRUD, `returning`, upsert, batch, nested transactions, concurrency control

## Scope

write paths — `insert`/`update`/`delete`/`returning`, `onConflict*`, `db.transaction` + nested savepoints, `db.batch` (sqlite/libsql), prepared statements

## Execute

### 1. CRUD Mutations

```ts
await db.insert(users).values({ email, name }).returning()
await db.insert(users).values([...rows])                       // bulk
await db.update(users).set({ name }).where(eq(users.id, id)).returning()
await db.delete(users).where(eq(users.id, id)).returning()
```

- `.returning()` — supported on pg/sqlite (mysql doesn't → re-select)
- `.onConflictDoUpdate({ target, set })` / `.onConflictDoNothing()` — upsert
- `$dynamic()` — build queries conditionally (`let q = db.select().$dynamic()`)

### 2. Transactions

```ts
await db.transaction(async (tx) => {
  const [user] = await tx.insert(users).values(u).returning()
  await tx.insert(profiles).values({ userId: user.id })
  // throw → automatic rollback
})
```

- Nested `tx.transaction()` = savepoint — an inner rollback doesn't fail the outer
- `tx.rollback()` — manual rollback; return value = tx result
- Isolation levels (driver support): `.transaction(fn, { isolationLevel: 'serializable' })`

### 3. Batch And Prepared

```ts
await db.batch([db.insert(logs).values(a), db.update(stats).set(...)]) // libsql/d1 atomic batch
const prepared = db.select().from(users).where(eq(users.id, sql.placeholder('id'))).prepare()
await prepared.execute({ id: 1 })
```

- `db.batch` = atomic multi-statement (sqlite/libsql/D1) — use instead of a tx when the driver supports it
- `sql.placeholder` + `.prepare()` — reuse statement plans on hot paths

### 4. Concurrency Patterns

- Optimistic: version column + `where(and(eq(id), eq(version, v)))` → 0 rows = conflict
- Pessimistic: `select().for('update')` (pg) row lock inside the tx
- Idempotent writes: natural key + `onConflictDoNothing` + check `.returning()` empty

## Rules

- Multi-write operations must be in `db.transaction` — never fire sequential inserts that must be atomic
- Check driver support for `.returning()` (mysql has none)
- Nested tx = savepoints — don't assume independent
- `batch` for libsql/d1 beats tx in serverless (single round trip)

## Expected Outcome

- Type-safe mutations across insert/update/delete/upsert
- Nested transactions correct, concurrency strategy clear
