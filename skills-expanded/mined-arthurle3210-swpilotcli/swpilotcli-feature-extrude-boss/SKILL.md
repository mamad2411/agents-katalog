---
name: swpilotcli-feature-extrude-boss
description: Extrude the active sketch outward to create a Boss-Extrude solid feature. Must be called while a sketch is active in editing mode. Use after sketch-on-face + sketch-draw to build up solid geometry.
---

# swpilotcli-feature-extrude-boss

Extrude the currently active sketch to create a Boss-Extrude feature (adds material).

## Prerequisites

- SolidWorks is running with an active Part document
- A sketch must be active in editing mode (run `sketch-on-face` then `sketch-draw` first)

## Usage

```bash
dotnet run --project ./sup_tools/swpilotcli-feature-extrude-boss/scripts/ExtrudeBoss/ExtrudeBoss.csproj -- <depth_mm>
```

## Arguments

| Arg | Description |
|-----|-------------|
| `depth_mm` | Extrusion depth in millimetres (e.g. `10`) |

## Examples

```bash
# Extrude active sketch 10mm
dotnet run ... -- 10

# Extrude 25.5mm
dotnet run ... -- 25.5
```

## How it works

1. Reads `depth_mm` from command-line argument
2. Calls `FeatureExtrusion3` (Blind, single direction, sketch-plane start)
3. Calls `EditRebuild3` and `GraphicsRedraw2`

## Notes

- This tool exits sketch mode as part of creating the feature
- For cutting material instead of adding it, use `extrude-cut`
- Typical flow: `sketch-on-face` → `sketch-draw` → `extrude-boss`
