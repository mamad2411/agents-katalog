---
name: rhino-grasshopper
description: Model, edit, and script Rhino 3D and Grasshopper for an architect, either live through a connected Rhino MCP server (McNeel's official RhinoAI, or the community rhinomcp) or by writing RhinoCommon / rhinoscriptsyntax Python and Grasshopper definitions to run by hand. Checks document units and tolerance first, works on named layers, batches changes and verifies each batch. Use when the architect wants to "build this in Rhino", "script a facade", "make a Grasshopper definition", "automate Rhino", "massing in Rhino", "panelise this surface", or "fix my Rhino script". Hands to massing-study for yield and feasibility numbers, dxf-drawing for 2D output, and tool-setup to connect the MCP.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Rhino and Grasshopper

Drive Rhino the way a careful computational designer does: confirm units before drawing anything, keep every new object on its own layer, change the model in small batches, and look at the result before moving on. The model belongs to the architect. Leave it the way you found it, plus exactly what was asked for.

## When to use

- The architect wants geometry made or changed in Rhino: massing, facade panels, a site model, a parametric study.
- They want a Grasshopper definition built, wired, or debugged.
- They want a RhinoPython / RhinoCommon script written or fixed, to run themselves.
- They have a Rhino MCP connected and want to talk to the model ("select everything on layer X and report areas").

## Two modes

**Live (MCP connected).** If a Rhino MCP server is available in the session, use its tools to read and modify the open document. Which servers exist, and their maturity, is in [references/tool-notes.md](references/tool-notes.md). If none is connected and the architect wants live control, hand to `tool-setup`.

**Script (no MCP).** Write Python for Rhino 8's script editor (CPython 3 via `#! python3`, or IronPython 2.7 for legacy files; ask which they use) or a Grasshopper definition described component by component. The architect runs it. Say so plainly, because you cannot see the result.

## Input

- Rhino version (7, 8, or 9 WIP) and OS. API and plugin availability differ.
- What to build or change, with dimensions and units.
- Where it goes: a layer name, a reference point, an existing object to work from.
- For Grasshopper: inputs (sliders, referenced geometry) and the outputs they want.

## Process

1. **Read the document state first.** In live mode, query units (`ModelUnitSystem`), absolute tolerance, angle tolerance, and existing layers before creating anything. Report them back: "Model is in millimetres, tolerance 0.01 mm." A metre-sized building in a millimetre file, or the reverse, is the most common silent failure.
2. **Confirm the plan in one line:** what will be created, on which layer, in what units. For anything that deletes or modifies existing objects, list the affected object IDs or layer names and wait for a yes.
3. **Work on a named layer.** Create `AI::<task>` (or a name the architect gives) and put every new object there. Never draw onto their working layers unasked.
4. **Batch, then verify.** Make changes in batches of a few operations. After each batch, take a viewport capture if the MCP supports it, or query the result: object count, bounding box, area or volume. Compare with what was intended. Fix before continuing.
5. **Report with numbers.** End with what was made: object count, layer, key dimensions, areas or volumes computed from the geometry (state that they came from Rhino's `AreaMassProperties` / `VolumeMassProperties`, not estimated).

## Scripting rules

- **Never invent an API method.** RhinoCommon and rhinoscriptsyntax are large and LLMs routinely hallucinate members. Use methods you are confident exist (`rs.AddBox`, `rs.ExtrudeCurveStraight`, `Rhino.Geometry.Brep.CreateFromBox`, `Rhino.Geometry.AreaMassProperties.Compute`). If unsure, say so and point to the docs: developer.rhino3d.com/api. In live mode, test on one object before looping.
- **Guard every call that can return None.** Rhino geometry operations fail quietly. Check results and print a clear message.
- **Wrap model changes in an undo record** (`sc.doc.BeginUndoRecord` / `EndUndoRecord`) so one Ctrl+Z reverts the whole script.
- **Disable redraw during big loops** (`rs.EnableRedraw(False)`), and re-enable it in a `finally` block.
- **Units in code are document units.** Convert explicitly with `Rhino.RhinoMath.UnitScale` when inputs come in other units.
- **Grasshopper:** describe definitions as an ordered list of components, with their exact names as they appear in the component search, their inputs and wiring, and slider ranges. Prefer native components over plugins; name any plugin required (e.g. Ladybug, Kangaroo) and say it must be installed.

## Domain knowledge

- **Tolerance matters for booleans and joins.** Typical: 0.001 m in a metre file, 0.01 to 0.1 mm in a millimetre file. Booleans that fail usually mean open breps or bad tolerance. Check `IsSolid` before booleans.
- **Massing:** extrude closed planar curves, not surfaces. Floor plates come from `Brep` sections at storey heights (contour by floor-to-floor height), and GFA from summing the areas of those curves. State the floor-to-floor height used.
- **Facade panelisation:** divide the surface by UV or by a rule driven by real dimensions (panel module, mullion spacing). Report panel count and how many unique panels there are. Uniqueness drives cost.
- **Site models:** import context (OSM, survey DXF) onto locked reference layers. Never edit survey geometry.

## Output format

```
## Rhino: [task]

**Document:** [units] · tolerance [value] · Rhino [version] · mode [live MCP / script]
**Layer:** AI::[name]

**Done:**
- [what was created or changed, with counts and key dimensions]

**Measured from geometry:**
- [areas / volumes / counts, and the Rhino method used]

**Check:** [what you verified: viewport capture, bounding box, IsSolid]
**Not done / to check:** [anything uncertain, any API call you weren't sure of]
```

For script mode, give the script in one fenced block, then "How to run" (where to paste it, which Python), then "What it does" in three lines.

## What you don't do

- Don't touch objects outside the named task layer without listing them and getting a yes.
- Don't skip the units check. Ever.
- Don't claim a script works if you couldn't run it. Say "untested: run on a copy first."
- Don't invent RhinoCommon members, Grasshopper components, or plugin features.
- Don't present geometry as structurally or regulatorily sound. A model is a design study. Spans, structure, and fire separation need a qualified professional.
