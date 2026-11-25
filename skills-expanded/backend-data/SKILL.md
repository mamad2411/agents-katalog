---
name: backend-data
description: "Data access from the application: ORM, query builder or SQL, where queries live, migrations, column types for money, time and ids (UUIDv7), constraints and validation at write, transactions and race-free writes (stock, balances, unique values), optimistic concurrency end to end, queries without N+1, pagination helpers, bulk operations, money and time zone arithmetic, soft deletes, archives and audit trails, seeds and fixtures, connection pools, read replicas, SQLite settings. Read before writing queries, models or migrations."
---

# Data

The generated version loads a table to filter it in code, checks stock and
then writes it, adds money in floats, and opens a pool per request. One part
of the backend; the whole is in `backend`. Schema design in depth is the
database specialist's (`database-schema`, `database-migrations`,
`database-queries`, `database-indexes`, `database-transactions`, the
engine's skill); these are the rules all server code touching data keeps.

## 1. The query layer, and where queries live

Keep the project's. With none:

| Choice | When | Examples |
|---|---|---|
| ORM | CRUD-heavy apps; the framework's default | Prisma, Eloquent, Active Record, Django ORM, EF Core, Hibernate, SQLAlchemy ORM |
| Query builder | Typed queries that read like SQL; reports | Drizzle, Kysely, SQLAlchemy Core, jOOQ |
| SQL with generated types | Go and Rust by default; complex or hot queries | sqlc, sqlx, PgTyped, Dapper |

- An ORM for everyday writes plus hand-written SQL for a report is fine,
  through the same connection and transaction; two ORMs is not. Log the SQL
  in development and read it for anything that lists or loops.
- Data access functions per feature, named for what they do and returning
  domain types (`orders.findForCustomer(customerId, page)`,
  `orders.insertWithItems(tx, order)`); the service calls them and nothing
  else writes SQL. No generic `Repository<T>` re-wrapping the ORM one to
  one, and no interface with one implementation unless a test needs a fake.
- The transaction is opened in the service and passed down: the `tx` of
  `db.transaction(async (tx) => ...)`, SQLAlchemy's request `Session`,
  sqlc's `queries.WithTx(tx)`, `DB::transaction`, Spring's `@Transactional`.

## 2. Migrations

- Every change to the schema is a migration, made with the project's tool
  (Drizzle Kit, Prisma Migrate, Alembic, Laravel, sqlx, goose or atlas), and
  committed. Never tables created by hand, never an ORM's "sync the schema"
  against a real database.
- One migration per change, named for what it does
  (`add_status_to_orders`). A migration that has run anywhere is never
  edited; a fix is a new one.
- Reversible where it can be. A change that drops or rewrites data says so
  in the report before it runs; renaming a column in use is three steps (add,
  copy and write both, drop later). Locks, batched backfills and the order
  against deploys are in `database-migrations`.

## 3. Columns

- Money: an integer in the smallest unit (`1500000` rupiah, `1999` cents)
  with its currency, or `numeric(12, 2)`; never `float` or `double`.
- Time: `timestamptz` (or UTC in a text or integer column in SQLite), always
  UTC in storage, converted to the user's zone only when shown. Dates without
  a time (a birthday, a due date) as `date`.
- Ids: `bigint` identity, or UUIDv7 when ids are made outside the database or
  must not be guessable in URLs. Never an id built from a count.
- `NOT NULL` unless empty has a meaning; defaults in the database
  (`created_at default now()`); a `CHECK` for rules the data must always keep
  (`stock >= 0`, `status in (...)`).
- Foreign keys for every reference, with `ON DELETE` chosen on purpose
  (`restrict` for records with history such as orders, `cascade` for parts
  that mean nothing alone), and an index on the referencing column.
- Uniqueness the business depends on is a unique constraint (a lowercased
  email, a SKU per shop), not a check in code.
- UUIDv7 begins with a millisecond timestamp, so new rows land at the end of
  the index instead of scattering like v4. Stored as `uuid`, never text;
  made by `uuidv7()` in PostgreSQL 18 or in the app (the `uuid` package's
  `v7()`, Python 3.14's `uuid.uuid7()`, google/uuid's `NewV7()`,
  `Guid.CreateVersion7()`). It dates the row: use v4 where that matters.

## 4. Checked at write

- Three layers, each catching what the others cannot: the request schema
  (`backend-api`), the service (rules that need other data), and the
  database: `NOT NULL`, `CHECK`, `UNIQUE`, foreign keys, and an exclusion
  constraint for ranges that must not overlap
  (`EXCLUDE USING gist (room_id WITH =, during WITH &&)`, with `btree_gist`).
- A constraint that fires is an expected outcome, mapped by SQLSTATE and
  constraint name, never by message text:

| SQLSTATE | Meaning | Becomes |
|---|---|---|
| `23505` | Unique violation | `409` with a specific code (`users_email_key` to `email_taken`) |
| `23503` | Foreign key violation | `409` (still referenced) or `422` (unknown reference) |
| `23514`, `23502` | Check, not null | `422` when input can cause it, otherwise a bug |
| `40001`, `40P01` | Serialisation failure, deadlock | Retry the whole transaction, up to 3 times with jitter |
| `57014` | Statement timeout | `503` |

- Bulk methods skip model validation and callbacks (`insert_all`,
  `bulk_create`, Laravel's builder `insert`): validate before calling them.

## 5. Transactions and races

- Writes that belong together run in one transaction: an order and its
  items, a payment and the balance it changes. On error the whole of it rolls
  back.
- Never read, decide in code, then write, when two requests can interleave.
  Let the database decide:
  - stock and balances with a conditional update, then check the rows
    affected:
    ```sql
    UPDATE products SET stock = stock - $2
    WHERE id = $1 AND stock >= $2
    ```
    zero rows means not enough stock: roll back and answer `409`;
  - "create if it does not exist" with the unique constraint and an upsert
    (`INSERT ... ON CONFLICT`), and a duplicate turned into `409`;
  - an edit two people can make at once with a `version` column checked in
    the `WHERE` of the update (section 6);
  - a sequence number (an invoice number per shop) from the database, never
    `max(n) + 1` in code.
- A row that must be read before it changes is locked: `SELECT ... FOR
  UPDATE` (`lockForUpdate`, `with_for_update()`, Rails's `lock`), rows
  locked in a fixed order to avoid deadlocks, `SKIP LOCKED` for work queues.
- Keep transactions short: no calls to other services, no waiting on a user,
  inside one. Send the email after the commit (a job, `backend-jobs`).

## 6. Optimistic concurrency, end to end

1. The table has `version integer NOT NULL DEFAULT 1`; every read returns it
   (in the body and as the `ETag`, `backend-api`).
2. The client sends it back with the edit (`If-Match`, or `version`).
3. The update bumps it only while it still matches:
   ```sql
   UPDATE documents SET body = $3, version = version + 1, updated_at = now()
   WHERE id = $1 AND version = $2
   RETURNING version
   ```
4. No row: the record is gone (`404`) or changed (`409` `stale_version`, or
   `412` for `If-Match`). The client shows the current version and lets the
   person redo or merge; it never retries blindly with the new number.

Built in: JPA `@Version`, EF Core concurrency tokens, Rails's `lock_version`;
with Prisma, an `updateMany` whose `where` holds the version, then `count`.

## 7. Queries and pagination

- Always parameterised: the query layer's placeholders or builder; never
  values or column names pasted into a string. Sort and filter columns come
  from an allowed list.
- Select the columns you need. Related rows in one query (a join, `IN`, the
  ORM's eager load: `with`, `include`, `selectinload`, `prefetch_related`),
  never one query per row in a loop.
- Lists paginated in the query with a limit, by keyset on an indexed sort
  column and the id for long lists (`WHERE (created_at, id) < ($1, $2)
  ORDER BY created_at DESC, id DESC LIMIT 25`), by offset only for short
  lists or page numbers.
- One pagination helper: it clamps the limit to 100, fetches one row extra
  to know whether a next page exists, encodes the last row's sort value and
  id as the cursor (base64url JSON), and answers a bad cursor with `400`.
- Counts, sums and reports computed in SQL with `GROUP BY`, never by
  loading rows to add them up in code. Heavy ones cached or kept in a summary
  table that is updated when the data changes.
- An index for each filter and sort that runs on every request, composite in
  the order the query uses; `EXPLAIN` a query that is slow before adding one.

## 8. Bulk operations

- Many rows in: multi-row `INSERT` in batches of 500 to 1,000 (PostgreSQL
  takes at most 65,535 parameters per statement), or `COPY` past about
  10,000 rows (pgx `CopyFrom`, psycopg's `cursor.copy()`, pg-copy-streams).
- Upserted in one statement with two parameters, each key once per batch
  (one statement cannot update a row twice):
  ```sql
  INSERT INTO prices (sku, amount_minor)
  SELECT * FROM unnest($1::text[], $2::bigint[])
  ON CONFLICT (sku) DO UPDATE SET amount_minor = EXCLUDED.amount_minor
  ```
- Changed or deleted in batches by key range (1,000 to 10,000), each in its
  own short transaction, so locks and replication lag stay small; long runs
  belong in a job (`backend-jobs`).

## 9. Money and time in code

- Money is computed in integers of the smallest unit or a decimal type
  (decimal.js or big.js, Python's `Decimal`, `BigDecimal`,
  shopspring/decimal, rust_decimal), never floats; the currency's exponent
  comes from ISO 4217 (2 for USD, 0 for JPY, 3 for KWD), not an assumed 2.
- Rounding is a written business rule: half-even or half-up, per line or per
  invoice, matching the invoices and the tax rules. A split gives the
  remainder to some parts (100 in three is 34, 33, 33) so they add up.
- A converted amount keeps the rate and both amounts. Never PostgreSQL's
  locale-bound `money` type; `numeric` arrives as a string in node-postgres.
- Database sessions run in UTC (`SET TIME ZONE 'UTC'` or the driver's
  option), so `now()`, `date_trunc` and casts do not move with the server.
- "Orders on 29 September in Jakarta" is a half-open range computed in code
  from the zone, `created_at >= $1 AND created_at < $2`, so the index is
  used; never `date(created_at) = $1`. Grouped by local day:
  `date_trunc('day', created_at AT TIME ZONE 'Asia/Jakarta')`.
- A future event in local time (every Monday at 09:00, a meeting next year)
  is stored as the local time plus the IANA zone, since zone rules can change
  before it arrives; past instants are stored in UTC.

## 10. Deleting, history and audit

- Delete for real unless the domain needs history or undo; then a
  `deleted_at` column, and every query and unique constraint made aware of
  it.
- `deleted_at` costs a filter on every query (one forgotten join shows
  deleted rows), partial unique indexes
  (`CREATE UNIQUE INDEX ON users (lower(email)) WHERE deleted_at IS NULL`),
  foreign keys that no longer cascade, and personal data kept after an
  erasure request. Use it for undo within a window (30 days), purged by a
  job after. Otherwise move the row to an archive table (or a
  `deleted_records` table holding it as JSON) in the delete's transaction.
- Anything about money keeps an append-only record (the ledger, the stock
  movements) beside the current value, so the current value can be checked
  and rebuilt.
- An audit trail answers who changed what and when: an append-only
  `audit_events` table (actor, action, entity type and id, tenant, changed
  fields before and after with secrets removed, request id, time), written
  in the same transaction as the change, the app's role allowed to insert
  but not update or delete. Per-model libraries: PaperTrail,
  django-simple-history, Hibernate Envers, laravel-auditing.

## 11. Connections, pools and replicas

- One client or pool for the process, created at start; never a connection
  per request. On serverless platforms, the provider's pooler (PgBouncer, the
  Neon or Supabase pooler) and a small pool per instance.
- In development with hot reload, keep the client on a global so reloads do
  not open new pools (`backend-stack-next`).
- Size against the ceiling: PostgreSQL allows 100 connections by default,
  shared by every instance, worker and migration. Small pools are faster:
  about twice the database's cores in total, 5 to 20 per instance, and a
  worker's pool at least its job concurrency.
- An acquire timeout of a few seconds (then `503`, not a hang; node-postgres
  `connectionTimeoutMillis`, SQLAlchemy `pool_timeout`), connections
  recycled after about 30 minutes, and on the app's role a
  `statement_timeout` (5 to 30 seconds for web traffic) and an
  `idle_in_transaction_session_timeout`.
- Transaction-mode poolers (PgBouncer, Supavisor) drop session state between
  transactions: no session `SET`, session advisory locks or `LISTEN`;
  prepared statements need PgBouncer 1.21 or later with
  `max_prepared_statements`.
- Read replicas serve reads that tolerate a second of lag (lists, reports),
  never a read that decides a write. After a user writes, their reads go to
  the primary for a few seconds (Laravel's `sticky`, Rails's automatic role
  switching with a `delay`, or a flag in the session).
- SQLite: `PRAGMA journal_mode = WAL`, `PRAGMA busy_timeout = 5000`,
  `PRAGMA foreign_keys = ON` on every connection, one writer at a time, and
  the file outside the web root and inside the backup.

## 12. Seeds and fixtures

- A seed script, separate from the migrations and safe to run twice, with
  plausible sample data for development that is clearly sample
  (`Sample product 1`, `owner@example.com`), in the product's language; not
  invented real brands or people. Never run against production.
- Safe twice means upserts by a natural key, and a fixed seed for any faker,
  so everyone gets the same data. Reference data every environment needs
  (countries, currencies, plans, roles) ships in a migration, not a seed.
- Tests build their own rows with factories (Factory Bot, factory_boy,
  Laravel factories, fishery with `@faker-js/faker`), setting only the
  fields the test is about (`backend-testing`). Production data copied for
  development is anonymised first.

## Check it

- The migrations apply to an empty database and roll back where they claim
  to; the drift check is clean (`alembic check`,
  `manage.py makemigrations --check`, `prisma migrate diff --exit-code`).
- The SQL log for one list request shows a fixed number of queries, however
  many rows; `EXPLAIN ANALYZE` shows index scans on large tables.
- Two concurrent buys of the last item: one succeeds, one gets `409`; a
  stale `version` gets `409`; a split amount adds up to the whole.

## Avoid

Floats for money; times without a zone; a table created by hand; an edited
migration that already ran; stock or a balance updated with a read, a sum in
code and a write; `max(id) + 1`; a query in a loop; `SELECT *` sent to the
client; values or sort columns concatenated into SQL; a list with no limit;
an email sent inside a transaction; a pool per request; constraint errors
parsed from message text; `date(created_at)` in a `WHERE`; a replica read
deciding a write; bulk inserts fed rows nobody validated.
