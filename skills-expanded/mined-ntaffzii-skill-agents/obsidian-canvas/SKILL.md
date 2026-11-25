---
name: obsidian-canvas
description: Create and edit Obsidian JSON Canvas .canvas files with nodes, edges, groups, colors, links, files, and spatial layouts. Use when the user asks for an Obsidian canvas, visual map, knowledge graph, board, flow, or .canvas file.
---

# Obsidian Canvas

Use this skill to create valid JSON Canvas files for Obsidian.

## Canvas Shape

A canvas file is JSON with:

```json
{
  "nodes": [],
  "edges": []
}
```

Nodes need stable IDs and position fields:

- `id`
- `type`
- `x`
- `y`
- `width`
- `height`

Common node types:

- `text` with `text`
- `file` with `file`
- `link` with `url`
- `group` with `label`

Edges connect node sides:

- `id`
- `fromNode`
- `fromSide`
- `toNode`
- `toSide`

## Workflow

1. Identify the canvas purpose
   - Map, timeline, workflow, dashboard, argument, project board, or concept graph.

2. Choose layout
   - Left to right for process flows.
   - Top to bottom for hierarchy.
   - Hub and spoke for concept maps.
   - Columns for project boards.

3. Create nodes
   - Use readable dimensions.
   - Keep text concise.
   - Use file nodes for notes that already exist or should be created separately.

4. Connect edges
   - Use edges only for meaningful relationships.
   - Avoid visual clutter.
   - Use stable IDs such as `edge-plan-build`.

5. Validate JSON
   - Ensure valid JSON, no trailing commas.
   - Ensure every edge references existing node IDs.
   - Ensure nodes do not overlap unintentionally.

## Rules

- Do not invent files unless the user asked to create them.
- Prefer text nodes for new ideas and file nodes for existing notes.
- Keep coordinates simple and grid-like.

## Output Format

End with:

- Canvas file created or changed
- Node and edge count
- Linked files referenced
- JSON validation result
