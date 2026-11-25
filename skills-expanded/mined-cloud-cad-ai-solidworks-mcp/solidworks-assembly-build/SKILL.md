---
name: "solidworks-assembly-build"
description: "Model parts and build SolidWorks assemblies from a design state or spec: frames, generated equations file, sub-assemblies in dependency order, static and moving mate schemes, and per-level checks. Use for any multi-part SolidWorks build, including moving mechanisms. When memory_* tools are listed and this is a new part or assembly, save it, then follow the engineering-memory skill's New project section."
---

# SolidWorks parts and assemblies: the build method

This skill is the **method** (what to build, in what order, with which mate scheme). The exact calls that work through the bridge, and the ones that fail, are in `solidworks-bridge-tool-selection`; read it first. For a whole design job, `cad-design-orchestrator` plans the agents and the shared files; this skill is what its CAD agents follow.

When `memory_*` tools are listed and this is a new part or assembly, save it, then follow the engineering-memory skill's New project section.

## 0. Gate on the inputs
- Build from a settled design state (`design_state.json` or the spec): every dimension, material and position comes from it. Never invent a size.
- If sizing inputs are still open, ask the user: placeholder layout, supply the inputs first, or skeleton only. Never present assumed sizes as a design.
- Placeholder parts carry custom properties: PartNo, Description, Material (OPEN if not given), Status = `PLACEHOLDER - NOT SIZED`, and a Note naming the input that will size them.
- If no product structure exists yet, write one first (assembly tree with sub-assemblies, make/buy, CAD source per part). Building a flat assembly of everything is the pattern to avoid.

## 1. One source of truth, projected into CAD
- The design state is the master. Generate `05_CAD/Equations/<PROJ>_GlobalVariables.txt` from it by script (one `"Name"= value` per line, in mm, derived values as expressions). Never edit the equations file by hand, or it drifts from the documents.
- Link a dimension to the file only when the dimension will not be deleted later: an equation on a deleted feature or mate is left broken and cannot be removed through the bridge.
- Do not put equations on the mates of moving parts; a driven mate dimension is locked and the part cannot move (see 5.3).

## 2. Frames
Use the frame rule recorded in the design state. The default, if none is recorded:
- unique parts (housing, cover, this product's shafts) in the **top-assembly frame**, so their mates are simple plane coincidences;
- reusable and purchased parts about **their own origin**, with the axis on a principal axis, so one file serves every instance;
- each sub-assembly with its origin at a natural datum (a shaft unit on its axis at the gear mid-plane).
Record each part's frame (which part axis is the main axis) in the README; mates depend on it.

## 3. Parts
Choose methods whose result can be predicted by hand, so a volume check can locate any error:
- **Revolved parts** (shafts, caps, spacers, simplified bearings and seals): one closed half-profile from the segment table, revolved once. Expected volume = Σ π/4·(D²−d²)·L.
- **Prismatic parts**: sketches centred on the origin, mid-plane extrudes where symmetric, so few position dimensions are needed.
- **Repeated features**: one seed feature plus a pattern; expected change = n × one instance.
- **Standard geometry** (involute tooth spaces, keyways, bolt circles, holes on a PCD): generate the sketch points or batch steps from the design state with a small script rather than placing them by hand; reuse the script across parts and jobs.
- One feature per design intent, renamed after it (`Keyway_K3`, `CoverBolts_10xM6`), so a failing feature is identifiable by name.
- `mass_properties` is a step in the part batch. Compare volume and centre of gravity in the batch result. After the part: `feature_errors` in that batch, volume within 0.5%, density from mass ÷ volume, custom properties set, `save` with a full path as a step.
- Do not put `CloseDoc` and `NewDocument` in the same batch. `CloseDoc` is the next call after you accept the batch result. `NewDocument` is its own call.
- Overlapping features (bosses running into each other, a sliver left by a cut) are a design conflict: stop and report the proposed change so the design state and documents are updated, instead of quietly resizing in CAD.
- Simplified stand-ins for purchased parts: list them with the interference they will cause, and replace them with supplier models when those arrive.

## 4. Sub-assemblies in dependency order
1. Build the **deepest sub-assemblies first**, one at a time, each saved in `05_CAD/SubAssemblies`. A sub-assembly is accepted only when all its mates are healthy and its interference count is zero or explained.
2. Inside a sub-assembly, insert the **base part** first (the shaft, the frame), unfix it if it was auto-fixed, and mate its three planes to the sub-assembly planes.
3. Add the other parts **in the order they are physically fitted** (key, gear, spacer, bearings), checking each mate's status immediately after adding it.
4. In the parent, insert the base (the housing unit) first, then each child sub-assembly, mating its datum planes or axis to the parent's interfaces, then the closing parts (caps, seals, fasteners).
5. Mate between sub-assembly **datums** rather than deep faces inside them, so a change inside a sub-assembly does not break the parent's mates.
6. Set sub-assemblies that must move (rotating shaft units, slides) to **flexible**, so their internal motion solves in the parent.
7. Insert each component near its final position; distance mates then tend to solve on the correct side.

## 5. Mate schemes
### 5.1 Static parts
Three plane mates to the parent's planes: two coincident, one distance along the main axis (value from the design state). Choose aligned or anti-aligned per plane pair so the part's axis maps correctly and the frame stays right-handed; a part that must face the other way uses anti-aligned.

### 5.2 Rotating parts (shafts, gears, rollers)
Axis coincident or concentric to the bore axis, plus one axial mate (plane coincident or distance). Leave rotation free; that is the one intended degree of freedom. Parts fixed to the shaft (gear, key, spacer, bearing inner ring) are mated to the shaft, not to the housing, so they rotate with it. Meshing gears need a gear mate to lock tooth phase and ratio; if the bridge cannot create one (it needs object arguments), set the tooth phase with an angle mate or leave it as a recorded open item, and expect tooth interference until then.

### 5.3 Linear motion (cylinders, slides, strokes)
- One **driver** (the piston, the carriage) carries the single motion degree of freedom: the off-axis mates fix it laterally, and its position along the stroke is either a **limit distance mate** (min = retracted, max = extended), which needs the macro route and the user's agreement, or a plain distance mate driven by a motion variable in the equations file (e.g. `StrokePos`, 0 = retracted).
- **Followers** (rod, rod eye, pins) chain to the driver, not to the parent's axial planes: fixed offsets from the driver (equations allowed on those, because they never change), plus the off-axis mates to the parent planes to stay on axis.
- Result: exactly one free degree of freedom, bounded.

### 5.4 Generally
- Count the free degrees of freedom of every moving part; only the intended ones should remain.
- Map mate names to their dimensions (e.g. `D1@Distance3`) before writing any equation on them; names keep counting after deletions.

## 6. Validate each level, then the parent
- **Mates:** sweep every mate's error status; component count equals the product structure for that level.
- **Interference:** coincidence excluded; subtract the expected cases from the stand-in list; bisect by suppression if pairs cannot be read; confirm causes with a section view before fixing.
- **Position:** a front/top view or a section through the shaft axes, because a distance mate can solve on the wrong side with no error.
- **Motion:** for rotating parts, confirm only rotation is free; for linear drivers, set the motion variable (or limit) to each end, rebuild, read back the position, re-check interference, then restore. Ask the user to drag the driver if a visual check is wanted. Where motion can't be checked through the bridge (e.g. no gear mate), say so.
- Read back that every suppressed or hidden component is restored before saving.
- A clean rebuild is geometry only, not engineering acceptance. Say so.

## 7. Deliver
Save all levels; export STEP and a picture of the top assembly to `08_Exports`; write the README: assembly tree, frames, how to change sizes (edit the design state, regenerate the equations file, rebuild), what moves and its limits, stand-in parts not yet replaced, macros used (if any) and which to re-run after a change, checks done and their results, and what remains unverified.