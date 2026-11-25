---
name: swpilotcli-inspect-drawing
description: Full attribute diagnostic tool for the active SolidWorks drawing. Dumps every annotation's complete properties: for dimensions — name, value, type, text parts (prefix/suffix/callout), tolerance type and values, precision, arrow style, layer, color; for notes — text content, leader attach point, arrow count and style, angle, layer, color. Also lists all visible geometry vertices with both model and sheet coordinates. Use when debugging dangling repairs, auditing annotation attributes before migration, or understanding drawing geometry for automation development.
---

# SolidWorks Inspect Drawing

Full attribute diagnostic dump for every annotation and geometry vertex in the active drawing.

## Prerequisites

- **SolidWorks 2024+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime** on the system
- An active `.slddrw` drawing document open in SolidWorks

## What this Skill does

For every sheet and view, outputs:

**DisplayDimension** (each dimension):
- Full name, system value, type code, text position
- All text parts 1–8: Prefix, Suffix, CalloutAbove, CalloutBelow (and Def variants)
- Tolerance: type, max value, min value
- Precision: Primary, TolPrimary
- Arrow head style
- Layer, color (ARGB), visibility

**Note** (each note):
- Text content, text position
- Leader attach point coordinates
- Arrow head count, style, size
- Rotation angle, layer, color

**Geometry vertices** (per view):
- Model coordinates (X, Y, Z) in mm
- Sheet/drawing coordinates (X, Y) in mm via ModelToViewTransform

## When to use

- **Before RepairDanglingAI**: understand full attribute set that must be preserved
- **After repair**: verify prefix, tolerance, layer were correctly restored
- **API development**: discover what properties an annotation actually holds
- **Coordinate mapping debug**: inspect vertex positions in both model and sheet space

## Quick start

```bash
dotnet run --project ./sup_tools/swpilotcli-inspect-drawing/scripts/InspectDrawing/InspectDrawing.csproj
```

Expected output (excerpt):

```
【視圖】前視圖
  [v正常] DisplayDimension
    名稱       : D1@草圖1@零件1
    數值       : 25.000 mm
    類型       : 2
    文字位置   : (120.500, 85.200) mm
    文字[Prefix]: "<C#-1>"
    公差Type   : 2
    公差Max    : +0.100 mm
    公差Min    : -0.200 mm
    精度Primary: 3
    圖層       : "尺寸"
    顏色(ARGB) : 0xFF000000

  P0[V] 模型=(0.00,0.00,0.00)  圖紙=(50.00,60.00) mm
  P1[V] 模型=(25.00,0.00,0.00)  圖紙=(75.00,60.00) mm
```

## Reference

See [API_REFERENCE.md](API_REFERENCE.md) for output format and APIs used.

## Notes

- Read-only — does not modify the drawing
- Output can be long for complex drawings; pipe to a file if needed
- Geometry vertices only: edges and faces are not listed
