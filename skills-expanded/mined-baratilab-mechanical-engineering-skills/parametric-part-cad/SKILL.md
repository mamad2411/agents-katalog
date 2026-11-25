---
name: parametric-part-cad
description: Turns a plain-English or dimensioned part description into a parametric CadQuery script and exports STEP, STL, a shaded preview image, and a mass/volume report. Use when the user asks to model, create, or generate a 3D part, bracket, flange, enclosure, fixture, or any CAD geometry, or wants a STEP/STL file.
---

# Parametric Part CAD (CadQuery)

## Setup
`pip install cadquery`. If the install fails (some platforms lack OCP wheels), fall back to `build123d`. The same structure applies.

## Workflow
1. **Spec → parameter table.** List every dimension as a named parameter, with units in mm. Fill gaps using `references/design_defaults.md` (clearance holes, wall thickness, fillets) and mark the filled values as assumptions. Ask the user only about dimensions that change function, such as interfaces and mating features.
2. **Choose the datum.** State where the origin is and which way +Z points, chosen so that functional faces sit on principal planes.
3. **Write the part script** following `scripts/example_flanged_bushing.py`:
   - a `PARAMS` dict, updated from `OVERRIDES`;
   - `assert` geometry sanity checks (minimum wall, hole-to-edge distance) with readable messages;
   - build order: base solid → bosses and ribs → holes and pockets → fillets → chamfers. Do fillets last; they fail most often;
   - end with `result = ...`;
   - set `DENSITY_KG_M3` to get a mass estimate.
4. **Build and export:**
   ```bash
   python scripts/build_part.py part.py --out out/part
   python scripts/build_part.py part.py --out out/part_v2 --set n_bolts=6 --set bore=22
   ```
   Exit code 2 means the geometry is invalid or not a single solid. Fix it before going further.
5. **Look at the preview.** View `out/part_preview.png` (isometric, top, and front) and check it against the spec. Confirm the bounding box matches the expected envelope.
6. **Deliver** the STEP (for CAD), STL (for printing), preview image, parameter table, and the `.py` file so the user can keep changing it.

## Debugging CadQuery
- A fillet fails (`BRep_API: command not done`) → reduce the radius, or select edges more narrowly (`NearestToPointSelector`, `.edges("|Z")`).
- A boolean leaves two solids → the features don't overlap. Extend one by 0.01 mm into the other.
- A hole lands on the wrong face → re-select with `.faces(">Z").workplane(centerOption="CenterOfBoundBox")`.

## Assemblies
For multi-part designs, build each part as its own function and combine them with `cq.Assembly()` and constraints. Export with `assy.save("out/assy.step")`.
