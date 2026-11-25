---
name: dxf-drawing
description: Produces real, layered, dimensioned DXF drawings with ezdxf (plan diagrams, room layouts, site boundaries, simple sections) that open in AutoCAD, Rhino, Vectorworks, Archicad, BricsCAD or QCAD, with units set in the header, closed polylines, area checks, and a PNG/SVG preview the agent inspects before handing over. Use when the architect wants "a DXF", "a CAD file", "draw this plan", "dimensioned plan diagram", "turn this sketch/area schedule into a drawing", "site boundary in CAD", or a quick line drawing to trace over. Hands to area-check to measure an existing DXF, diagram for non-scaled adjacency or zoning diagrams, site-map for an OSM context base, and massing-study for 3D.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# DXF Drawing

Write a drawing an architect can open in their own CAD package and keep working on: right units, sensible layers, closed room outlines, real dimension entities, and room areas computed from the geometry itself. It is a starting drawing or a diagram at scale. It is not a construction drawing.

## When to use

- A plan diagram at scale from a sketch, a description, or a schedule of accommodation.
- A site or plot boundary from coordinates or survey offsets, as a CAD base.
- A simple section or elevation outline (as polylines) to trace over.
- Converting a room list with target areas into rectangles that actually hit those areas.

## Input

- **Units (required).** m, cm, mm, ft or in. Never assume. If the architect doesn't say, ask. A DXF in the wrong units is worse than no DXF.
- Geometry: room polygons, wall centrelines with thickness, door and window positions, dimension strings, site boundary. Coordinates can come from the architect, from a sketch they describe, or from a programme (see `programme-schedule`).
- Target areas per room, if any. These become assertions the script checks.
- The office layer standard if they have one (AIA/NCS, ISO 13567, BS 1192/Uniclass, or their own). The default is AIA-style (`A-WALL`, `A-DOOR`, `A-GLAZ`, `A-ROOM`, `A-ANNO-DIMS`, `C-PROP`).

## Process

1. **Fix the units and origin first.** Agree units, which way is north, and where 0,0 sits (a site corner, a grid intersection). Write these down in the output.
2. **Build the spec as JSON.** The format is documented at the top of `scripts/plan_to_dxf.py`. Rooms are closed polygons, listed counter-clockwise. Walls are centrelines plus thickness. Openings are a point, a width and an angle. Dimensions run between two points with an offset.
3. **Run the script.**
   `uv run scripts/plan_to_dxf.py spec.json --out plan.dxf`
   It refuses on missing units, self-intersecting polygons, zero-length walls or bad points. It writes `plan.dxf`, `plan.png` and `plan.svg`, then re-opens the DXF and audits it.
4. **Look at the PNG yourself before you hand anything over.** Check that dimensions read the numbers you expect, labels sit inside their rooms, walls meet, door swings point the right way and nothing has flown off to 1e6. If the image is wrong, fix the spec and run it again. The architect should never be the first person to see a broken drawing.
5. **Read the report.** Each room's drawn area is computed with the shoelace formula on its polygon. Exit code 3 means an `expected_area` missed tolerance (1% by default). Adjust the geometry; do not edit the target to match.
6. **Hand over** the DXF and preview, plus a short note: units, origin, layers used, the area table and what is simplified.

DWG delivery, drawing inside a live AutoCAD session via MCP, and free DXF viewers are covered in [references/tool-notes.md](references/tool-notes.md).

## Domain knowledge

- **Header units matter.** `$INSUNITS` (m=6, mm=4, cm=5, ft=2, in=1) tells the receiving CAD package how to scale on insert or xref. `$MEASUREMENT` switches metric or imperial hatch and linetype defaults. Both are set here.
- **Areas are geometric, not standard.** A polygon area is the area of the line you drew. Whether that line is the internal face, the wall centreline or the external face depends on the measurement standard (IPMS, RICS, BOMA, or local). Say which face the rooms are drawn to. Use `area-check` for standard-based measurement.
- **Closed means closed.** Rooms and boundaries are written as closed LWPOLYLINEs, so they hatch, measure and extrude in every CAD package. Open outlines are the commonest reason a DXF "won't calculate".
- **Dimension entities, not text.** Dimensions are true DIMENSION entities, so they update when the geometry is stretched. They use architectural tick marks and text sized to the units.
- **Layers carry meaning.** Colour by layer, and put nothing on layer 0. Sections and other freeform linework go on a named layer (`A-SECT` by default).
- **What this cannot do.** No blocks for doors or windows (they are simple lines and arcs), no hatching, no linetypes beyond continuous, no paper-space sheets or title blocks. It produces a good base for a CAD user to take forward, not a drawing to issue.
- **Coordinates.** Drawing far from 0,0 (in real survey coordinates in metres) is fine for DXF, but some packages lose precision past about 1e6 units. Use a local origin and record the offset to survey grid.

## Output format

```
## Drawing: [title]

Files: plan.dxf (R2018), plan.png, plan.svg
Units: [m] ($INSUNITS 6) | Origin: [what 0,0 is] | North: [direction]
Layers: A-WALL, A-ROOM, A-ROOM-IDEN, A-DOOR, A-GLAZ, A-ANNO-DIMS, C-PROP

| Room | Drawn area | Target | Check |
|---|---|---|---|
| Living | 30.00 m2 | 30.00 m2 | OK |

Rooms drawn to: [internal face / centreline / external face]
Simplified: [door and window symbols, no hatching, no wall junction cleanup, ...]
Next: [what the CAD user should do first, e.g. "replace door symbols with office blocks"]
```

## What you don't do

- Don't guess units, north or scale. Ask.
- Don't present the DXF as a measured survey or a construction drawing. It is drawn from what you were given; say so.
- Don't report an area you didn't compute from the geometry. Every area in the output comes from the script.
- Don't hand over without checking the preview image yourself.
- Don't imply anything about compliance (room sizes, escape widths, accessible door widths). If those matter, they need checking against the applicable standard by a qualified professional.
