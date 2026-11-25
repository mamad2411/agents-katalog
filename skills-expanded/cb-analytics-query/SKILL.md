---
name: cb-analytics-query
description: |
  Use this skill when the user wants to write or improve SQL++ queries against
  Couchbase Analytics through cb-analytics-mcp. Trigger when they mention
  "SQL++", "Analytics query", "execute_query", "scan_consistency", "request_plus",
  "pagination", "EXPLAIN", "truncated", "row cap", or anything about querying
  datasets, dataverses, joins, aggregations, windowing, query plans, or
  N1QL/SQL++ language features in this server's context.
license: MIT
---

# Querying Couchbase Analytics via cb-analytics-mcp

You have **five SQL++ tools** for talking to the Analytics service. Picking
the right one matters — they have different cost profiles, rate-limit
budgets, and result shapes.

| Tool | Cost | Result shape | When to reach for it |
|---|---|---|---|
| `execute_query` | high (full result) | rows, may be truncated | DDL, mutations, small SELECTs |
| `execute_query_readonly` | high (full result), **cached** | rows, may be truncated, `cached: bool` | repeated SELECTs in an investigation loop |
| `execute_query_paginated` | constant per page | first page + handle | SELECTs that might return many rows |
| `fetch_next_page` | constant per page | next page for a handle | follow-up to paginated |
| `explain_query` | tiny (no execution) | query plan | "why is this slow" |

## The cardinal rule: pick the tool that matches what you'll do with the result

If you only need the **first N rows** to answer the user's question, use
`execute_query_paginated` with `page_size=N`. Don't pull a million rows
through the MCP boundary just to take the first 20.

If you need to **show the user the data** (and the dataset is small),
`execute_query_readonly` is fine — but watch for `truncated: true` in the
response.

If you need to **make a decision** based on aggregates (`COUNT`, `SUM`,
`AVG`, `GROUP BY`), the result is small by construction. Use
`execute_query_readonly` and benefit from the cache.

## The soft cap (you will see `truncated: true`)

Both `execute_query` and `execute_query_readonly` enforce a server-side row
cap (default 1000, configurable via `MAX_QUERY_ROWS`). Responses include:

- `truncated: true` if the cap kicked in
- `row_cap`: the cap that was applied (or `null` if disabled)
- `full_row_count`: how many rows the cluster actually had

When you see `truncated: true`, **do not silently report incomplete data**.
Either:

1. Tell the user the result is truncated and ask if they want all rows
   (then re-issue as paginated), or
2. If you only needed a sample, acknowledge it and continue ("here are the
   first 1000 of 47,832 matching rows").

The user is operating an LLM-driven tool. Hidden truncation will eventually
produce wrong answers.

## The cache (you will see `cached: true`)

`execute_query_readonly` results are cached for ~60 seconds keyed by
`(cluster, statement, scan_consistency)`. Responses include `cached: true`
on a cache hit, `cached: false` on a miss. Practical implications:

- Repeating an identical query inside an investigation loop is free; lean
  into it.
- If freshness matters (e.g. you're watching an ingestion catch up), add
  `scan_consistency="request_plus"` so the cache key differs from the
  default-consistency cached entry.
- If you need a definitively fresh read, use `execute_query` (uncached) or
  wait 60s.

## Pagination, end-to-end

```python
# 1. First page
first = execute_query_paginated(
    statement="SELECT id, name, status FROM Default.Orders WHERE region = $r",
    named_args={"r": "EMEA"},
    page_size=100,
)
handle = first["data"]["pagination_handle"]
# Use first["data"]["results"] — that's your page 0

# 2. Walk pages until exhausted
while first["data"]["has_more"]:
    nxt = fetch_next_page(pagination_handle=handle)
    # Process nxt["data"]["results"]
    if not nxt["data"]["has_more"]:
        break
    handle = nxt["data"]["pagination_handle"]  # handle stays the same; this is for clarity
```

Important details:

- `page_size` must be between 1 and 10000. Default 100.
- A trailing `LIMIT/OFFSET` clause in your statement gets **stripped** —
  the server adds its own.
- Handles expire after 30 minutes of inactivity. If you get
  `"not found or expired"`, just call `execute_query_paginated` again to
  start fresh.
- When `has_more` is `false`, the handle is auto-dropped on the server.
  Don't call `fetch_next_page` again with it.
- `total_seen` accumulates across pages; use it for progress reporting.

## EXPLAIN — your slow-query diagnostic

```python
plan = explain_query(statement="SELECT * FROM Default.Orders WHERE customer_id = 'C-1234'")
# plan["data"]["plan"] is the service-internal JSON plan
```

When to reach for `explain_query`:

- The user reports a slow query.
- You ran a query and `data.metrics.executionTime` was surprising.
- The user asks "is this query using an index?"
- You're about to recommend adding an index — check first that the planner
  isn't already using one.

You don't have to add `EXPLAIN` to your statement; the tool prepends it if
not present.

## Parameterisation rules (still apply)

Never interpolate user-controlled values into the statement string. Use
`named_args`:

```python
execute_query(
    statement="SELECT * FROM Default.Orders o WHERE o.customer_id = $cust",
    named_args={"cust": "C-1234"},
)
```

Identifiers (dataset names, field names) **can't** be parameterised by
SQL++. If you must inject one, validate it first (the server already does
this for `infer_schema`).

Note: `execute_query_paginated` also accepts `named_args` and
`positional_args`. Parameter values are reused across pages — no need to
re-pass them to `fetch_next_page`.

## Scan consistency

- `not_bounded` (default) — fastest, may see stale results.
- `request_plus` — wait for ingest to catch up to this point in time. Use
  when correctness matters more than latency.
- `at_plus` — wait for a specific mutation token; rarely needed outside
  SDK code.

`scan_consistency` is part of the cache key for `execute_query_readonly`.
Changing it gives you a fresh read without bypassing the cache for other
callers.

## Result shape

All five tools return `{ok, data, cluster}`. The `data` object's common
fields:

| Field | execute_query | _readonly | _paginated | fetch_next_page | explain |
|---|---|---|---|---|---|
| `results` | ✓ | ✓ | ✓ (page) | ✓ (page) | — |
| `plan` | — | — | — | — | ✓ |
| `metrics` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `warnings` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `request_id`, `status` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `truncated`, `row_cap`, `full_row_count` | ✓ | ✓ | — | — | — |
| `cached` | — | ✓ | — | — | — |
| `pagination_handle`, `page_size`, `page_offset`, `rows_returned`, `has_more` | — | — | ✓ | ✓ | — |
| `total_seen` | — | — | — | ✓ | — |

Always surface `data.warnings` to the user — Couchbase Analytics uses
warnings for things like "this query ran but ignored an index hint."

## Rate limits & safety

Query tools share a single token bucket per API key, category `"query"`,
default 10 requests/sec. That means **all five query tools together**
contribute to the same budget, not 10/sec each.

If you hit the limit:

```json
{ "ok": false, "error": "RateLimitExceeded",
  "message": "Rate limit exceeded for category 'query' (limit 10/sec). Retry in 0.41s.",
  "category": "query", "rate_per_sec": 10, "retry_after_sec": 0.41 }
```

Honour `retry_after_sec`. Don't retry-storm — the bucket only refills at
the rate, so hammering it just keeps failing. Better: explain to the user
what happened ("hit the query rate limit, waiting half a second") and back
off.

Caching helps: every cache hit on `execute_query_readonly` does not
consume a token. So in investigative loops, the second-and-onward hits of
the same query are free both for the cluster and for the rate budget.

## Common patterns

### Counting documents

```sql
SELECT VALUE COUNT(*) FROM Default.Users
```

Use `execute_query_readonly`. Tiny result, cacheable, almost free.

### Schema discovery

Prefer the `infer_schema` tool (separate skill) over
`SELECT VALUE OBJECT_NAMES(d) FROM x d`; it returns a typed summary
including presence rates. Note: `infer_schema` runs a SELECT under the
hood so it counts against the same `"query"` rate-limit category.

### Working with multiple clusters

Always pass `cluster="..."` if there's any ambiguity. Use `list_clusters`
first if you don't know what's configured.

### Diagnosing slow queries

1. `get_active_requests` — see what's running now.
2. `get_completed_requests` — recent history with timings.
3. `explain_query(stmt)` — show the plan, look for full scans.
4. If the plan looks fine but the query is still slow, check
   `get_service_status` for resource pressure.

## What to avoid

- Don't run `SELECT *` against multi-million-row datasets via
  `execute_query`. Use `execute_query_paginated` with a reasonable
  `page_size` (100–1000) instead. The soft cap will catch you anyway,
  but using the right tool is cleaner.
- Don't use `request_plus` on hot-path queries unless the freshness is
  actually needed. It defeats both the in-memory cache and Analytics'
  internal optimisations.
- Don't drop or replace datasets without checking `get_active_requests`
  first — in-flight queries against the target will fail.
- Don't silently ignore `truncated: true`. The user is operating an
  LLM-driven tool; hidden truncation produces wrong answers.
- Don't keep paginating "to see if there's more" if `has_more` is `false`.
  The handle is dropped server-side; the next call returns an error.
- Don't reach for `execute_query` (uncached, full result) when
  `execute_query_readonly` would do. The cache pays for itself within two
  identical calls.

## Related skills

- `cb-analytics-schema` — discover dataverses and infer dataset field shapes before writing queries
- `cb-analytics-admin` — monitor active/completed requests, cancel runaway queries, restart the service
- `couchbase-sqlpp-tuning` — SQL++ tuning principles (index design, EXPLAIN plans, anti-patterns) apply equally to Analytics; that skill has the deep reference docs
