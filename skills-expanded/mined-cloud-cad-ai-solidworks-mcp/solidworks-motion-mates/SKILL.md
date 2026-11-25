---
name: "solidworks-motion-mates"
description: "Use when a SolidWorks assembly must move (cylinder extend/retract, slide, stroke) so the user can drag it within limits, instead of positioning everything with fixed distance equations."
---

# Mating a moving assembly through the MCP bridge

Use with solidworks-bridge-tool-selection (calls) and solidworks-macro-fallback (limit mate).

## Decide before mating
Ask or infer whether the user wants to drag the mechanism. If yes, do not drive moving parts with distance-mate equations: a mate dimension with an equation is locked, so the part cannot move. Equations on a mate that later needs deleting leave broken equations that cannot be removed. Plan the mate scheme first.

## Mate scheme (example: hydraulic cylinder, axis = assembly X)
- Static group (cap end, barrel, head, cap pin and bearing, valves): three plane mates each to the assembly planes, axial distance mates driven by equations from the global-variables file.
- Driver (piston): Top coincident, side plane coincident, and ONE limit distance mate from its face to the assembly Right Plane, min = retracted position, max = retracted + stroke. Create it with the .swb macro (AddMate5 type 5 with limits). No equation on it.
- Followers chain to the driver, not to the assembly axial planes:
  - rod Front Plane to piston Front Plane, distance = PistonLen (equation OK, fixed offset)
  - rod eye Right Plane to rod Front Plane, distance = RodLen + LugLen, anti-aligned (equation OK)
  - rod-end pin and bearing: Right Plane coincident to rod eye Right Plane (align closest)
  - followers keep Top / side coincident mates to the assembly planes to stay on axis
- Result: exactly one free degree of freedom (stroke), bounded by the limit mate.

## Checklist
1. After inserting components: select the first component ("Comp-1@AsmName", COMPONENT) and UnfixComponent. An auto-fixed first part made a coincident mate unsolvable (55 mm off) and caused false interference.
2. Insert components near their final positions (AddComponent5 x,y,z) so distance mates solve to the correct side.
3. After each group, capture_view top and isometric. Look for parts that solved flipped: a part rotated 180 degrees (lug pointing outward) or offset to the wrong side. Fix: FeatureByName(mate) then GetSpecificFeature2 then set_property Flipped. The user may need to flip a coincident mate's alignment in the UI if the API flip does not take.
4. Map mate names to values before writing equations: doc Parameter("D1@DistanceN") then SystemValue. Names keep counting after deletions (a deleted Distance9 leaves a gap).
5. Validate: rebuild, check_interference, read the limit mate MinimumVariation / MaximumVariation, and ask the user to drag the driver end to end.
6. Document in the README: which part to drag, the limit values, that the limits are not linked to the parameter file, and the macro to re-run after changing stroke.