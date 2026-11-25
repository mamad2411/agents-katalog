---
name: init-contracts
description: >
  Generate source-of-truth contract docs for any project from scratch.
  Reads actual source code systematically — does not guess or assume.
  Produces docs/contracts/, docs/ARCHITECTURE.md, and docs/patterns/.
  Works on any stack. Run once when starting a project or when docs don't exist yet.
---

# Init Contracts

Generate source-of-truth documentation for this project. Accuracy over speed. Use tools to gather hard data before writing anything.

---

## Step 1: Run Codegraph

Load and run the codegraph MCP tools first. They give you the dependency map so you know which files matter before reading anything.

```
ToolSearch: "codegraph scan"
→ mcp__codegraph__codegraph_scan (scan the project)
→ mcp__codegraph__codegraph_get_stats (entry points, most-depended-on files)
→ mcp__codegraph__codegraph_find_entry_points (server + client entry points)
```

From the stats output, identify:
- **Entry points** (server + client)
- **Most depended-on files** — these are the critical ones (schema, state machine, events, api client)

---

## Step 2: Enumerate Before Reading

Use Grep to build a complete inventory BEFORE opening any file. This prevents missing things.

```bash
# All API routes
grep -r "router\.\(get\|post\|patch\|put\|delete\)" server/src/routes/ --include="*.js" -n

# All WebSocket emits
grep -r "bus\.emit\|socket\.emit\|io\.emit" server/src/ --include="*.js" -n

# All CREATE TABLE statements
grep -r "CREATE TABLE" server/src/ -n

# All status/state enums (CHECK constraints or equivalent)
grep -r "CHECK\|status IN\|IN (" server/src/db/ --include="*.js" -n

# State machine transition map
grep -r "TRANSITION\|transitions\|from.*to\|nextStates" server/src/ --include="*.js" -l
```

Record the output. You now have a complete list of endpoints, events, tables, and states to document — you can't miss anything because you enumerated first.

---

## Step 3: Targeted Reads

Now read only the files that matter, identified by codegraph and grep:

1. **Entry point** — middleware order, route mounting, WS setup
2. **Schema file** — complete CREATE TABLE statements
3. **State machine file** — exact TRANSITION_MAP and guard conditions
4. **Events file** — EventEmitter setup
5. **WS relay file** — how bus events reach clients
6. **Each route file** — request shape, response shape, side effects
7. **DB query modules** — function names per table
8. **Frontend hooks** — what API calls they make, what events they subscribe to

Use `mcp__codegraph__codegraph_get_dependencies` on the entry point and schema file to find anything you might have missed.

---

## Step 4: Write the Docs

Write in this order. Each doc builds on what you already read — no re-reading needed.

### `docs/contracts/database-schema.md`

For each table found in Step 2:
- Paste the exact CREATE TABLE SQL
- Build the fields table from it (name, type, nullable, default, description)
- Document JSON fields with example shapes
- List all migrations from the schema init function

### `docs/contracts/api-endpoints.md`

For each route found in Step 2:
- Method + path (exact)
- Required vs optional body fields (from the route validation logic)
- Response shape (from `res.json(...)` calls)
- Side effects (which `bus.emit` calls follow this route)
- Backend file + frontend consumer hook

### `docs/contracts/state-machine.md` *(skip if no state machine)*

From the TRANSITION_MAP read in Step 3:
- States table (exact values from source)
- ASCII transition diagram (derived from the map, not invented)
- Valid transitions table (every entry in the map)
- Guard conditions (exact required fields + exact error messages from source)
- Which route enforces it and how

### `docs/contracts/websocket-events.md` *(skip if no real-time)*

From the emit calls found in Step 2:
- Every event: name, which route emits it, exact payload shape, which frontend hook subscribes
- The bus → ws → client flow diagram
- Frontend refetch pattern (from actual hook code)

### `docs/ARCHITECTURE.md`

Write last — synthesizes everything already read:
- System purpose (1 paragraph)
- ASCII architecture diagram
- Tech stack (exact versions from package.json)
- Core components (one section each, referencing their contract docs)
- 2-3 key data flows end-to-end (using actual file names)
- Actual directory tree with annotations
- Design decisions (infer from code choices)
- Critical invariants (from guards, CHECK constraints, and comments)

### `docs/patterns/api-endpoints.md` and `docs/patterns/react-components.md`

Two short files (< 30 lines each). Describe the pattern this codebase already uses, not a generic pattern. Include a code template.

---

## Step 5: Verify with Grep

Cross-check the docs against source before finishing:

```bash
# Count routes in source vs entries in api-endpoints.md
grep -rc "router\." server/src/routes/

# Count bus.emit calls vs events in websocket-events.md
grep -r "bus\.emit" server/src/ --include="*.js" | wc -l

# Count tables in source vs tables in database-schema.md
grep -r "CREATE TABLE" server/src/ --include="*.js"
```

If the counts don't match, find and fix the missing items.

---

## Output

```
CONTRACTS GENERATED
  docs/ARCHITECTURE.md              ✓
  docs/contracts/api-endpoints.md   ✓  ([N] endpoints)
  docs/contracts/database-schema.md ✓  ([N] tables)
  docs/contracts/state-machine.md   ✓ / N/A
  docs/contracts/websocket-events.md ✓ / N/A  ([N] events)
  docs/patterns/api-endpoints.md    ✓
  docs/patterns/react-components.md ✓

Verification:
  Routes in source: [N] | Documented: [N]
  Emit calls in source: [N] | Documented: [N]
  Tables in source: [N] | Documented: [N]
```

---

## After This

Copy `.claude/skills/source-of-truth-sync/SKILL.md` into this project and update its contract map table to match this project's file paths. That keeps the docs accurate as the code changes.
