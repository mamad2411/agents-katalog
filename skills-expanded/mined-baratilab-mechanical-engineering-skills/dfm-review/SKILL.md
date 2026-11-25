---
name: dfm-review
description: Design-for-manufacturing and assembly review of a part or assembly (CAD, STEP, drawing, or description) for CNC machining, sheet metal, injection molding, casting, and 3D printing — flags rule violations, cost drivers, and process mismatches, and proposes specific geometry changes. Use when the user asks if a part is manufacturable, how to make it cheaper, which process to use, or for a DFM/DFA review.
---

# DFM / DFA Review

## Workflow
1. **Context.** Find out the process (or pick one), annual volume, material, and critical functions. If the process isn't given, recommend one with `references/process_select.md` before reviewing.
2. **Get the geometry facts.** From a STEP file, measure with CadQuery: bounding box, minimum wall (sample with ray casts or offset tests), hole diameters and depths, internal corner radii, face normals (for undercuts and draft), and the number of distinct setup directions. From a drawing or images, read them off and list what you couldn't measure.
3. **Apply the rules** for that process in `references/rules.md`. For every violation, give:
   `Feature | Rule | Measured | Limit | Impact (cost/quality/infeasible) | Fix`.
4. **Cost drivers.** Rank the top 3: setups and orientations, tight tolerances, deep pockets or small tools, secondary operations, scrap rate, tooling complexity (side actions, lifters).
5. **DFA** (for assemblies): count parts, mark each one as theoretically necessary or not (Boothroyd: does it move relative to others, does it need a different material, must it be separate for assembly or service?), and give the DFA index = 3 × N_min / total assembly time estimate. Suggest part consolidations and snap-fits in place of fasteners.
6. **Output**: verdict (manufacturable as-is / with changes / wrong process) → violations table sorted by impact → cost-driver list → redesign suggestions with before/after sketches or CadQuery edits when useful.

## Principles
- Every suggestion must keep the function. If a change trades off function, say so.
- Give numbers ("increase R0.5 to R3 so a Ø6 end mill can reach"), not general advice.
- Volume changes the answer: at 10 parts, CNC beats molding even with ugly geometry.
