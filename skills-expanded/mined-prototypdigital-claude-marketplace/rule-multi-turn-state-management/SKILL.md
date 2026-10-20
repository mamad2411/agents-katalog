---
name: multi-turn-state-management
description: Manage state across multi-turn interactions — track what was decided, what changed, and what is still open.
---

# Multi-turn state management

Long tasks that span many tool calls accumulate implicit state. Making that state explicit prevents contradictions and avoids re-doing work.

## Rules

- At the start of a multi-step task, enumerate the steps and track completion status explicitly (e.g. in a scratchpad or task list tool).
- After each significant subtask, record: what was done, what was found, and what constraint or decision it established.
- Before continuing after a long retrieval chain, briefly restate the active goal and remaining steps so the reasoning stays anchored.
- When new information contradicts a prior assumption, explicitly resolve the contradiction before proceeding — don't silently carry both.
- Mark tasks done as soon as they are done. Never batch completions — a stale task list is worse than no task list.

## Decision log pattern

When a non-obvious choice is made during task execution, record it inline:

```text
Decision: using `pnpm` (detected in package.json lockfileVersion)
Decision: targeting `src/api/` only (no matching files in `src/lib/`)
Decision: skipping format pass — `.prettierignore` excludes `*.generated.ts`
```

These become searchable context if the task is resumed or reviewed.

## Examples

```text
// BAD — implicit state; no record of what was decided or why
[tool: read src/api/users.ts]
[tool: read src/api/orders.ts]
[tool: edit src/api/orders.ts]
→ No record of why orders.ts was targeted, what was found, or what changed

// GOOD — explicit state log after each significant step
Step 1 ✓ — read users.ts: auth uses JWT, no session store
Step 2 ✓ — read orders.ts: missing ownership check on GET /orders/:id
Decision: targeting orders.ts only (users.ts has no vulnerability)
Step 3 ✓ — added ownership check at line 42
```
