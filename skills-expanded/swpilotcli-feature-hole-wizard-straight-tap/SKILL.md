---
name: swpilotcli-feature-hole-wizard-straight-tap
description: Create a HoleWizard ISO Straight Tap feature on a specified face at one or more positions. Selects the face programmatically by world coordinates — no manual pre-selection required. Supports any metric size (M3–M12), blind depth in mm, or through-all. Use when the user asks to add tapped holes, M-size threaded holes, or straight taps to a face.
---

# swpilotcli-feature-hole-wizard-straight-tap

Create a SolidWorks HoleWizard ISO Straight Tap feature at one or more positions on a specified face.

## Prerequisites

- SolidWorks is running with an active Part document
- No sketch should be active (tool manages its own sketch context)

## Usage

```bash
dotnet run --project ./sup_tools/swpilotcli-feature-hole-wizard-straight-tap/scripts/HoleWizardStraightTap/HoleWizardStraightTap.csproj -- <size> <depth> <face_x,face_y,face_z> <x1,y1;x2,y2;...>
```

## Arguments

| Arg | Description |
|-----|-------------|
| `size` | Metric tap size: `M3` `M4` `M5` `M6` `M8` `M10` `M12` |
| `depth` | Depth in mm (e.g. `12`) or `through_all` |
| `face_x,face_y,face_z` | World coordinates (mm) of any point on the target face |
| `x1,y1;x2,y2;...` | Hole positions (mm) in the face's sketch coordinate system |

## Examples

```bash
# 4× M6 through-all taps on top face at Z=10mm
dotnet run ... -- M6 through_all "20,10,5" "-10.6,-11.65;10.6,-11.65;-10.6,11.65;10.6,11.65"

# 4× M3 through-all taps, positions symmetric about face centre (25,20)
dotnet run ... -- M3 through_all "25,10,-20" "20,10;30,10;20,30;30,30"

# Single M8 blind 15mm tap
dotnet run ... -- M8 15 "0,50,0" "0,0"
```

## How it works

1. Selects the target face using the provided world coordinates
2. Calls `HoleWizard5` with face only → creates feature with one default position
3. Enters the internal position sketch, deletes the default point
4. Adds points at the specified positions
5. Exits sketch and rebuilds

## Finding face coordinates

Use the `DiagFaces` helper or read geometry directly. The face coordinate
`(fx, fy, fz)` must lie on the face surface — avoid points inside holes or on edges.

## Tap drill diameters (ISO metric, mm)

| Size | Tap drill |
|------|-----------|
| M3   | 2.5 mm |
| M4   | 3.3 mm |
| M5   | 4.2 mm |
| M6   | 5.0 mm |
| M8   | 6.7 mm |
| M10  | 8.5 mm |
| M12  | 10.2 mm |

## Notes

- Positions are in **face sketch coordinates** (not world coordinates)
- Face sketch axes depend on face orientation — use `DiagFaces` to inspect if unsure
- For Top Plane (上基準面) faces: sketch X = world X, sketch Y = world −Z
- For Front Plane (前基準面) faces: sketch X = world X, sketch Y = world Y
