---
name: kysely-writes-transactions
description: "Kysely data mutations: INSERT, UPDATE, DELETE, upserts (onConflict/onDuplicateKeyUpdate), MERGE, transactions (callback and controlled), savepoints, and connection pinning. NOT for SELECT queries or schema DDL."
---

# Kysely Writes & Transactions

## Decision Tree

| Need | Pattern |
|---|---|
| Single insert | `insertInto().values().execute()` |
| Insert + return row | `.returningAll().executeTakeFirstOrThrow()` (PG/SQLite) |
| Bulk insert | `.values([...])` |
| Insert from select | `.columns([...]).expression(selectQuery)` |
| Upsert (PG/SQLite) | `.onConflict(oc => oc.column().doUpdateSet())` |
| Upsert (MySQL) | `.onDuplicateKeyUpdate({...})` |
| Ignore conflict | `.onConflict(oc => oc.column().doNothing())` |
| MERGE | `.mergeInto().using().whenMatched().thenUpdateSet()` |
| Update | `updateTable().set().where().execute()` |
| Delete | `deleteFrom().where().execute()` |
| Transaction (auto) | `db.transaction().execute(async trx => {})` |
| Transaction (manual) | `db.startTransaction().execute()` |
| Pin connection | `db.connection().execute(async db => {})` |

## Canonical Patterns

### INSERT — Single Row

```ts
const result = await db
  .insertInto('person')
  .values({
    first_name: 'Jennifer',
    last_name: 'Aniston',
    age: 40,
  })
  .executeTakeFirstOrThrow()

// result: InsertResult { insertId: bigint | undefined, numInsertedOrUpdatedRows: bigint | undefined }
```

### INSERT — Multiple Rows

```ts
await db
  .insertInto('person')
  .values([
    { first_name: 'Jennifer', last_name: 'Aniston', age: 40 },
    { first_name: 'Brad', last_name: 'Pitt', age: 50 },
  ])
  .execute()
```

### INSERT — With returning / returningAll (PG/SQLite)

```ts
const row = await db
  .insertInto('person')
  .values({ first_name: 'Jennifer', last_name: 'Aniston', age: 40 })
  .returningAll()
  .executeTakeFirstOrThrow()
// row is typed as the full table row

const partial = await db
  .insertInto('person')
  .values({ first_name: 'Jennifer', last_name: 'Aniston', age: 40 })
  .returning(['id', 'first_name'])
  .executeTakeFirstOrThrow()
// partial is typed as { id: ..., first_name: ... }
```

### INSERT — From SELECT

```ts
await db
  .insertInto('person')
  .columns(['first_name', 'last_name', 'age'])
  .expression((eb) =>
    eb
      .selectFrom('pet')
      .select((eb) => [
        'pet.name',
        eb.val('Petson').as('last_name'),
        eb.lit(7).as('age'),
      ])
  )
  .execute()
```

### UPDATE — Object Form

```ts
const result = await db
  .updateTable('person')
  .set({ first_name: 'Updated', age: 41 })
  .where('id', '=', 123)
  .executeTakeFirstOrThrow()

// result: UpdateResult { numUpdatedRows: bigint, numChangedRows?: bigint (MySQL only) }
```

### UPDATE — Expression Builder Callback (Computed Values)

```ts
await db
  .updateTable('person')
  .set((eb) => ({
    age: eb('age', '+', 1),
    updated_at: eb.fn('now'),
  }))
  .where('id', '=', 123)
  .execute()
```

### UPDATE — With .from() Cross-Table (PG Only)

```ts
await db
  .updateTable('person')
  .from('pet')
  .set((eb) => ({
    first_name: eb.ref('pet.name'),
  }))
  .whereRef('pet.owner_id', '=', 'person.id')
  .execute()
// SQL: update "person" set "first_name" = "pet"."name" from "pet" where "pet"."owner_id" = "person"."id"
```

### UPDATE — With returning (PG/SQLite)

```ts
const updated = await db
  .updateTable('person')
  .set({ first_name: 'Updated' })
  .where('id', '=', 123)
  .returningAll()
  .executeTakeFirstOrThrow()
```

### DELETE — Basic

```ts
const result = await db
  .deleteFrom('person')
  .where('id', '=', 123)
  .executeTakeFirstOrThrow()

// result: DeleteResult { numDeletedRows: bigint }
```

### DELETE — With .using() (PG/MySQL)

```ts
// PG
await db
  .deleteFrom('pet')
  .using('person')
  .whereRef('pet.owner_id', '=', 'person.id')
  .where('person.first_name', '=', 'Bob')
  .execute()

// MySQL — using with join
await db
  .deleteFrom('pet')
  .using('pet')
  .leftJoin('person', 'person.id', 'pet.owner_id')
  .where('person.first_name', '=', 'Bob')
  .execute()
```

### DELETE — With returning (PG/SQLite)

```ts
const deleted = await db
  .deleteFrom('person')
  .where('id', '=', 123)
  .returning(['id', 'first_name'])
  .executeTakeFirstOrThrow()
```

### ON CONFLICT DO NOTHING (PG/SQLite)

```ts
await db
  .insertInto('person')
  .values({ id: 1, first_name: 'John', last_name: 'Doe', gender: 'male' })
  .onConflict((oc) => oc.column('id').doNothing())
  .execute()
```

### ON CONFLICT DO UPDATE SET — Upsert (PG/SQLite)

```ts
await db
  .insertInto('person')
  .values({ id: 1, first_name: 'John', last_name: 'Doe', gender: 'male' })
  .onConflict((oc) =>
    oc.column('id').doUpdateSet({
      first_name: (eb) => eb.ref('excluded.first_name'),
      last_name: (eb) => eb.ref('excluded.last_name'),
    })
  )
  .execute()
// "excluded" is the virtual table referencing the row that would have been inserted
```

With a WHERE filter on the update:

```ts
await db
  .insertInto('pet')
  .values({ name: 'Catto', species: 'cat', owner_id: 3 })
  .onConflict((oc) =>
    oc
      .column('name')
      .doUpdateSet({ species: 'hamster' })
      .where('excluded.name', '!=', 'Catto')
  )
  .execute()
```

By constraint name:

```ts
.onConflict((oc) => oc.constraint('pet_name_key').doUpdateSet({ species: 'hamster' }))
```

### ON DUPLICATE KEY UPDATE — Upsert (MySQL)

```ts
await db
  .insertInto('person')
  .values({ id: 1, first_name: 'John', last_name: 'Doe', gender: 'male' })
  .onDuplicateKeyUpdate({ updated_at: new Date().toISOString() })
  .execute()
```

### MERGE Statement (MSSQL, PG 15+)

```ts
const result = await db
  .mergeInto('person')
  .using('pet', 'person.id', 'pet.owner_id')
  .whenMatched()
  .thenUpdateSet({ first_name: 'Updated' })
  .whenNotMatched()
  .thenInsertValues({ first_name: 'New', last_name: 'Person', gender: 'other' })
  .execute()

// result: MergeResult { numChangedRows: bigint | undefined }
```

With delete:

```ts
await db
  .mergeInto('person')
  .using('pet', 'pet.owner_id', 'person.id')
  .whenMatched()
  .thenDelete()
  .execute()
```

### Transaction — Callback (Auto Commit/Rollback)

```ts
const catto = await db.transaction().execute(async (trx) => {
  const jennifer = await trx
    .insertInto('person')
    .values({ first_name: 'Jennifer', last_name: 'Aniston', age: 40 })
    .returning('id')
    .executeTakeFirstOrThrow()

  return await trx
    .insertInto('pet')
    .values({ owner_id: jennifer.id, name: 'Catto', species: 'cat', is_favorite: false })
    .returningAll()
    .executeTakeFirst()
})
// If callback throws → transaction rolls back, exception re-thrown
// If callback returns → transaction commits, return value forwarded
```

### Transaction — With Isolation Level

```ts
await db
  .transaction()
  .setIsolationLevel('serializable')
  .execute(async (trx) => {
    await doStuff(trx)
  })
```

### Transaction — Controlled (Manual Commit/Rollback)

```ts
const trx = await db.startTransaction().execute()

try {
  const jennifer = await trx
    .insertInto('person')
    .values({ first_name: 'Jennifer', last_name: 'Aniston', age: 40 })
    .returning('id')
    .executeTakeFirstOrThrow()

  await trx
    .insertInto('pet')
    .values({ owner_id: jennifer.id, name: 'Catto', species: 'cat', is_favorite: false })
    .execute()

  await trx.commit().execute()
} catch (error) {
  await trx.rollback().execute()
}
// After commit or rollback, trx cannot be reused — all queries will throw
```

### Savepoints (Controlled Transactions)

```ts
const trx = await db.startTransaction().execute()

try {
  await trx
    .insertInto('person')
    .values({ first_name: 'Jennifer', last_name: 'Aniston', age: 40 })
    .execute()

  const trxAfterInsert = await trx.savepoint('after_person').execute()

  try {
    await trxAfterInsert
      .insertInto('pet')
      .values({ owner_id: 1, name: 'Catto', species: 'cat' })
      .execute()
  } catch (error) {
    await trxAfterInsert.rollbackToSavepoint('after_person').execute()
  }

  await trxAfterInsert.releaseSavepoint('after_person').execute()
  await trx.commit().execute()
} catch (error) {
  await trx.rollback().execute()
}
```

### Connection Pinning

```ts
await db.connection().execute(async (db) => {
  // All queries use the same underlying database connection.
  // Useful when relying on session state, temp tables, etc.
  await doStuff(db)
})
```

## Result Types

| Type | Properties |
|---|---|
| `InsertResult` | `insertId: bigint \| undefined`, `numInsertedOrUpdatedRows: bigint \| undefined` |
| `UpdateResult` | `numUpdatedRows: bigint`, `numChangedRows?: bigint` (MySQL only) |
| `DeleteResult` | `numDeletedRows: bigint` |
| `MergeResult` | `numChangedRows: bigint \| undefined` |

When using `.returning()` / `.returningAll()`, the result type changes from the above to the selected column types.

## Common Pitfalls

### Forgetting .where() on UPDATE/DELETE
No compile-time error — silently updates/deletes every row in the table.
Always add `.where()` or explicitly use a subquery/condition.

### Using returning() on MySQL
MySQL does not support `RETURNING`. Use a separate `SELECT` after the write, or use `InsertResult.insertId` for auto-increment IDs.

### Nesting transaction() calls
Calling `db.transaction().execute()` inside another transaction callback throws an error. Use savepoints instead for nested atomic units within a controlled transaction.

### Not awaiting commit/rollback in controlled transactions
`trx.commit()` and `trx.rollback()` return builders — you must call `.execute()` AND `await` the result:
```ts
await trx.commit().execute()  // correct
trx.commit().execute()        // BUG: not awaited
trx.commit()                  // BUG: never executed
```

### Using db instead of trx inside transaction callback
Queries using `db` run outside the transaction. Always use the `trx` parameter:
```ts
await db.transaction().execute(async (trx) => {
  await trx.insertInto('person').values({...}).execute()  // correct — inside transaction
  await db.insertInto('person').values({...}).execute()   // BUG — outside transaction
})
```

## Dialect Compatibility

| Feature | PostgreSQL | MySQL | SQLite | MSSQL |
|---|---|---|---|---|
| `returning()` / `returningAll()` | ✅ | ❌ | ✅ | ❌ |
| `output()` | ❌ | ❌ | ❌ | ✅ |
| `onConflict()` | ✅ | ❌ | ✅ | ❌ |
| `onDuplicateKeyUpdate()` | ❌ | ✅ | ❌ | ❌ |
| `mergeInto()` | ✅ (v15+) | ❌ | ❌ | ✅ |
| `top()` on write queries | ❌ | ❌ | ❌ | ✅ |
| `limit()` on UPDATE/DELETE | ❌ | ✅ | ✅ | ❌ |
| `.from()` on UPDATE | ✅ | ❌ | ❌ | ❌ |
| `.using()` on DELETE | ✅ | ✅ | ❌ | ❌ |
