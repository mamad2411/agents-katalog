---
name: refactor-safely
description: Plan and execute safe refactoring using dependency analysis and code-review-graph
---

> **Condition d'entrée.** `code-review-graph` est un MCP *project-scope*. S'il
> n'apparaît pas dans le `mcp_config.json` du projet courant, aucun des outils
> cités ci-dessous n'existe : utilise la skill `code-search` à la place.
> N'invente jamais un appel à un outil absent.

## Refactor Safely

Use the knowledge graph to plan and execute refactoring with confidence.

### Steps

1. Use `refactor_tool` with mode="suggest" for community-driven refactoring suggestions.
2. Use `refactor_tool` with mode="dead_code" to find unreferenced code.
3. For renames, use `refactor_tool` with mode="rename" to preview all affected locations.
4. After changes, run `detect_changes_tool` to verify the refactoring impact.

### Safety Checks

- Check `get_impact_radius_tool` before major refactors.
- Use `get_affected_flows_tool` to ensure no critical paths are broken.
- Always run tests after refactoring (`pytest`, `npm run build`).
