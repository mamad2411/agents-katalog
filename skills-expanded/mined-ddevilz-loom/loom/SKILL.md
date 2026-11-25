---
name: loom
description: >
  Use Loom MCP tools for code intelligence — symbol search, context packets,
  blast radius, session primer, delta context, topology insights. Invoke when
  working on any codebase indexed with `loom analyze .`.
trigger: >
  When connected to an MCP server named "loom" OR when user says "use loom"
  OR when search_code / get_context / store_understanding tools are available.
allowed-tools:
  - mcp__loom__search_code
  - mcp__loom__get_context
  - mcp__loom__get_blast_radius
  - mcp__loom__get_neighbors
  - mcp__loom__get_community
  - mcp__loom__shortest_path
  - mcp__loom__graph_stats
  - mcp__loom__god_nodes
  - mcp__loom__store_understanding
  - mcp__loom__store_understanding_batch
  - mcp__loom__get_savings
  - mcp__loom__start_session
  - mcp__loom__get_delta
  - mcp__loom__get_surprising_connections
  - mcp__loom__suggest_questions
  - mcp__loom__get_status
  - mcp__loom__get_work_plan
  - Read
  - Glob
---

# Loom Workflow

Loom is a persistent symbol index. Every session gets faster as agent summaries
accumulate. Zero LLM cost — all data from tree-sitter + your own stored summaries.

---

## Session Start Protocol

### Step 1 — Register session

```
start_session(agent_id="claude-code")   → { session_id, agent_id, started_at, unannotated_reads, annotation_gaps }
```
Save `session_id` — pass to `get_delta()` at start of **next** session.

`unannotated_reads` lists nodes you visited last session but never annotated — prioritize `store_understanding` on these.
`annotation_gaps` lists high-value nodes with no summary — good targets for documentation.

### Step 2 — Check delta (if you have a prior session_id)

```
get_delta(previous_session_id="<id>")
```
Returns only changed/deleted nodes since last session. Three response shapes:
- **Normal:** `{changed: [context_packets...], deleted: [ids...]}` → review each
- **Too many changes:** `{too_many_changes: true, top_changed_paths: [...]}` → treat as fresh start, use `search_code`
- **Error:** `{error: "session_not_found"}` → session expired, skip delta, proceed to primer

If no prior session_id, pass `agent_id="claude-code"` instead — loom finds your most recent session.

### Step 3 — Load primer (always)

Read `loom://primer` resource → ~200-token codebase overview.

**Act on primer data:**

| Primer Signal | Agent Action |
|---------------|--------------|
| `empty: true` | Repo not indexed. Tell user: `loom analyze .` — or wait, auto-index may be running |
| `coverage.summaries < 30%` | Prioritize `store_understanding` after every file read |
| `coverage.summaries > 80%` | Summaries are rich — trust them, skip file reads when possible |
| `hot` functions listed | Start exploration from these — they're the most-connected entry points |
| `last_analyzed` > 24h old | Suggest user runs `loom analyze .` for fresh data |

### Step 4 — Prioritize work

```
suggest_questions()           → dead code, bridge nodes, missing summaries, low cohesion
get_surprising_connections()  → hidden coupling, unexpected cross-module bridges
```

---

## Task Mode (ticket or task description given)

Skip orientation. The task defines scope.

1. Extract 2–3 key terms from the task (mental step, no tool call)
2. Search in parallel:
   ```
   search_code("<term1>", limit=5)
   search_code("<term2>", limit=5)
   ```
3. `get_context` on top 2–3 hits
4. Output ≤50 tokens: what maps to what, what needs changing
5. Proceed

No primer. No suggest_questions. No god_nodes. Total orientation: ~300 tokens.

---

## Finding Code

```
search_code("validate token", limit=10)
```
Returns: `id, name, path, kind, line, score, summary, signature, tokens_saved`.

**Decision tree after search:**
- Has `summary` → read it, **skip file read**. Summary is authoritative.
- Has `signature` but no summary → you know the shape, call `get_context` for callers/callees.
- Neither → call `get_context(node_id)` before opening the file.

---

## Progressive Detail (Use the Cheapest Tool First)

| Need | Tool | Response Size |
|------|------|---------------|
| "Does this exist?" | `get_context(id, brief=True)` | ~50 tokens |
| "What does this do?" | `get_context(id)` | ~200 tokens |
| "What calls/uses this?" | `get_context(id, callees_limit=0)` / `get_context(id, callers_limit=0)` | ~100-300 tokens |
| "What breaks if I change this?" | `get_blast_radius(id, depth=3)` | ~500-2000 tokens |

Don't jump to `get_blast_radius` when `get_context` would suffice.

---

## Reasoning About a Function

```
get_context("function:src/auth.py:validate_token")
```

Returns:
- `summary` — what it does and why
- `signature` — full type-annotated signature
- `callers` — top 10 by frequency (same-file first), each with `summary`
- `callees` — top 10, each with `summary`
- `summary_stale` — `true` if source changed since summary was written
- `summary_source` — `"AGENT"` (verified by agent) or `"AUTO"` (tree-sitter metadata)
- `auto_summary` — tree-sitter-extracted metadata (always present as baseline)
- `edge_coverage` — 0.0–1.0 confidence in call graph completeness
- `has_dynamic_dispatch` — `true` if callers/callees may be incomplete

**Staleness handling:**
If `summary_stale: true` → source changed since summary was written.
Read the source file, then update:
```
store_understanding(node_id="...", summary="...", force=True)
```

**If `get_context` returns `None`:** Node ID is wrong. Use `search_code` to find correct ID.

---

## Impact Analysis

```
get_blast_radius("function:src/auth.py:validate_token", depth=3)
```
Each result includes `summary`. Read summaries directly — only call `get_context` on
nodes where summary is null or you need their callers/callees too.

```
get_context("function:src/auth.py:validate_token", callees_limit=0)  → callers list
get_context("function:src/auth.py:validate_token", callers_limit=0)  → callees list
```

**If callers/callees returns `[]`:** Function is a leaf (no callers = dead code or entry point, no callees = leaf function). Check `suggest_questions()` — it flags dead code automatically.

---

## Topology Exploration

```
get_surprising_connections(limit=10)
```
Returns `caller_summary` and `callee_summary` on each result. Read these before
deciding whether to investigate further.

```
graph_stats(include_cohesion=True)
```
Cohesion score per community (0.0–1.0). Low cohesion (<0.2) = refactor candidate.

```
suggest_questions(limit=7)
```
Question types and what they mean:
- `dead_code` — function has no callers. Safe to delete? Or undiscovered entry point?
- `bridge_node` — connects two otherwise-separate communities. High blast radius.
- `missing_summary` — hot function with no agent summary. Document it.
- `low_cohesion` — community with too many external dependencies. Refactor candidate.

---

## Storing Understanding (Do This Every Time)

After reading any function source:
```
store_understanding(
    node_id="function:src/auth.py:validate_token",
    summary="Validates JWT tokens, returns False if expired or signature invalid."
)
```

**Good summary:** what + why, one sentence, ≤120 chars.
- "Validates JWT tokens, returns False if expired or malformed."
- "Entry point for /api/users — authenticates, then delegates to UserService."

**Bad summary:**
- "Handles auth." — too vague, doesn't help next agent
- "Calls jwt.decode() then checks exp claim." — describes HOW, not WHAT/WHY

**Batch version** (after reading multiple files):
```
store_understanding_batch([
    {"node_id": "function:src/auth.py:validate_token", "summary": "..."},
    {"node_id": "function:src/auth.py:refresh_token", "summary": "..."},
])
```
Max 50 per call.

**Idempotency:** `store_understanding` is content-hash-aware.
- Same summary + unchanged source → `{skipped: true}` — no write, no cost.
- Source changed since last summary → use `force=True` to overwrite.
- Node not found → `{ok: false, error: "node not found"}` — check ID with `search_code`.

---

## Error Handling Reference

| Tool | Returns on "not found" | What to do |
|------|----------------------|------------|
| `get_context(id)` | `None` | ID is wrong — use `search_code` |
| `get_context(id, callees_limit=0)` | `callers: []` | No callers exist (dead code or entry point) |
| `get_context(id, callers_limit=0)` | `callees: []` | Leaf function — no outgoing calls |
| `shortest_path(a, b)` | `None` | No path exists between these nodes |
| `store_understanding(id)` | `{ok: false}` | Node not found — verify ID |
| `get_delta(session_id)` | `{error: "session_not_found"}` | Session expired — skip delta |
| `get_delta()` (no args) | `{error: "missing_args"}` | Pass `previous_session_id` or `agent_id` |

---

## Node ID Format

`{kind}:{path}:{symbol}`

| Kind | Example |
|------|---------|
| `function` | `function:src/auth.py:validate_token` |
| `method` | `method:src/models/user.py:User.save` |
| `class` | `class:src/models/user.py:User` |
| `file` | `file:src/auth.py` |

Path is always relative to repo root. When in doubt, use `search_code` to find exact ID.

---

## DB Path

Resolved in order:
1. `LOOM_DB_PATH` env var (explicit override)
2. `~/.loom/projects/{git-root-name}.db` (per-project, automatic)
3. `~/.loom/loom.db` (fallback for non-git repos)

---

## Quick Reference

| Tool | Use When | Cost |
|------|----------|------|
| `start_session(agent_id)` | Session start — always first | ~20 tok |
| `get_delta(prev_session_id)` | Session start — see what changed | ~50-500 tok |
| `search_code(query)` | Finding symbols by name/keyword | ~100 tok |
| `get_context(node_id, brief=True)` | Quick existence check / basic info | ~50 tok |
| `get_context(node_id)` | Full picture: summary + callers + callees + staleness | ~200 tok |
| `get_blast_radius(node_id)` | Transitive callers — impact of a change | ~500-2000 tok |
| `get_neighbors(node_id)` | All connected nodes (any edge type) | ~100-300 tok |
| `get_community(community_id)` | All members of a cluster | ~200-500 tok |
| `shortest_path(from, to)` | Dependency chain between two functions | ~100-300 tok |
| `store_understanding(id, summary)` | After reading any function — always do this | ~20 tok |
| `store_understanding_batch(updates)` | Batch summaries — up to 50 at once | ~20 tok |
| `graph_stats()` | Repo overview: node/edge counts by kind | ~50 tok |
| `god_nodes()` | Most-called functions (entry points) | ~100-200 tok |
| `suggest_questions()` | Investigation priorities from graph topology | ~100-200 tok |
| `get_surprising_connections()` | Hidden coupling with caller/callee summaries | ~200-500 tok |
| `graph_stats(include_cohesion=True)` | Cluster quality scores for refactoring | ~100-200 tok |
| `get_savings()` | Token savings report from cache hits | ~50 tok |
| `get_status()` | Node count + DB health check | ~20 tok |
| `get_work_plan()` | Prioritized task list: DOCUMENT / INVESTIGATE / EXPLORE / NOTHING | ~100 tok |
