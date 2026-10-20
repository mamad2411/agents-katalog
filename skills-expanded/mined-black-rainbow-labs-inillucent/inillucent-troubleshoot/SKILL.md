---
name: inillucent-troubleshoot
description: Diagnose an inillucent failure. Covers exit code 3 and the unsupported status, the other status names (syntax, not_found, constraint, readonly, busy, corrupt, invalid_state), a refused overwrite or a path outside --root, a busy database, a slow query, a value with an unexpected type, a failed migration, a damaged file, and a test run that passes because its prerequisite is missing. Use when inillucent did something unexpected, an error message needs interpreting, or a passing result looks too easy.
---

# When inillucent does something you did not expect

This skill explains what an inillucent failure means and what to do next. Start with the class of
the failure, then read the message. Every way of running inillucent reports the class: the exit
code of the `inillucent` command, and the `status` name in `--output json`, in a driver error and in
an MCP result.

## Terms used on this page

| Term | Meaning |
|---|---|
| status | one word that names the class of a failure, such as `unsupported` or `busy`. The drivers, the command line and MCP use the same names |
| `--root` | a flag that confines `inillucent` and `inillucent-mcp` to one directory. Every path must resolve inside it |
| affinity | the rule a column's declared type sets for converting a value on the way in. It does not fix the type of what is stored |
| query plan | the steps the engine chooses to answer a query. `inillucent explain` prints it |
| prerequisite | something a test suite needs that the workspace cannot build, such as the pinned SQLite or a live PostgreSQL |

Other terms are in [the glossary](../../docs/glossary.md).

## Read the exit code and the status first

```mermaid
flowchart TB
    A["inillucent exits"] --> B{"exit code"}
    B -- "0" --> C["it worked"]
    B -- "1" --> D["it failed: read the status"]
    B -- "2" --> E["the command line was wrong: run inillucent help"]
    B -- "3" --> F["unsupported: the engine has not built that construct"]
```

| Exit code | Status | Meaning |
|---|---|---|
| `0` | | it worked |
| `1` | every status except `unsupported` | it failed, and the status says how |
| `2` | | the command line was not one `inillucent` could act on: an unknown verb or flag, or a missing argument |
| `3` | `unsupported` | the engine has not built that construct |

The statuses you will see most often, each produced by the release build:

| Status | What caused it | An example message |
|---|---|---|
| `unsupported` | a construct the engine has not built | `unsupported: nested EXPLAIN` |
| `syntax` | the statement is not valid SQL | `near "SELEC": syntax error` |
| `not_found` | no such table, column, index, function or capability | `no such table: nothere` |
| `constraint` | a constraint refused the write | `UNIQUE constraint failed: t.a` |
| `readonly` | a write on a connection opened with `--readonly`, or on a file this process may not write, which opens read only | `'exec' changes the database, and this is read only.` |
| `busy` | another process holds the file for writing, for longer than `PRAGMA busy_timeout` | `another process holds the file for writing; ...` |
| `corrupt` | the file is not a database, or is damaged | `database disk image is malformed` |
| `io` | the file system refused a read or a write | |
| `invalid_state` | a misuse the command itself refused: a file that already exists, a path outside `--root`, two statements given to `query` or `exec` | `exec runs one statement and this is several; ... Use batch` |

The driver has four more statuses: `interrupted`, `full`, `too_big` and `internal`. `internal` is a
defect in inillucent. Report it. `full` means the disk refused a write, or the file is at its
`PRAGMA max_page_count` (the message is `database or disk is full` in both cases). The statement that
met it failed, and the next statement on the same connection writes again once space is free. If the
disk has room, run `PRAGMA max_page_count` and compare it with `PRAGMA page_count`. A limit that was
set on the connection stays until the file is reopened, and `PRAGMA max_page_count = 4294967294`
removes it. The transaction the statement was in stays open. A file in the default `auto_vacuum` mode
keeps the pages that deletes free, so it can be full of free pages: `PRAGMA freelist_count` says how
many, and `PRAGMA auto_vacuum = FULL` followed by `VACUUM` makes the file give them back. `too_big`
also covers a page cache with no page it can give up, which a larger `PRAGMA cache_size` lifts.
Before version 2.0.8 `inillucent batch` and `inillucent analyze` reported `busy` as `syntax`, and the
driver reported out of memory as `syntax`.

With `--output json`, a failure prints one object with these members:

| Member | What it holds |
|---|---|
| `ok` | `false` |
| `command` | the verb that failed |
| `status` | the status name from the table above |
| `message` | what went wrong, in a sentence |
| `feature` | only for `unsupported`: the construct the engine has not built |
| `offset` | only when the failure knows it: the byte in the statement where it went wrong |
| `text` | the same failure as the text output prints it |

Branch on `status` or on the exit code. Do not match on `message`, because the wording of a message
can change between releases.

## "It says unsupported" or "it exited 3"

```sh
inillucent --db app.rdb exec "EXPLAIN EXPLAIN SELECT 1"
```

```text
Error [unsupported]: unsupported: nested EXPLAIN
  not built yet: nested EXPLAIN
```

The SQL is correct. The engine has not built that construct, so rewording the same construct gets
the same answer. Write the statement another way: here, run `EXPLAIN` on the inner statement
alone. Ask what the engine supports before you write an unusual statement:

```sh
inillucent capabilities                  # the whole table
inillucent capabilities triggers         # one row
```

`inillucent capabilities` lists 57 capabilities. A test checks every row but two against the running
engine in both directions: a row that says yes and fails, or a row that says no and works, fails the
build. The two unchecked rows are `cancel` and `readonly_open`, and both say `partial`. A name that
is not in the table is the status `not_found` and means no.

An older release that opens a file a newer release created also exits 3:

```text
Error [unsupported]: could not open "app.rdb": this database is format version 3 and this build reads version 2; upgrade inillucent to open it
```

Every file that 2.5.0 or a later release creates is format 3, and releases from 0.1.5 to 2.4.2
refuse it with this message. Upgrade the program that opens the file. This happens most often when
an application built with the `inillucent` crate writes the file and an older `inillucent` command
line, installed separately, is used to look at it. Install the command line at the crate's version. Nothing converts a format 3
file back to format 2. A file that an earlier release created stays at format 2 until it stores a
key longer than `page_size / 8` or is rebuilt by `VACUUM`, so the earlier release can still open it.
A file becomes format 4 when `ALTER TABLE ... ADD COLUMN` is run on a table that has rows or a row of
more than about 1,900 integers is stored. Releases 2.5.0 to this one refuse it with
`this database is format version 4 and this build reads version 3`.

[`docs/feature-comparison.md`](../../docs/feature-comparison.md) compares inillucent with the pinned
SQLite 3.53.4, case by case. On the 1.0.32 build, 402 of 416 probed cases produce the same answer.
Of the other fourteen:

| Cases | What they are |
|---|---|
| 6 | vector features SQLite does not have |
| 6 | answers that differ from SQLite's |
| 2 | `DELETE ... LIMIT` and `UPDATE ... LIMIT`, which the pinned SQLite build refuses and inillucent runs |

## "It refuses to write the file"

| Message | What it means | What to do |
|---|---|---|
| `"<path>" already exists. Open it instead of creating it.` | `inillucent create` never replaces a file | open the file with `--db`, or create a different path |
| `"<path>" already exists. This tool never overwrites.` | `inillucent migrate` never replaces its destination | choose another `--destination`. The existing file is untouched |
| `"<path>" is outside <DIR>, which this server is confined to.` | the command runs with `--root`, and the path is outside `<DIR>` | use a path under `<DIR>` |
| `"<path>" resolves to <RESOLVED>, which is outside <DIR>, which this server is confined to.` | the path resolved to `<RESOLVED>`, outside `<DIR>` | compare `<RESOLVED>` with what you typed. When the path you typed is under `<DIR>`, a Windows junction or a symbolic link on the way leads out of `<DIR>` |
| `this surface is confined to a directory with --root, and a migration from a server reaches a host and a port ...` | `--root` also refuses network access | run the server migration without `--root` |
| `'exec' changes the database, and this is read only.` | the connection was opened with `--readonly` | drop `--readonly`, or run a `SELECT` |

`inillucent backup <file>` replaces an existing file at `<file>`, but only after the copy is
written beside it and checked, and it removes the log files the replaced database left. A backup
onto the database it is copying is refused with `cannot back up ... onto itself`. Builds before this
change copied the file onto itself and destroyed it.

`--readonly` decides by what a statement does. The SQL parser classifies the statement, so
`SELECT 'delete' FROM t` runs, and `DELETE FROM t` is refused with `readonly`.

## "The database is busy"

One process writes at a time. A second writer waits up to `PRAGMA busy_timeout`, which is 5000
milliseconds by default, and then fails with the status `busy`. A reader does not wait for a write
transaction from 2.0.4 on; it waits only while a writer folds the log into the file, or for a writer
under `PRAGMA locking_mode = exclusive`. On the 1.0.32 build, while one
process held a write transaction open, a second process could not open the file at all. It waited
5013 ms and failed:

```text
Error [busy]: could not open "<path>": another process holds the file for writing; this connection wanted it for reading, and waited 5013 ms of the 5000 ms PRAGMA busy_timeout
```

Find the process that holds a write transaction open, and make it commit or roll back. To wait
longer, run `PRAGMA busy_timeout = <milliseconds>` on the connection that waits.

A transaction that reads first and then writes can fail with `busy` at its first write:
`another process committed after this transaction began reading, so it cannot write`. Roll it back
and run it again, or start it with `BEGIN IMMEDIATE`, which takes the write lock at `BEGIN`. A plain
`BEGIN` takes no lock from version 2.0.8 on, so a read transaction no longer waits for a writer;
before it, every `BEGIN` took the write lock and failed with `busy` beside any open write
transaction.

To set the wait before a connection exists, set `INILLUCENT_BUSY_TIMEOUT=<milliseconds>` in the
environment of the process that opens, or pass the wait to the open: `OpenOptions::busy_timeout` in
Rust, `inillucent_open_with_timeout` in C, `busy_timeout_ms` in Python. The connection starts with
that value as its `busy_timeout`. An open does not wait for a writer; its first statement does. A
message that starts `could not open` means the open itself waited, which it does only for a file
another process is still creating.

Inside one Rust program, a `Database` from `inillucent-driver` is neither `Send` nor `Sync`, so it
cannot move between threads. To use one database from several threads, open a `SharedDatabase`.
`SharedDatabase` runs one statement at a time.

## "A query is slower than I expected"

```sh
inillucent --db app.rdb explain "SELECT * FROM n WHERE k = 'a'"
```

```text
SCAN n
```

`SCAN n` means the engine reads every row of `n`. After `CREATE INDEX n_k ON n(k)`, the same
command prints `SEARCH n USING INDEX n_k (k=?)`, which means the engine uses the index.

| Check | Command |
|---|---|
| which indexes a table has | `inillucent --db app.rdb describe n` |
| gather the statistics the query planner reads | `inillucent --db app.rdb analyze` |
| the query plan | `inillucent --db app.rdb explain "<SQL>"` |

An `OR` uses an index only when every arm of it can: `WHERE a = 1 OR b = 2` prints `MULTI-INDEX OR`
and reads a few rows when both `a` and `b` are indexed, and scans the table when one of them is not.

Two things cost more than they appear to:

- **`--limit` does not make a query faster.** The engine reads every row so that `total` is exact.
  `--limit` (200 by default) cuts the rows kept and printed, and the other rows are counted and not
  held, so a query over millions of rows needs memory for 200 rows. Put `LIMIT` in the SQL itself to
  read fewer rows. `--limit 0` asks for every row, and the output object holds them all.
- **A vector search with no index reads every row.** The answer is still correct.
  `CREATE INDEX <name> ON <table> USING inillucent_hnsw (<column>)` adds an HNSW index, including
  over rows already in the table.
- **An HNSW index created by inillucent 1.0.29 or earlier also compares every row.** Those releases
  created every `inillucent_hnsw` index in exact mode. `SELECT v FROM <index>_config WHERE k = 'mode'`
  says which mode an index has. Drop the index and create it again to make it walk the graph.

## "A value came back with the wrong type"

Values are typed as in SQLite. A column's declared type sets its affinity: how a value is converted
when it is written. The declared type does not guarantee the type of what is stored.

`--output json` reports each result column's `type` from the values in the result. When the values
have different types, the `type` is `mixed`. That is what was stored. The type in
`inillucent describe` is only the declared type.

A server migration stores some columns as `TEXT` on purpose, to keep every digit:

| Source column | Stored as |
|---|---|
| PostgreSQL `numeric`, MySQL `decimal` or `numeric` | `TEXT`, digit for digit |
| MySQL `BIGINT UNSIGNED` | `TEXT`, because a value above the signed 64 bit range does not fit an `INTEGER` |

The [`inillucent-migrate`](../inillucent-migrate/SKILL.md) skill lists every type.

## "A migration failed"

`inillucent migrate` prints every check, passed or failed. A failed check names the table and says
whether the row count or the digest disagreed.

- Nothing that failed a check is published. The destination path stays empty.
- The staging file `.<name>.staging` stays beside the destination. A server migration also writes
  `<name>.migration-report.md` there. Both are the evidence of what happened.
- A server migration refuses to start while an old staging file is there. It never resumes, because
  the server may have changed since the first run. Move or remove the staging file, then run
  `inillucent migrate` again.

For a SQLite file, a digest that disagrees on a table is explained. The message says how many rows
each side holds, which columns were compared, and up to three rows that only one side holds, written
as `name=value`. A `VIRTUAL` generated column is left out of the digest on both sides, because no
file stores its value. A separate `columns.<table>` check compares the declared column lists.

A server login failure starts with the server's own error code: `postgres 28P01: ...` or
`mysql 1045 (28000): ...`. Match on the code. The rest of the sentence is in the server's language.

## "Is this file damaged?"

```sh
inillucent --db app.rdb integrity-check
```

`inillucent integrity-check` exits 0 with `"ok": true` only when every row of
`PRAGMA integrity_check` is exactly `ok`. Any other answer, including no rows, fails with the status
`corrupt`, and the message lists what is wrong. Examples: a page two tables both claim, a page the
free map lists as free while a table uses it, an index entry with no row, or `Page N: never used`.
A file that cannot be opened at all also fails with `corrupt`.

An encrypted database fails with `corrupt` in three more ways, and the message says which:

| Message | What to do |
|---|---|
| `this database is encrypted. Open it with its key` | pass `--key-file`, set `INILLUCENT_KEY`, or use a driver's key option |
| `this database is not encrypted, so it cannot be opened with a key` | open it without a key, or write an encrypted copy with `inillucent encrypt` |
| `file is not a database, or the key is wrong` | the key is wrong. A passphrase is the whole text, and a raw key is `x'` followed by 64 hex digits and `'` |

`PRAGMA encryption` answers `xchacha20-poly1305` on an encrypted database and `none` otherwise.
See `docs/encryption.md` in the repository.

A tree whose keys are out of order is named in the message, with the leaf pages involved:
`index <name>: a key does not increase across the leaf chain: leaf 211739 holds a key at or below
the one before it, which leaf 95106 holds`. An index can be rebuilt from its table with `REINDEX`,
and `integrity-check` afterwards says whether that was enough.

`Page N: never used` is a leak: the free map counts the page as in use and no table or index
reaches it. No row is lost. Every leaked page is listed, one line each, up to a hundred, and
`VACUUM` gives them back.

| Pragma | What it checks |
|---|---|
| `PRAGMA quick_check` | every tree's structure, and which tree owns each page |
| `PRAGMA integrity_check` | the same, then every index against its table. This is the slower one |

A file whose free map chain returns to a page it already read is refused when it is opened, with a
message that names the chain.

Releases up to 2.0.2 could damage a file that one process wrote while another process opened it.
The writer had to be changing more pages than its buffer pool holds. The damage looks like one of
these:

- `page N checksum 00000000 is not the computed ...`, with pages of zeros near the end of the file;
- `the sibling chain visits N leaves and the interior levels reach M`;
- `replaying InsertRow at ... found no room in leaf N`, when the file is opened;
- rows whose committed changes are gone, with `integrity-check` answering `ok`.

2.0.3 fixes it. Upgrade every program that opens the file, including drivers and the MCP server.
An upgrade does not repair a file that is already damaged. Copy the tables that still read into a
new file, or build the file again from its source.

## "The test suite passes and I do not believe it"

Some suites need a prerequisite the workspace cannot build: the pinned SQLite, a fixture corpus, a
live PostgreSQL or MySQL server. Such a suite reports success when its prerequisite is absent.

```sh
target/debug/inillucent-testrun --strict
```

`--strict` counts those suites as failures and names them. Set up the prerequisites first:

| Prerequisite | How to get it |
|---|---|
| the pinned SQLite, in `.sqlite-ref/` | `pwsh tools/sqlite-reference.ps1`, or `tools/sqlite-reference.sh` |
| the fixtures in `_agent_output/fixtures/` | `tools/build-gate-fixtures.sh`, or copy them from the main checkout |
| a live PostgreSQL or MySQL | the comments at the top of `crates/inillucent-remote/tests/live_postgres.rs` and `live_mysql.rs` |

## "It printed an error and the exit code was zero"

`inillucent-testrun` has three exit codes:

| Exit code | Meaning |
|---|---|
| `0` | every selected target ran and passed |
| `1` | the run happened and failed |
| `2` | the run did not happen: the build failed, a named selection matched nothing, or `--filter` matched no test. Nothing was graded |

In a shell, `$?` after a pipeline is the exit code of the last command in the pipeline:

```sh
target/debug/inillucent-testrun --changed | tail -40 ; echo $?       # the exit code of tail, always 0
target/debug/inillucent-testrun --changed > run.log 2>&1 ; echo $?   # the exit code of the runner
```

## Where to look next

| Question | Page |
|---|---|
| what SQL the engine supports, and what it refuses | [`docs/sql.md`](../../docs/sql.md) |
| every probed construct, measured against SQLite | [`docs/feature-comparison.md`](../../docs/feature-comparison.md) |
| what is not built yet | [`docs/roadmap.md`](../../docs/roadmap.md) |
| what a driver promises | `drivers/README.md` in the repository, `DRIVER.md` in a release archive |
| how the test runner decides what to run | [`tests/inillucent-testing-tdd.md`](../../tests/inillucent-testing-tdd.md) |
