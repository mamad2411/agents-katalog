---
name: write-dql
description: >
  Writes, reviews and debugs Ditto DQL: SELECT, INSERT … ON ID CONFLICT, UPDATE/APPLY,
  EVICT, DELETE, JOIN, CREATE INDEX, EXPLAIN/ADVISE and ALTER SYSTEM/SHOW. Covers SDK
  4.14.x, 5.0.x, 5.1.x and 5.2.0; JOIN and other features are version-gated. Use when
  a task involves a DQL string for execute or registerSubscription, a query returning no rows or missing fields, CRDT declarations, or a
  slow query. Not for schema design (data-modeling) or subscription coverage
  (sync-subscriptions).
allowed-tools: Read, Grep, Glob, Edit, Write
---

# DQL — Ditto Query Language

DQL is Ditto's SQL-like language for querying and mutating documents in a CRDT-aware, peer-to-peer database. It looks like SQL, but the semantics are different in three ways that matter every day:

1. **SQL compatibility is version-gated.** Check the target SDK before using a SQL construct; JOINs require 5.1+.
2. **`NULL` and `MISSING` are distinct.** `NULL` = field exists, value is null. `MISSING` = field is absent. They behave differently in every operator.
3. **Every field is a CRDT.** The CRDT type (REGISTER, MAP, COUNTER, PN_COUNTER, ATTACHMENT) controls how concurrent edits merge.

Scope: this skill covers DQL syntax and semantics. For schema design — CRDT type selection, embed-vs-split decisions, document size budgets, reviewing raw JSON models — use the `data-modeling` skill.

## When this skill applies

- "Write a DQL query that returns orders over 100 with the customer name."
- "Why does `SELECT … WHERE status = 'open'` return nothing?"
- "How do I upsert / increment a counter / remove a key in DQL?"
- "Is `JOIN` / `RETURNING` / a composite index supported on our SDK version?"
- "What's the difference between `EVICT` and `DELETE`?"
- "This query is slow — which index do I need? How do I read `EXPLAIN`?"
- A DQL parse error, or a string passed to `execute` / `registerSubscription` / `registerObserver`.

## Workflow

Copy this checklist and work through it for any non-trivial query:

```
- [ ] 1. SDK version and strict mode established
- [ ] 2. Every field path checked against real documents or the stated schema
- [ ] 3. Statement written for that version's feature set, values parameterized
- [ ] 4. Checked against "Five things that bite"; plan verified if performance matters
- [ ] 5. Destructive statements confirmed with the user
```

1. **Establish the SDK version.** Read the project's dependency files first
   (`Package.swift`/`Package.resolved`, `build.gradle(.kts)`/`libs.versions.toml`,
   `package.json`); ask the user only when no project is available. Supported:
   **4.14.x (LTS), 5.0.x, 5.1.x and 5.2.0** (the skill's knowledge baseline). For a newer
   resolved release, check its release notes and validate the query. Filter features with
   [versions.md](references/versions.md).
2. **Ground field names.** Check each path against documents or a schema the user
   supplied. If there is none, ask for a sample or suggest `SELECT * FROM <collection> LIMIT 3`.
   A misspelled or absent field evaluates to `MISSING`: filters match nothing and
   projections omit it, **with no error**. Respect case in field names and string values.
3. **Write the statement.** Use the routing table below. **Always** bind literal values as
   `:name` parameters and show the arguments object, even in short answers; never
   concatenate strings ([expressions.md](references/expressions.md) §3). Pass one statement
   per `execute` call, without a trailing `;`; DQL rejects multi-statement strings.
4. **Verify.** Re-check the five pitfalls below. For a performance-sensitive read, inspect
   `EXPLAIN` (all versions), `#profile` (5.0+) or `ADVISE` (5.1+) via
   [query-diagnostics.md](references/query-diagnostics.md); if the plan scans the whole
   collection, add or adjust an index and inspect the plan again.
5. **Confirm destructive statements.** Before running, or wiring into app code, a `DELETE`,
   `EVICT`, an `UPDATE` without a selective `WHERE`/`_id` filter, or an `ALTER SYSTEM`
   change, state the collection, the filter and whether the effect is local or mesh-wide,
   and get an explicit yes. When the user asked only for the statement text, deliver it with
   that warning and say it must be confirmed before it runs.

**Strict mode:** this skill assumes `dql_strict_mode = false` (lenient) on every peer — the 5.x default and the migration target for 4.14.x meshes. Examples therefore use no `MAP`/`REGISTER` keywords on reads or writes (objects infer MAP; reads see every type). `SHOW dql_strict_mode` reports a peer's setting. If a 4.x user reports fields missing from query results or whole-object overwrites on merge, suspect an un-migrated strict peer first — see [legacy-types.md](references/legacy-types.md#7-strict-mode-and-the-dql_strict_mode-system-parameter) and [strict-mode-safety.md](references/strict-mode-safety.md#strict-mode).

## Where to look

Read only the matching reference section: check a long file's contents first, and in
matrices find the feature row and its version notes. Do not load every reference or the
README.

| Task | Read |
|---|---|
| Field names in the movies/reviews examples (not the user's schema) | [schema.md](references/schema.md) |
| 5.2.0 diagnostics, USE IDS fixes, startup parameters | [sdk-5.2.md](references/sdk-5.2.md) |
| Version overview/defaults | [versions.md](references/versions.md) |
| Statement/index compatibility | [compatibility-statements.md](references/compatibility-statements.md) |
| Expression/operator/function compatibility | [compatibility-expressions.md](references/compatibility-expressions.md) |
| CRDT/subscription compatibility | [compatibility-types-sync.md](references/compatibility-types-sync.md) |
| SELECT grammar, filtering, sorting, grouping | [select-basics.md](references/select-basics.md) |
| JOIN queries (5.1+) | [joins.md](references/joins.md) |
| SELECT USE IDS/INDEX/DIRECTIVES | [select-access.md](references/select-access.md) |
| Subscription query restrictions | [subscription-queries.md](references/subscription-queries.md) |
| INSERT/UPDATE/EVICT/DELETE/TOMBSTONE | [statements.md](references/statements.md) |
| ALTER SYSTEM/SHOW/SYNC CONTEXT/PROFILE | [system-statements.md](references/system-statements.md) |
| Operator precedence or NULL/MISSING | [operators.md](references/operators.md) |
| Scalar/aggregate functions | [functions.md](references/functions.md) |
| String functions | [string-functions.md](references/string-functions.md) |
| Date/time/duration functions | [date-time-functions.md](references/date-time-functions.md) |
| CASE, quantifiers, comprehensions, parameters | [expressions.md](references/expressions.md) |
| REGISTER/MAP/COUNTER/ATTACHMENT | [types-mutators.md](references/types-mutators.md) |
| PN_COUNTER or strict-mode declarations | [legacy-types.md](references/legacy-types.md) |
| CREATE/DROP INDEX or index strategy | [indexing.md](references/indexing.md) |
| Planner directives/hints | [planner-hints.md](references/planner-hints.md) |
| EXPLAIN, #profile, ADVISE | [query-diagnostics.md](references/query-diagnostics.md) |
| Schema evolution and model patterns | [modeling-patterns.md](references/modeling-patterns.md); use data-modeling for a complete design |
| Query performance | [query-performance.md](references/query-performance.md) |
| Strict-mode migration or query safety | [strict-mode-safety.md](references/strict-mode-safety.md) |
| Timestamp design | [timestamps.md](references/timestamps.md) |
| Worked movie reads or mutations | [movie-reads.md](examples/movie-reads.md) or [movie-mutations.md](examples/movie-mutations.md) |
| Complete movie dataset/setup and JOIN/performance tasks | [movies-cookbook.md](examples/movies-cookbook.md) |
| Compare retail tasks with/without JOIN | [retail-cookbook.md](examples/retail-cookbook.md) or [retail-joins-cookbook.md](examples/retail-joins-cookbook.md) |

## Five things that bite people

1. **Use `AND` / `OR` / `NOT` keywords**, not `&&` / `||` / `!`.
2. **Single and double quotes both delimit strings**; backticks delimit identifiers. `WHERE title = "x"` and `WHERE title = 'x'` are equivalent. Prefer single quotes for consistency with JSON-style examples.
3. **`= NULL` is always NULL**, not TRUE. Use `IS NULL` / `IS NOT NULL` / `IS MISSING`.
4. **`INSERT` requires an explicit `ON ID CONFLICT`** for upserts. Default is FAIL.
5. **`EVICT` is local-only and reversible** (other peers will re-sync). **`DELETE` is mesh-wide and permanent** (subject to TTL) — it writes a replicating tombstone, and is the mesh-wide delete available from an Edge SDK. Don't mix them up.

## Compatibility

Every feature in the reference files is tagged with its minimum SDK version; [versions.md](references/versions.md) holds the full matrix.

Rejected on every tested SDK version (verified against 4.14.6 / 5.0.3 / 5.1.0): `XOR`, `TOMBSTONE` (Big-Peer-only), `EXCLUDE MISSING` index keys, the parenthesised `USE IDS ('a', 'b')` tuple, inline `PN_COUNTER` declarations on `INSERT`, and structured `PROFILE` output. Note that multi-id `USE IDS` **does** work everywhere in its comma form (`USE IDS 'a', 'b'`).

On 4.14.x under its default strict mode, `APPLY ... INCREMENT BY` on a not-yet-existing field silently does nothing.

`DO MERGE` is supported on every tested SDK version as an alias for `DO UPDATE`.

## Decision tree for query problems

```
Need to read documents?
├── By known id(s)?         → USE IDS on SELECT (references/select-access.md)
├── With aggregation?       → GROUP BY + aggregates (references/select-basics.md, references/functions.md)
├── Across collections?     → JOIN, 5.1+ (references/joins.md)
├── Across array elements?  → ANY ... IN ... SATISFIES (references/expressions.md, v5.0+)
└── Otherwise               → WHERE clause (references/select-basics.md, references/operators.md)

Need to write documents?
├── Adding new?       → INSERT (references/statements.md)
├── Modifying?        → UPDATE with SET / UNSET / APPLY (references/statements.md)
└── Removing?         → EVICT (local) or DELETE (mesh) (references/statements.md) — confirm first

Need to make it fast?
├── See the plan?     → EXPLAIN (references/query-diagnostics.md)
├── See timing?       → #profile directive, 5.0+ (references/query-diagnostics.md)
├── Get a suggestion? → ADVISE, 5.1+ (references/query-diagnostics.md)
└── Add an index?     → CREATE INDEX (references/indexing.md)
```
