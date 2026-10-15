---
name: kysely-schema-migrations
description: "Kysely schema DDL and migrations: createTable, alterTable, createIndex, createType, createView, migration files (up/down), Migrator, FileMigrationProvider. Use for any database schema changes or migration setup."
---

# Kysely Schema Builders & Migrations

Write type-safe database schema changes and migrations using Kysely's schema builder API.

## Decision Tree

- Create a table → `db.schema.createTable()`
- Add a column to existing table → `db.schema.alterTable().addColumn()`
- Modify a column → `db.schema.alterTable().alterColumn()`
- Drop a column → `db.schema.alterTable().dropColumn()`
- Rename a table → `db.schema.alterTable().renameTo()`
- Create an index → `db.schema.createIndex()`
- Create a PG enum → `db.schema.createType().asEnum()`
- Create a view → `db.schema.createView()`
- Write a migration → export `up`/`down` functions with `Kysely<any>`
- Run migrations → `Migrator` + `FileMigrationProvider`

## Schema Builder Patterns

### createTable

```ts
import { sql } from 'kysely'

await db.schema
  .createTable('person')
  .ifNotExists()
  .addColumn('id', 'integer', (col) =>
    col.generatedAlwaysAsIdentity().primaryKey()
  )
  .addColumn('first_name', 'varchar(255)', (col) => col.notNull())
  .addColumn('last_name', 'varchar(255)')
  .addColumn('email', 'varchar(255)', (col) => col.unique().notNull())
  .addColumn('created_at', 'timestamptz', (col) =>
    col.defaultTo(sql`NOW()`).notNull()
  )
  .execute()
```

### ColumnDefinitionBuilder Methods

| Method | Description |
|--------|-------------|
| `primaryKey()` | Single-column primary key |
| `notNull()` | NOT NULL constraint |
| `unique()` | UNIQUE constraint |
| `defaultTo(value)` | Default value (use `sql` tag for expressions) |
| `references('table.column')` | Foreign key reference |
| `onDelete('cascade'|'set null'|'set default'|'restrict'|'no action')` | ON DELETE action |
| `onUpdate('cascade'|'set null'|'set default'|'restrict'|'no action')` | ON UPDATE action |
| `autoIncrement()` | Auto-increment (MySQL/SQLite only) |
| `generatedAlwaysAsIdentity()` | Identity column (PostgreSQL) |
| `generatedByDefaultAsIdentity()` | Identity column with override (PostgreSQL) |
| `identity()` | Identity column (MSSQL) |
| `unsigned()` | Unsigned integer (MySQL) |
| `check(sql`...`)` | CHECK constraint |
| `modifyFront(sql`...`)` | SQL after data type |
| `modifyEnd(sql`...`)` | SQL at end of column def |
| `ifNotExists()` | IF NOT EXISTS (PostgreSQL, for ALTER TABLE ADD COLUMN) |
| `nullsNotDistinct()` | NULLS NOT DISTINCT on UNIQUE (PostgreSQL) |

### Auto-increment by Dialect

```ts
// MySQL / SQLite
.addColumn('id', 'integer', (col) => col.autoIncrement().primaryKey())

// PostgreSQL
.addColumn('id', 'integer', (col) => col.generatedAlwaysAsIdentity().primaryKey())
// or use 'serial' / 'bigserial' data type

// MSSQL
.addColumn('id', 'integer', (col) => col.identity().primaryKey())
```

### Composite Primary Key

```ts
await db.schema
  .createTable('order_item')
  .addColumn('order_id', 'integer', (col) => col.references('order.id').notNull())
  .addColumn('item_id', 'integer', (col) => col.references('item.id').notNull())
  .addColumn('quantity', 'integer', (col) => col.notNull())
  .addPrimaryKeyConstraint('pk_order_item', ['order_id', 'item_id'])
  .execute()
```

### Foreign Key Constraint (Table-Level)

```ts
await db.schema
  .createTable('pet')
  .addColumn('id', 'integer', (col) => col.generatedAlwaysAsIdentity().primaryKey())
  .addColumn('owner_id', 'integer', (col) => col.notNull())
  .addColumn('species', 'varchar(50)')
  .addForeignKeyConstraint(
    'fk_pet_owner',
    ['owner_id'],
    'person',
    ['id'],
    (cb) => cb.onDelete('cascade').onUpdate('cascade')
  )
  .execute()
```

### createIndex

```ts
// Simple index
await db.schema
  .createIndex('person_email_index')
  .on('person')
  .column('email')
  .execute()

// Unique index
await db.schema
  .createIndex('person_email_unique')
  .on('person')
  .column('email')
  .unique()
  .execute()

// Multi-column index with ordering
await db.schema
  .createIndex('person_name_index')
  .on('person')
  .columns(['last_name', 'first_name desc'])
  .execute()

// Index type (btree, gin, gist, hash)
await db.schema
  .createIndex('person_data_index')
  .on('person')
  .column('data')
  .using('gin')
  .execute()

// Partial index (with WHERE)
await db.schema
  .createIndex('orders_unbilled_index')
  .on('orders')
  .column('order_nr')
  .where(sql.ref('billed'), 'is not', true)
  .execute()

// Expression-based index
await db.schema
  .createIndex('person_lower_email_index')
  .on('person')
  .expression(sql`lower(email)`)
  .execute()

// If not exists
await db.schema
  .createIndex('person_email_index')
  .on('person')
  .column('email')
  .ifNotExists()
  .execute()
```

### alterTable

```ts
// Add column
await db.schema
  .alterTable('person')
  .addColumn('phone', 'varchar(20)')
  .execute()

// Drop column
await db.schema
  .alterTable('person')
  .dropColumn('phone')
  .execute()

// Rename column
await db.schema
  .alterTable('person')
  .renameColumn('first_name', 'given_name')
  .execute()

// Rename table
await db.schema
  .alterTable('person')
  .renameTo('people')
  .execute()

// Alter column – each alteration is a separate call
await db.schema
  .alterTable('person')
  .alterColumn('email', (ac) => ac.setNotNull())
  .execute()

await db.schema
  .alterTable('person')
  .alterColumn('email', (ac) => ac.dropNotNull())
  .execute()

await db.schema
  .alterTable('person')
  .alterColumn('age', (ac) => ac.setDataType('bigint'))
  .execute()

await db.schema
  .alterTable('person')
  .alterColumn('status', (ac) => ac.setDefault('active'))
  .execute()

await db.schema
  .alterTable('person')
  .alterColumn('status', (ac) => ac.dropDefault())
  .execute()
```

**AlterColumnBuilder allows exactly one alteration per call**: `setDataType`, `setNotNull`, `dropNotNull`, `setDefault`, or `dropDefault`.

### createType (PostgreSQL Enums)

```ts
// Create enum
await db.schema
  .createType('species')
  .asEnum(['cat', 'dog', 'frog'])
  .execute()

// Use in table
await db.schema
  .createTable('pet')
  .addColumn('species', sql`species`, (col) => col.notNull())
  .execute()

// Drop enum
await db.schema.dropType('species').execute()
```

### createView / dropView

```ts
await db.schema
  .createView('active_users')
  .orReplace()
  .as(db.selectFrom('person').selectAll().where('active', '=', true))
  .execute()

await db.schema.dropView('active_users').ifExists().execute()
```

### Drop Operations

```ts
await db.schema.dropTable('person').ifExists().execute()
await db.schema.dropTable('person').cascade().execute()
await db.schema.dropIndex('person_email_index').ifExists().execute()
```

## Migration Patterns

### File Naming

```
migrations/
  2024_01_15_10_30_00_create_person_table.ts
  2024_01_15_10_31_00_create_pet_table.ts
  2024_02_01_09_00_00_add_email_to_person.ts
```

Format: `YYYY_MM_DD_HH_mm_ss_description.ts`

Migrations run in alphabetical order. Never rename or reorder migration files.

### Migration File Structure

```ts
import type { Kysely } from 'kysely'

export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .createTable('person')
    .addColumn('id', 'serial', (col) => col.primaryKey())
    .addColumn('first_name', 'varchar(255)', (col) => col.notNull())
    .addColumn('last_name', 'varchar(255)')
    .addColumn('created_at', 'timestamptz', (col) =>
      col.defaultTo(sql`NOW()`).notNull()
    )
    .execute()
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema.dropTable('person').execute()
}
```

### Using sql Tagged Template for Defaults

```ts
import { sql, type Kysely } from 'kysely'

export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .createTable('post')
    .addColumn('id', 'uuid', (col) =>
      col.primaryKey().defaultTo(sql`gen_random_uuid()`)
    )
    .addColumn('title', 'varchar(255)', (col) => col.notNull())
    .addColumn('published', 'boolean', (col) => col.defaultTo(false).notNull())
    .addColumn('created_at', 'timestamptz', (col) =>
      col.defaultTo(sql`NOW()`).notNull()
    )
    .addColumn('updated_at', 'timestamptz', (col) =>
      col.defaultTo(sql`NOW()`).notNull()
    )
    .execute()
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema.dropTable('post').execute()
}
```

### Multi-Step Migration

```ts
import { sql, type Kysely } from 'kysely'

export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .createType('status')
    .asEnum(['draft', 'published', 'archived'])
    .execute()

  await db.schema
    .createTable('article')
    .addColumn('id', 'serial', (col) => col.primaryKey())
    .addColumn('status', sql`status`, (col) =>
      col.defaultTo('draft').notNull()
    )
    .execute()

  await db.schema
    .createIndex('article_status_index')
    .on('article')
    .column('status')
    .execute()
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema.dropTable('article').execute()
  await db.schema.dropType('status').execute()
}
```

## Migrator Setup

### FileMigrationProvider

```ts
import { promises as fs } from 'node:fs'
import path from 'node:path'
import {
  Kysely,
  Migrator,
  FileMigrationProvider,
  PostgresDialect,
} from 'kysely'
import pg from 'pg'

const db = new Kysely<any>({
  dialect: new PostgresDialect({
    pool: new pg.Pool({ connectionString: process.env.DATABASE_URL }),
  }),
})

const migrator = new Migrator({
  db,
  provider: new FileMigrationProvider({
    fs,
    path,
    migrationFolder: path.join(__dirname, 'migrations'),
  }),
})
```

### FileMigrationProvider Props

| Prop | Type | Description |
|------|------|-------------|
| `fs` | `{ readdir(path: string): Promise<string[]> }` | Node.js `fs.promises` or compatible |
| `path` | `{ join(...path: string[]): string }` | Node.js `path` or compatible |
| `migrationFolder` | `string` | Absolute path to migrations folder |

Supported file extensions: `.js`, `.ts` (not `.d.ts`), `.mjs`, `.mts` (not `.d.mts`).

### migrateToLatest Pattern

```ts
async function migrateToLatest() {
  const { error, results } = await migrator.migrateToLatest()

  results?.forEach((it) => {
    if (it.status === 'Success') {
      console.log(`migration "${it.migrationName}" was executed successfully`)
    } else if (it.status === 'Error') {
      console.error(`failed to execute migration "${it.migrationName}"`)
    }
  })

  if (error) {
    console.error('failed to run `migrateToLatest`')
    console.error(error)
    process.exit(1)
  }

  await db.destroy()
}

migrateToLatest()
```

**Important**: `migrateToLatest()` never throws. Always check `error` on the result.

### Other Migrator Methods

```ts
// Migrate to a specific migration
await migrator.migrateTo('2024_01_15_10_30_00_create_person_table')

// Migrate all the way down
import { NO_MIGRATIONS } from 'kysely'
await migrator.migrateTo(NO_MIGRATIONS)

// Migrate one step up
await migrator.migrateUp()

// Migrate one step down
await migrator.migrateDown()

// Introspect migration status
const migrations = await migrator.getMigrations()
for (const m of migrations) {
  console.log(m.name, m.executedAt ? `ran at ${m.executedAt}` : 'pending')
}
```

### MigratorProps

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Kysely<any>` | required | Kysely instance |
| `provider` | `MigrationProvider` | required | Migration provider |
| `migrationTableName` | `string` | `'kysely_migration'` | Metadata table name |
| `migrationLockTableName` | `string` | `'kysely_migration_lock'` | Lock table name |
| `migrationTableSchema` | `string` | default schema | Schema for migration tables (PG/MSSQL) |
| `allowUnorderedMigrations` | `boolean` | `false` | Allow gaps in migration order |
| `disableTransactions` | `boolean` | `false` | Skip wrapping migrations in transactions |

**Warning**: Once set, `migrationTableName`, `migrationLockTableName`, and `migrationTableSchema` must never change. Changing them causes Kysely to create new empty tables and re-run all migrations.

## Safety Checklist

- **Always use `Kysely<any>`** in migration files, never `Kysely<Database>`
- **Always write `down()` migrations** for rollback capability
- **Always call `.execute()`** on schema builders — they do nothing without it
- **Never modify a migration** after it has been run in any environment
- **Never rename or reorder** migration files
- **Test migrations** on a copy of production data before deploying
- **Call `db.destroy()`** after migration scripts complete to close connections
- **Use consistent `migrationTableName`** across all environments

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| `Kysely<Database>` in migrations | Use `Kysely<any>` — migrations are historical snapshots |
| Missing `.execute()` on schema builders | Always chain `.execute()` — builders are inert without it |
| MSSQL `ifNotExists()` | Check `adapter.supportsCreateIfNotExists` first |
| Missing `down()` function | Always write `down()` for rollback capability |
| Different `migrationTableName` per env | Use identical name everywhere — changing it re-runs all migrations |
