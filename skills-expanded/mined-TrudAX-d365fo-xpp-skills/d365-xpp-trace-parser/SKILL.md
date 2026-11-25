---
name: d365-xpp-trace-parser
description: Read a Dynamics 365 Finance & Operations (D365 F&O, AX7) trace that was imported into a Trace Parser SQL database and link it to the X++ code - which SQL statement wrote a value, the actual bind values of every insert and update, the call stack of a statement, and which methods ran in what order. Use this when the user has captured a trace (Settings > Trace, Trace Parser, an .etl file) and asks why a field got a value, which code created or changed a record, what a batch job or wave run did, or to "read the trace", "the trace is imported into the database", "find in the trace where X was set", "link the trace to the X++ logic".
---

# D365FO trace analysis from the Trace Parser database

Trace Parser imports a trace into an ordinary SQL Server database: every X++ call and every SQL statement, and, when the trace was captured with SQL parameter values, the actual values each statement bound. The Trace Parser UI shows timelines and call trees, but questions like "which code set `WorkTemplateCode` on this record?" mean digging through millions of lines by hand. Querying the database answers them in seconds: find the statement that wrote the value, then its X++ call stack, then read those methods in the source.

The scripts are read-only and work on a development VM, a cloud-hosted Tier1, or any SQL Server that holds the imported trace. Microsoft's Trace Parser agent (Copilot Studio plus a Data API Builder server over the same schema) isn't needed for this.

## Before you start

- **The trace must include SQL parameter values.** In the tracing pane (Settings > Trace) the option is *Include SQL parameter values*. Without it the statements are there, but the scripts show empty values.
- **Import it into a Trace Parser database** (Trace Parser desktop app: open or capture the trace, *Stop and Import*). The scripts find the database themselves when the server has exactly one; otherwise pass `-Database`.
- **Have the X++ source of the same code version** (`PackagesLocalDirectory`), because the trace gives method names, not code.
- Ask the user for what they already know: the record (work id, order number, RecId), the field, and which trace (name or time).

## Steps

1. **Find the trace and the thread.** `Get-TraceSession.ps1` lists the traces; with `-TraceId` it lists sessions and the busiest threads with their main call. A batch job, wave or posting usually runs in one thread whose main call is a `BatchRun` method.
2. **Find the statement that wrote the value.**
   - If you know the table and column: `Find-TraceSql.ps1 -TraceId N -Table WHSWORKTABLE` lists its statements; add `-Operation Insert -Columns WORKID,WORKTEMPLATECODE -Filter 'WORKID=WORK-000123'` to see each call with its values.
   - If you only know a value: `Find-TraceValue.ps1 -TraceId N -Value 'WORK-000123'` finds every table and column it was bound to, in time order. It also shows values written to temporary or staging tables first (`*TMP*` tables), which is often where the decision was made.
   - **Later changes are keyed by RecId.** Updates and deletes usually bind only `RECID` (and `RECVERSION`), not the business key. Get the record's RecId from its insert (`-Columns WORKID,RECID`), then find every change with `Find-TraceValue.ps1 -Value <RecId> -Operation Write` or `Find-TraceSql.ps1 -Operation Update -Columns FROZEN,RECID -Filter 'RECID=<RecId>'`.
   Both scripts return a **TraceLineId** per call.
3. **Get the call stack.** `Get-TraceCallStack.ps1 -TraceLineId <id>`. Read the confirmed chain from the bottom up: the statement, the table method (`insert`, `update`), and the business methods that called it.
4. **See what ran around it.** `Find-TraceMethod.ps1 -TraceId N -Thread T -Name 'WhsWorkCreate::*'` lists a class's methods in the order they first ran, with call counts. Loops show up as high counts between two sequence numbers. `-Calls` lists each call of one method with its TraceLineId, for its own call stack.
5. **Read the X++.** Open the methods from the stack in `PackagesLocalDirectory\<Package>\<Model>\AxClass\<Class>.xml` (and the matching extensions; the `d365-xpp-xref` skill finds callers and extension classes). Find the line that assigns the field, and match each condition in the code with the values the trace shows.
6. **Confirm with the data** (the database of the environment the trace came from) before you explain the cause: the final record should match the last value the trace wrote.
7. **Report** the chain of methods, the method and condition that decided the value, and the evidence: trace line ids, statement hashes and the values.

## Scripts

All scripts are in `<skill-dir>\scripts\` (Windows PowerShell 5.1, SELECT-only, Windows authentication). Common parameters: `-Server` (default `.`), `-Database` (default: auto-detected), `-TimeoutSeconds`. Output is a summary line plus tab-separated rows. Exit codes: `0` rows found, `1` nothing found, `2` setup or connection failure.

| Script | What it answers |
|---|---|
| `Get-TraceSession.ps1 [-TraceId N] [-Top 20]` | Which traces are imported; for one trace, its sessions and its busiest threads (`Thread` = `UserSessionProcessThreadId`, used by the other scripts) with their main X++ call and duration. |
| `Find-TraceSql.ps1 -TraceId N -Table T [-Operation Write\|Insert\|Update\|Delete\|Select\|Any] [-Columns A,B \| *] [-Filter 'A=v;B=x*'] [-Thread T] [-StatementHash H] [-Top 500]` | Without `-Columns`: the statements on a table with call counts. With `-Columns`: every call with the bound values of those columns; `*` prints all parameters as `NAME=value`. |
| `Find-TraceValue.ps1 -TraceId N -Value 'X' [-Operation Any\|Write\|...] [-Thread T]` | Where a value (exact, or `*` pattern) was bound: operation, table, column, calls, threads, first sequence and first TraceLineId. |
| `Get-TraceCallStack.ps1 -TraceLineId L [-ExcludeMethod 'A*','B::*']` | The X++ call stack of a statement or method call, outermost first. |
| `Find-TraceMethod.ps1 -TraceId N -Name 'Class::*' [-Thread T] [-ExcludeName '*::parm*'] [-Calls] [-Top 300]` | Methods matching a pattern in first-run order, with calls, first/last sequence and total time; `-Calls` lists each call. |

From Bash, run them as `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>/scripts/<Script>.ps1" ...`; list parameters can then be passed as one comma-separated string (`-Columns 'WORKID,WAVEID'`).

For a question the scripts don't cover (for example everything that ran between two sequence numbers, or the slowest statements of a thread), read `references/trace-schema.md` and query the database directly.

## Reading the output

- **`Find-TraceSql` value columns:** `-` means the statement doesn't bind that column (it may be a literal in the SQL text); an empty value means it's bound but empty. Statements that don't bind a `-Filter` column are skipped, so `-Filter 'COL=*'` keeps only statements that set `COL`.
- **Parameter names:** positions follow the `?` placeholders. `INSERT ... VALUES` uses the column list; `INSERT ... SELECT` (`insert_recordset`) maps the n-th SELECT item to the n-th insert column; everything else uses the column compared with the `?` (`SET STATUS=?`, `WHERE T1.ITEMID=?`). A repeated column becomes `COLUMN#2` (for example `RECVERSION` in `SET` and `RECVERSION#2` in `WHERE`), and an aliased one is also available as `T2.COLUMN`. `Op` marked `!` means the call captured a different number of values than the statement has placeholders; don't trust its mapping.
- **`Get-TraceCallStack` confirmed chain:** every frame is the caller of the next, proven by the trace's parent links. Repeated kernel frames (such as `PropertyChange`) are printed once with a count.
- **`Get-TraceCallStack` unconfirmed part:** when the parent chain breaks (see Gotchas), the script lists the calls that enclose the top of the confirmed chain. The real callers are among them, but so are calls that had already returned. Names that occur 3 or more times are collapsed into one line. Decide the real caller from the X++ source and from the call order (`Find-TraceMethod`).

## Gotchas

- **Durations aren't nanoseconds.** `TraceLines.TimeStamp` is a Windows FILETIME (100-ns ticks, UTC), and the `*DurationNano` columns use the same 100-ns unit: `InclusiveDurationNano` equals `TimeStampEnd - TimeStamp`. The scripts convert to milliseconds (`InclMs`, `TotalMs`). SQL views that divide by 1,000,000 show times 10 times too small. If a duration matters, sanity-check it against something with a known length, such as the batch job's run time.
- **`Sequence` is trace-wide.** It's unique in the whole trace and follows time across threads, so `FirstSeq` orders events from different threads. `UserSessions` is keyed by `(SessionId, TraceId)`: session numbers repeat in every trace in the database, so always filter by trace.
- **Batch traces break the parent links.** Lock keep-alive threads (`ReqReaderWriterLock...`, used by wave processing, MRP and other parallel batch work) and finalizers (`Connection::finalize`) are recorded inside the same thread. After the first lock, the parent links of later calls can point into those frames, so the confirmed chain may be only the last few frames, and calls that already returned look open. Pass extra noise patterns with `-ExcludeMethod` if a lock helper of your feature floods the list, and confirm the callers in the source.
- **Not every value is a bind value.** The kernel often writes `DATAAREAID`, `PARTITION` and constants into the SQL text as literals; `Find-TraceValue` can't find those. Enums appear as their integer value; dates as the date part only.
- **Physical names.** The SQL text uses upper-case physical table names. TempDB temporary tables get generated names such as `TEMPDB."DBO".T12345<SERVER>_<session>_<guid>`: pass `-Table 'TEMPDB."DBO".T12345*'`. In-memory temporary tables never reach SQL, so they aren't in the trace at all; tables named `...Tmp...` that are regular tables are traced normally.
- **SQL lines vs X++ lines.** SQL statements are trace lines with `CallTypeId = 64` and carry the bind values; X++ methods are `CallTypeId = 8`. The X++ method that issued a statement also carries its statement hash, so don't count both when you count executions.
- **Large traces are fine.** The scripts take a few seconds on a 2.6-million-line trace. Narrow with `-Thread`, `-Operation`, `-Filter` and `-Top` rather than printing everything.
