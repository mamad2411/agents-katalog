---
name: inspector-operations
description: Navigate and inspect 3Lens entities including meshes, materials, textures, and shaders. Use when examining specific entities, understanding dependencies, tracing cost attribution, or selecting entities by query.
---

# Inspector Operations

The Inspector is the spine of 3Lens. All tools route through selection and entity inspection. Use these commands to examine entities in detail.

## When to Use

- Examining a specific entity (mesh, material, texture, shader)
- Understanding entity dependencies and relationships
- Tracing cost attribution paths
- Selecting entities programmatically via query

## Commands

### Inspect an Entity

```bash
# Basic entity inspection
3lens inspect <entityId>

# Include additional data
3lens inspect <entityId> --include edges,cost,diffs

# Output as JSON
3lens inspect <entityId> --format json
```

**Output includes:**

- **Identity**: type, id, origin
- **Dependencies**: incoming/outgoing edges
- **Cost attribution**: weighted blame chains
- **Lifecycle + diffs**: creation, updates, disposal

### Select by Query

```bash
# Select top GPU cost entities
3lens inspect --query "top_gpu_cost" --limit 5

# Select materials using a specific texture
3lens inspect --query "materials_using_texture:tex123"
```

## The 5 Inspector Questions

Every entity inspection should answer:

1. **What is this?** (type, properties, origin)
2. **What does it depend on?** (incoming edges)
3. **What depends on it?** (outgoing edges)
4. **How much does it cost?** (attributed metrics with blame chain)
5. **How has it changed?** (diffs over time/traces)

## Entity ID Format

Entity IDs follow a stable, namespaced format:

```
<type>:<namespace>:<identifier>

Examples:
  mesh:scene:Player_Avatar
  material:default:PBR_Metal_01
  texture:loaded:albedo_diffuse.png
  shader:compiled:StandardPBR_v123
```

## Agent Use Cases

1. **Root cause analysis**: "Inspect entity mesh:scene:Player to find why it's expensive"
2. **Dependency tracking**: "Show all materials that depend on this texture"
3. **Cost attribution**: "Trace the blame chain for this GPU hotspot"
4. **Bulk selection**: "Select all entities matching this query"

## Additional Resources

- For detailed command syntax, see [.cursor/commands/](../../commands/)
- For Inspector contract, see [.cursor/contracts/inspector.md](../../../.cursor/contracts/inspector.md)
- For entity graph rules, see [.cursor/contracts/entity-graph.md](../../../.cursor/contracts/entity-graph.md)
- Inspector is runtime/UI; see addon-inspector for implementation
- Contract: [attribution.md](../../../.cursor/contracts/attribution.md)
- Contract: [fidelity.md](../../../.cursor/contracts/fidelity.md)
