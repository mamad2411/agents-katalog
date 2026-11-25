---
name: area-check
description: Measures areas from the architect's own drawings or model (closed polylines by layer in a DXF, IfcSpace quantities in an IFC, or a CSV), totals them by category, computes net-to-gross efficiency, and checks each space against the brief within a stated tolerance, showing the basis of every figure. It is explicit that measurement standards differ (IPMS, RICS, BOMA, local regulations) and asks which applies. Use when the architect wants to "check the areas", "measure this plan", "net to gross", "efficiency", "does the scheme hit the brief", "area schedule from the drawing", "GIA / NIA / GEA", "sellable or lettable area", or a quick area audit before a client meeting. Pairs with programme-schedule, which sets targets; dxf-drawing, which draws them; ifc-query for broader model QA; and massing-study for feasibility yield.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Area Check

The brief says 30 m2, the plan says something else, and nobody has measured since the last revision. This skill measures what is actually drawn or modelled, compares it with what was asked for, and shows every number's source, so the area schedule survives a quantity surveyor, an agent or a client.

## When to use

- Before a client meeting, planning submission or cost check: does the scheme still hit the brief?
- To produce an area schedule from a drawing or model rather than by hand.
- To compute efficiency (net-to-gross) and see where the gross is going.
- To reconcile two area schedules that disagree (usually they measure to different faces).

## Input

- **One source:** a DXF with closed room outlines on a known layer (and optionally gross outlines on another), an IFC with modelled `IfcSpace` objects carrying `Qto_SpaceBaseQuantities`, or a CSV of `name,area[,category,level]`.
- **The measurement standard**, which you have to ask for: IPMS (International Property Measurement Standards), RICS Code of Measuring Practice / RICS Property Measurement (UK and Commonwealth), BOMA (North America offices), ANSI Z765 (US homes), DIN 277 (Germany), NEN 2580 (Netherlands), or a local planning or building-regulation definition. Ask which, and which face (internal face, wall centreline, external face) the outlines are drawn to. The script measures geometry; the standard decides what counts.
- Optionally: a **brief** CSV (`name,target_area[,tolerance_pct]`), a **categories** CSV mapping names to `net`, `circulation`, `core`, `plant` and so on, and a gross area if it isn't drawn.

## Process

1. **Agree the standard and the face** before measuring. Write both into the output.
2. **Run the script** on the source:
   - `uv run scripts/area_check.py --dxf plan.dxf --room-layer A-ROOM --gross-layer A-AREA-GROS --brief brief.csv --categories cats.csv --md areas.md`
   - `uv run scripts/area_check.py --ifc model.ifc --brief brief.csv`
   - `uv run scripts/area_check.py --csv areas.csv --gross 1250`

   It refuses when units are unknown (pass `--units` if the DXF header lacks them), when the layer is empty, or when outlines are open. Open polylines are skipped and counted, never closed silently. IFC spaces with no area quantity are listed but left out of totals.
3. **Read the basis column.** Each area traces back to a polyline and layer, an IfcSpace GlobalId and quantity name, or a CSV line. Exit code 3 means a brief item is outside tolerance or missing.
4. **Explain the gaps.** "Gross minus measured" is walls, ducts, voids and unmeasured spaces, or an outline mismatch. If efficiency looks implausible for the building type, check the categories and the drawing faces before reporting it.
5. **Report** the schedule, the brief comparison and the efficiency calculation written out in full.

## Domain knowledge

- **Faces decide everything.** The same room measured to the internal face of the finishes, to the wall centreline, or to the external face can differ by several percent, and a lot more for small rooms with thick walls. Most disagreements between schedules come down to this.
- **Standards differ in what they include.** Columns, internal walls, stair and lift shafts, plant, balconies, areas under low headroom, and voids are treated differently by IPMS, RICS, BOMA and national codes. Some planning systems use their own definitions (residential space standards, floor area ratio, plot coverage). Don't convert between standards with a factor. Re-measure.
- **Efficiency** = net / gross, where "net" means the categories the architect says are net (usable, lettable, sellable). Typical ranges vary a lot by building type, core strategy and plate depth. Don't quote a typical range unless you can cite a source the architect accepts, and even then label it a benchmark to verify.
- **IFC quantities** are only as good as the export. `NetFloorArea` versus `GrossFloorArea` in `Qto_SpaceBaseQuantities` are calculated by the authoring tool (Revit, Archicad and others), and the settings vary. The script reports which one it used, per space, and scales to m2 from the project's area unit.
- **DXF arcs** are flattened to 10 mm chords, which keeps area error negligible at building scale. Text inside each outline becomes the room name; numeric labels such as "30.00 m2" are ignored so the script never reads its own answer.
- **Imperial.** Every area is given in m2 and sq ft (1 m2 = 10.7639 sq ft).

## Output format

```
## Area check: [project / drawing / revision]

Source: [file, layer or IFC schema]  |  Standard: [IPMS 3 / RICS GIA / BOMA / local definition]  |  Measured to: [internal face / centreline]

| Space | Category | Area m2 | Area sq ft | Basis |
|---|---|---|---|---|

| Category | Total m2 | Share |
|---|---|---|

Net-to-gross = [net] / [gross] = [x%]  (net = categories [..])

| Brief item | Target | Measured | Difference | Check |
|---|---|---|---|---|

Gaps and caveats: [open outlines skipped, spaces without quantities, faces assumed]

> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.
<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.

The disclaimer applies when areas feed planning, leases, sales or cost. A purely internal design check can leave it off.

## What you don't do

- Don't pick the measurement standard for the architect, and don't convert between standards with a ratio.
- Don't close open outlines or invent areas for spaces without quantities. List them as gaps.
- Don't quote "typical" efficiencies or space standards without a citable source, labelled as a benchmark.
- Don't present a drawing measurement as a surveyed, legal, lettable or sellable area. Those need a qualified measurer working to the agreed standard.
