---
name: inillucent-embed
description: Put inillucent inside an application. Covers the Rust driver, the C library, and the Python, Node, Go and PHP packages. Use when asked to add inillucent to a codebase, write or fix a language binding, or replace SQLite or another embedded database in an application.
---

# Embedding inillucent in an application

This page shows how an application uses inillucent as a library, and the behaviors that most often
surprise a new user. `drivers/README.md` in the repository, copied as `DRIVER.md` into every
release archive, has the full contract.

## Terms used on this page

| Term | Meaning |
|---|---|
| driver | the Rust crate `inillucent-driver`. Every language reaches the engine through it |
| C library | `inillucent-driver-capi`, a C interface over the driver. Its header is `drivers/inillucent-driver-capi/include/inillucent_driver.h` |
| binding | code in another language that calls the C library |
| capability table | the list of features the engine reports, each marked `yes`, `partial` or `no` |
| session | what `temp.` tables, `ATTACH`, connection pragmas and a transaction belong to. Each connection is one session |

## How each language reaches the engine

| Language | Package | How it reaches the engine |
|---|---|---|
| Rust | `inillucent-driver` on crates.io | calls the driver directly |
| C and C++ | the C library | calls the C library |
| Python | `pip install inillucent` | the `Database` class calls the C library. `run()` and `query()` start the `inillucent` program |
| Node | `npm install inillucent` | loads the C library as a Node addon for `query()`, `exec`, `batch` and `open(db)`, in process. Other commands, and calls with `key` or `root`, start `inillucent --output json` or one `inillucent-mcp` process |
| Go | `go get github.com/Black-Rainbow-Labs/Inillucent/packages/go/v2` | starts `inillucent --output json` and parses the JSON |
| PHP | `composer require black-rainbow-labs/inillucent` | starts `inillucent --output json` and parses the JSON |

All four language packages are published at version 1.0.32. The Python wheel holds the C library
and the four programs, so it needs no compiler.

A package that starts the program gets JSON. A blob comes back as `{"blob": "<hex>"}`. An integer
larger than 2^53 is rounded by JavaScript's `JSON.parse`, and by Go's `encoding/json` unless the
decoder calls `UseNumber()`.

## Design for `unsupported`

The engine returns the status `unsupported` for a statement it has not built. The same status is
`Status::Unsupported` in Rust, `INILLUCENT_UNSUPPORTED` in C, and exit code 3 on the command line.
A mistyped statement gets a different status, such as `syntax`.

```sh
inillucent --db app.rdb exec "EXPLAIN EXPLAIN SELECT 1"
```

```
Error [unsupported]: unsupported: nested EXPLAIN
  not built yet: nested EXPLAIN
```

Keep `unsupported` separate from other errors in your code. An application can then tell its user
"this engine cannot do that yet" instead of "check your SQL". No case in the 416 case probe against
SQLite returns `unsupported`, and the capability table still lists 12 features as `no`, so write the
branch.

**Ask the capability table before you write unusual SQL.** `inillucent capabilities` prints it, and
the driver's `capability(name)` returns one row. A test checks each row against the running engine.
An unknown name returns nothing. Treat that as no.

## Rust

```rust
use inillucent_driver::{Database, Status, Value};

let database = Database::open("app.rdb")?;
let connection = database.session();

connection.execute("CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT)", &[])?;
connection.execute(
    "INSERT INTO people VALUES (?1, ?2)",
    &[Value::Integer(1), Value::Text("Ada".into())],
)?;

let rows = connection.query("SELECT id, name FROM people", &[], 200)?;
println!("{} of {}{}", rows.rows.len(), rows.total, if rows.more { "+" } else { "" });

// `limit` is a count. query(.., 0) returns no rows, with `total` set to the real count.
// Use query_all to get every row.
let everything = connection.query_all("SELECT id, name FROM people", &[])?;

match connection.query_all(statement, &[]) {
    Err(why) if why.status == Status::Unsupported => {
        println!("not yet: {}", why.feature.unwrap_or_default());
    }
    other => { other?; }
}
```

`Database::session` returns a `Connection`. The older name `Database::connect` still works and is
deprecated. Each connection has a transaction of its own: another connection reads only what is
committed, and a second writer waits for the busy timeout and then fails with `busy`. Rust calls the driver directly and does not go through the C library.

`embed(TEXT)` is compiled in only with the `embed` feature. Name it on the crate you depend on:
`inillucent = { version = "1.0", features = ["embed"] }`, or `features = ["embed"]` on
`inillucent-driver`. Releases up to 1.0.29 have no such feature on either crate. With those, add
`inillucent-engine = { version = "1.0.29", features = ["embed"] }` beside it. The model is loaded
when `embed(TEXT)` is first called, from the folder `inillucent setup-embeddings all` installs it in.

Releases 2.6.0 and earlier ask for `ort` `2.0.0-rc.10`, which cargo reads as any later release
candidate. A new project has no lock file, so cargo picks `2.0.0-rc.14`, and `inillucent-core` does
not compile against it. With those releases, add `ort = "=2.0.0-rc.13"` to your own
`[dependencies]`. Later releases ask for exactly `=2.0.0-rc.13`.

The `inillucent` command line has to be at least as new as the crate that wrote a file. A file that
2.5.0 or later creates is format 3, and command lines from 2.4.2 and earlier refuse it with
`this database is format version 3 and this build reads version 2`. Install the command line at the
crate's version, or run the query through a program built with the crate.

`Database::open` uses these defaults from `OpenOptions`:

| Option | Default |
|---|---|
| `create` | `true` |
| `read_only` | `false` |
| `cache_frames` | 4,096 frames, which is 128 MiB at the engine's 32 KiB page |
| `limits` | unbounded |
| `key` | `None`. With a key the database is encrypted at rest; see below |

### An encrypted database

```rust
use inillucent_driver::{Database, EncryptionKey, OpenOptions};

let options = OpenOptions {
    key: Some(EncryptionKey::parse("correct horse battery staple")),
    ..OpenOptions::default()
};
let database = Database::open_with("app.rdb", options)?;
```

The database file, its log and its journals are encrypted with XChaCha20-Poly1305.
`EncryptionKey::parse` reads `x'<64 hex digits>'` as a raw 32 byte key and anything else as a
passphrase, which costs about 200 ms of PBKDF2 per open. A wrong key, no key for an encrypted file
and a key for a plaintext file all fail with `Status::Corrupt`. `Database::export_to(path, key)`
writes an encrypted or a plaintext copy, and `PRAGMA rekey = '...'` changes the key. The C library
has `inillucent_open_with_key`, and the npm, Go, PHP and Python packages have a `key` option that
reaches the command line through `INILLUCENT_KEY`. Keep the key out of source code and out of a
command line: read it from a secret store or from the environment.

## Six behaviors to design around

| Behavior | What it means for your code |
|---|---|
| **Values are typed.** | A value is `Null`, `Integer`, `Real`, `Text` or `Blob`. The driver does not turn numbers into text. |
| **`Null` is its own value.** | `Value::Null` and an empty `Value::Text` are different values. |
| **`total` is exact.** | `limit` only caps the rows `query` hands back, and `more` is true when rows were left out. `query` and `query_all` hold every row the statement produced until they return, so a query over a large table costs the whole result. Put a `LIMIT` in the SQL, or read the rows with `Connection::query_each(sql, params, &sink)`, which hands each row to a `RowSink` as it is produced and holds none. The C library's `step` still builds the whole result. |
| **A batch is one transaction, checked before the commit.** | `Connection::transaction(work, check)` runs every statement, passes the changed row counts to `check`, and commits only when `check` returns `Ok`. Any failure rolls back every statement. |
| **One database runs one statement at a time.** | A `Database` is neither `Send` nor `Sync`. To use one database from several threads, open it with `SharedDatabase`, which runs each statement in turn on a thread of its own. |
| **Read only is enforced by the driver.** | With `OpenOptions::read_only` set, the driver refuses any statement that does not bind to a query, including a `PRAGMA`. The file is still open for writing, so the `readonly_open` capability says `partial`. |

## Writing a binding for another language

Bind the C library. These files are the contract:

| File | What it holds |
|---|---|
| `drivers/inillucent-driver-capi/include/inillucent_driver.h` | the header a binding compiles against |
| `drivers/abi.toml` | every C symbol, with its stability and the version it first appeared in |
| `drivers/conformance/suite.json` | the driver's expected behavior, written as test cases |
| `drivers/bindings/python/inillucent.py` | the reference binding. It uses only the Python standard library |
| `drivers/bindings/python/run_conformance.py` | a runner for `suite.json`, written in Python |

The rules a binding must follow:

- **The three ownership rules.** A handle with a `_free` or `_close` function is yours to free,
  once. A pointer the library returns points inside a handle, stays valid until that handle is
  freed, and is never freed by you. The library copies every pointer you pass in before the call
  returns.
- **Map `INILLUCENT_UNSUPPORTED` to its own error type.**
- **Keep each database and its handles on one thread,** or guard every call with a lock your
  binding owns. The C library has no lock inside it. `inillucent_cancel` is the one call that is
  safe from another thread. In Rust, `Database::cancel_handle()` gives a handle another thread can
  cancel with.
- **Run `drivers/conformance/suite.json`.** A binding that passes it agrees with the driver on every
  status, value and lifetime.

`drivers/README.md` has the full list of steps, the status codes and the lifetime rules for a language with
a garbage collector.

## Using the command line instead

When the caller is a person or an agent, the command line returns the same result object a binding
sees:

```sh
inillucent --db app.rdb query "SELECT * FROM note" --output json
```

`inillucent` has all 35 commands, and `inillucent-mcp` serves 30 of those commands over MCP. See
[`inillucent-mcp`](../inillucent-mcp/SKILL.md).
