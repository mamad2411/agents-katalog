---
name: inillucent-query
description: Explore and query an existing inillucent database. List tables, describe a schema, run SELECT statements safely with bound parameters and read only mode, read the query plan, and export rows. Use when asked to look at, inspect, report on or extract data from an .rdb file you did not create.
---

# Querying a database somebody else built

Work in this order: find out what the file holds, look at the one table you need, then write SQL
against that table. Guessing at column names first wastes calls.

## 1. See what the file holds

An encrypted database needs its key on every command: `--key-file <file>`, or the key in
`INILLUCENT_KEY`. Without it every command fails with the status `corrupt` and a message that says
the database is encrypted.

```sh
inillucent --db app.rdb tables            # tables and views
inillucent --db app.rdb schema            # every CREATE statement
inillucent --db app.rdb schema 'user%'    # CREATE statements whose name matches a LIKE pattern
inillucent --db app.rdb indexes           # every index and its table
inillucent --db app.rdb stats             # page cache, pool size, page size and page count
```

## 2. Describe the one table

```sh
inillucent --db app.rdb describe note
```

`describe` returns the columns and their types, the primary key, every index, the row count and the
`CREATE TABLE` statement in one call. It lists every column, including generated ones, and its
`kind` column says `generated stored`, `generated virtual`, or `hidden` for a hidden column of a
virtual table. Run `describe` before you write SQL against a table you did
not create. `describe` also shows whether the table is a keyword search or vector search table,
which changes how you query it. The [`inillucent-search`](../inillucent-search/SKILL.md) skill covers
those tables.

## 3. Run the query

```sh
inillucent --db app.rdb query "SELECT id, body FROM note WHERE created > ?1 ORDER BY id" \
  --params '["2026-01-01"]' --limit 50 --output json
```

- **`--params` binds `?1`, `?2` and so on, in order.** Pasting a value into the SQL text causes
  quoting bugs. `--params-file` reads the same JSON array from a file.
- **`--limit` cuts the rows returned, not the count.** The result's `total` is the real number of
  rows, and `more` is `true` when rows were cut. The default is 200. `--limit 0` returns every row.
- **`--readonly` refuses every statement that would change the database.** The engine decides this
  from the parsed statement, so `SELECT 'delete me'` runs and `DELETE FROM note` is refused with the
  status `readonly`. Add `--readonly` whenever you only mean to read. It also refuses the `.shell`
  and `.system` commands of `run`, because a program can write files the engine never sees.

```sh
inillucent --db app.rdb --readonly query "SELECT count(*) FROM note"
```

## 4. When a query is slow

```sh
inillucent --db app.rdb explain "SELECT * FROM note WHERE created = '2026-01-01'"
```

```text
SEARCH note USING INDEX ic (created=?)
```

`explain` prints the query plan in the format of SQLite's `EXPLAIN QUERY PLAN`, without running the
statement. `SEARCH note USING INDEX ic` means the engine uses the index `ic`. `SCAN note` means it reads
every row. If you expected an index and see `SCAN`, run `describe` to check that the index exists.

```sh
inillucent --db app.rdb analyze
```

`analyze` gathers the statistics the query planner reads.

## 5. Get the rows out

```sh
inillucent --db app.rdb export note --format csv --out note.csv
inillucent --db app.rdb export --sql "SELECT id, body FROM note WHERE id < 100" --format json
inillucent --db app.rdb dump                       # the SQL that would rebuild the database
inillucent --db app.rdb backup app-backup.rdb      # a copy of the database file
```

`export` writes csv (the default), json, tabs, markdown, insert, quote, line or html. Without
`--out`, the rows come back in the result. With `--out`, the rows go to the file and the result
reports the file path in `wrote`, the byte count in `bytes`, and the row count in `total`. Compare
`total` with the row count you expected.

## Writing, when you have to

```sh
inillucent --db app.rdb exec "UPDATE note SET body = ?1 WHERE id = ?2" --params '["edited", 1]'
inillucent --db app.rdb batch "UPDATE note SET body = 'a' WHERE id = 1; DELETE FROM note WHERE id = 2"
```

`exec` runs one statement and reports the number of rows changed. `batch` runs several statements as
one transaction: all of them take effect, or none do. `batch` opens the transaction itself, so do
not put `BEGIN` or `COMMIT` in its input. Use `batch` whenever two changes must agree.

## Two things that surprise people

- **Exit code 3, or the status `unsupported`, means the engine has not built that feature.** The SQL
  is not wrong, and rewording it does not help. `inillucent capabilities` lists what the engine can
  do.
- **Values are dynamically typed, as in SQLite.** A column's declared type is its affinity: a rule
  for converting values as they are written. The declared type does not guarantee the type of what
  comes back. With `--output json`, each column in `columns` reports the storage class its values
  really had, or `mixed` when the values had different classes. Trust `columns`. The declared type
  that `describe` shows is only the affinity.
- **A file does not get shorter when rows are deleted, unless `auto_vacuum` is on.** `PRAGMA
  auto_vacuum` reads 0 (NONE, the default), 1 (FULL) or 2 (INCREMENTAL). In NONE mode the pages a
  delete frees stay in the file and later writes reuse them. In FULL mode each commit gives the free
  pages back, so `PRAGMA freelist_count` reads 0 and the file is shorter. In INCREMENTAL mode
  `PRAGMA incremental_vacuum(100)` gives back up to 100 free pages. `PRAGMA auto_vacuum = FULL` on a
  file that already has tables takes effect after `VACUUM`. It is a write, so a `--readonly`
  connection refuses it.

## Anything the commands do not cover

```sh
inillucent --db app.rdb run ".schema note
SELECT count(*) FROM note;"
```

`run` takes shell input, dot commands and SQL, and returns what the shell printed. Everything the
interactive shell can do is available through `run`, which helps when a script drives inillucent and
there is no terminal.
