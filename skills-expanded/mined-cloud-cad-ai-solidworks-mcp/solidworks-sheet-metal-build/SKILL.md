---
name: "solidworks-sheet-metal-build"
description: "Build native SolidWorks sheet-metal parts (base flange, edge flanges, corners, K-factor, flat pattern, DXF) through the SolidWorks MCP bridge, with a macro fallback for edge flanges. Use for any sheet-metal part (enclosure, bracket, tray, lid, cover, chassis) or when the user mentions bends, flanges, K-factor, bend radius, flat pattern or DXF. When memory_* tools are listed and this is a new part, save it, then follow the engineering-memory skill's New project section."
---

# Sheet metal through the MCP bridge

Read `solidworks-bridge-tool-selection` for general bridge rules and `solidworks-macro-fallback` for running macros. Lengths are metres, angles radians. Proven on SOLIDWORKS 2026.

When `memory_*` tools are listed and this is a new part, save it, then follow the engineering-memory skill's New project section.

## 1. Agree the spec before modelling

Use native sheet-metal features (Base Flange, Edge Flange, Hem, Miter Flange...). Do not model a solid, shell it and insert bends unless the user asks for that; `convert_to_sheet_metal` and `insert_bends` are for existing solids.

Confirm, or state as assumptions:
- Thickness `t`, inside bend radius `Ri`, K-factor `K` (or bend table).
- Relief type and ratio; corner treatment (butt, overlap, gap `g`).
- Which dimensions are outer, and flange position. **Material Inside** (1) keeps the flange's outer face flush with the base edge, so outer size = base sketch. **Material Outside** (2) adds `t` beyond the base edge.

Edge flanges need edge and sketch objects, which the bridge cannot pass. Ask for macro approval up front.

## 2. Build order

1. **Base flange (bridge).** `create_sketch` on a plane, draw the profile centred on the origin, exit with SketchManager `InsertSketch(true)`, `ClearSelection2`, select the sketch by name, then doc `InsertSheetMetalBaseFlange(t, false, Ri, d1, d2, false, 0, 0, 0)`. Use this legacy IModelDoc2 call; `InsertSheetMetalBaseFlange2` returns no feature through the bridge. Read the body box to learn which way the sheet thickened (on Front Plane it goes to −Z, so flanges go to +Z).
2. **Edge flanges (macro).** Use one feature per opposite pair of edges: do the long pair, rebuild and check, then the other pair. Putting four adjacent edges in one feature failed. Template: [references/macros.md](references/macros.md).
3. **K-factor on every bend feature (macro).** The Sheet-Metal1 default K cannot be changed through the API (it stays 0.5). Set a custom K on each flange and prove it with the flat size.
4. **Cuts, holes, hems, other features.** Add them before any flat read (see section 4). For calls not listed here, find the member with `solidworks-api`, probe it on a throwaway part, then add the finding to `solidworks-bridge-tool-selection`.

## 3. Corners

- Butt corner with gap `g`: the full-length pair uses profile length = edge length. The butting pair uses length = edge length − 2t − 2g.
- If both pairs are full length the corners overlap, and the second flange shows a warning. Fix the profile length rather than adding a corner feature.
- `InsertSheetMetalClosedCorner` creates nothing when corners are already closed or overlapping.

## 4. Flat-pattern trap

Any flat read (`sheet_metal_info`, `export_dxf`, cut-list box) unsuppresses Flat-Pattern1 and leaves the part flattened. Features added after that land after Flat-Pattern1 and produce nothing. Straight after every flat read, select `Flat-Pattern1` (`BODYFEATURE`), call `EditSuppress2`, and check that the mass and box match the folded part. `model` suppress of the name `Flat-Pattern1` is the alternative.

## 5. Verify every feature

- What's Wrong is empty, and volume is close to a hand estimate (`area × t`).
- `GetBodyBox` equals the intended outer size.
- Wall ends and gaps: probe planar end faces of width `t` (macro in the reference file).
- Flat size for 90° bends: `BD = 2(Ri + t) − (π/2)(Ri + K·t)`. Along one direction, flat = sum of outer leg lengths − (number of bends × BD). Compare with the `sheet_metal_info` cut-list bounding box, then suppress the flat pattern again.
- Last of all, `export_dxf` if the user wants a flat drawing (then suppress the flat pattern again).

## 6. Recovery and hygiene

- Save after each verified feature. If a delete or recreate goes wrong (orphan sketches, dead tree), close without saving and reopen the last good save. Do not repair.
- Feature and sketch names keep counting after deletes. Re-read the tree before you select by name.
- `$n` inside an `invoke` arguments JSON array is substituted. Use `$n`. Do not call `invoke` to read a handle you can name as `$n`.
- Macros: write one job per macro, keep them in the project `Macros` folder, and re-read the model after each run. Tell the user which macro to edit and re-run when a driving dimension (t, Ri, K, flange length) changes.
