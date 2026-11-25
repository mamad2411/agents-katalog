---
name: debug-issue
description: Systematically debug issues using graph-powered code navigation and code-review-graph
---

> **Condition d'entrée.** `code-review-graph` est un MCP *project-scope*. S'il
> n'apparaît pas dans le `mcp_config.json` du projet courant, aucun des outils
> cités ci-dessous n'existe : utilise la skill `code-search` à la place.
> N'invente jamais un appel à un outil absent.

## Debug Issue

Use the knowledge graph to systematically trace and debug issues.

### Steps

1. Use `semantic_search_nodes_tool` to find code related to the issue.
2. Use `query_graph_tool` with `callers_of` and `callees_of` to trace call chains.
3. Use `get_flow` to see full execution paths through suspected areas.
4. Run `detect_changes_tool` to check if recent changes caused the issue.
5. Use `get_impact_radius_tool` on suspected files to see what else is affected.

### Tips

- Check both callers and callees to understand the full context.
- Look at affected flows to find the entry point that triggers the bug.
- Fallback to `mgrep` for literal text search if the symbol is not in the graph.
