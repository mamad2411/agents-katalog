---
name: explore-codebase
description: Navigate and understand codebase structure using the knowledge graph (code-review-graph)
---

> **Condition d'entrée.** `code-review-graph` est un MCP *project-scope*. S'il
> n'apparaît pas dans le `mcp_config.json` du projet courant, aucun des outils
> cités ci-dessous n'existe : utilise la skill `code-search` à la place.
> N'invente jamais un appel à un outil absent.

## Explore Codebase

Use the code-review-graph MCP tools to explore and understand the codebase.

### Steps

1. Run `get_architecture_overview_tool` for high-level community structure.
2. Use `list_communities_tool` to find major modules, then `get_community` for details.
3. Use `semantic_search_nodes_tool` to find specific functions or classes.
4. Use `query_graph_tool` with patterns like `callers_of`, `callees_of`, `imports_of` to trace relationships.
5. Use `list_flows` and `get_flow` to understand execution paths.

### Tips

- Start broad (architecture) then narrow down to specific areas.
- Use `query_graph_tool` with pattern="children_of" on a file to see all its functions and classes.
- Use `mgrep` as fallback if textual search is needed outside the graph.
