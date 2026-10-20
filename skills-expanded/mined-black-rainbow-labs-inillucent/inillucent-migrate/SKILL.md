---
name: inillucent-migrate
description: Move an existing database into inillucent. The source can be a SQLite file, a running PostgreSQL or MySQL server, or a legacy retrieval index. Every table is checked by row count and by digest, and the new file is published only when every check passes. Use when asked to migrate, import, convert or move data into an .rdb, or to try inillucent on data that already exists somewhere else.
---

# Migrating into inillucent

This page shows how to build an inillucent database from data you already have. It covers the four
sources, the checks that decide whether the new file is published, and what to do when a check
fails.

| Source | Command |
|---|---|
| a SQLite database file | `inillucent migrate legacy.db --destination app.rdb` |
| a running PostgreSQL server | `inillucent migrate "postgres://user@host:5432/db" --destination app.rdb` |
| a running MySQL server | `inillucent migrate "mysql://user@host:3306/db" --destination app.rdb` |
| a legacy retrieval index directory | `inillucent-migrate <source-index-dir> <destination.db>` |

## Terms used on this page

| Term | Meaning |
|---|---|
| destination | the new `.rdb` file the migration builds |
| staging file | the file the migration writes first. It sits beside the destination under a hidden name, such as `.app.rdb.staging` |
| publish | rename the staging file to the destination name. This happens only after every check passes |
| digest | a SHA-256 hash over every row of a table. It does not depend on the order the rows are read in |
| snapshot | a view of the server's data as of one instant. Writes that commit later are not visible in it |
| TLS | the encryption a database server connection uses. See the [glossary](../../docs/glossary.md) for other terms |

## What every migration does

```mermaid
flowchart TB
    A["Read the source"] --> B["Write the staging file beside the destination"]
    B --> C["Close and reopen the staging file"]
    C --> D["Check every table: row count, digest, column list"]
    D -->|"every check passes"| E["Rename the staging file to the destination"]
    D -->|"a check fails"| F["Stop. Keep the staging file and the report"]
```

Three rules hold for every source:

1. **The source is never written to.** No flag changes the source, and no step deletes anything.
   To go back, open the source. It is unchanged.
2. **The destination is never overwritten.** `inillucent migrate` refuses a destination path that
   already exists. The build goes to the staging file, so a half written database never sits at the
   path an application opens.
3. **Nothing unverified is published.** Every table is checked by row count and by digest. A copy
   with the right number of rows and the wrong bytes passes a count check. The digest catches it.
   When a check fails, nothing is published, and the staging file stays on disk for you to look at.

## From a SQLite file

```sh
inillucent migrate legacy.db --destination app.rdb
```

```
imported legacy.db into app.rdb
```

`inillucent migrate` treats a source that is a path as a SQLite file. `--kind sqlite` says the same
thing explicitly.

What comes across:

| Object | What happens |
|---|---|
| tables and their rows | copied, then checked by count, digest and column list |
| indexes, views, triggers | copied |
| FTS5 tables | rebuilt: the text is indexed again through inillucent's own `fts5`, and the row ids are kept |
| a virtual table using any other module, such as `rtree` | the migration fails and names the module. SQLite stores that module's data in its own format, and inillucent has no content table to rebuild it from |
| `PRAGMA user_version`, `PRAGMA application_id` | copied from the source file's header and checked |

`--output json` returns every check with its name, whether it passed, and a detail. This is the
result of a migration of a table `note` with three rows and an FTS5 table `doc`:

```json
{
  "ok": true,
  "command": "migrate",
  "columns": [],
  "rows": [],
  "row_count": 0,
  "total": 0,
  "more": false,
  "changes": 0,
  "last_insert_rowid": 0,
  "elapsed_ms": 106.0701,
  "destination": "app.rdb",
  "checks": [
    {
      "name": "columns.note",
      "passed": true,
      "detail": "3 columns, in the order the source declares"
    },
    {
      "name": "count.note",
      "passed": true,
      "detail": "3 rows"
    },
    {
      "name": "digest.note",
      "passed": true,
      "detail": "c49ee80130e38a4eadd292ae05452225521ea9758ab159d42aac23215b2e1e25"
    },
    {
      "name": "carried.doc",
      "passed": true,
      "detail": "1 rows rebuilt through this engine's own fts5"
    },
    {
      "name": "pragma.application_id",
      "passed": true,
      "detail": "0 carried from the source"
    },
    {
      "name": "pragma.user_version",
      "passed": true,
      "detail": "7 carried from the source"
    }
  ],
  "text": "imported legacy.db into app.rdb"
}
```

### Generated columns

A `STORED` generated column has a value in each SQLite row, so it is copied and included in the
digest like any other column. A `VIRTUAL` generated column has no stored value. SQLite computes it
when the row is read, and inillucent does the same.

So the digest covers only the stored columns. The `columns.<table>` check compares the full list of
declared columns, in order, so a `VIRTUAL` column that was dropped or moved still fails the
migration.

## From a running PostgreSQL or MySQL server

```sh
inillucent migrate "postgres://user@127.0.0.1:5432/corpus" --destination corpus.rdb
inillucent migrate "mysql://root@127.0.0.1:3306/app" --destination app.rdb
```

The URL's scheme picks the kind. `--kind postgres` or `--kind mysql` overrides it.

| Option | What it does |
|---|---|
| `--destination <file>` | the `.rdb` file to build. Required |
| `--kind <kind>` | `sqlite`, `postgres`, `mysql` or `index` |
| `--batch <n>` | rows per destination transaction. Default 10,000. It changes how long the migration takes. It does not change the result |
| `--insecure-plaintext` | allows an unencrypted connection to a host that is not a loopback address. See [Encryption](#encryption) |

**The whole read happens inside one read only snapshot at the repeatable read isolation level.**
The snapshot opens before the migration reads the list of tables. So every table, and the schema
itself, comes from the same instant. Rows arrive through a cursor, so a table larger than memory
costs one batch of memory.

### Where the password goes

A URL on the command line is visible in the process list for the whole run. There are four ways to
give the password or the whole URL:

| Where | How |
|---|---|
| in the URL | `postgres://user:secret@host/db` |
| `INILLUCENT_SOURCE_URL` | leave out the source argument and set this variable to the URL |
| standard input | write `-` as the source, and `inillucent migrate` reads one line from standard input |
| `PGPASSWORD` or `MYSQL_PWD` | the password alone, read when the URL has none |

The password is replaced with `***` everywhere it is printed: the terminal, the report file, and
the MCP result.

### What comes across

| Object | What happens |
|---|---|
| ordinary tables | copied: columns in order, whether each column allows NULL, and the primary key |
| views, materialized views, sequences, foreign tables, partitioned tables, triggers | listed in the report as not carried, one line each |
| MySQL routines | listed in the report as not carried |
| PostgreSQL tables in a schema other than `public` | copied with the schema in the name, as `schema__table`. inillucent has one namespace for table names, so two tables with the same name in two schemas do not collide |

### How values are converted

| Source type | Stored as |
|---|---|
| integer types | `INTEGER`, exactly |
| `real`, `double`, `float` | `REAL` |
| `numeric`, `decimal`, PostgreSQL `money`, MySQL `BIGINT UNSIGNED` | `TEXT`, digit for digit |
| `boolean` | `INTEGER`, 0 or 1 |
| MySQL `TINYINT(1)` | `INTEGER`, the value the server holds |
| `bytea`, `BLOB`, `BINARY`, `VARBINARY`, MySQL `BIT` and geometry types | `BLOB` |
| dates, times, `uuid`, `json`, arrays, ranges, enums and every other type | `TEXT`, exactly as the server prints it |

A `numeric(38,10)` converted to a 64 bit float loses digits, and no check would notice. Stored as
text, it keeps every digit the server printed. To use the value as a number, cast it in a query on
the destination.

### Encryption

A migration from a host that is not a loopback address uses TLS. inillucent checks the certificate
chain and the host name before it sends any user name, database name or password. When TLS fails,
the migration stops. It does not fall back to an unencrypted connection.

| What you write | What happens |
|---|---|
| nothing about encryption, and the host is not a loopback address | verified TLS |
| `sslmode=require`, `verify-ca` or `verify-full`, or MySQL's `ssl-mode=REQUIRED` | verified TLS |
| nothing, and the host is `127.0.0.1`, `::1` or `localhost` | no encryption |
| `sslmode=disable` and the `--insecure-plaintext` flag | no encryption |
| only one of `sslmode=disable` and `--insecure-plaintext` | refused |
| `sslmode=prefer` or `allow`, or MySQL's `preferred` | refused |

`prefer` means "encrypt if the server allows it". The answer would depend on a server setting the
migration cannot see, so inillucent refuses it and asks for `require` or `disable`.

A server with a certificate from a private authority needs `sslrootcert=<file>` in the URL
(`ssl-ca=<file>` also works). That authority then becomes the only trusted root for the connection.

The report file and the `transport` field in `--output json` say `verified-tls` or `plaintext`.

This is about the connection. The `.rdb` a migration writes is not encrypted, even when the command
line has a key. For an encrypted result, run
`inillucent --db new.rdb --key-file app.key encrypt new-encrypted.rdb` afterwards and remove the
plaintext file.

### MySQL 8 accounts that use `caching_sha2_password`

inillucent cannot complete the full `caching_sha2_password` login. That login needs an RSA key
exchange the client does not implement. The fast path works when the server has the account in its
cache. When it does not, the migration is refused, and the message names two fixes:

- connect once with the `mysql` client, which puts the account in the server's cache, or
- run the migration as an account created `IDENTIFIED WITH mysql_native_password`.

## From a legacy retrieval index

```sh
inillucent-migrate <source-index-dir> <destination.db> [--no-publish]
```

This migration uses the separate program `inillucent-migrate`, because it needs the retrieval
engine. `inillucent migrate --kind index` returns the status `unsupported` and prints this command.

`--no-publish` stops with a verified staging file and does not rename it.

A legacy index migration can resume. It keeps a manifest and continues from the last committed
batch, because a directory does not change between runs. A server can change between runs, so a
migration from PostgreSQL or MySQL always runs in one pass and refuses a staging file left by an
earlier run.

## Reading the result from a server migration

Every check is printed, whether it passed or failed:

```
postgres://user:***@127.0.0.1:5432/corpus -> corpus.rdb
PostgreSQL 17.2, 6 tables, 13 rows
transport: plaintext
  pass structure.integrity every tree walks in key order on a fresh open
  pass source.count.note 3 rows, counted separately from the scan
  pass count.note 3 rows
  pass digest.note 3b226c3862edea05bf0590bb25b713ec...
  ...
published: corpus.rdb
```

A file named `<destination>.migration-report.md` is written beside the destination. It has the same
checks, the transport, and the list of objects that were not carried.

`--output json` adds these fields to the result: `destination`, `transport`, `source` (with the
password replaced), `server`, `rows`, `tables`, `checks` and `notCarried`.

**What the checks prove.** The source rows come off the network through one reader. The
destination rows come off inillucent's own storage through another reader. When the two digests
agree, every value the migration read reached the destination unchanged.

**What the checks do not prove.** The copy and the source digest share the reader that decodes the
server's network protocol. If that reader decoded a value wrongly, both sides would agree on the
wrong value. The tests `crates/inillucent-remote/tests/live_postgres.rs` and `live_mysql.rs` check
that reader against `psql` and `mysql` themselves.

## From an agent, over MCP

The MCP tool `inillucent_migrate` takes the same arguments as `inillucent migrate`.

An MCP server started with `--root DIR` refuses a `postgres://` or `mysql://` source. `--root`
limits which files an agent can reach, and a migration from a server connects to a host and a port
outside that limit. Run a server migration from a command line without `--root`.

On a server started with `--root`, the source `-` (read from standard input) is also refused,
because MCP uses standard input for its own messages. Set `INILLUCENT_SOURCE_URL` instead.

## When it fails

| Message | Meaning | What to do |
|---|---|---|
| `"app.rdb" already exists. This tool never overwrites.` | the destination path is taken. The file there is untouched | pick another destination |
| `... is left over from an earlier migration` | a server migration failed before and left its staging file | read the report beside the staging file, move the staging file somewhere else, and run again |
| `postgres 28P01: ...` or `mysql 1045 (28000): ...` | the server refused the login. The code at the start is the server's own error code | match on the code. The wording after it can change |
| `... was not published: carried.r: r uses the rtree module ...` | a SQLite virtual table uses a module inillucent cannot rebuild | drop that table from a copy of the source, or migrate without it |
| `verification failed; nothing was published` | a count, digest or column check disagreed | read the report. It names the table and the check |

A digest failure on a SQLite source also names the rows: how many rows each side holds, which
columns were compared, and up to three rows that only one side holds, written as `name=value`.
