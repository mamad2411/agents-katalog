---
name: blender-python-scripting
description: "Automate Blender with Python: `bpy` data API, operators versus direct data access, headless batch runs, add-on structure and exporting assets from a script."
type: procedural
category: 3d
domain: 3d
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - blender python script
  - bpy headless render automation
  - blender addon development
  - batch export blender files
  - blender background python
keywords:
  - blender
  - bpy
  - python
  - automation
  - addon
  - headless
  - batch
mcp_servers:
  - blender
source: custom
enabled: true
---

# Blender Python Scripting

## Purpose

Automate Blender with Python: `bpy` data API, operators versus direct data access, headless batch runs, add-on structure and exporting assets from a script.

## When to Use

- The same operation must run across many files or assets.
- An asset pipeline needs deterministic, repeatable exports.
- An add-on must package a workflow for a team.

## When NOT to Use

- A single manual edit is faster than writing code.
- The task needs interactive artistic judgement per asset.
- The target engine's own scripting API is the better integration point.

## Capabilities

- Use `bpy.data` for deterministic edits instead of context-dependent operators.
- Run headless with `blender -b -P script.py` and capture exit codes.
- Structure an add-on with registration, properties and operator classes.
- Export glTF/FBX/USD programmatically with explicit settings.

## Inputs

- The Blender version (the API changes between releases).
- The batch input: file list, naming convention, output contract.
- Whether it ships as an add-on or an internal script.

## Workflow

1. Check the Blender version and API differences before writing code.
2. Prefer data API edits; only use operators with a correct context override.
3. Write the script to be idempotent and to fail loudly on missing inputs.
4. Run headless on a single file, then scale to the batch with logging.
5. Verify output by re-importing an exported file.

## Tools

- `bpy` / `bmesh`
- `blender -b -P`
- glTF/FBX exporters

## Examples

- `blender -b -P batch_export.py -- --input assets/ --output dist/`
- `blender --version`
- `allskills route "batch export gltf from blender"`

## Safety

- Operators depend on context; calling them headless often silently no-ops.
- Scripts that overwrite source .blend files destroy work — always write copies.
- API changes between Blender versions break add-ons; pin the version you support.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `blender` | stdio | standard | medium | `BLENDER_HOST`, `BLENDER_PORT` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/3d/blender-python-scripting`). First-party skill, maintained in this repository.

## Notes

- `bpy.data` changes are undo-safe and context-free; operators are neither.
- Log the Blender version with every batch run so outputs are comparable.
- Pairs with: `3d/three-d-asset-pipeline`, `3d/blender-geometry-nodes`.
