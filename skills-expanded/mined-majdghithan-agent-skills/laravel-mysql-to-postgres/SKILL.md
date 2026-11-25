---
name: laravel-mysql-to-postgres
description: Migrate a Laravel application's database from MySQL/MariaDB to PostgreSQL safely. Use when moving a Laravel app to Postgres, when Eloquent/queries behave differently after switching drivers, or when planning a MySQL->Postgres cutover. Covers the migration strategy (pgloader vs query-builder), the Laravel-specific behavior differences that silently break (case sensitivity, booleans, the id-sequence trap, raw SQL, GROUP BY strictness), and a verification checklist.
---

# Laravel: MySQL -> PostgreSQL migration

The data moves fine. What breaks is the assumptions your app baked in over the years, because **MySQL is forgiving and Postgres is strict**. Every place you leaned on MySQL being lenient is a bug waiting on the other side. Treat a migration as an *audit of your app's lazy assumptions*, not a data transfer.

## Step 0 - The one test that surfaces half the problems

Before touching real data, point `php artisan migrate` at a **fresh empty Postgres database** and watch what throws. If every migration runs clean, your schema is genuinely database-agnostic. If it throws, you just found your MySQL-only assumptions for free.

```bash
# .env pointed at an empty pgsql db
php artisan migrate:fresh   # does the schema even build on Postgres?
```

Do not delete MySQL the day you switch. Keep it running for days/weeks until you're sure - cutovers get reverted.

## Step 1 - Move the data (pick one)

- **`pgloader`** - a single tool built for exactly this. Reads MySQL, writes Postgres, converting types as it goes (`TINYINT(1)` -> `boolean`, `AUTO_INCREMENT` -> sequence). One command, most of the job. **Usually resets sequences for you** (see the trap below).
- **Laravel's query builder** - read from the old connection, write to the new one in PHP, transforming rows. More control, more code; good when the schema has corners pgloader trips on. **Does NOT reset sequences** - you must do it manually.

## The behavior differences that silently break Laravel

### 1. Search stops matching (case sensitivity) - the big one for any app with search
MySQL's default collation is case-INsensitive; Postgres is case-SENSITIVE.
```php
// Worked on MySQL ('iphone' matched 'iPhone'), silently returns nothing on Postgres:
Product::where('name', 'LIKE', "%{$q}%")->get();
// Fix - case-insensitive LIKE:
Product::where('name', 'ILIKE', "%{$q}%")->get();
// Heavy search: the citext extension, or a functional index on LOWER(name).
```
Audit every product search, "find by email", and user-typed filter.

### 2. 0 and 1 are not true/false
MySQL has no real boolean (`TINYINT(1)`); Postgres has a real `boolean`. Laravel casts smooth over most of it, but raw comparisons bite:
```php
DB::table('shops')->whereRaw('is_active = 1')->get();   // PG: "operator does not exist: boolean = integer"
Shop::where('is_active', true)->get();                  // let Eloquent + the 'boolean' cast handle it
```

### 3. The id-sequence trap (the nastiest - passes tests, explodes in prod)
When you bulk-import existing rows, the table's id **sequence does not advance**. Your data has ids up to 40,000; the sequence still thinks the next id is 1. The first insert after go-live collides on a duplicate key - on checkout, in production.
```sql
-- After a data import, bump every table's sequence past its max id:
SELECT setval(pg_get_serial_sequence('orders','id'), (SELECT MAX(id) FROM orders));
-- repeat for every imported table. pgloader usually handles this; a query-builder migration does NOT.
```

### 4. Your raw SQL speaks MySQL
Anywhere you used `DB::raw`, `whereRaw`, `selectRaw`, or a MySQL function, Postgres may not understand it:
- `FIND_IN_SET()`, `GROUP_CONCAT()` -> Postgres arrays / `string_agg()`
- `DATE_FORMAT()` -> `to_char()`
- `RAND()` -> `RANDOM()`
- Backtick quoting `` `col` `` -> double quotes `"col"`

Grep the whole app for `DB::raw|whereRaw|selectRaw` before cutover; each hit is a manual review.

### 5. Postgres won't let sloppy queries slide
- **GROUP BY is strict:** every non-aggregated column in `SELECT` must appear in `GROUP BY`. MySQL guessed; Postgres refuses. Reporting/dashboard queries hide this.
- **No silent truncation:** a string longer than the column throws instead of being trimmed. A bad value in a `uuid` column throws instead of being stored. Postgres is protecting your data, but old code that relied on the trim now errors.

## Verification checklist (before deleting MySQL)
- [ ] `migrate:fresh` runs clean on empty Postgres
- [ ] Every `DB::raw`/`whereRaw`/`selectRaw` reviewed and ported
- [ ] All search/filter code uses `ILIKE` (or `LOWER()`/citext) where case-insensitivity is expected
- [ ] Every imported table's sequence reset (`setval(pg_get_serial_sequence(...))`); create one record per critical table and confirm no duplicate-key error
- [ ] Boolean columns cast to `'boolean'`; no raw `= 1`/`= 0`
- [ ] Reporting/GROUP BY queries run without error
- [ ] Run the full test suite against Postgres; smoke-test the real app end to end
- [ ] Keep MySQL live and revertible until confident

## Why bother
On the other side: `JSONB` with real indexing (great for attribute-heavy catalogs), stricter integrity that catches bugs MySQL swallowed, and query planning that holds up as data grows. Postgres is the strict senior reviewer your codebase never had - it will find things, and that's the point.

## Sources
[Laravel Cloud: Migrate MySQL to PostgreSQL](https://cloud.laravel.com/docs/knowledge-base/migrating-mysql-to-postgresql) · [Flare: migrating with Laravel's query builder](https://flareapp.io/blog/migrating-from-mysql-to-postgres-using-laravels-query-builder) · [pgloader](https://pgloader.io)
