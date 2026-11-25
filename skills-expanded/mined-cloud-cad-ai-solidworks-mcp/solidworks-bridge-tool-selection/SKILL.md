---
name: "solidworks-bridge-tool-selection"
description: "Use before any SolidWorks MCP modeling or assembly work to pick the tool or API call that actually works through this bridge and avoid known failures."
---

# SolidWorks bridge: which call to use

The single home for bridge facts learned from real runs (SOLIDWORKS 2026 via the remote-devices solidworks MCP). Prefer the Use column; the Avoid column failed or misbehaved. The build method (what to model, assembly order, mate schemes) is in `solidworks-assembly-build`. When a run finds a new fact, add it here rather than to another skill.

Changing an existing named dimension, suppression, delete, or material is `model`, and `model` delete only reports a leftover equation.

## What the bridge cannot do (do not retry)
- When a ref or out argument is written, invoke returns it beside the method result: `Result` plus `WrittenBack` in parameter order. In-only arguments are not echoed. A call that does not write a by-ref value keeps today's result. Read `GetEquationParameters2` that way. `OpenDoc6` writes errors and warnings into `WrittenBack`. AddMate5 and RunMacro2 were not re-checked on a live session.
- `IFeature.ModifyDefinition`, `CreateMate(data)`, `EntitiesToMate`, and gear or limit mates through the API are still out.
- Methods that return arrays (`Object[]`) can still come back as handles: transforms, sketch-segment arrays, and the interference manager's component and volume lists.
- IEquationMgr.Delete and SetEquationAndConfigurationOption return -1 and change nothing, linked or unlinked, in parts and assemblies.
- For any of these: design around it (alternatives below), or use `solidworks-macro-fallback` only if the user agrees to macros. Otherwise record it as an open item.

## Handles and lists
- `IsSame(doc, doc)` with two handles returns same (1).
- `GetPartBox` returns six numbers.
- `MultiSelect2` takes a list of plane handles (objects or live handle id strings); items are passed as `DispatchWrapper`. The wrapper was added because a live list of handles selected nothing.
- `set_property` does not create file custom properties; `set_custom_properties` does.

## Session safety
- Call `active_document` before the first batch and after any error; "RPC server unavailable" means SolidWorks has crashed or hung: ask the user to restart it, then re-read the model state.
- **A rejected, refused or timed-out call may still have executed.** Re-read the state (feature tree, mate list) before retrying, or you create duplicates.
- Pack every allowed step whose arguments you can write now. `$n` inside an invoke arguments JSON array is substituted. At most 32 steps.
- Do not put CloseDoc and NewDocument in the same steps array. That pair has crashed SolidWorks. CloseDoc is the next call after you accept the batch result. NewDocument is its own call. set_units is its own call. save_as is refused inside a batch; save takes a full path as a step. One OpenDoc per call.

## Documents
| Task | Use | Avoid / note |
|---|---|---|
| Template path | app GetUserPreferenceStringValue(8) part, (9) assembly | - |
| New doc | app NewDocument(template,0,0,0), then set_units(4) for MMGS (own call) | set_units inside a batch |
| Doc handle | Re-read with active_document after any open, activate or close | Reusing old handles; they go stale |
| Open file | app OpenDoc(path,1) part or (path,2) assembly, one call at a time | Parallel OpenDoc calls (device timeout); open_or_activate_document (failed on saved files). `OpenDoc6` writes errors and warnings into `WrittenBack`. |
| Switch doc | app ActivateDoc(title) | ActivateDoc2 (ref param) |
| Close | app CloseDoc(title) | CloseAllDocuments (refused) |
| Save | save(path) | save_as inside a batch (refused) |
| Export | save(path) with .STEP or .jpg writes a copy; doc stays native | - |

## Sketching
- Plane: create_sketch(Front) is reliable. For any other plane: Extension SelectByID2("Right Plane","PLANE",0,0,0,false,0,null,0) then SketchManager InsertSketch(true). create_sketch(Right) landed on Front.
- **Axis mapping:** on the Right Plane, sketch x = −model Z (sketch y = model Y). On a plane parallel to Top, sketch y = −model Z (sketch x = model X). Front: sketch x, y = model X, Y. Confirm on a scratch part for any other plane.
- Exit or delete a sketch: SketchManager InsertSketch(true); select "SketchN" type SKETCH then doc EditDelete.
- Circles: add_sketch_entity(circle) returns a handle that dimension accepts.
- Rectangles: add_sketch_entity(rectangle) (corner, no construction lines). Its returned handle may not dimension; get edge handles with SelectByID2("","SKETCHSEGMENT",x,y,0,...) then SelectionManager GetSelectedObject6(1,-1).
- Avoid CreateCenterRectangle: its diagonal construction lines get picked by coordinate selection, so the dimension lands on a diagonal. Check a picked segment with get_property ConstructionGeometry and invoke GetLength.
- Symmetric lug or eye: SketchManager CreateSketchSlot(0,0,width,x1,y1,0,x2,y2,0,0,0,0,1,true). Auto dims: D1 = width, D2 = centre-to-centre length. Start point stays at the origin.
- **Units:** the `dimension` tool takes DOCUMENT units (mm in MMGS) despite saying meters (0.32 gave 0.32 mm). Sketch coordinates and feature depths through `invoke` and `extrude` are meters.
- IModelDoc AddDimension2 / AddVerticalDimension2 via invoke returned nothing. Only single-entity dims via the dimension tool work, so design sketches to need no position dims: draw at exact coordinates generated from the design state, centre on the origin, place parts by mates.

**Curves and splines**
- Curve through points: `InsertCurveFileBegin()`, `InsertCurveFilePoint(x, y, z)` per point (meters), `InsertCurveFileEnd()`. Creates `CurveN`, type `CurveInFile`.
- Point lists for `CreateSpline2` are a flat array of meters, and a nested array of points is accepted because the codec flattens it. `SimulateNaturalEnds` true was the flag that created the spline in the live check.
- Equation spline: `SketchManager.CreateEquationSpline2(x, y, z, start, end, false, 0, 0, 0, false, false)`. Numbers inside the equation text are document units (mm in MMGS), not meters. The range accepts `pi`.
- 3D sketch: open and close with `doc.Insert3DSketch2(true)`, then confirm `SketchManager.ActiveSketch.Is3D` is true. `Insert3DSketch2(true)` remains the 3D-sketch call. `Insert3DSketch(true)` can leave a planar sketch and drop Z.
- Check a curve with `GetLength` (one number). `GetEquationParameters2` is read from `WrittenBack` beside the invoke result.

## Features
- Blind boss: extrude tool (depth in meters, from sketch plane along normal).
- Mid-plane boss: FeatureManager FeatureExtrusion2(true,false,false,6,0,depth,0.01,false,false,false,false,0,0,false,false,false,false,true,true,true,0,0,false).
- Through-all cut both sides: FeatureManager FeatureCut4(false,false,false,1,1,0.01,0.01,false,false,false,false,0,0,false,false,false,false,false,true,true,true,true,false,0,0,false,false).
- **Cut direction:** with FeatureCut4, Dir = false cuts opposite to the sketch-plane normal; Dir = true along it. A keyway cut the wrong way removes the wrong side or misses: check the volume change.
- Offset-start cut (e.g. a keyway that starts part-way along a shaft): FeatureCut4 with start condition T0 = 3 (offset) and the StartOffset value; describe_api it once before use.
- Revolve: one closed half-profile on a plane through the axis, with a centreline on the axis; expected volume = Σ π/4·(D²−d²)·L.
- Offset plane: select base plane, FeatureManager InsertRefPlane(8,dist,0,0,0,0). Dim name D1@PlaneN.
- Read a value: doc Parameter("D1@Sketch1") then get_property SystemValue (meters).
- Delete a feature: doc FeatureByName("Name") → Feature.Select2(false,0) → doc EditDelete.
- Feature and sketch names keep counting after a delete (Sketch2 deleted, next is Sketch3). List the feature tree before writing equations or deleting by name.
- Materials: see `set-material`; unknown names fail silently.

## Equations / global variables
- doc GetEquationMgr; set_property FilePath; set_property LinkToFile true; invoke UpdateValuesFromExternalEquationFile; then Add2(-1, "\"D1@Sketch1\" = \"Bore\"", true). Values in the file are mm.
- Dimension equations added in a part are NOT written back to the shared file.
- Equations cannot be deleted (see above), and deleting a feature or mate leaves its equation behind, broken (Status -1). Never put an equation on something you may delete. Get the dimension right first; if wrong, close without saving and rebuild the document.

## Assembly
- Parts (or sub-assemblies) must be loaded before IAssemblyDoc AddComponent5(path,0,"",false,"",x,y,z). It places the component by its **bounding-box centre**, not its origin, so position by mates.
- The first inserted component is auto-fixed off-origin. Before mating it: SelectByID2("Comp-1@AsmName","COMPONENT",...) then assembly UnfixComponent. Missing this caused an unsolvable coincident mate (55 mm off) and false interference.
- Mates: legacy assembly AddMate(type, align, flip, dist, angle) after selecting two entities with mark 1. Types: 0 coincident, 1 concentric, 5 distance, 6 angle. Align: 0 aligned, 1 anti-aligned, 2 closest.
  - Plane-to-plane distance: align 0 (aligned).
  - Axis-to-plane distance: align 2 (closest); aligned returns error 47 (ill-defined).
  - For a rotated standard part, choose aligned/anti-aligned per plane pair so the mapped frame stays right-handed.
- Plane selection names: "Front Plane@Comp-1@AsmName" type PLANE; assembly planes just "Front Plane"; inside a sub-assembly "Front Plane@Part-1@SubAsm-1@AsmName".
- A distance mate can solve to the wrong side with no error. Fix: doc FeatureByName("DistanceN") then GetSpecificFeature2 then set_property Flipped; if that doesn't clear an error, delete and recreate with the other align option. Confirm with a view or section.
- Mate dim names: D1@DistanceN, so assembly equations can drive positions.
- **Mate status:** mates don't list under the Mates folder through `list`. Walk them: doc FeatureByName("Mates") → GetFirstSubFeature → loop GetNextSubFeature, reading Name and GetErrorCode (0 = ok). Decode with get_enum swFeatureError_e (46 over-defined, 47 ill-defined). Check after every new mate. Mates inside a sub-assembly are checked in the sub-assembly document.
- Delete a mate: FeatureByName("CoincidentN") → Select2(false,0) → EditDelete.
- Suppress / unsuppress a component: select it, then EditSuppress2 / EditUnsuppress2. EditUnsuppress2 can return false without unsuppressing: read the component's suppression state back before saving. Hide/show the same way, and restore before saving.
- Gear and limit mates that need a COM object argument are still not possible directly. AddMate5's ref error status comes back in `WrittenBack`; that call was not re-checked on a live session. See `solidworks-assembly-build` 5.2 and 5.3.

## Checks
- Interference: check_interference, or doc InterferenceDetectionManager with TreatCoincidenceAsInterference = false to ignore line-to-line fits; read the count. Results are cached: call Done() and get a fresh manager before recounting. The pair list is an unreadable array, so find pairs by suppressing groups and recounting.
- Sections: `create_section_view` through the shaft axes or gear mid-plane, then `capture_view` (or save a .jpg) to inspect inside a housing.
- mass_properties (volume, CG) against a hand calculation catches a wrong dimension; mass ÷ volume catches a missing material.
- capture_view front/top/isometric after each major step; it resets zoom. Keep images few and small.