---
name: swpilotcli-feature-extrude-cut
description: Cut-extrude the active sketch through the solid to remove material. Supports a fixed depth in mm or through-all. Must be called while a sketch is active in editing mode. Use after sketch-on-face + sketch-draw to create holes, pockets, or slots.
---

# swpilotcli-feature-extrude-cut

Cut-extrude the currently active sketch to create a Cut-Extrude feature (removes material).

## Prerequisites

- SolidWorks is running with an active Part document
- A sketch must be active in editing mode (run `sketch-on-face` then `sketch-draw` first)

## Usage

```bash
dotnet run --project ./sup_tools/swpilotcli-feature-extrude-cut/scripts/ExtrudeCut/ExtrudeCut.csproj -- <depth_mm | through_all>
```

## Arguments

| Arg | Description |
|-----|-------------|
| `depth_mm` | Cut depth in millimetres (e.g. `5`) |
| `through_all` | Cut through the entire solid |

## Examples

```bash
# Cut 5mm deep pocket
dotnet run ... -- 5

# Through-all hole
dotnet run ... -- through_all
```

## How it works

1. Reads depth from command-line argument
2. Calls `FeatureCut3` (Blind or ThroughAll, single direction)
3. Traverses feature tree to find the newly created cut feature
4. Calls `EditRebuild3` and `GraphicsRedraw2`

## Notes

- This tool exits sketch mode as part of creating the feature
- For adding material instead of removing it, use `extrude-boss`
- Typical flow: `sketch-on-face` → `sketch-draw` → `extrude-cut`
- The sketch profile must be a closed contour on the face
