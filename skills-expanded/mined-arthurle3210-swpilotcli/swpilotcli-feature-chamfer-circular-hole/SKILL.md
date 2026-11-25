---
name: swpilotcli-feature-chamfer-circular-hole
description: Apply an angle-distance chamfer to circular hole edge(s) in the active SolidWorks part. Targets full circular edges by diameter and can optionally limit selection to the nearest matching edge to a supplied world coordinate. Use for chamfering drilled/cut hole openings such as 0.5 C x 45 deg center-hole chamfers.
---

# swpilotcli-feature-chamfer-circular-hole

Apply an angle-distance chamfer to circular hole edge(s) in the active SolidWorks part.

## Prerequisites

- SolidWorks is running with an active Part document
- The target hole already exists as circular edge geometry

## Usage

```bash
dotnet run --project ./sup_tools/swpilotcli-feature-chamfer-circular-hole/scripts/ChamferCircularHole/ChamferCircularHole.csproj -- [diameter_mm] [chamfer_mm] [angle_deg] [nearest_x,nearest_y,nearest_z]
```

## Arguments

| Arg | Description |
|-----|-------------|
| `diameter_mm` | Target hole diameter in millimetres. Default: `10` |
| `chamfer_mm` | Chamfer distance in millimetres. Default: `0.5` |
| `angle_deg` | Chamfer angle in degrees. Default: `45` |
| `nearest_x,nearest_y,nearest_z` | Optional world coordinate in millimetres. If supplied, only the nearest matching circular edge is chamfered. |

## Examples

```bash
# Apply 0.5 C x 45 deg chamfer to all 10 mm circular hole openings
dotnet run --project ./sup_tools/swpilotcli-feature-chamfer-circular-hole/scripts/ChamferCircularHole/ChamferCircularHole.csproj

# Apply to the matching circular edge nearest the top center of a 40 x 40 x 10 block
dotnet run --project ./sup_tools/swpilotcli-feature-chamfer-circular-hole/scripts/ChamferCircularHole/ChamferCircularHole.csproj -- 10 0.5 45 20,20,10
```

## How it works

1. Traverses visible solid bodies in the active part
2. Finds full circular edges matching the requested diameter
3. Optionally keeps only the matching edge nearest the supplied world coordinate
4. Selects the target edge(s)
5. Calls `FeatureChamferType` with `swChamferAngleDistance`
6. Rebuilds and redraws the model

## Notes

- Without `nearest_x,nearest_y,nearest_z`, every matching full circular edge is chamfered.
- Use the coordinate option when the part has multiple holes of the same diameter.
