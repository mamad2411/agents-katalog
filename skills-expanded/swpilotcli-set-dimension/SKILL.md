---
name: swpilotcli-set-dimension
description: Set the value of a driving dimension in the active SolidWorks document by its full name. Requires two arguments, the dimension full name (e.g. `D1@Sketch1` or `D1@Boss-Extrude1`) and the new value in millimetres. Calls Parameter().SetSystemValue3 then rebuilds. Use as an atomic building block whenever you need to change a sketch or feature dimension, regardless of what that dimension drives (hole radius, extrude depth, rectangle length, etc.).
---

# swpilotcli-set-dimension

Set a driving dimension by full name to a new value in millimetres.

## Usage

```bash
dotnet run --project ./sup_tools/swpilotcli-set-dimension/scripts/SetDimension/SetDimension.csproj -- <dimName@owner> <value_mm>
```

## Arguments

| Argument | Description |
|----------|-------------|
| `<dimName@owner>` | Full dimension name, e.g. `D1@Sketch1`, `RadiusHole@Sketch2`, `D1@Boss-Extrude1`. |
| `<value_mm>` | New value in millimetres (converted to metres internally). |

## Notes

- Uses `ModelDoc2.Parameter(fullName)` to fetch the dimension.
- Writes via `Dimension.SetSystemValue3(valueMeters, swSetValue_InThisConfiguration, null)`.
- Calls `EditRebuild3()` and `GraphicsRedraw2()` after the change.
- Returns non-zero exit code if the dimension name cannot be found.

## Examples

```bash
# Change hole radius dimension D1 in Sketch2 to 8 mm
dotnet run --project ./sup_tools/swpilotcli-set-dimension/scripts/SetDimension/SetDimension.csproj -- "D1@Sketch2" 8

# Change extrude depth D1 in Boss-Extrude1 to 25 mm
dotnet run --project ./sup_tools/swpilotcli-set-dimension/scripts/SetDimension/SetDimension.csproj -- "D1@Boss-Extrude1" 25
```
