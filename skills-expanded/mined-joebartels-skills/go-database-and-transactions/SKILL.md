---
name: go-database-and-transactions
description: Use when Go work adds or changes database queries, transaction participation, commit/rollback, row or connection lifetimes, or concurrent database invariants. Skip pure calculations and changes that do not cross a database boundary.
---

# Go database and transactions

Trace the database operation from its caller to the handle executing every statement and the outcome the caller may rely on. Read the schema, constraints, driver/version, supported Go version and existing transaction conventions. Preserve the repository's database stack; do not introduce an ORM, repository framework or transaction abstraction by default.

## Keep participants on the same transaction

`*sql.DB` is a reusable pool, not the connection currently held by `*sql.Tx`. Once an operation owns a transaction, trace every helper, prepared statement and callback that must participate. A helper using its stored DB executes outside that transaction or waits for another pool connection. Pass the Tx or an existing suitable executor explicitly. Keep independently usable helpers working through the pool. Use a small private interface only when it actually expresses shared DB/Tx behavior; a concrete Tx parameter is often sufficient.

The starter owns commit/rollback. A helper borrowing a transaction stages work and returns its outcome without finalizing the caller's transaction. Nested work needs the stack's explicit savepoint semantics or participation in the outer transaction; another pool Begin does not nest inside it. Do not close a borrowed pool or connection.

## Finish queries and transactions before claiming success

For database/sql, BeginTx with the operation context, arrange rollback immediately after a successful begin, check each operation and check Commit. Defer rollback for abandoned paths; after a completed Commit the sql.Tx is finished even if Commit returned an error. Return only the result that the failure contract permits. A commit error prevents claiming confirmed success but does not prove no durable effect occurred; reconcile an uncertain outcome rather than automatically replaying it.

| Boundary | Go decision |
| --- | --- |
| QueryRow / QueryRowContext | Inspect Scan; lookup errors and sql.ErrNoRows are reported there. |
| Query / QueryContext | Close owned Rows on every path, check Scan and Rows.Err after iteration. |
| Bounded or early-ended iteration | Close rows before the next operation needs that connection; a function-exit defer may be too late. |
| Update or generated result | Check RowsAffected/CommandTag or returned identity when the invariant depends on it; successful Exec alone need not mean a row changed. |
| Commit or rollback | Use the actual driver's completion/cleanup contract; preserve required independent causes and never replace a failure with success. |

Keep the operation context alive through row consumption and transaction completion. Propagate it into blocking calls. Context cancellation is neither a successful commit nor proof that arbitrary database work has stopped. Read [native pgx/PostgreSQL](references/pgx-postgresql.md) when that stack is used; its transaction cancellation behavior differs from database/sql.

## Establish the database invariant

State which rows and conditions must change together and what concurrent callers may observe. A transaction gives an atomic unit; the actual isolation, constraints and statements determine which interleavings it permits. Use existing constraints, conditional writes, affected-row checks, row locks or appropriate isolation for that invariant. A Go mutex cannot coordinate independent processes or database pools. Do not prescribe Serializable for every transaction.

Keep external callbacks, remote calls and irreversible publication outside a transaction unless the operation's coordination contract requires them. Retry only an identified retryable database outcome under the existing operation budget, repeating all reads and decisions of the transaction when required. Do not retry an ambiguous commit as if rollback were established. For SQLite locking, per-connection settings and test topology, read [SQLite](references/sqlite.md).

Verify through the boundary that establishes the claim: actual pool/Tx participation and one-connection reuse; query, scan, terminal iteration and completion failures; zero/unconfirmed results where promised; cancellation after a driver call enters; borrowed versus owned cleanup. Use the real target database for constraints and concurrent persisted-state invariants. Driver doubles can isolate Go API failures but cannot prove engine isolation, SQL semantics or wire cancellation. Existing behavior/isolation skills own test mechanics; context owns generic budgets and composition owns API/dependency shape. Report the driver, engine, toolchain and boundaries actually exercised.

Sources: [Go transactions](https://go.dev/doc/database/execute-transactions), [queries](https://go.dev/doc/database/querying), [database/sql](https://pkg.go.dev/database/sql).
