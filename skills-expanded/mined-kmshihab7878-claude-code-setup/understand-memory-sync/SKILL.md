---
name: understand-memory-sync
description: Sync knowledge graph entities to Memory MCP for cross-session codebase awareness
argument-hint: [project-path]
---

# /understand-memory-sync

Sync the most important entities from a project's knowledge graph to the Memory MCP server, enabling cross-session codebase recall without re-analysis.

## Instructions

1. **Locate the knowledge graph**:
   - If `$ARGUMENTS` contains a path, use that as the project directory
   - Otherwise, use the current working directory
   - Read `.understand-anything/knowledge-graph.json`
   - If not found, tell the user to run `/understand` first

2. **Extract key entities** (top ~50-100 nodes by architectural importance):
   - All `module` nodes (architectural boundaries)
   - All `class` nodes tagged as `agent`, `core-module`, or `governance`
   - File nodes with >200 lines (complexity hotspots)
   - Nodes referenced in the tour steps
   - The project node itself

3. **Create Memory MCP entities** using `mcp__memory__create_entities`:
   - Entity name: `{project}:{node.name}` (e.g., `CoreMind:CoreMind`)
   - Entity type: map node type → Memory entity type (`module` → `Architecture`, `class` → `Component`, `file` → `File`, `function` → `Function`)
   - Observations: node summary, tags, layer assignment, line count, file path

4. **Create Memory MCP relations** using `mcp__memory__create_relations`:
   - For each `imports` edge between synced nodes → `imports` relation
   - For each `inherits` edge → `extends` relation
   - For each `depends_on` edge between modules → `depends_on` relation
   - For each `contains` edge (module → key class) → `contains` relation

5. **Add a project-level observation** via `mcp__memory__add_observations`:
   - Entity: `CoreMind`
   - Observations:
     - "Knowledge graph: {N} nodes, {M} edges, {L} layers"
     - "Analyzed at: {timestamp}, commit: {hash}"
     - "Dashboard: cd ~/Projects/understand-anything/understand-anything-plugin/packages/dashboard && GRAPH_DIR=/path/to/project npx vite --open"

6. **Report** what was synced:
   ```
   Synced to Memory MCP:
   - {N} entities created
   - {M} relations created
   - Key modules: {list}
   - Key components: {list}

   These entities are now available across sessions via mcp__memory__search_nodes.
   ```

## When to Re-Sync

Re-sync after running `/understand` on new changes (incremental update). The skill should check if entities already exist and update observations rather than creating duplicates.
