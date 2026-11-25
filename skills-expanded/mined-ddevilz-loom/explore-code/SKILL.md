---
name: explore-code
description: Navigate and understand a codebase using Loom context packets. Find functions, trace call chains, understand architecture — without reading files.
argument-hint: "<keyword or question>"
allowed-tools:
  - mcp__loom__search_code
  - mcp__loom__get_context
  - mcp__loom__get_blast_radius
  - mcp__loom__get_neighbors
  - mcp__loom__get_community
  - mcp__loom__shortest_path
  - mcp__loom__graph_stats
  - mcp__loom__god_nodes
  - mcp__loom__get_surprising_connections
  - mcp__loom__suggest_questions
  - mcp__loom__start_session
  - mcp__loom__get_delta
  - mcp__loom__store_understanding
  - mcp__loom__get_work_plan
  - Read
  - Glob
---

# Explore Code

Navigate an indexed codebase using Loom's search and context tools.

## Steps

### 1. Session start

Call `start_session(agent_id="claude-code")` — record the returned `session_id` for use at next session start.

If you have a previous `session_id`, call `get_delta(previous_session_id=<id>)` first to see what changed since last time.

### 2. Orient to the codebase

Call `graph_stats()` — understand the repo shape (how many functions, files, classes, communities).

Call `get_work_plan()` — get a prioritized action list (`DOCUMENT` / `INVESTIGATE` / `EXPLORE` / `NOTHING`) based on annotation coverage and graph topology.

Call `suggest_questions(limit=5)` — get the graph topology's suggested investigation priorities.

### 3. Find the code the user is asking about

Use the user's keyword/question as search input:

```
search_code("<user's keyword>", limit=10)
```

If results have `summary` fields — read them. Skip file reads.

### 4. Get context on the most relevant result

```
get_context("<node_id from step 3>")
```

Returns: summary, signature, callers (top 10), callees (top 10), community, staleness.

If `summary_stale: true` — mention to user that source changed and summary may be outdated.

### 5. Trace call chains if needed

For "who calls this?" questions:
```
get_context("<node_id>", callees_limit=0)
get_blast_radius("<node_id>", depth=2)
```

For "what does this depend on?":
```
get_context("<node_id>", callers_limit=0)
```

For "how does A connect to B?":
```
shortest_path("<from_id>", "<to_id>")
```

### 6. Read source only if needed

Only open files when:
- No summary exists AND `get_context` is insufficient
- User explicitly asks for implementation details
- `summary_stale: true` AND you need current behavior

### 7. Store any new understanding

After reading any file:
```
store_understanding("<node_id>", "<one sentence: what it does and why>")
```

Good: "Validates JWT tokens against the configured secret, returns False if expired or malformed."
Bad: "Handles auth." / "Calls jwt.decode()."

### 8. Answer the user's question

Synthesize from Loom data (summary, signature, callers, callees) into a direct answer.
Reference node IDs so the user can explore further with other Loom tools.

---

## Task Mode (ticket or task description given)

Skip orientation entirely. The ticket already defines the scope.

1. Extract 2–3 key terms from the task (mental step, no tool call)
2. Search in parallel:
   ```
   search_code("<term1>", limit=5)
   search_code("<term2>", limit=5)
   ```
3. `get_context` on top 2–3 results
4. Output ≤50 tokens: what you found, what it maps to, what needs changing
5. Proceed with work

**No primer. No suggest_questions. No god_nodes.**

Example — ticket says "filter Products by Product Category, add toggle from #28274":
```
search_code("product category filter")
search_code("toggle component")
```
Get context on hits → map to files → start implementing. Total orientation cost: ~300 tokens.
