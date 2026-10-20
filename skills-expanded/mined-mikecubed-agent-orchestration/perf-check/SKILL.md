---
name: perf-check
description: >
  Enforces performance rules (PERF-1 through PERF-3). Loaded by the conductor for
  review operations. Detects N+1 query patterns, unbounded loops over large
  collections, and missing pagination on list endpoints using static analysis.
version: "1.0.0"
last-reviewed: "2026-04-03"
languages: [typescript, python, go, rust, javascript]
changelog: "../../CHANGELOG.md"
tools: Read, Grep
model: claude-sonnet-4.6
permissionMode: default
---

# Perf Check — Performance Enforcement

Precedence in the overall system: SEC → TDD → ARCH/TYPE →
**PERF-1 (BLOCK)** → PERF-2, PERF-3 (WARN).

---

## Rules

### PERF-1 — N+1 Query Pattern
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: A database query or external API call executed inside a
loop body, causing O(n) queries for a list of n items.

**Detection patterns**:
1. Loop (`for`/`while`/`forEach`/`map`) containing ORM call:
   - `.find()`, `.findOne()`, `.query()`, `db.execute()` inside iteration body
   - `await fetch()`, `axios.get()` inside loop body
2. Nested async/await in map:
   - `items.map(async item => await repo.findBy(item.id))`
3. Python: `for item in items:` with `session.query(...)` or `Model.objects.get()`
   inside the loop body
4. Go: `for _, item := range items` with `db.QueryRow()` or `db.Query()`
   inside the loop body

**agent_action**:
1. Cite: `PERF-1 (BLOCK): N+1 query pattern at {file}:{line_range} — '{pattern}' called inside loop.`
2. **STOP ALL WORK** on this code path until resolved.
3. Suggestion: use `.findByIds()`, batch load, DataLoader, or `WHERE id IN (...)` query
4. If `--fix`: refactor the loop to use a batch query and map results by key

---

### PERF-2 — Unbounded Loop Over Collection
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Iteration over a collection that may be large with no
limit, early-exit condition, or pagination guard.

**Detection patterns**:
1. `for item in collection:` / `for _, item := range collection` /
   `items.forEach(` with no `.slice()`, `.limit()`, `break`, or size guard
   within the loop
2. Processing all rows from a DB query result with no `LIMIT` clause in the query
3. `while` loops consuming an iterator/generator with no `take()`, `islice()`,
   or maximum iteration count

**agent_action**:
1. Report: `PERF-2 (WARN): Unbounded loop at {file}:{line} — iterating '{collection}' with no limit guard.`
2. Suggestion: add limit guard, paginate, or document max-size invariant
3. If the collection has a known bounded size (e.g., enum values, config entries):
   accept with a comment documenting the upper bound
4. If `--fix`: add a `.slice(0, MAX)` or equivalent guard with a configurable limit

---

### PERF-3 — Missing Pagination on List Endpoint
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: An API handler or route that returns a list of items
without pagination parameters.

**Detection patterns**:
1. Route handler returning array/list with no `limit`, `offset`, `page`, `cursor`,
   or `take`/`skip` parameters in the request schema
2. ORM query with no `.limit()`, `.take()`, `LIMIT` clause, or page-size guard
3. GraphQL resolvers returning unbounded lists without `first`/`after` arguments
4. REST endpoints returning `findAll()` or `SELECT *` without pagination

**agent_action**:
1. Report: `PERF-3 (WARN): Missing pagination at {file}:{line} — endpoint '{path}' returns unbounded list.`
2. Suggestion: add cursor-based or offset pagination
3. Recommended patterns:
   ```typescript
   // Cursor-based (preferred for large datasets)
   app.get('/items', async (req, res) => {
     const { cursor, limit = 20 } = req.query;
     const items = await repo.findAfter(cursor, Math.min(limit, 100));
     res.json({ items, nextCursor: items[items.length - 1]?.id });
   });
   ```
4. If `--fix`: add pagination parameters and apply default + maximum limits

---

**Output format per finding**:
```
PERF-N | BLOCK/WARN | <file>:<line> | <pattern name> | Suggestion: <guidance>
```

**Activation**:
Loaded by the conductor for `review` operations. Signal phrases: "review",
"check", "audit", "performance", "slow query", "N+1".

Report schema: see `skills/conductor/shared-contracts.md`.
