---
name: couchbase-sqlpp-tuning
description: "Diagnose and tune slow Couchbase SQL++ / N1QL queries. Use whenever the user asks about query performance, slow queries, EXPLAIN plans, why an index isn't being used, IntersectScan, PrimaryScan, covering indexes, partial indexes, array indexes (ANY / EVERY / UNNEST), index selection, query hints, the cost-based optimizer, the Index Advisor (ADVISE), system:completed_requests, query profiling (kernTime / servTime / execTime), pagination performance, prepared statements, or 'this query is slow / how do I make it faster.' Distinct from couchbase-data-modeling (document shape) and couchbase-mcp (operating the cluster) — this skill is about reading plans, designing the right indexes, and reshaping queries that already exist. Use proactively when the user shares an EXPLAIN output or a slow query."
license: MIT
---

# Couchbase SQL++ tuning

A skill for diagnosing and fixing slow SQL++ / N1QL queries on Couchbase Server (7.x and 8.x). The mechanics of reading execution plans, choosing the right index type, fixing common anti-patterns, and wiring up the diagnostic tools.

Distinct from the sibling skills:
- `couchbase-data-modeling` — how to MODEL the data (document shape, boundaries, access patterns)
- `couchbase-sizing` — how to size the cluster
- `couchbase-app-integration` — how to write app code that uses Couchbase
- `couchbase-migration-execution` — how to move data INTO Couchbase
- `couchbase-mcp` — operating the cluster (the MCP server's `cb_explain_query`, `cb_index_advisor`, `cb_perf_*` tools)
- **`couchbase-sqlpp-tuning` (this skill)** — making queries that already exist run faster

If the conversation is "this query is slow, what do I do," this is the right skill.

## When this skill applies

- "Why is this query slow?"
- "How do I read this EXPLAIN plan?"
- "Why isn't my index being used?"
- "I'm seeing PrimaryScan / IntersectScan — is that bad?"
- "How do I make this a covering index?"
- "Should I use a partial index here?"
- "How do I index an array field with ANY / EVERY / UNNEST?"
- "ADVISE recommended this index — should I create it?"
- "How do I tune pagination — LIMIT / OFFSET is slow at high offsets"
- "What does kernTime / servTime / execTime mean in the profile?"
- "Can I force the optimizer to use a specific index?"
- "What do the cost-based optimizer hints do in 7.6+?"

## Core principles (read first)

These are the headline rules. Read them before diving into references.

1. **Pareto applies to query tuning.** 80% of perf problems come from 20% of queries. Use `system:completed_requests` (or the MCP `cb_perf_longest_running` / `cb_perf_most_frequent` tools) to find that 20% first. Don't tune the wrong queries.

2. **CBO needs stats to help; without them it falls back to rule-based logic.** Couchbase has a cost-based optimizer (GA in 7.0, EE only), but it needs statistics on indexes and collections to do its job. Without stats, single-keyspace access is rule-based — index cardinality doesn't influence the choice, the optimizer picks based on which leading keys are in the WHERE clause. In 7.6+, statistics are gathered automatically when an index is created or built; in earlier versions, you run `UPDATE STATISTICS` manually. Either way: design indexes so the rules pick them, and run `UPDATE STATISTICS` on a schedule.

3. **The leading key of the index must appear in the WHERE clause** for an index to be picked. If a field can be missing, you need `INCLUDE MISSING` on the leading key, or you need `IS NOT MISSING` / `IS NOT NULL` in the WHERE clause to force selection.

4. **Cover the query when it's hot.** A covering index includes every field the query SELECTs and filters on, so the query never touches the Data service. Look for `"covers": [...]` in the EXPLAIN plan and the absence of a `Fetch` operator — that's the signal.

5. **Don't index low-cardinality fields like `docType` alone.** It causes IntersectScans and wrong plans. Use a partial index (`WHERE type = 'X'`) instead — the field gates the index, but isn't the leading key.

6. **Match the query shape to the index shape for arrays.** `ANY ... SATISFIES` and `ANY AND EVERY` can use array indexes; bare `EVERY` cannot. `UNNEST` must use the **exact same binding variable name** as the `CREATE INDEX ... FOR <var> IN ...`.

7. **Avoid PrimaryScan in production.** A PrimaryScan is the equivalent of a full table scan. Drop primary indexes in prod, or at least confirm no production query relies on one.

## Pick the right reference

| Question | Read |
|---|---|
| "How do I read this EXPLAIN plan? What's PrimaryScan / IntersectScan / Fetch?" | `references/explain-plan.md` |
| "What kind of index should I create? Covering / partial / array / composite / vector?" | `references/index-design.md` |
| "Why isn't my index being used? Common query anti-patterns and how to fix them" | `references/query-patterns.md` |
| "What does the cost-based optimizer do? What are the hints?" | `references/cost-based-optimizer.md` |
| "How do I wire this up with the MCP server tools (`cb_explain_query`, `cb_index_advisor`, `cb_perf_*`)" | `references/diagnostic-workflow.md` |
| "How do I do efficient pagination on a large result set?" | `references/pagination.md` |
| "How do I tune queries that join across keyspaces?" | `references/joins-and-cbo.md` |

## Workflow

The general approach to tuning a slow query:

```
1. Identify  →  Find the slow query (Pareto: top-20% by frequency × duration)
                Tools: cb_perf_longest_running, cb_perf_most_frequent,
                       system:completed_requests

2. Understand →  Run EXPLAIN. Read the plan.
                 Tools: cb_explain_query (returns plan + parsed findings)
                 What to look for: PrimaryScan? IntersectScan? Fetch present?
                                   Is the leading key of an index in WHERE?

3. Hypothesize → Pick one of:
                 - Add a covering index (everything in the index, no Fetch)
                 - Add a partial index (smaller, indexed on a subset)
                 - Add an array index (DISTINCT ARRAY ... FOR ... IN ... END)
                 - Reshape the query (drop OR predicates, add IS NOT MISSING)
                 - Add a USE INDEX hint
                 Tools: cb_index_advisor (ADVISE) for index recommendations

4. Verify     → Re-run EXPLAIN. Check the new index is picked.
                Run the query. Check kernTime / servTime / execTime in the profile.
                Tools: cb_explain_query, cb_query with profile=on

5. Iterate    → Repeat until the query meets SLA, or further tuning has
                diminishing returns. Most queries reach acceptable performance
                in 1-3 iterations.
```

## Anti-pattern checklist

Quick scan list — if you see any of these, jump to `references/query-patterns.md`:

- `SELECT *` from a large keyspace (forces Fetch, can't cover)
- `WHERE docType = 'X'` as the leading filter (low-cardinality leading key)
- `WHERE NOT (...)`, `!=`, `NOT IN` predicates (often not sargable)
- `OR` across different fields (often forces IntersectScan)
- `EVERY x IN arr SATISFIES ... END` without `ANY AND EVERY` (no array index)
- `UNNEST` binding variable not matching the index definition
- `LIMIT 10 OFFSET 1000000` (deep pagination — use KeySet pagination)
- Raw user input concatenated into the statement (injection + can't prepare)
- A query that runs thousands of times per second with no `PREPARE`

## Tooling

The MCP server in this project (`celticht32/MCP-Couchbase`) exposes the tuning tools you need:

| Tool | Purpose |
|---|---|
| `cb_explain_query` | EXPLAIN + parsed plan findings |
| `cb_index_advisor` | ADVISE statement; recommends indexes |
| `cb_perf_longest_running` | Top N queries by duration |
| `cb_perf_most_frequent` | Top N queries by frequency |
| `cb_perf_largest_responses` | Queries returning the most bytes |
| `cb_perf_large_result_count` | Queries returning the most rows |
| `cb_perf_using_primary_index` | Queries hitting the primary index (BAD in prod) |
| `cb_perf_not_using_covering_index` | Queries that could be covered but aren't |
| `cb_perf_not_selective` | Queries where the WHERE filter doesn't narrow much |
| `cb_perf_by_user` | (8.x) attribute slow queries to a specific user |
| `cb_get_schema_for_collection` | Sample document schema (for designing the right index) |

See `references/diagnostic-workflow.md` for the full step-by-step using these tools.

## Version notes

- **Pre-7.0:** No scope/collection — indexes are bucket-level
- **7.0:** Scopes and collections; covering, partial, array indexes; CBO went GA (preview was in 6.5) — requires `UPDATE STATISTICS` to be useful
- **7.1+:** `INCLUDE MISSING` for leading index keys (so docs without the leading-key field still get indexed)
- **7.6+:** CBO auto-gathers stats on index create/build; join-enumeration improvements; `/*+ ... */` optimizer hints (`productivity`, `ORDERED`, `USE HASH`); `UPDATE STATISTICS` still available for manual refresh
- **8.0+:** Vector indexes (HYPERSCALE / COMPOSITE VECTOR INDEX); Auto Update Statistics (AUS) keeps stats fresh automatically; FTS synonym sets; user lock/unlock; XDCR conflict logging

Always verify against the cluster version before recommending a feature — the MCP `cb_mcp_status` tool reports the version it has detected.
