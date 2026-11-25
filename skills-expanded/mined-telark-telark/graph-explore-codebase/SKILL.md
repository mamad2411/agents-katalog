---
name: graph-explore-codebase
description: Use to map how the codebase is structured (modules, where a symbol lives, what calls what, execution flows) when the code-review-graph MCP server is connected and list_graph_stats shows this repository indexed. Without an indexed graph, use normal search instead.
---

# Explore the codebase with the graph

Goal: an accurate map of the part of the codebase your task touches (modules, entry points, call relationships, flows) before you read files in detail.

Check the graph with `list_graph_stats` first: it shows whether this repository is indexed and when it was last updated. If it isn't indexed, or is older than the code you're looking at, use ordinary search instead. The graph covers this repository only; the shared Go modules (`data`, `rest`, `kcore`, `x-ware`) live in other repositories.

`get_minimal_context(task="…")` is a cheap starting point: stats, top communities and flows, and suggested next tools. Where a tool accepts `detail_level`, start with `"minimal"` and switch to `"standard"` when the compact answer isn't enough. Some server versions add a `_tool` suffix to these names (`query_graph_tool`).

| Question | Tools |
|---|---|
| Size, languages, freshness | `list_graph_stats` |
| High-level structure | `get_architecture_overview`, `list_communities`, `get_community` |
| Where a function or type lives | `semantic_search_nodes` |
| What a file contains | `query_graph` with `children_of` or `file_summary` |
| Callers, callees, imports | `query_graph` with `callers_of`, `callees_of`, `imports_of`, `importers_of` |
| Execution paths | `list_flows`, `get_flow` |
| Complexity hot spots | `find_large_functions` |

Work from broad (architecture) to narrow (one symbol's callers). The graph is a map, not the source: open the files before drawing conclusions or editing.
