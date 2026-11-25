---
name: swpilotcli-sketch-on-face
description: Open a new sketch on a specified face or plane. Accepts either a named plane (e.g. 前基準面) or world face coordinates in mm (e.g. 25,10,-20). Enters sketch editing mode and stays there — follow up with sketch-draw to draw geometry, then extrude-boss or extrude-cut.
---

# swpilotcli-sketch-on-face

Open a new sketch on a face or reference plane. Enters sketch editing mode.

## Prerequisites

- SolidWorks is running with an active Part document
- No sketch should currently be active

## Usage

```bash
dotnet run --project ./sup_tools/swpilotcli-sketch-on-face/scripts/SketchOnFace/SketchOnFace.csproj -- [plane_name | x,y,z]
```

## Arguments

| Arg | Description |
|-----|-------------|
| `plane_name` | Name of a reference plane (e.g. `前基準面`, `上基準面`, `右基準面`) |
| `x,y,z` | World coordinates (mm) of any point on the target face |
| *(none)* | Uses the currently pre-selected face or plane |

## Examples

```bash
# Open sketch on the front plane
dotnet run ... -- 前基準面

# Open sketch on a face by world coordinates
dotnet run ... -- 25,10,-20

# Open sketch on the pre-selected face (no arg)
dotnet run ...
```

## How it works

1. If a plane name is given → selects it by name using `SelectByID2`
2. If `x,y,z` coords are given → selects the face at those world coordinates
3. Calls `InsertSketch` to enter sketch editing mode
4. Stays in sketch — caller must run `sketch-draw` then `extrude-boss`/`extrude-cut`

## Notes

- Face coordinate `(fx, fy, fz)` must lie on the face surface (not on an edge or in a hole)
- For the top face of an extruded block at Z = −depth/2, the sketch axes are:
  - Sketch X = World X
  - Sketch Y = World −Z
- After this tool, run `sketch-draw` with a DSL JSON, then `extrude-boss` or `extrude-cut`
