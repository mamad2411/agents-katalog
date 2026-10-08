---
name: json-canvas
description: Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections. Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, or when the user mentions Canvas files in Obsidian.
---

# JSON Canvas Skill

## File Structure

A canvas file (`.canvas`) contains two top-level arrays following the [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/):

```json
{
  "nodes": [],
  "edges": []
}
```

- `nodes` (optional): Array of node objects
- `edges` (optional): Array of edge objects connecting nodes

## Common Workflows

### 1. Create a New Canvas

1. Create a `.canvas` file with the base structure `{"nodes": [], "edges": []}`
2. Generate unique 16-character hex IDs for each node (e.g., `"6f0ad84f44ce9c17"`)
3. Add nodes with required fields: `id`, `type`, `x`, `y`, `width`, `height`
4. Add edges referencing valid node IDs via `fromNode` and `toNode`
5. **Validate**: Parse the JSON to confirm it is valid. Verify all `fromNode`/`toNode` values exist in the nodes array

### 2. Add a Node to an Existing Canvas

1. Read and parse the existing `.canvas` file
2. Generate a unique ID that does not collide with existing node or edge IDs
3. Choose position (`x`, `y`) that avoids overlapping existing nodes (leave 50-100px spacing)
4. Append the new node object to the `nodes` array
5. Optionally add edges connecting the new node to existing nodes
6. **Validate**: Confirm all IDs are unique and all edge references resolve to existing nodes

### 3. Connect Two Nodes

1. Identify the source and target node IDs
2. Generate a unique edge ID
3. Set `fromNode` and `toNode` to the source and target IDs
4. Optionally set `fromSide`/`toSide` (top, right, bottom, left) for anchor points
5. Optionally set `label` for descriptive text on the edge
6. Append the edge to the `edges` array
7. **Validate**: Confirm both `fromNode` and `toNode` reference existing node IDs

### 4. Edit an Existing Canvas

1. Read and parse the `.canvas` file as JSON
2. Locate the target node or edge by `id`
3. Modify the desired attributes (text, position, color, etc.)
4. Write the updated JSON back to the file
5. **Validate**: Re-check all ID uniqueness and edge reference integrity after editing

## Reference Docs

- For node types, edge schema, colors, IDs, layout, and validation: [references/SPEC.md](references/SPEC.md)
- For full canvas examples (mind maps, project boards, flowcharts): [references/EXAMPLES.md](references/EXAMPLES.md)

## External Links

- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/)
- [JSON Canvas GitHub](https://github.com/obsidianmd/jsoncanvas)
