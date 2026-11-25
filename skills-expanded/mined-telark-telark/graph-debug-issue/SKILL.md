---
name: graph-debug-issue
description: Use to trace a bug to its root cause through call chains, execution flows and recent changes when the code-review-graph MCP server is connected and list_graph_stats shows this repository indexed. Without an indexed graph, trace with normal search instead.
---

# Debug an issue with the graph

Goal: find the code path that produces the symptom, the root cause behind it, and every caller of the function you'll change, so the fix lands once where all callers route through.

Confirm with `list_graph_stats` that the graph covers this repository and is current; otherwise use ordinary search. `get_minimal_context(task="…")` is a cheap starting point, and `detail_level="minimal"` keeps answers compact where a tool accepts it.

| Need | Tools |
|---|---|
| Code related to the symptom | `semantic_search_nodes` |
| Call chains in both directions | `query_graph` with `callers_of` and `callees_of` |
| The entry point that triggers the path | `get_affected_flows`, `get_flow` |
| Whether a recent change caused it | `detect_changes` |
| What else the suspect code affects | `get_impact_radius` |

Check both callers and callees: a report names a symptom, and the cause often sits a hop away. Recent changes are the most common source of new issues. Confirm the root cause in the source and reproduce it with a test before fixing.
