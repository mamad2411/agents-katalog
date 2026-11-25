# CLAUDE.md

CAD workspace for creating face-annotated STEP files that feed into the AI+CAD pipeline for training graph neural networks on parametric CAD models.

## Pipeline

```
FreeCAD / CadQuery → STEP export → STEP Labeler (../steplabeler/) → Named STEP → Graph_CAD (../Graph_CAD/)
```

## Parts

Each part directory contains a build script, STEP output, part spec, and session log. **Read the build script first** when editing — it encodes the full parametric feature tree.

| Part | Faces | Key features | Spec |
|------|-------|-------------|------|
| `blkarc_slot/` | 10 | Arc top, angled slot | [`PART_SPEC.md`](blkarc_slot/PART_SPEC.md) |
| `cylinder/` | 66 | Spline teeth, bore, chamfers, channels, fillets | — |
| `crankset/` | 104 | 5-arm spider, hub boss, swept crank arm, pedal boss, JIS taper | [`PART_SPEC.md`](crankset/PART_SPEC.md) |
| `coffee_mug/` | 50 | Swept handle, full-round rim, junction fillets | [`PART_SPEC.md`](coffee_mug/PART_SPEC.md) |
| `disc/` | 36 | 5-spoke, tapered profile, conical recess | [`PART_SPEC.md`](disc/PART_SPEC.md) |
| `spoke_v2/` | 23 | 3-spoke, lenticular double-taper, hub arcs | [`PART_SPEC.md`](spoke_v2/PART_SPEC.md) |
| `showerhead_tee/` | 28 | KF10 flanges, counterbores, fillets, cross bore | [`PART_SPEC.md`](showerhead_tee/PART_SPEC.md) |
| `cross_assembly/` | 74 | **Assembly**: stepped-split clamp, cast fillets, bolt holes | [`PART_SPEC.md`](cross_assembly/PART_SPEC.md) |

Session logs (what worked, what didn't, errors resolved): [`blkarc_slot/`](blkarc_slot/SESSION_LOG.md) | [`crankset/`](crankset/SESSION_LOG.md) | [`coffee_mug/`](coffee_mug/SESSION_LOG.md) | [`disc/`](disc/SESSION_LOG.md) | [`spoke_v2/`](spoke_v2/SESSION_LOG.md) | [`showerhead_tee/`](showerhead_tee/SESSION_LOG.md) | [`cross_assembly/`](cross_assembly/SESSION_LOG.md)

## Build Script Convention

Every part gets a `build_*.py` with this structure:

```python
# Parameters
cyl_radius = 5.0

def build_geometry():
    """CadQuery boolean ops → CQ Workplane"""
    ...
def classify_faces(filepath):
    """OCC centroid + surface type → ordered label list"""
    ...
def write_labels(filepath, labels):
    """CLOSED_SHELL mapping → regex write labels into STEP"""
    ...

if __name__ == "__main__":
    result = build_geometry()
    cq.exporters.export(result, OUTPUT_PATH)
    labels = classify_faces(OUTPUT_PATH)
    write_labels(OUTPUT_PATH, labels)
```

**When editing**, modify the build script and re-run — don't rebuild from scratch or edit STEP text unless the change is coordinate-only with no topology change.

### Assembly builds

For multi-body STEP files, use `cq.Assembly`:

```python
assy = cq.Assembly()
assy.add(body_a, name="body_a")
assy.add(body_b, name="body_b")
assy.save(OUTPUT_PATH)
```

Each body gets its own CLOSED_SHELL in the STEP file. Face labeling iterates across all CLOSED_SHELLs in order. The `make_box(xmin, xmax, ymin, ymax, zmin, zmax)` helper is useful for boolean cutters — creates axis-aligned boxes from min/max coordinates via `.transformed(offset=center).box(dx, dy, dz)`.

## STEP Text Edit vs CadQuery Rebuild

- **Text edit**: topology unchanged, just moving coordinates. Trace entities by ID through `ADVANCED_FACE → PLANE → AXIS2_PLACEMENT_3D → CARTESIAN_POINT`. Edit by entity ID, not text match.
- **Rebuild**: new faces appear, faces split, or edge connectivity changes (chamfers, fillets, bores, boolean cuts).
- **Rule of thumb**: if intersection curves change, rebuild. If existing geometry just translates, text-edit.

## Face Labeling Pipeline

```python
# OCC face classification
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Torus

result = cq.importers.importStep("output.step")
for face in result.faces().vals():
    props = GProp_GProps()
    BRepGProp.SurfaceProperties_s(face.wrapped, props)
    centroid = props.CentreOfMass()
    surf = BRepAdaptor_Surface(face.wrapped)
    surface_type = surf.GetType()  # → classify by centroid + type
```

**Classification strategies**: Planar → centroid Z/X/Y or normal direction. Cylindrical → `surf.Cylinder().Radius()` + `surf.Cylinder().Axis().Direction()` for bore vs bolt hole vs body. Conical → chamfers. Toroidal → fillets. SurfaceOfRevolution → swept cross-section corner rounds. Same-type disambiguation → centroid position. Angled walls → `sin(θ)*cx + cos(θ)*cy`.

**CLOSED_SHELL** entity ordering in STEP corresponds 1:1 with `importStep().faces().vals()`. Parse CLOSED_SHELL for ADVANCED_FACE IDs, then regex-replace labels.

**In-memory classification avoids face count mismatch.** OCCT STEP export/import round-trip can split faces, causing the reimported face count to differ from the in-memory solid. Pass the CQ result object to `classify_faces(solid)` instead of reimporting from the STEP file.

**STEP naming**: `ADVANCED_FACE('feature.sub_face', ...)` — dot-separated hierarchy. Standalone faces use a single name.

## OCCT/CadQuery Gotchas

### Boolean operations
- **Cuts after all unions.** Union fills previously-cut voids. Any bore/hole through shared volumes must go after all unions.
- **Tangent surfaces hang the boolean kernel.** Offset the cut tool by ~0.5mm so it intersects rather than osculates, then clean up with a secondary cut.
- **Booleans can split faces.** Count faces after each operation to verify.
- **Z-limit annular cuts** near tapered structures. Compute `Z_taper(r)` at cut boundaries before writing code.
- **L-shaped cutters via box union.** For stepped/complex splits, build each cutter as a union of two overlapping boxes (add ~0.1mm overlap at the transition seam to avoid coincident-face failures). Test that each resulting piece is 1 solid.
- **Feature order for cast+machined parts:** fillet the raw block → cut bores → split → drill bolt holes. Filleting a simple box is reliable; cutting through filleted surfaces works fine.

### Fillets
- **Pre-union fillet** works around "BRep_API: command not done" on union seam edges — fillet the standalone solid before union.
- **Union seam fillets CAN work** on smooth geometry (e.g., surface of revolution + sweep). Always try first; don't assume failure.
- **Curved-on-curved fillet before union** produces 100+ fragment faces. Skip or accept the limitation.
- **Full rounds**: build into the revolved cross-section as quarter-circle arcs rather than using fillet API.
- **Rounded cross-section sweep** avoids fillet API for handle/bar edges entirely. Build the cross-section as a rounded rectangle (quarter-circle arcs at corners), sweep along a path wire. The swept solid unions cleanly with other bodies — no COMPOUND issue.
- **Pre-fillet + union → COMPOUND.** Filleting a solid (creating torus surfaces) before `union()` with an intersecting body can produce a COMPOUND (2 solids) instead of 1 fused solid. Bores then only cut one body. Fix: use rounded cross-section sweep instead of extrude+fillet, or fillet after union.

### OCC API
- **`edge.Center()` on circles** returns the axis center, not a circumference point. Use bounding box: `r = (bb.xmax - bb.xmin) / 2`.
- **Loft → BSplineSurface**, not Plane, even for geometrically planar results. Handle `GeomAbs_BSplineSurface` in classifiers.
- **STEP continuation lines** (leading whitespace) must be joined to parent entities before parsing.

### Workplane offset + extrude
- **XZ/YZ workplane offset direction is inverted.** `.workplane(offset=N)` on XZ goes in -Y, not +Y. Negative `extrude()` mirrors through origin rather than reversing direction. **Workaround**: build geometry on XY, then `rotate()` + `translate()` to the target position.

### Sweep/extrusion
- **Use `.sweep()` over extrusion** for features attached to curved bodies. Extrusion can silently produce a COMPOUND instead of a fused SOLID.
- **Coupled handle parameters**: verify attachment points remain outside the main arc (`distance > radius`) when adjusting geometry.

## Design Patterns

### Perpendicular bore clamping (stepped split)

When two bores have skew axes (perpendicular and offset), no single plane can split both lengthwise. Solutions:
- **Stepped split** (2 pieces): L-shaped parting surface transitions from one split plane to another. Each bore region gets the correct split. Halves interlock at diagonal quadrants. Pros: fewer pieces, shear resistance. Cons: complex parting surface.
- **Parallel splits** (3 pieces): two separate planes, each normal to the bore-connecting axis, one at each bore center. Front cap + middle body + back cap. Pros: simple flat splits, easy to machine. Cons: extra piece, no interlocking.

### Bolt clearance geometry

For bolt holes near bores, check: `distance(bolt_center, bore_axis) - bore_radius - bolt_hole_radius > ~2mm`. Wall thickness must accommodate both bore and bolt with margin. With 5mm bore radius and M5 clearance (2.75mm radius), minimum wall ~10mm.

## Interpreting CAD Instructions

Common ambiguity categories: geometric reference (which edge?), measurement datum (nearest wall vs centerline?), feature direction (blind vs through?), naming conventions (internal vs external spline?).

**Use face labels as shared vocabulary.** Reference edges as intersections of labeled faces: "edge between `bore.wall` and `top`" instead of "the top edge of the bore." Ask targeted clarifying questions using face labels.

**Sketches verify, words define.** User provides verbal dimensions referencing labeled datums. Sketch serves as cross-check after build, not as primary spec. Common sketch failures: ambiguous datum direction, implicit features, diameter/radius confusion.

## Tools

- **CadQuery** (`pip install cadquery`): programmatic CAD via Python
- **OCC** (via CadQuery): `BRepGProp`, `BRepAdaptor_Surface`, `GeomAbs_*`
- **STEP Labeler**: `cd ../steplabeler && python app.py ../AI_CAD/<part>.step`
- **FreeCAD**: native CAD for complex surface modeling

### render_step.py

Render and inspect geometry after every feature change. Section cuts catch most internal bugs (bores, tapers, pockets).

```bash
python render_step.py part.step                    # 4 views: iso, front, back, top
python render_step.py part.step --section          # + section cut at Y=0
python render_step.py --cq build_part.py --section # direct from build script
python render_step.py part.step --camera '{"section": {"normal": [1,0,0]}}'
```

Requires: `pip install pyvista cadquery` (PyVista 0.44.x + VTK 9.3.x)
