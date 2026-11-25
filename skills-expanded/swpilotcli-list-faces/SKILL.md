---
name: swpilotcli-list-faces
description: List every face of every solid body in the active SolidWorks part, printing each face's surface normal and bounding-box centroid in millimetres. Use as a pre-selection scan before `sketch-on-face` or `feature-hole-wizard-straight-tap`, or when you need to identify a target face by coordinates without manually probing the model.
---

# SolidWorks List Faces

Dump normal + centroid for every face on every solid body of the active part.

## Prerequisites

- **SolidWorks 2024+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime**
- An active Part document (`.sldprt`)

## What this Skill does

- Casts the active document to `PartDoc`
- Calls `GetBodies2(swSolidBody)` to iterate all solid bodies
- For each body, iterates `GetFaces()` and reads:
  - `Face2.Normal` — unit normal vector
  - `Face2.GetBox()` — bounding box, used to compute centroid
- Prints one line per face:
  ```
  Normal=(nx,ny,nz)  Centre=(cx,cy,cz)mm
  ```

## When to use

- Before `sketch-on-face` when you want to see all candidate faces
- Debugging: find the exact world coordinate to pass to `SelectByID2("", "FACE", x, y, z, ...)`
- Auditing: verify a generated part has the expected number of faces

## Quick start

```bash
dotnet run --project ./sup_tools/swpilotcli-list-faces/scripts/ListFaces/ListFaces.csproj
```

## Return codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | No solid bodies found, or general error |
| 2 | Cannot connect to SolidWorks |
| 3 | No active document |
