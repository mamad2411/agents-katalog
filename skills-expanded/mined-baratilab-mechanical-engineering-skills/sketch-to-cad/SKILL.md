---
name: sketch-to-cad
description: Reconstructs a dimensioned parametric CAD model from a hand sketch, photo, screenshot, drawing scan, or video frames — extracts features and dimensions, infers missing ones from scale references, and records confidence for every dimension. Use when the user uploads an image or video of a part or product and wants a CAD model, reverse engineering, or a measured drawing.
---

# Sketch / Photo / Video → CAD

Pairs with `parametric-part-cad`, which builds and exports the final model.

## Workflow
1. **Ingest.**
   - Images: view each one. For video, pull frames at viewpoint changes: `ffmpeg -i in.mp4 -vf "select='gt(scene,0.25)'" -vsync vfr frames/f_%03d.png`, and keep 6–12 frames that cover the main views.
   - Classify each view: front, side, top, isometric, or oblique. Note perspective distortion. Orthographic sketches are the easiest case.
2. **Establish scale.** Use, in order of preference: a dimension written on the sketch, then a known-size object in frame (`references/scale_refs.md`), then a standard part on the object (bolt head, bearing, USB-C port), then a user-supplied overall size. If none exists, ask for one overall dimension. Don't guess absolute scale.
3. **Feature decomposition.** List features in build order: base prism or revolve → bosses and ribs → pockets and holes → patterns → fillets and chamfers. Identify symmetry and patterns explicitly (they cut the number of unknowns).
4. **Dimension table.** For every parameter, record: value, unit, source (`annotated` / `measured px→mm` / `standard part` / `assumed`), and confidence (high / medium / low).
   For pixel measurements, measure along the axis least affected by perspective, and give ±% uncertainty. Round to sensible design values: whole mm, standard hole sizes, and standard thicknesses.
5. **Build** with the `parametric-part-cad` workflow, keeping each dimension a named parameter.
6. **Verify by overlay.** Render the model from the same viewpoint as the source (CadQuery SVG with a matching `projectionDir`), then compare silhouettes side by side. List any mismatches and fix the parameters. Two iterations is usually enough.
7. **Deliver**: STEP/STL, the parameter script, the dimension table with confidence, and a "please confirm" list of the 3–5 low-confidence dimensions that matter most.

## Multi-part products
Break the product into an assembly tree first: a subassembly → part list with interfaces. Model the interfaces (mating faces, shafts, fastener patterns) at high confidence before cosmetic surfaces. For vehicles and products filmed in motion, use rotating or turntable segments for proportions and close-ups for details.
