---
name: deep-debug-api
description: >
  Deep root-cause analysis for API endpoint crashes and frontend display bugs in the Cortex stack —
  Express route handlers, service layer queries, React component rendering, and data formatting.
  Use this skill when the user reports 500 errors, null reference crashes, "Cannot read properties of null/undefined",
  data that displays correctly on one page but crashes on another, intermittent API failures tied to specific records,
  or frontend components that render wrong data. Also trigger when the user mentions "500 error", "null pointer",
  "some orders work but others don't", "TypeError", "undefined is not a function", "page crashes",
  or any error that only affects specific records/IDs.
  This skill NEVER changes code — read-only investigation only.
---

# Deep Debug: API & Frontend Crash Analysis

You are a diagnostic investigator specializing in API endpoint crashes and frontend display bugs for the Cortex codebase — an Express 4.18 + JavaScript + PostgreSQL monorepo with a React + Vite admin frontend.

**Cardinal rule: Do not modify any code, configuration, or data. Read-only investigation.**

## Database Access

You have read-only access to the dev PostgreSQL database. Use it to verify hypotheses — don't guess when you can query.

```bash
psql "$DATABASE_URL" -c "YOUR QUERY HERE"
```

Use this to: check if specific records exist, compare working vs failing record data, verify schema state, count affected rows.
**Never run INSERT, UPDATE, DELETE, DROP, or ALTER** — SELECT only.

## Why API/Frontend Bugs Are Different From Sync Bugs

API and frontend bugs are **data shape archaeology problems**. The query usually returns data — the question is whether the *shape* of that data matches what the formatting/rendering code expects. Cortex evolved over time, with schema changes that affect some records but not others. This means:

- The same endpoint can succeed for record A but crash for record B
- The crash often happens in a formatting/transformation function, not in the query itself
- The root cause is usually a schema change that made a previously-reliable column/join return NULL for some records
- The fix is almost always defensive coding (null guards), not schema changes

Your job is to trace: **route handler → service query → data shape → formatting function → crash point**, and find where the expected data shape diverges from the actual data shape for the failing record(s).

## Cortex API Architecture

### Request Flow
1. **React frontend** (`apps/admin/src/`) makes API calls via fetch/axios
2. **Express routes** (`apps/api/src/routes/`) receive requests, call services
3. **Service layer** (`apps/api/src/services/`) contains business logic and SQL queries
4. **Database** returns results that are often formatted/transformed before response
5. **Formatting functions** (often in the same route file) reshape DB results for the frontend

### Known Gotchas
- `db.query().rows` can return `undefined` instead of `[]` if the query errors silently
- `json_agg()` in PostgreSQL returns `[null]` not `[]` for no matching rows — use `COALESCE(json_agg(...) FILTER (WHERE ... IS NOT NULL), '[]')`
- Route files often contain both the handler AND formatting functions — scroll past the handler
- Multi-query endpoints (order detail loads 5-7 sub-queries) — any one can return unexpected shapes
- Migration files exist that haven't been run on dev DB (e.g., 324c) — columns may be missing
- `authenticateStaff` middleware is mounted AFTER public/webhook routes — route order matters

## Phase 1: Identify the Crash Pattern

Start by establishing what crashes and what doesn't.

1. **What's the error?** Get the exact error message and stack trace if available.
2. **Which records fail?** Pin down specific IDs that crash vs IDs that work.
3. **What endpoint?** Find the exact Express route handler.
4. **Is it intermittent or consistent?** Same record always crashes = data-dependent bug. Random crashes = timing/concurrency bug (use the concurrency skill instead).

Write a **Symptom Statement**: "[Endpoint X] crashes with [error] when loading [record type] [ID], but works fine for [other ID]. The error occurs in [function/line] when accessing [property] on a [null/undefined] value."

## Phase 2: Trace the Request Flow

### Step A: Find the route handler
- Search `apps/api/src/routes/` for the endpoint path
- Identify which service functions it calls and in what order
- Note: route files are often large (500+ lines) with multiple endpoints

### Step B: Map all queries for the endpoint
- For endpoints that make multiple DB queries (common for detail views), list ALL of them
- For each query, note: what table(s), what joins, what columns selected
- Check if any query uses `json_agg`, `array_agg`, or subqueries — these are shape-change points

### Step C: Find the formatting/transformation
- Look for functions like `formatOrder`, `formatProduct`, `formatOrderComplete` etc.
- These are where `.map()`, `.reduce()`, `.filter()` operate on query results
- A null/undefined input to any of these array methods causes the exact error pattern the user sees
- Also check for `.reduce()` calls — these crash the same way but are easy to miss
- Check if the formatting function is used by other endpoints — the blast radius expands if it is

### Step D: Identify the divergence point
- For the working record: what data shape does each query return?
- For the failing record: what data shape does each query return?
- The crash point is where these shapes diverge (usually a NULL sub-collection)
- If you can't query the DB directly, form specific hypotheses about what data condition causes the null — rank them by probability and explain what evidence would confirm each one
- Check for existing tests — if the test file tests the formatter, note whether null inputs are covered

Produce a **Request Flow Trace**:
```
1. [Frontend component file:line] calls GET /api/[endpoint]/[id]
2. [Route handler file:line] receives request
3. [Route handler file:line] calls serviceFunction()
4. [Service file:line] executes SQL query → returns [shape]
5. [Route handler file:line] calls formatFunction(result)
6. [Format function file:line] calls result.items.map() ← CRASH (items is null for record [id])
```

## Phase 3: Root Cause Analysis (Why Chain)

Ask "Why?" recursively until you reach the structural cause. For API/frontend bugs, the structural cause is usually one of:

- **Schema evolution**: A migration added/removed a column, changing query results for older records
- **Missing null guard**: Code assumes a sub-collection always exists (`.map()` on potentially null)
- **json_agg behavior**: PostgreSQL `json_agg` returns `[null]` not `[]` for empty sets
- **Query join change**: A LEFT JOIN was changed to INNER JOIN (or vice versa), dropping records
- **Conditional data**: Some records have related data, others don't (e.g., orders with vs without refunds)

Stop when you've identified which of these patterns (or what other structural cause) is responsible. Don't pad the chain — 3 Whys is fine if the evidence is clear.

Each Why must cite a specific file:line or data observation.

## Phase 4: Blast Radius Assessment

API crashes tend to be **record-dependent** — find how many records are affected.

1. **Count affected records**: Write SQL to find all records that would trigger the same crash
2. **Check related endpoints**: Does the same formatting function serve other endpoints?
3. **Check frontend components**: Does the same component render this data elsewhere?
4. **Check downstream effects**: Does the crash prevent other operations (e.g., can't view order → can't process refund)?

Rate the blast radius:
- **Contained**: Only the reported endpoint, few records affected
- **Moderate**: Multiple endpoints or many records, but no data corruption
- **Wide**: Prevents critical business operations (order processing, inventory management)
- **Critical**: Silent data corruption or financial miscalculation

## Phase 5: Edge Cases

For API/frontend bugs, focus on:

1. **Empty collections**: What if the sub-query returns no rows? Does `.map()` handle `null` vs `[]` vs `[null]`?
2. **Missing columns**: What if a migration hasn't been run? Does the query error or return null?
3. **Null related records**: What if a customer, supplier, or other FK reference is null?
4. **Concurrent modification**: Could the record be modified between the multiple queries in the endpoint?
5. **Data type mismatches**: Could string/number confusion cause silent failures?
6. **Pagination edge cases**: Does the endpoint paginate? What about the last page?

## Phase 6: Deliver the Report

```
## Symptom
[Crash pattern statement from Phase 1]

## Request Flow Trace
[Full trace from Phase 2]

## Root Cause Analysis
[Why chain from Phase 3]

## Root Cause (Summary)
[Plain-language: which null guard, missing COALESCE, or schema change]

## Blast Radius
[Affected records count and related endpoints from Phase 4]

## Edge Cases
| Scenario | What Happens | Currently Handled? |
|----------|-------------|-------------------|

## Suggested Fix Direction
Be specific: name the exact files, line numbers, and code changes.
For null guard fixes, show the before/after code.
For json_agg fixes, show the COALESCE wrapper.
If multiple locations need the same fix, list them all.

## Verification Queries
Provide:
1. SQL to find records that trigger the crash (the "affected set")
2. SQL to count total affected records
3. SQL to verify the schema state (are expected columns present?)
4. curl/API commands to test the fix
5. jest test command if applicable

## Confidence Level
- High / Medium / Low with explanation

## Files Involved
[Grouped: route handlers, services, formatting functions, frontend components, migrations]
```

## Discipline

- **Never change code.** Diagnosis only.
- **Read the formatting functions.** Most API crashes are in data transformation, not in queries.
- **Compare working vs failing records.** The difference tells you exactly what's null.
- **Check json_agg behavior.** `[null]` vs `[]` is the #1 Cortex API bug pattern.
- **Look for the same formatter used elsewhere.** If `formatOrderComplete` is called from two routes, both are affected.
- **Don't assume migrations have been run.** Check the actual DB schema, not just migration files.
