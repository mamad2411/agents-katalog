---
name: blender-geometry-nodes
description: "Build procedural systems in Blender Geometry Nodes: field evaluation, instances versus realized geometry, attribute flow, collection and curve inputs, and asset-ready node groups."
type: procedural
category: 3d
domain: 3d
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - blender geometry nodes tutorial
  - geometry nodes fields
  - instance vs realize geometry
  - procedural scatter blender
  - node group asset
keywords:
  - blender
  - geometry-nodes
  - procedural
  - fields
  - instancing
  - attributes
mcp_servers:
  - blender
source: custom
enabled: true
---

# Blender Geometry Nodes

## Purpose

Build procedural systems in Blender Geometry Nodes: field evaluation, instances versus realized geometry, attribute flow, collection and curve inputs, and asset-ready node groups.

## When to Use

- Variation is parametric (scatter, patterns, arrays, kitbashing).
- An asset must adapt to different inputs without remodelling.
- Repeating detail should be instanced rather than modelled.

## When NOT to Use

- A one-off mesh is faster to model directly.
- The runtime does not evaluate geometry nodes (bake required).
- The logic needs per-frame simulation, which belongs in simulation nodes.

## Capabilities

- Think in fields (per-element evaluation) versus single values.
- Choose instancing for performance and realize only when required.
- Read and write named attributes through the node graph.
- Package node groups as reusable assets with exposed inputs.

## Inputs

- The inputs that should vary and their ranges.
- Whether output is baked geometry or instances at runtime.
- Poly budget and performance target.

## Workflow

1. Write down the inputs and outputs of the node group before wiring.
2. Build on primitives with debug viewers at each stage.
3. Prefer instances; realize only for booleans, UVs or export.
4. Expose parameters with sensible names and ranges.
5. Test extreme values and check the resulting poly count.

## Tools

- Blender Geometry Nodes editor
- spreadsheet editor for attribute debugging
- Node Wrangler

## Examples

- `blender -b scene.blend -P build_scatter.py`
- `allskills explain 3d/blender-geometry-nodes --query "scatter without realizing"`
- `allskills route "procedural fence generator"`

## Safety

- Realizing instances multiplies geometry and can exhaust memory on large counts.
- Attribute name typos fail silently and produce empty results.
- Procedural assets exported to engines must be baked or they lose their logic.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `blender` | stdio | standard | medium | `BLENDER_HOST`, `BLENDER_PORT` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/3d/blender-geometry-nodes`). First-party skill, maintained in this repository.

## Notes

- The spreadsheet editor is the fastest way to debug attribute flow.
- Instance attributes act on the instance; realized geometry acts per element.
- Pairs with: `cad/rhino-grasshopper`, `3d/houdini-procedural-vfx`.
