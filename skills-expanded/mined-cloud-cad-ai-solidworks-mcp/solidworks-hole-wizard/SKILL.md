---
name: "solidworks-hole-wizard"
description: "Create correct SolidWorks Hole Wizard holes (clearance, tapped blind or through, dowel H7) through the SolidWorks MCP bridge with verified HoleWizard5 parameters, callout-style names, metadata and checks. Use whenever a part has holes, threads (M6-6H etc.), dia THRU callouts or dowel/reamed holes, or the user asks for Hole Wizard, hole callouts or hole metadata, even if they only say 'add the holes'."
---

# Hole Wizard through the MCP bridge

Read `solidworks-bridge-tool-selection` first. Lengths are metres, angles radians. Verified on SOLIDWORKS 2026 by reading values back from the feature definition.

Model every functional hole (clearance, tapped, dowel, counterbore, countersink) as a Hole Wizard feature, not an extruded cut. A cut stores only a cylinder. Hole Wizard stores the thread, class, tap drill, depths and cosmetic thread, so drawing callouts, hole tables, CAM and PDM read the real intent. Plain cuts are fine for slots, pockets, lightening holes and odd profiles.

Enum values, argument arrays, thread and fit tables: [references/hole-data.md](references/hole-data.md).

## 1. Decode the callout

| Callout | Type | End |
|---|---|---|
| Ø15 THRU (bolt clearance) | Hole (2), ISO drill sizes (143), `Ø15.0` | Through All (1) |
| Ø5 ↧18 / M6-6H ↧12 | Tap (4), ISO tapped hole (147), `M6x1.0` | Blind (0) |
| Ø5 THRU / M6-6H THRU | Tap (4), 147, `M6x1.0` | Through All (1), thread through |
| Ø8 H7 THRU (dowel) | Hole (2), 143, `Ø8.0` | Through All (1), H7 as metadata |

- The Ø line with ↧ is the drill depth. The M line with ↧ is the thread depth. Drill depth ≥ thread depth. Read both from the drawing; do not assume thread depth = 2×D.
- For a clearance hole, compare the diameter with ISO 273 and state the fit (close, medium, coarse) in the feature name.
- If the size or depth is unclear, ask. Do not guess a standard size.

## 2. Procedure (per hole group)

When the ray point and the `HoleWizard5` argument array are already chosen, steps 1–4 whose coordinates are known are one `batch`. `$n` is a handle from an earlier step, including inside an `invoke` arguments JSON array. Read `GetDefinition` and the read-back properties in that same batch. The next hole group is the next batch. `set_custom_properties`, `save_as`, `set_units`, and `create_directory` stay single calls.

1. **Handles.** `active_document`, then `get_property` for `Extension` and `FeatureManager`. Re-read them after any `ActivateDoc` or error.
2. **Pick the face with a ray** at the first hole centre, aimed from outside the part: `Extension.SelectByRay(x,y,z, dx,dy,dz, 0.0005, 2, false, 0, 0)`. `SelectByID2` picks on edges and corners are unreliable.
3. **Call `HoleWizard5`** on the FeatureManager with the argument array from the reference. A non-null feature means success.
4. **Add the other centres in the position sketch.** Several ray picks on one face collapse into one location. Instead: `feature.GetFirstSubFeature()` gives the sketch. Call `Select2(false,0)`, then doc `EditSketch`. On the SketchManager, set `AddToDB = true`, call `CreatePoint(x,y,0)` for each extra centre, then set `AddToDB = false`. Finish with `InsertSketch(true)` and `EditRebuild3`. Sketch axes depend on the face; on a face parallel to Top they are x = model X and y = −model Z. If the sketch axes are already known, the `CreatePoint` calls are steps in the same batch. A live point comes first only when a coordinate depends on a point you have not read.
5. **Name the feature like the callout**, for example `M6x1.0-6H Tapped Dp12, Dia5 Dp18` or `4x Dia15 THRU - M14 Close Clearance`. When the name is already chosen, that rename is a step in the same batch.
6. **Read-back** (section 3) is steps in this batch. The next hole group is the next batch.
7. **Metadata.** `set_custom_properties` is its own call, with one key per group, for example `Holes_A1-A4 = "4x M6x1.0-6H THRU, Tap Drill Dia5.0 THRU"`. Then `save("")`.

## 3. Verify every hole group

- **Readback.** Call `feature.GetDefinition()`, then `get_property` on these:
  - Blind tap: `TapDrillDiameter`, `TapDrillDepth`, `ThreadDepth`, `CosmeticThreadType`, `ThreadEndCondition`, `DrillAngle`.
  - Through tap: `ThruTapDrillDiameter`. `TapDrillDiameter` and `ThreadDepth` read 0 for through holes, which is normal.
  - If `ThreadDepth` equals 2×D when you asked for something else, the thread-depth slot was ignored.
- **Volume** with `mass_properties`. A through hole removes π r² t. A blind drilled hole removes π r² d plus the drill-point cone (π/3) r³ / tan 59°. The centre of gravity shifts away from the side with the holes; a symmetric pattern keeps it on the axis.
- **Position by rays.** A pattern rotated 90° gives the same volume and centre of gravity, so fire `SelectByRay` (radius 0.0003) down each intended centre; it must return false because it falls through the hole. Then fire one control ray at a swapped position (x↔z); it must return true because it hits solid.
- `feature_errors` reports nothing. In an assembly, run `ForceRebuild3` and then `check_interference`.

## 4. Pitfalls

- Thread depth goes in V1, not `Length`. The wrong slot silently gives the 2×D default.
- All −1 in the V slots of a plain hole (type 2) makes `HoleWizard5` return nothing. Use the recorder-style values from the reference.
- The cosmetic thread is created only when V7 = 1 or 2. Without it the drawing shows no thread.
- `SSize` must match the standard table exactly (`M6x1.0`, `Ø15.0`; Ø is U+00D8).
- H7 and other tolerances are not applied by Hole Wizard: they need a dimension object, which the bridge cannot pass. Put the tolerance in the feature name and custom properties, and list it as an open item for the drawing. Use `solidworks-macro-fallback` only if the user agrees.
- `EditUndo2` can undo creations you did not intend, and names shift. Re-read the feature tree after every undo.
- When replacing old cut-holes, `DeleteSelection2(1)` can leave sketches and reference planes behind. Delete those named leftovers with `model` delete, then check the volume is back to the un-holed value.
- Not allowed inside a batch: `create_directory`, `set_custom_properties`, `save_as`, `set_units`.

## 5. Report to the user

- Every functional hole is a Hole Wizard feature with a callout-style name.
- Readback matches the drawing: drill diameter and depth, thread, thread depth, end condition, cosmetic thread.
- The volume and ray checks passed.
- Custom properties list the hole callouts.
- Part saved; any STEP export is redone; any assembly is rebuilt and checked for interference.
- Open items, for example "H7 tolerance to be added on the drawing".
