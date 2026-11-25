---
name: woodworking
description: >
  Complete design of custom woodworking and cabinetmaking projects from a description, photos,
  sketches, or dimensions. Produces a needs analysis, dimensioned 2D plans (front, side, and top
  views), an INTERACTIVE 3D MODEL you can inspect (rotate, zoom, exploded view, dimensions shown on
  click), a cut list of parts, an optimized cutting diagram, the hardware list, the tool list, the
  build and assembly steps, quality checks, a cost estimate, and safety precautions. Use this WHENEVER
  the user mentions custom furniture, a cabinet, a carcass, a bookshelf, a bookcase, a wardrobe, a
  closet, a shelf or shelving, a countertop, a desk, a table, a built-in, a workbench, woodworking,
  joinery, cabinetmaking, a cutting diagram, a cut list, wood joints, or asks for "furniture plans"
  or a "3D model" of furniture — even without using the word "woodworking".
---

# Woodworking — design, plans, and 3D model

This skill turns a furniture description into a complete, shop-ready build package and an
**interactive 3D model**. It targets a woodworker or serious DIYer who has to buy the material, cut
accurately, and assemble without surprises.

## Non-negotiable rules

Three rules anchor the whole skill. They exist because one wrong dimension or one ambiguous unit
costs a full sheet and a day of work.

1. **Everything is in millimeters (mm).** Never cm, never inches. A dimension with no unit is in mm.
2. **Never invent an important dimension.** If an overall dimension (available width, height, depth),
   a panel thickness, or a load to support is missing, ask for it. If the user still wants a draft,
   make an assumption that is **explicitly flagged** and listed in the "Dimensions to verify before
   cutting" section.
3. **Always separate available space from part dimension.** The available space is the room you have;
   the part dimension accounts for functional clearances, thicknesses, and joinery (see
   `references/joinery-calculations.md`).

## Step 0 — Gather the information

Start by filling in this brief. Fields marked 🔴 are critical: without them, do not start cutting.
If any are missing, ask for them (a tappable-options picker works well for material, finish, or joint
type; an open question for dimensions).

```
Project type          :
Use                   :
Location              :
🔴 Available width    :            mm
🔴 Available height   :            mm
🔴 Available depth    :            mm
🔴 Desired material   :
🔴 Panel thickness    :            mm
Color / finish        :
Number of doors       :
Number of drawers     :
Number of shelves     :
🔴 Load to support    :            kg (per shelf / per drawer)
Budget                :            (currency)
Tools available       :
Specific constraints  :   (toe kick, pipe, outlet, out-of-square wall, uneven floor…)
Photos / sketches     :
```

If photos or sketches are provided, analyze them: check wall plumb, obstacles (outlets, pipes, toe
kicks, radiators), the expected style, and any readable dimension. Never derive a precise dimension
from a photo without confirming it.

## Steps 1 → 14 — The deliverables

Produce the following sections **in this order**. This is the skeleton of the package; each project
fills it in. For the technical sections, rely on the reference files indicated.

### 1. Needs analysis
Restate the use, constraints, and priorities (looks / cost / strength / lead time). If several
solutions are possible (e.g. wall-hung vs. plinth-mounted carcass, overlay vs. inset fronts, ball-
bearing vs. full-extension drawer slides), present **2–3 options** with their trade-offs before
settling on one.

### 2. Overall dimensions
The chosen exterior envelope and the structural principle. State the subtraction logic here: "inside
carcass width = outside width − 2 × side thickness", etc. Refer to
`references/joinery-calculations.md` for drawer/door clearances and back-panel setback.

### 3. Concept sketch
A simple schematic (3D or line perspective) showing the general layout: number of carcasses, position
of dividers, doors, and drawers. Use the 3D model (deliverable 14) for the detailed render; keep this
schematic.

### 4. Dimensioned drawing of each part
For **every** part in the cut list, give its finished dimensions (length × width × thickness in mm),
the grain or face direction if relevant, and the machining (grooves, rabbets, hinge borings, shelf-pin
positions). See `references/plans-2d.md` for dimensioning conventions and the SVG template.

### 5. Front, side, and top views
Three dimensioned orthographic views (front, side, top), to scale, with overall and key functional
dimensions. Generate them in **SVG** from the template in `references/plans-2d.md`. Always show the
scale and carry a dual dimension chain: overall dimensions in the outer chain, detail dimensions in
the inner chain.

### 6. Cut list (bill of materials)
Summary table. Columns: Ref · Description · Qty · Length (mm) · Width (mm) · Thickness (mm) · Material
· Edge banding · Notes. This is the keystone of the package: the cutting diagram, the budget, and the
shopping list all derive from it. Detailed template in `references/plans-2d.md`.

### 7. Cutting diagram
Optimize how parts nest on standard sheets (formats in `references/materials-hardware.md`). Give: the
number of sheets needed, a nesting layout per sheet (ideally an SVG of each sheet with parts placed),
the kerf accounted for (3–4 mm by default), and the waste ratio. Respect decor/grain direction on
melamine/laminate. Method and SVG in `references/plans-2d.md`.

### 8. Hardware list
Hinges, slides, shelf pins, screws, dowels, biscuits, handles, feet, wall-fixing systems, soft-close
dampers. Exact quantities and size references (e.g. "Ø35 cup concealed hinge, 0 crank; full-extension
slide 450 mm"). See `references/materials-hardware.md` for sizing (number of hinges per door, slide
length per depth, etc.).

### 9. Tool list
List only what the project requires, noting alternatives based on the tools declared in Step 0.
Separate cutting, assembly, drilling, measuring, and finishing tools. If a machining step needs a tool
the user lacks (e.g. a router for a groove), offer a workaround (e.g. a surface-mounted screwed back
panel instead of a grooved one).

### 10. Build and assembly steps
A logical, numbered order: breaking down stock → machining → edge banding → pre-drilling → dry-fit →
glue/screw → install hardware → adjustments → on-site fixing. Call out the watch points at each step
(squareness, part orientation, clamping). A dry-fit before gluing is always recommended.

### 11. Quality checks
A verification checklist: carcass squareness (measure both diagonals, difference ≤ 2 mm), flatness,
front alignment, even gaps between doors/drawers, slide and hinge operation, stability and fixing.
State the target tolerances.

### 12. Cost estimate
A table of Material (sheets + edge banding) + Hardware + Finish + Consumables, with subtotals and a
total. Compute the material from the **number of sheets** in the cutting diagram (not theoretical
square meters), waste included. Give a range if prices are missing, and note the figures are
indicative, excluding delivery, to be confirmed with the supplier.

### 13. Safety precautions
Project-specific risks and PPE: eye protection, hearing protection, dust mask (especially MDF and
sanding), dust extraction. Power-tool rules (push stick on the saw, feed direction, workpiece
clamped). Ventilation for finishing products. Adapt to the tools actually used.

### 14. Interactive 3D model  ⭐
This is the skill's signature. Build a **standalone HTML artifact** showing the piece in 3D,
manipulable by mouse and touch, with dimensions and details. Follow `references/viewer-3d.md` in
full: it contains the complete template and how to parametrize it from the cut list. The model must
allow:
- free rotation, zoom, recenter;
- an **exploded view** (slider) to understand the assembly;
- **show/hide dimensions** for the overall envelope;
- **click a part** → highlight + show its reference and exact dimensions (W × H × D);
- a legend listing every part.

Place this deliverable right after the concept sketch if the user wants to "see" the piece first, or
at the end as a synthesis — your call based on the request.

## When to ask before producing

Before generating the full package, confirm you have the 6 🔴 fields. If any are missing, ask first —
a package built on invented dimensions is useless and dangerous at the saw. For a deliberately drafted
project, open the package with an **"Assumptions to confirm"** box listing each assumed dimension.

## Reference files

Load the file you need when you need it; don't read them all at once.

- `references/viewer-3d.md` — complete HTML/Three.js template for the interactive 3D model and how to
  parametrize it (read this for deliverable 14, every time).
- `references/plans-2d.md` — dimensioning conventions, SVG template for orthographic views, cut-list
  template, and the cutting-diagram method (deliverables 4 to 7).
- `references/materials-hardware.md` — standard panel thicknesses and sheet formats, choosing species
  and panels, and hardware sizing (hinges, slides, screws, dowels, biscuits).
- `references/joinery-calculations.md` — choosing joints by use, functional clearances, shelf
  deflection, wood movement, squareness, and cutting-optimization rules.
