---
name: cad-build123d-general
description: 'Foundational build123d (Python CAD) patterns and OCCT gotchas that apply to ANY parametric 3D model — not specific to electronics enclosures. USE FOR: BuildPart/BuildSketch/BuildLine context managers, sketch-on-face + extrude, face selection, plane orientation, sign of extrude amounts, fusion rules, fillets/chamfers, parameterization, shallow copies, packing for 3D print plates, common FDM print-orientation rules. Load this BEFORE any enclosure / 3D-model skill.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["build123d","cad","parametric","python","occt","3d-modeling"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# Build123d General Skill

Foundational patterns for writing build123d Python scripts. This is the
**source of truth** for build123d API idioms and OCCT (OpenCascade) behaviour
that other skills build on top of.

If you are about to write or edit any `.py` file that imports `build123d`,
load this skill first.

---

## 1. Builder Idioms

### BuildPart / BuildSketch / BuildLine
Use the context-manager (builder) form. It auto-fuses additions and tracks the
current workplane.

```python
from build123d import *

with BuildPart() as part:
    with BuildSketch():
        Rectangle(40, 30)
    extrude(amount=10)
```

### Workplanes do **not** inherit when nested
A nested `BuildSketch` or `BuildPart` does **not** pick up the parent's workplane.
It always starts on `Plane.XY` unless you pass one explicitly:

```python
with BuildPart() as p:
    with BuildSketch(Plane.XZ):   # must specify; not inherited
        Rectangle(10, 5)
    extrude(amount=2)
```

### `Mode.SUBTRACT`, `Mode.ADD` (default), `Mode.INTERSECT`
Pass `mode=Mode.SUBTRACT` to cut a feature from the active part. Common for
holes, debossed text, and slots.

```python
with BuildPart(mode=Mode.SUBTRACT):
    Cylinder(radius=2, height=20)
```

---

## 2. The Cardinal Rule: 2D before 3D

Build complex shapes in 2D (`BuildSketch`) first, then promote to 3D with
`extrude()` or `revolve()`. 2D operations are faster, more reliable, and
2D fillets/chamfers rarely fail where 3D ones do.

```python
with BuildPart() as bracket:
    with BuildSketch() as profile:
        Rectangle(50, 30)
        Circle(8, mode=Mode.SUBTRACT)
        fillet(profile.vertices(), radius=3)   # 2D fillet — safe
    extrude(amount=5)
```

---

## 3. Delay Chamfers and Fillets

Apply 3D `chamfer()` and `fillet()` operations **last**. They turn flat edges
into curved/angled faces, multiplying topology complexity. Doing them early
makes every later boolean and selector slower and more failure-prone.

---

## 4. Sketch-on-Face + Extrude (the only safe way to add material)

**Never place a free-floating `Box()` or `Cylinder()` at computed absolute
coordinates and expect OCCT to fuse it to an existing part.** The kernel does
not reliably fuse solids that merely *touch* a face without overlapping.
The result is a disconnected body that the slicer treats as floating geometry.

### Correct pattern
```python
with BuildPart() as part:
    Box(40, 30, 5)

# Add a boss to the top
top = part.faces().sort_by(Axis.Z)[-1]
with BuildPart() as part:                     # re-enter the same builder
    with BuildSketch(top):
        Circle(3)
    extrude(amount=4)                         # follows face normal (+Z here)
```

### Sign of `extrude(amount=...)` follows the face normal
- Positive amount → grows along the face's outward normal
- Negative amount → grows opposite to the normal (often *into* the parent body, where it gets absorbed)

| Face | Normal | `extrude(amount=+h)` grows… |
|------|--------|----------------------------|
| Top of base (`sort_by(Axis.Z)[-1]`) | +Z | upward (good for standoffs) |
| Bottom of base (`sort_by(Axis.Z)[0]`) | -Z | downward (out of part) |
| Lid underside (`sort_by(Axis.Z)[0]` of a lid sitting at +Z) | -Z | **downward, into the compartment** |

A common bug: writing `extrude(amount=-RIDGE_H)` on the lid underside. This
goes *against* the normal — back up into the lid body — so the ridge is
absorbed and disappears.

### Inverse rule: free-floating SUBTRACTIONS are safe
The "never free-floating" rule applies to **adding** material. For
**subtracting**, a free-floating `Box(..., mode=Mode.SUBTRACT)` placed in
world coordinates is perfectly safe and is often the *better* choice for
through-wall cuts (notches, finger pulls, vents):

- The cutter only has to overlap the wall it removes — oversize it
  generously (e.g. `WALL * 3` along the cut axis) so corner rounding or
  small numerical errors can't leave a sliver.
- World coordinates avoid the local-frame Y-flip that bites you when
  sketching on -Y / -Z normal faces (see section 5). This is the cleanest
  way to cut symmetric features through opposing walls (e.g. a notch on
  each end) without the second one ending up mirrored.

```python
# Cut a centered notch from the rim of the +X short wall.
notch_z_center = OUTER_H - NOTCH_D / 2
with Locations((OUTER_L / 2, 0, notch_z_center)):
    Box(WALL * 3, NOTCH_W, NOTCH_D, mode=Mode.SUBTRACT)
```

---

## 5. Face Selection Hazards

### Stale face references after geometry changes
After you extrude a protrusion from a face, `faces().sort_by(Axis.Z)[-1]` may
now select the **tip of that protrusion**, not the original surface. Any
subsequent feature sketched on the stale reference will float.

```python
top = part.faces().sort_by(Axis.Z)[-1]   # original top
# ... add a tall boss here ...
top2 = part.faces().sort_by(Axis.Z)[-1]  # WRONG: this is now the boss top
```

### Fix: sketch on a known plane offset, not on a face selector
```python
ORIG_TOP_Z = 5.0
with BuildSketch(Plane.XY.offset(ORIG_TOP_Z)):
    Circle(2)
extrude(amount=-3)        # downward from a +Z-normal plane
```
Using `Plane.XY.offset(z)` also avoids the next two hazards.

### Y-axis flips on downward-facing faces
When you sketch on a face whose normal points `-Z` (e.g. a lid's underside),
the local sketch frame flips: **sketch +Y = global -Y**. Off-centre features
end up mirrored unless you negate Y in `Locations(...)`.

```python
# On a lid underside (face normal = -Z):
with Locations((x, -global_y)):    # negate Y to land on the right side
    Circle(2)
```

Symmetric features (Y = 0) are unaffected, which is why this bug often hides
until you add the first asymmetric feature.

### Object Selection — go via topology
When picking edges to chamfer/fillet, select the parent face first, then the
edges from that face. This is more robust than filtering all edges of the
part.

```python
top_face = plate.faces().sort_by(Axis.Z)[-1]
hole_edges = top_face.edges().filter_by(GeomType.CIRCLE)
chamfer(hole_edges, length=1)
```

---

## 6. BuildSketch Plane Gotchas

### `BuildSketch(Plane.XZ)` does NOT draw on Plane.XZ
All sketches are drawn on a **local** `Plane.XY` and then rotated/placed onto
the workplane you provided. This means:

- `sort_by(Axis.Z)` inside a `BuildSketch(Plane.XZ)` is sorting points whose
  Z = 0 (because the sketch is local) — results are random.
- Use `sort_by(Axis.Y)` (the local "up" of the sketch) instead.

### `BuildLine` inside `BuildSketch` must use the default plane
```python
with BuildSketch() as s:
    with BuildLine():            # default Plane.XY — correct
        Polyline(...)
    make_face()
```

If you write `BuildLine(Plane.XZ)` inside a `BuildSketch`, the resulting face
gets reoriented back to `Plane.XY` — almost never what you wanted.

### Rotating a sketch plane to orient text / asymmetric features
Use `Plane.XY.offset(z).rotated((0, 0, deg))` when you need text or other
directional features to read from a specific side of the part. Convention:
**letter tops point along the world axis where the local sketch +Y axis
lands after rotation**.

| Rotation about Z | Sketch +Y maps to | Reads from… |
|------------------|-------------------|-------------|
| `0`              | world +Y          | the +Y side |
| `+90`            | world +X          | the +X side |
| `-90` (or `270`) | world -X          | the -X side |
| `180`            | world -Y          | the -Y side |

If the first try comes out wrong, **flip the sign** — don't try to reason
about clockwise-from-above vs counter-clockwise-from-below.

---

## 7. Parameterize Everything

Make every dimension a named module-level constant. Derive related dimensions
arithmetically. Future change requests become one-line edits.

```python
WALL = 2.5
PCB_W, PCB_L = 60.0, 80.0
INNER_W = PCB_W + 4.0
INNER_L = PCB_L + 4.0
OUTER_W = INNER_W + 2 * WALL
OUTER_L = INNER_L + 2 * WALL
```

Bonus: parameterised scripts double as a family of variants (small / medium / large).

---

## 8. Use Shallow Copies for Repeated Parts

For fasteners, standoffs, and other repeated geometry, build once and shallow-copy.
This dramatically reduces memory and viewer/export time. Keep in mind: editing
one shallow copy affects all of them.

---

## 8a. Design / Test / Production Export Workflow

Every parametric model that produces printable STLs should expose a single
`EXPORT_MODE` constant and a `User Orientation Map` so on-screen review,
test fits, and final prints all share the same source.

**`"design"` is the default for any new script, from its very first run.**
Not after the shape settles, not once it is "worth" the scaffolding — the
first version. Early models are built from assumptions and reviewed by
someone who has never seen them, which is precisely when unlabelled axes
cause misreads. If a user ever has to ask for design mode, it was added
too late.

### The three modes

| Mode | Axis reference block? | On-part axis labels? | Use it for |
|------|-----------------------|----------------------|------------|
| `"design"`     | **Yes** — exported alongside each part | No | Inspecting in CAD viewer / slicer to confirm orientation |
| `"test"`       | No | **Yes** — debossed on walls/floor | Test prints; the on-part labels survive into your hand so you can talk about "the +X side" with the printed object in front of you |
| `"production"` | No | No | Final prints (clean appearance) |

All three modes always export every STL — never gate exports on mode, or
you'll end up with stale files on disk that don't match the current code.

### The User Orientation Map

Axis labels (`+X`, `-X`) are precise but users say "front", "left", "up".
Bake the mapping in once, at the top of the script:

```python
EXPORT_MODE = "design"   # "design" | "test" | "production"

ORIENTATION = {
    "front":  "-X",
    "back":   "+X",
    "left":   "-Y",
    "right":  "+Y",
    "top":    "+Z",
    "bottom": "-Z",
}
```

When the user later says "move it toward the front 15 mm", look up
`ORIENTATION["front"]` → `-X` → subtract 15 from X. Never guess. If no
map exists yet and the user uses directional language, **ask** before
guessing.

### Axis reference block (design mode)

A small labeled cube exported next to each part. It shows the axis on the
top of each face, the friendly direction below it, and "BED" on the face
that goes on the build plate. This makes orientation obvious in the slicer
and makes mistakes (a part you forgot to flip) immediately visible.

```python
def make_axis_reference_block(size=15, label_depth=0.5,
                              font_size=6, dir_font_size=3.5,
                              bed_face=None, bed_font_size=4):
    dir_labels = {v: k.capitalize() for k, v in ORIENTATION.items()}
    with BuildPart() as ref:
        Box(size, size, size)
        for axis, signs in [(Axis.X, ("+X", "-X")),
                            (Axis.Y, ("+Y", "-Y")),
                            (Axis.Z, ("+Z", "-Z"))]:
            for idx, label in enumerate(signs):
                face = ref.faces().sort_by(axis)[-1 if idx == 0 else 0]
                with BuildSketch(face):
                    with Locations((0, size / 2 - font_size * 0.7)):
                        Text(label, font_size=font_size,
                             align=(Align.CENTER, Align.CENTER))
                extrude(amount=-label_depth, mode=Mode.SUBTRACT)
                if label in dir_labels:
                    with BuildSketch(face):
                        with Locations((0, -size / 2 + dir_font_size * 1.2)):
                            Text(dir_labels[label], font_size=dir_font_size,
                                 align=(Align.CENTER, Align.CENTER))
                    extrude(amount=-label_depth, mode=Mode.SUBTRACT)
                if bed_face and label == bed_face:
                    with BuildSketch(face):
                        Text("BED", font_size=bed_font_size,
                             font_style=FontStyle.BOLD,
                             align=(Align.CENTER, Align.CENTER))
                    extrude(amount=-label_depth, mode=Mode.SUBTRACT)
    return ref.part


def export_with_reference(part, filename,
                          offset_x=0, offset_y=0, offset_z=0,
                          bed_face=None):
    """Export STL. In 'design' mode, includes axis ref block beside the part."""
    if EXPORT_MODE == "design":
        ref_block = make_axis_reference_block(bed_face=bed_face)
        ref_block = ref_block.move(Location((offset_x, offset_y, offset_z)))
        combined = Compound(children=[part, ref_block])
        export_stl(combined, filename)
    else:
        export_stl(part, filename)
```

### On-part axis labels (test mode)

In test mode, deboss small axis + friendly-direction labels directly onto
the outer vertical walls of the part. These survive into the physical
print so you can identify each face with the object in your hand ("this
is +X / Front"). Labels are positioned near the base of each wall to
avoid collisions with functional features (notches, name text, etc.).

Each label has two lines: the axis code (e.g. `+X`) above and the
friendly name (e.g. `Front`) below, both centered on the wall.

**Plane construction for wall labels:** for each vertical wall, the plane
needs `z_dir` = outward normal and `x_dir` chosen so the cross product
`z_dir × x_dir` = world `+Z` (letters upright). The table:

| Wall | `z_dir`    | `x_dir`     | Viewer sees text L→R along… |
|------|-----------|-------------|----------------------------|
| `+X` | `(1,0,0)` | `(0,1,0)`  | world +Y |
| `-X` | `(-1,0,0)` | `(0,-1,0)` | world -Y |
| `+Y` | `(0,1,0)` | `(-1,0,0)` | world -X |
| `-Y` | `(0,-1,0)` | `(1,0,0)`  | world +X |

```python
if EXPORT_MODE == "test":
    _TL_FONT  = 5.0   # cap height (mm)
    _TL_DEPTH = 0.5   # recess into wall (mm)
    _TL_Z     = _TL_FONT * 2  # label center Z — near bottom of wall
    _test_walls = {
        "+X": Plane(origin=( OUTER_L/2, 0, _TL_Z),
                    x_dir=(0,  1, 0), z_dir=( 1, 0, 0)),
        "-X": Plane(origin=(-OUTER_L/2, 0, _TL_Z),
                    x_dir=(0, -1, 0), z_dir=(-1, 0, 0)),
        "+Y": Plane(origin=(0,  OUTER_W/2, _TL_Z),
                    x_dir=(-1, 0, 0), z_dir=(0,  1, 0)),
        "-Y": Plane(origin=(0, -OUTER_W/2, _TL_Z),
                    x_dir=( 1, 0, 0), z_dir=(0, -1, 0)),
    }
    _dir_labels = {v: k.capitalize() for k, v in ORIENTATION.items()}
    _spacing = _TL_FONT * 1.2
    for _axis_label, _plane in _test_walls.items():
        _friendly = _dir_labels.get(_axis_label, "")
        with BuildSketch(_plane):
            with Locations((0, _spacing / 2)):
                Text(_axis_label, font_size=_TL_FONT,
                     font="Arial",
                     align=(Align.CENTER, Align.CENTER))
            with Locations((0, -_spacing / 2)):
                Text(_friendly, font_size=_TL_FONT * 0.7,
                     font="Arial",
                     align=(Align.CENTER, Align.CENTER))
        extrude(amount=-_TL_DEPTH, mode=Mode.SUBTRACT)
```

Place this block inside the `BuildPart` context, after all functional
features, gated on `EXPORT_MODE == "test"`. The labels are shallow
(0.5 mm) and small (5 mm) so they don't interfere with fit testing.

### Print orientation summary (every script)

Print which face goes on the build plate for every exported part. This is
the single most important piece of information for the operator — and it's
easy to forget when there are several STLs.

```python
print("\n  Print Orientation (bed_face = face on build plate):")
print(f"    {NAME}.stl  — BED: -Z (right-side up, open top faces up)")
```

### Production-only: per-STL print-settings sidecar (`*.print.md`)

When `EXPORT_MODE == "production"` **and only then**, also emit a
`<stl_name>.print.md` sidecar next to each STL. This is the file you'd
hand to whoever is slicing the part — including yourself in six months,
or a stranger downloading the model. It must be self-contained: someone
who has never read the source script should be able to slice it.

Required sections:

1. **Part name + STL filename + dimensions** (X × Y × Z mm) and
   approximate volume in cm³.
2. **Bed face / orientation** — which face goes on the build plate, in
   the script's friendly direction terms (e.g. `-Z (Bottom)`).
3. **Material** — recommended filament(s); call out whether food-contact,
   outdoor UV, or flex matters for this part.
4. **Recommended slicer settings** — layer height, walls, top/bottom
   layers, infill % + pattern, supports yes/no with rationale.
5. **Estimated print time** as a range. Be honest that it depends on
   printer.
6. **Notes** — anything orientation-specific (e.g. "the debossed text on
   the bed face prints cleanly without supports because it faces down")
   or post-processing (e.g. "tap the M3 hole after printing").

Generate the sidecar from the same script that exports the STL — don't
maintain it by hand. A minimal helper:

```python
def export_print_settings(stl_path, *, part_name, bed_face_label,
                          bbox, volume_cm3, material, settings, notes):
    """Write <stl_path>.print.md describing how to slice this STL.
    Production mode only — caller should gate on EXPORT_MODE."""
    md_path = stl_path.with_suffix(".print.md")
    lines = [
        f"# {part_name} — print settings",
        "",
        f"- **STL:** `{stl_path.name}`",
        f"- **Dimensions:** {bbox[0]:.2f} × {bbox[1]:.2f} × {bbox[2]:.2f} mm",
        f"- **Volume:** {volume_cm3:.2f} cm³",
        f"- **Bed face:** {bed_face_label}",
        "",
        "## Material",
        f"{material}",
        "",
        "## Recommended slicer settings",
    ]
    for k, v in settings.items():
        lines.append(f"- **{k}:** {v}")
    lines += ["", "## Notes", notes, ""]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Sidecar:  {md_path}")
```

Sidecar files are share-safe by design — no source code, no internal
ADRs, no axis ref cubes, just slicing instructions. They live next to
the STL in `exports/`.

**Why production-only:** during design and test iterations the slicer
settings are not yet locked in (you might change wall thickness or layer
height between test prints). Generating a sidecar before that is
premature and creates files that go stale instantly.

### When to use it

- **Always** for any new printable part — even a one-off. Adding the
  scaffolding takes 30 seconds and saves you the "wait, which way does
  this go?" round-trip on the first print.
- **Single-part projects** still benefit: the axis ref block in design
  mode makes the YouTube-screenshot view of your model self-documenting.
- For enclosure-specific extensions (on-part wall labels, lid edge
  labels, dual-label patterns, the `bed_face` table for standard
  enclosure parts), the `electronics-enclosure-3dprint` skill *(separate
  plugin)* covers it if you have that installed.

---

## 9. Self-Intersection

Avoid creating shapes that touch themselves — even at a single vertex. OCCT
will often report `is_valid() == True` while still producing broken booleans
downstream. Helices (threads) are the classic case: split into ≤180° segments
and combine via assembly if needed.

---

## 9a. Self-Verifying Models: Assert the Invariant

OCCT fails **silently and plausibly**. A destroyed body still exports as a
watertight STL. A cut that missed still renders. A bend that went the wrong
way looks fine from three of four angles. The only reliable defence is to
assert what must be true after every risky operation.

### Assert the invariant, not a percentage

The most common way a guard rots is encoding *the current geometry* instead
of *the rule*. Both of these were written and both broke within one session:

```python
# BAD — breaks when an unrelated parameter changes the part's mass
if not (0.05 * total < removed < 0.60 * total):

# GOOD — the cut must remove exactly what the tool overlaps
expected = part.intersect(cutter).volume
part = part - cutter
assert abs((before - part.volume) - expected) < max(0.5, 0.02 * expected)
```

```python
# BAD — "a fold preserves volume to 2%" is false for a hairpin, which
#       doubles the flap against the parent and unions the overlap away
if not (-1e-6 <= lost <= 0.02 * flap_vol):

# GOOD — holds at any fold angle
if not (-1e-6 <= lost <= flap_vol):   # can't lose more than the flap,
                                      # and a fold never adds material
```

A tolerance you have to re-tune whenever the design changes was measuring
the wrong thing.

### Verify direction, never trust a rotation sign

Whether `rotate(Axis.Y, +15)` moves a feature toward +X or −X depends on
which side of the hinge the material lies. A flap rising from its hinge and
a flap hanging below it rotate in **opposite** apparent directions for the
same sign. Both look believable when rendered.

```python
folded = flap.rotate(Axis((0, y, hinge_z), (0, 1, 0)), angle)
if folded.bounding_box().min.X > -SHEET_T:
    raise RuntimeError("bend went the wrong way; invert the angle")
```

### Guards worth writing every time

| After | Assert |
|---|---|
| Any boolean | `part.volume > 0` and the change matches the tool's overlap |
| Fusing a thread/`IsoThread` | host volume survived (skill Bug 4 family) |
| A cut that should open a bore | section area at mid-depth sits between "solid" and "no-feature" |
| Splitting a solid into regions | the pieces' volumes sum to the whole |
| Placing a feature on a face | the fused volume grew by *less* than the feature's own volume (otherwise it landed in mid-air) |
| Anything mating | `a.intersect(b)` volume is zero |

### Degenerate geometry that OCCT rejects or mishandles

- **Coincident consecutive `Polyline` points** → zero-length edge →
  `StdFail_NotDone: BRep_API: command not done`. Happens the moment a
  parameter makes two corners collide (e.g. a flap flush with an edge).
  Filter duplicates when generating outlines from constants:

  ```python
  out = [pts[0]]
  for p in pts[1:]:
      if abs(p[0]-out[-1][0]) > tol or abs(p[1]-out[-1][1]) > tol:
          out.append(p)
  ```

- **A solid that fully engulfs a thin host** destroys it. A Ø0.90 sphere
  cannot sit on a 0.24 mm sheet and protrude 0.18 mm — it swallows the
  sheet, and the fuse returns volume 0. Model surface bumps as shallow
  bosses or true spherical caps sized against the wall thickness.

- **`Shape.intersect()` may return a `ShapeList`**, not a `Shape`, when the
  parts foul in more than one place. Code that assumes a single result
  crashes exactly when the answer is most interesting:

  ```python
  ov = a.intersect(b)
  vol = 0.0 if ov is None else (
      ov.volume if hasattr(ov, "volume") else sum(s.volume for s in ov))
  ```

### Don't derive a user-supplied value from an assumed constraint

If someone gives you a dimension, don't recompute it from a rule you
invented. Deriving `fold_length = finger_height - straight_run` silently
overrode a measured fold length because the "post + fold must equal the
finger" constraint was an assumption, not physics. Derive only when the
constraint is genuinely necessary — and then make it raise, so a conflict
surfaces instead of resolving itself wrongly.

### Clearance belongs only where something protrudes

Adding clearance symmetrically is a reflex worth resisting. A pocket for a
feature that protrudes on one face only should stop flush on the other; the
stray gap becomes a notch across a structural wall.

---

## 10. Packing Multiple Parts on a Plate (3D printing)

`pack.pack(shapes, padding=...)` translates a list of `Shape`s so they no
longer overlap — handy for laying out a print plate. Pass `align_z=True` to
land everything on Z = 0 so the slicer doesn't have to.

```python
from build123d import pack
laid_out = pack.pack([base, lid, button], padding=5, align_z=True)
```

---

## 11. FDM 3D Printing Is Additive (Bottom-Up)

Every layer must be supported by the build plate or a previously printed
layer. When designing features:

- **Print-right-side-up parts** (e.g. an enclosure base) — standoffs, ridges,
  walls grow upward from the floor.
- **Print-face-down parts** (e.g. a lid) — features on the underside actually
  print *upward* during fabrication, so they're well-supported.
- **Overhangs > ~45°** without support will sag, droop, or print as spaghetti.
- **A horizontal surface with open air below it** is an unsupported overhang.

If a feature would print over open air in its intended orientation, redesign
it (add a chamfer/ramp) or change the print orientation.

### Measure overhangs, don't eyeball them

"It'll print without supports" is a claim, and it's cheap to check. Load the
exported STL and classify downward-facing faces:

```python
import numpy as np, trimesh
m = trimesh.load("part.stl")
n, a, cen = m.face_normals, m.area_faces, m.triangles_center
ang = np.degrees(np.arcsin(np.clip(-n[:, 2], 0, 1)))   # 0=wall, 90=flat ceiling
bed = cen[:, 2] < 0.05                                  # build-plate contact
over = (n[:, 2] < 0) & (ang >= 45) & (~bed)
print(f"{a[over].sum():.1f} mm2 unsupported ({100*a[over].sum()/a.sum():.1f}%)")
```

Two traps in reading the result:

1. **Exclude the bed contact face**, or a flat-bottomed part looks like it's
   almost entirely overhang.
2. **A bridge spans the SHORT way across a flat patch.** Reporting the patch's
   longest dimension overstates the difficulty — a 12 mm long, 1 mm wide
   ceiling ridge bridges 1 mm, not 12.

**Overhang area is not the whole story: ask what the surface does.** A large
overhang on a deliberate clearance relief costs nothing — nothing touches it
and roughness is irrelevant. A small one on a threaded bore or a mating face
costs function. Weigh area *and* purpose.

### Sloped walls are not bridges

A chamfer rising off the build plate is printable well past 45°, because each
layer sits partly on the one below rather than spanning air. Compute the
step-in to judge it:

```
step_in_per_layer = (run / rise) * layer_height
supported_fraction = (extrusion_width - step_in) / extrusion_width
```

A 27° chamfer at 0.12 mm layers leaves ~45% of each bead supported — rough
but sound. At 0.20 mm it collapses to ~8%. **Layer height, not just angle,
decides whether a shallow slope survives.**

### Compare orientations numerically before committing

Printability and *quality* are different questions, and the easy orientation
is often the worst one for the feature that matters. Score each candidate on
overhang area, worst bridge span, bed contact, **and the angle between any
critical axis (a threaded bore, a load-bearing wall) and Z**. Threads want
their axis vertical; cantilevers want layer lines out of their bending
plane; those two frequently disagree, and the trade should be made against
which one actually fails in service.

### Embossed vs debossed text (and other raised features) — pick debossed by default

This is the single most common avoidable-overhang mistake. Embossed text
(letters that stand *proud* of a surface) prints fine when the surface
they sit on is **horizontal and on the build plate** (e.g. text on a lid
that prints face-down). On any **vertical or sloped surface**, every
letter edge becomes a 90° unsupported overhang and looks ugly to
unprintable on FDM.

| Feature on this surface | Embossed (raised) | Debossed (recessed) |
|--|--|--|
| Top face that lies flat on build plate | ✅ great — prints clean | ✅ fine |
| Bottom face that prints face-down (e.g. underside of a lid) | ✅ great | ✅ fine |
| Vertical wall (sides of a box, enclosures) | ❌ 90° overhang per letter | ✅ recommended |
| Sloped face (>~45° from horizontal) | ❌ overhang | ✅ recommended |
| Inside floor of an open-top tray (faces +Z) | ✅ fine | ✅ fine |

**Rule for the agent:**
**Before adding any embossed (raised) feature \u2014 text, logo, ridge, raised
bezel, etc. \u2014 to a non-horizontal-build-plate face, pause and ask the
user:**

> "This will be embossed on a vertical/sloped wall, which prints as a
> 90° overhang on every edge. Switch to *debossed* (recessed) instead?
> Same look, no overhangs."

Only proceed with embossed if the user explicitly confirms and either:

1. The face will be horizontal during printing (orient the part so the
   embossed face goes face-down or face-up on the bed), or
2. They've planned for support material, or
3. The emboss height is small enough (≲ 0.4 mm) and they accept that it
   will look rough.

In code, the difference is usually a single sign flip and `mode=`:

```python
# Embossed (raised, +amount along face normal)
extrude(amount=NAME_TEXT_DEPTH)

# Debossed (recessed, -amount = into the body, with SUBTRACT)
extrude(amount=-NAME_TEXT_DEPTH, mode=Mode.SUBTRACT)
```

### Cantilevers, tabs, and bosses — add a 45° gusset by default

Any **horizontal tab, boss, or shelf that projects from a vertical wall**
has a 90° overhang on its underside. Slicers will either gap-fill it
poorly or demand tall, wasteful supports that are hard to remove cleanly
from an interior cavity (rod tabs in a bay, mounting ears inside an
enclosure, internal shelves, etc.).

**Default behavior: add a 45° triangular gusset under every cantilever
feature unless the user opts out.** Don't ask for permission for the
first version — build it in. Mention it in the rebuild summary so the
user can say "remove the gussets, I'll print with supports" if they
prefer the cleaner aesthetic.

Geometry rule of thumb (matches FDM's ~45° self-supporting limit):

- **Projection** = how far the cantilever sticks out from its anchor wall
- **Gusset height** = projection (so the hypotenuse is exactly 45°)
- **Gusset depth** = same as the cantilever depth (full support across the tab)
- **Top edge of gusset** = flush with the *underside* of the cantilever
- **Vertical edge of gusset** = flush against the anchor wall

Build it as a right-triangle prism. The cleanest pattern is
`Polyline` + `make_face` on the wall-perpendicular plane, then
`extrude(..., both=True)`:

```python
# Triangle in the X–Z plane: vertical leg on the wall, horizontal leg
# on the cantilever underside, hypotenuse is the printable 45° ramp.
GUSSET_PROJ = TAB_W - WALL_BITE          # how far tab sticks into the bay
GUSSET_H = GUSSET_PROJ                    # equal legs → 45°
tab_bottom_z = TAB_Z - TAB_H / 2
tip_x = wall_x + tip_dir * GUSSET_PROJ    # tip_dir = +1 for left wall, -1 for right
tri = [
    (wall_x, tab_bottom_z - GUSSET_H),    # bottom corner on the wall
    (wall_x, tab_bottom_z),                # top corner on the wall (under tab)
    (tip_x,  tab_bottom_z),                # tip at tab edge
    (wall_x, tab_bottom_z - GUSSET_H),    # close polygon
]
with BuildSketch(Plane.XZ.offset(-tab_y)) as gusset_sketch:
    with BuildLine():
        Polyline(tri)
    make_face()
extrude(gusset_sketch.sketch, amount=TAB_D / 2, both=True, mode=Mode.ADD)
```

When NOT to auto-add a gusset:

- The cantilever is < ~3 mm of projection (most slicers bridge that fine).
- The cantilever lies **face-down** in the chosen print orientation
  (its "underside" is on the build plate — nothing to support).
- The user has explicitly said this part will print with supports.

A half-round fillet/chamfer instead of a triangle works too
(`chamfer(edges, length=GUSSET_PROJ)` on the inside corner) but the
triangular prism is more predictable across OCCT versions and easier
to register in the FeatureRegistry.

```

### Snap-fits, lips, and press-fit interferences (material-specific)

Snap-fit interference (the amount the catching feature is wider than
the receiving feature) does NOT have a universal "good" value — it
depends on the material's elastic strain to failure and on the
**radial wall thickness of the flexing element**. The lessons:

| Material | Max snap interference | Min flexing wall | Notes |
|---|---|---|---|
| **PLA / PLA+** | 0.4 mm | 0.6 mm | Forgiving; original ranges hold |
| **PETG** | **0.2 mm** | **0.7 mm** | Notch-sensitive in thin sections; **half** the PLA interference |
| **ABS / ASA** | 0.2 mm | 0.7 mm | Same as PETG; less ductile in thin features |
| **TPU 95A** | 0.6+ mm | 0.4 mm | Stretchy; can take huge interference |
| **Nylon (PA12)** | 0.3 mm | 0.5 mm | Tough; the "ideal" snap-fit material |

> **PETG snap-fit failure rule:** if you have a thin radial ring
> (lip) flexing outward to capture a head, **multiply the PLA
> interference value by 0.5 AND multiply the wall thickness by
> 1.4** when switching from PLA to PETG. A snap that worked in PLA
> at 0.4 mm interference + 0.5 mm lip wall will *crack* in PETG;
> the equivalent PETG geometry is 0.2 mm interference + 0.7 mm lip
> wall.

**Always chamfer BOTH sides of the snap.** If the catching head has
a chamfer only on the entry side, the user can snap it on but
**cannot remove it** without yielding (or cracking) the receiving
feature. Add a symmetric chamfer on the underside so the snap is
bidirectional. Capture force is unchanged; recovery from
misassembly is now possible.

**Geometry checklist for a PETG cylindrical snap:**

1. ☐ Interference (head OD − lip ID) ≤ 0.2 mm
2. ☐ Lip radial wall (chamber bore − lip bore) / 2 ≥ 0.7 mm
3. ☐ Head TOP chamfer ≥ 0.5 mm (entry ramp)
4. ☐ Head BOTTOM chamfer ≥ 0.4 mm (removal ramp)
5. ☐ Lip mouth chamfer ≥ 0.3 mm (helps head find the lip)
6. ☐ Print orientation places the lip's flexing direction
   perpendicular to the layer lines (so the lip flexes through
   bulk material, not pulling layers apart)

Codified after the headphone-hook desk-clamp project's first
PETG print failed at the snap-fit (decision 0009).

---

## 12. Imports — `from build123d import *` is OK

Glob imports are fine in build123d scripts. Build123d is used as a domain-
specific language; scripts are short, self-contained, and edited in cramped
editors next to a CAD viewer. Idiomatic build123d code uses `from build123d
import *`. Don't waste time refactoring to `import build123d as bd` unless the
script is being embedded in a larger application.

---

## 12a. Companion Scripts (layout maps, six-view renderers, etc.)

Most CAD projects in this repo grow companion Python scripts that import
constants from the main model script (`layout_map.py`, `views.py`, etc.).
They silently rot as the model evolves, then mislead you visually until
you rerun them.

**Failure modes:**

- Imported constant gets renamed/removed → `ImportError` on next run.
- Hard-coded label or dimension (`"70x59x71"`, `"Tool tray 1/2"`) no longer
  matches the model. Script still runs, but the picture lies.
- Companion duplicates a derived expression (e.g. `tools_center_x`) and
  drifts when the main script's formula flips sign.

**Rules:**

1. After renaming or removing a constant, `grep_search` the **whole project
   folder** (not just the main script) for the old name.
2. Prefer importing dimension constants and computing labels via f-strings
   (`f"{SCOOP_BAY_W:.0f}x{SCOOP_BAY_D:.0f}"`) over hard-coded strings.
3. Prefer importing collection-driving constants (`TOOLS_BIN_COUNT`,
   `TOOLS_BIN_DIVIDER`) and looping, instead of hard-coding `tray_1`/`tray_2`.
4. Lift constants used by companion scripts (e.g. `WALL_BITE`) to the
   module-level constants section so importing the model module doesn't
   require running the `BuildPart` block.
5. **Rebuild AND rerun every companion script before committing.** A
   companion script that fails to import is just as bad as a broken main
   script.

---

## 13. "Can't Get There from Here" — Have a Plan B

OCCT cannot build every shape you can describe. If a `sweep()` fails, try
`loft()`. If a multi-section loft fails, build the pieces separately and
fuse / assembly them. If a fillet fails, reduce the radius or apply it earlier
in the chain. Patience is part of CAD.

---

## Quick Reference — Common Bugs and Their Fixes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Feature visible in viewer but missing / floating in slicer | Free-floating `Box`/`Cylinder` not fused | Sketch-on-face + extrude |
| Ridge invisible or shorter than expected | `extrude(amount=-h)` against face normal | Flip the sign, or sketch on offset plane |
| Off-centre feature ends up mirrored | Y-flip on a -Z normal face | Negate Y in `Locations(...)` |
| Wall cut lands on the opposite (back) wall | `Plane.XZ` normal is **-Y**; `offset(+d)` moves toward -Y | To cut +Y front wall: `Plane.XZ.offset(-(OUTER_D/2 + 1))` + positive extrude. Verify with both front.png AND back.png. |
| New feature lands at wrong height after adding earlier features | Stale face selector | Use `Plane.XY.offset(known_z)` |
| `sort_by(Axis.Z)` returns garbage inside a `BuildSketch` | All sketch points have Z = 0 | Sort by `Axis.Y` (sketch local) |
| Boolean fails after fillet/chamfer | Topology too complex too early | Move 3D fillets/chamfers to the end |
| Helix / thread reports valid but breaks downstream | Self-intersection | Split into ≤180° segments |
| Cantilever tab / boss prints poorly or needs tall supports | 90° overhang on the underside | Add a 45° triangular gusset (§11, "Cantilevers, tabs, and bosses") |
| Long extruded part shows a thin vertical seam / hairline gap exactly at its centerline | `extrude(..., amount=L/2, both=True)` leaves coincident faces at the centerline plane that OCCT doesn't always fuse cleanly | Sketch at one end (e.g. `Plane.YZ.offset(x_left)`) and `extrude(amount=L)` in one direction. Use `both=True` only for short, symmetric features (small gussets, tabs) where the seam isn't visible. |

---

## See Also

- Official tips: <https://build123d.readthedocs.io/en/latest/tips.html>
- Cheat sheet: <https://build123d.readthedocs.io/en/latest/cheat_sheet.html>
- For electronics enclosures (lid/base anatomy, standoffs, panel cutouts,
  PCB-aligned coordinate helpers): `electronics-enclosure-3dprint`
  *(separate plugin)* covers that ground when it is installed alongside
  this one.
