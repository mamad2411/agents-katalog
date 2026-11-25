---
name: rpeek
description: >
  Inspect a remote host that is running the read-only `rpeek serve` diagnostic server.
  Use when the user wants to read logs, configs, process state, disk usage, or
  journald on a remote machine reachable via the `rpeek` client — e.g. "check why nginx
  is down on 10.0.0.5", "tail the app log on the prod box", "what's eating disk there".
  Do NOT use for the local machine (use normal shell tools) or for anything that
  writes/mutates — this server is read-only by design.
---

# Remote diagnostics via rpeek

## Preconditions
- `rpeek` is on PATH.
- Connection details — a host (or host:port; the port defaults to 7017) and a token,
  both required — come from one of two sources, in this precedence:
  1. Positional args to this skill, invoked as `/rpeek <host> <token>`. Both are
     mandatory; the token is never optional.
  2. The environment: `RPEEK_HOST` and `RPEEK_TOKEN`, if already exported.
  If a host or token is missing from both, ask the user — never guess a host or
  fabricate a token.
- Confirm reachability and authorization with a cheap call (`rpeek hostname`) before a
  long investigation; it needs no jail and its output names the host that answered.

## Applying the connection details
Shell state does not persist between calls and no token file is used, so the host and
token must accompany every `rpeek` invocation:
- Given as positional args to the skill: prefix each call inline via environment
  variables — `RPEEK_HOST=<host> RPEEK_TOKEN=<token> rpeek <tool> [args]` — reusing the
  same values for every call this session.
- Already exported in the environment: call `rpeek <tool> [args]` directly.
Pass the token only through `RPEEK_TOKEN`, never via `--token`.

## Discovering the tools
The toolset is self-describing — do not rely on a hardcoded list, since it can change
between versions:
- `rpeek help` — lists the available tools, each with a one-line summary.
- `rpeek help <tool>`  — prints that tool's arguments and flags with their defaults
  and meanings.

Run `rpeek help` first whenever you are unsure what is available or what a tool
accepts; it is the authoritative reference. Every tool is READ-ONLY, and `help` needs no
host or token.

## How to use
Every invocation is one-shot: `rpeek <tool> [args]`, carrying the connection details as
described above. A tool's own flags and its path may appear in any order (`rpeek read /p
--max-bytes 200` and `rpeek read --max-bytes 200 /p` are equivalent). Read `stdout` as if
it were the output of the equivalent Unix command; it is already formatted server-side. On
a non-zero exit, read `stderr` and adapt — do not retry the identical command.

Representative calls (connection prefix omitted for brevity; see `rpeek help <tool>` for
each tool's full argument set):

```
rpeek hostname
rpeek version
rpeek list /var/log
rpeek read /etc/nginx/nginx.conf --max-bytes 20000
rpeek grep /var/log --pattern "ERROR" --ignore-case
rpeek tail /var/log/nginx/error.log --lines 200
rpeek stat /etc/hosts
rpeek ps
rpeek disk
rpeek journal --unit nginx --lines 100
rpeek db-list
rpeek db-tables --db app
rpeek db-schema --db app orders
rpeek sql --db app "SELECT state, COUNT(*) AS n FROM orders GROUP BY state ORDER BY n DESC"
```

## Databases
When the answer lives in an application database (row counts, joins, "how many are stuck
in `failed`?"), the server may expose read-only database access by **alias**. You never
supply a DSN — only the alias the operator configured. Work in this order:
1. `rpeek db-list` — the entry point: shows the configured aliases with engine and host.
   Nothing to query means no databases were configured; ask the user, do not guess a DSN.
2. `rpeek db-tables --db <alias>` — the tables and views you may read.
3. `rpeek db-schema --db <alias> <table>` — a table's columns, types, and nullability, so
   you use real column names.
4. `rpeek sql --db <alias> "<query>"` — run the query. Quote the whole query as one
   argument.

The query language looks like SQL but is a restricted, SELECT-only subset: `SELECT` with
joins, `WHERE`, `GROUP BY`, `ORDER BY`, and `LIMIT`, plus the aggregates `COUNT`, `SUM`,
`AVG`, `MIN`, `MAX`. Writes, subqueries, comments, multiple statements, and other functions
are not available — do not attempt them. Run `rpeek help sql` for the exact grammar before
composing non-trivial queries; if a query is rejected or reports an unknown table or
column, read the message and fix the query rather than retrying it unchanged.

## Rules
- Use only the tools `rpeek help` reports. Do not invent flags or tools; there is no
  write, delete, restart, or "run command" capability, by design.
- Paths are the host's **real** paths and must fall inside a jail root the operator
  granted. A "not within any allowed root" error means the directory was not granted
  — report that to the user; do not try to tunnel around it.
- Patterns are RE2 (Go `regexp`), not shell globs.
- If output ends with `... (truncated)` (stderr notes truncation), narrow the query
  (tighter `--pattern`, larger `--max-bytes` with `--offset` paging, fewer `--lines`)
  rather than assuming you saw everything.
- If the tool is not sufficient to solve the user's task, ask them for help. Eg. for
  manually running tools or edit files.

## Exit codes
`0` success · `1` protocol/transport error · `2` server-returned error (bad path,
unauthorized, tool error) · `3` usage error. A `2` with "unauthorized" means the token
is wrong — stop and ask the user; do not brute-force.

## Working a problem
1. **Establish context** — resolve the host and token (skill positional args or the
   environment); sanity-check with `hostname` (or `disk`/`ps`). Missing/rejected token →
   stop and ask the user.
2. **Map the question to tools** — "is the service up?" → `ps` / `journal --unit`;
   "why is it erroring?" → `tail` then `grep` the log; "is the box full?" → `disk`.
3. **Run, read, refine** — each call returns pre-formatted text; interpret it and choose
   the next call. Calls are cheap and read-only, so breadth-first probing is fine.
4. **Respect the boundaries** — jail/auth/truncation errors are signals to change
   approach or ask the user, never to escalate. There is nothing to escalate to.
5. **Report** — synthesize findings, citing the concrete evidence (`tail` lines, `grep`
   hits) rather than raw dumps.

Example (user: "nginx is down on the prod box, why?"):

```
rpeek ps                                  # is nginx running? -> not in the table
rpeek journal --unit nginx --lines 50     # why did it stop? -> "bind() to :443 failed"
rpeek grep /etc/nginx --pattern "listen"  # what claims 443? -> two server blocks
rpeek disk                                # rule out a full disk -> plenty free
# -> report: duplicate `listen 443` in <file:line>; nginx aborts on bind conflict.
```
