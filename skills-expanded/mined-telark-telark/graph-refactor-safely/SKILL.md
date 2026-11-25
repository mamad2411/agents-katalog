---
name: graph-refactor-safely
description: Use to plan and apply renames, find dead code or look for refactoring opportunities with dependency analysis when the code-review-graph MCP server is connected and list_graph_stats shows this repository indexed. Without an indexed graph, find references with normal search instead.
---

# Refactor safely with the graph

Goal: a refactor where every reference is accounted for, no critical path breaks, and the diff contains only what the refactor needs.

Confirm with `list_graph_stats` that the graph covers this repository and is current; otherwise find references with ordinary search.

## Renames: preview, then apply

1. `refactor_tool` with `mode="rename"`, `old_name` and `new_name` returns the edit list and a `refactor_id`.
2. Review the edit list; `apply_refactor_tool` with `dry_run=true` shows it as a diff.
3. `apply_refactor_tool` with the `refactor_id` applies it. Previews expire after about ten minutes; re-run step 1 if yours has.
4. `detect_changes` confirms the impact; then run the usual gate (`go-service-change-gate` for Go).

Check `get_impact_radius` before a large refactor, and `get_affected_flows` afterwards to make sure no critical path broke.

## Other tools

| Need | Tools |
|---|---|
| Refactoring suggestions | `refactor_tool` with `mode="suggest"` |
| Unreferenced functions and classes | `refactor_tool` with `mode="dead_code"` |
| Decomposition targets | `find_large_functions` |

In this repository:

- Renaming an exported symbol of a shared package (`internal/data`, `rest`, `kcore`, `x-ware`) changes every service that imports it; update them in the same diff.
- Dead code you didn't create: report it, don't delete it unless asked.
- A refactor changes no behavior: the tests pass before and after, unmodified.
