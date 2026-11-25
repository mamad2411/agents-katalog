---
name: trace-a-floor-plan
description: Turn a scanned or photographed floor plan into walls in 3D New Era AI, at real scale. Use when the user has an image or PDF of an existing plan and wants it drawn.
---

# Trace a floor plan

1. **Put the image under the plan.** `edit_background` with `action=set`, `path` (a file the user gave)
   and a scale: `calibrate={a:[x,y], b:[x,y], cm}` with two pixel points and the real
   distance between them — a dimension printed on the plan is the best reference. Two or
   more `calibrations` fit X and Y separately when the scan is stretched.
2. **Find the walls.** `background` lists them as rows `[[x1,y1],[x2,y2],t]` in plan
   cm without drawing anything. Narrow it with `region` or `threshold` when it picks up
   furniture or text.
3. **Draw them.** `edit_background` with `action=trace` and the same arguments creates them in one undo step.
4. **Compare.** `render_plan` with `bg=0.5` overlays the scan: walls off the lines show at
   once. Fix them with `move`, `update` or `edit_walls` (`action=merge`).
5. **Rooms.** `create` rooms with `at=[x,y]` inside each space; `layout` with
   `areas={"Sala": 18.5}` compares the areas with the ones printed on the plan.
