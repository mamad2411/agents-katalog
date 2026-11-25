---
name: cad-reverse-engineer-stl
description: 'Read an existing STL (or STEP) file, measure it, and rebuild it as a parametric build123d model. Covers mesh loading (trimesh / OCCT), bounding-box and primitive detection, hole/fillet inference, alignment to a sane coordinate system, and an iterative measure → propose → diff workflow. USE FOR: "rebuild this STL parametrically", "extract dimensions from this mesh", "convert STL to build123d", "reverse engineer a downloaded model", "I have an STL but no source", "measure features in a mesh", "import STEP into build123d".'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["stl","step","reverse-engineering","build123d","mesh"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# CAD Reverse-Engineer STL

> **Prerequisite:** Load `cad-build123d-general` first. This skill is the
> entry point *into* a parametric build; once you have a working
> reconstruction, everything from `cad-build123d-general` (export modes,
> orientation map, feature inventory, sidecar) applies normally.

## Purpose

Sometimes you don't get a parametric source — you get an STL off a
forum, a STEP export from a vendor, or a mesh you reconstructed from a
3D scan. This skill turns that into a clean, parametric build123d model
that you can edit with confidence.

The skill assumes the goal is a **functional reconstruction**, not a
forensic copy of every triangle. You want the design intent (this is
a 50 mm box with a 6 mm hole on the top, filleted at R3), not a 1:1
mesh import.

## The Cardinal Rule #−1: Check the license BEFORE you measure anything

A reverse-engineered build123d model derived from someone else's STL is
a **derivative work** under copyright law in most jurisdictions, even
if your code shares no lines with theirs. The license on the original
controls what you can do with the rebuild, not the fact that you typed
it from scratch in a different language.

**Before opening trimesh, do this:**

1. **Find the source page** for the STL. Check the download folder for
   a README, LICENSE, an order PDF, or a `.txt` next to the STLs.
   Search Printables / Thingiverse / Cults / Thangs / MakerWorld for
   the filename if needed.
2. **Read the license.** Common ones:

| License | Personal use | Modify locally | Publish modified version |
|---------|:------------:|:--------------:|:------------------------:|
| Public Domain / CC0 | ✅ | ✅ | ✅ |
| CC BY 4.0 | ✅ | ✅ | ✅ (must credit original) |
| CC BY-SA 4.0 | ✅ | ✅ | ✅ (must credit + share-alike) |
| CC BY-NC 4.0 | ✅ | ✅ | ✅ (non-commercial only) |
| **CC BY-ND** / **CC BY-NC-ND** | ✅ | ⚠️ gray | ❌ **No derivatives** |
| All Rights Reserved / no license | ✅ (download implies) | ⚠️ gray | ❌ |
| GPL / AGPL on STL | ✅ | ✅ | ✅ (must publish source) |

3. **If the license forbids derivatives** (any `-ND` variant, or "All
   Rights Reserved"), STOP and surface the problem to the user before
   doing the work. Common paths forward:
   - **Personal use only** — keep the rebuild on the user's machine,
     never commit to a public repo, never upload to MakerRepo /
     Printables / GitHub. Acceptable in many jurisdictions but a gray
     area; user makes the call.
   - **Clean-room rewrite from functional requirements** — discard the
     original STLs and rebuild from the user's *needs* (clamps a desk,
     holds my headphones), not from measurements of the original. The
     same hardware interface (M5 thumbscrew + square nut) is generally
     not copyrightable; the specific geometry is.
   - **Ask the original author** for permission to publish a derivative.
   - **Walk away** and find a permissively-licensed alternative.

4. **Record the license in `decisions/0001-license-check.md`** of the
   project before any measurement work, with: original URL, author
   name, license name + version, license URL, and which path forward
   the user chose. Quote the relevant license clause.

5. **If you've already started measuring before noticing the license
   problem**: any measurement-derived files (`measure_*.py`,
   diff scripts, the parametric script, exported STLs that match the
   original profile) become derivative work. Quarantine them — delete,
   or move into a `derivative-quarantine/` subfolder that is `.gitignore`'d
   — and start over from the clean-room path. Note the quarantine in
   the decision record. Filename suffixes alone don't undo derivation.

**Exception:** purely measurement-driven docs ("how big is this thing?",
"what's the screw size?") don't create a derivative work — they're
fact-finding, like reading the specs off a product page. The line is
crossed when you start *reproducing the geometry*.

The check takes 30 seconds. The recovery from skipping it is hours of
deleted work and an awkward email.

## The Cardinal Rule #0: Make it parametric, not a copy

The whole point of doing this work is to end up with a model you can
**edit** — change a wall thickness, scale up a dimension, swap M3 holes
for M4. If your reconstruction is just a wall of hard-coded numbers
that happen to add up to the original mesh, you've done the work twice
for the same result as importing the STL.

Concrete rules:

1. **Every dimension that comes out of measurement is a `CONSTANT` at
   the top of the file.** Not a literal in the middle of a `Box(...)`
   call. Name it after what it represents (`OUTER_W`, `WALL`, `M3_CLEAR`),
   not what it equals (`forty_two`).
2. **Derive what you can derive.** If the part is a shell, store
   `INNER_*` and `WALL` as inputs and compute `OUTER_* = INNER_* +
   2 * WALL`. If you store both, they will drift the moment you change
   one.
3. **Identify the design intent, not the measurement.** A 5.97 mm hole
   is an `M5_CLEAR = 5.0` (or 5.5 — ask). A 159.93 mm length is
   `INNER_L = 160`. Don't preserve manufacturing tolerance or mesh
   noise as if it were intentional.
4. **Group constants by purpose.** Wall + floor + lid thicknesses
   together. Hole sizes together. Text sizes together. A future-you
   reading the file should see "ah, the part is shell-thickness +
   feature-positions + text", not a soup of numbers.
5. **One source of truth per dimension.** The notch position and the
   wall it sits on must reference the same `OUTER_L` constant. If a
   change to `OUTER_L` doesn't move the notch, the notch isn't
   actually parametric.
6. **Patterns become loops, not copy-paste.** Four mounting holes at
   the corners → one `Locations([...])` call with the four corner
   coordinates derived from `OUTER_L` and `OUTER_W`, not four `hole(...)`
   calls with literal positions.
7. **Ask the user for tolerances and clearances.** A "6 mm hole" might
   be M6 thread (6.0), M6 clearance (6.5), or a 6 mm dowel press-fit
   (5.95). The mesh can't tell you which. Ask.

The litmus test for "is this parametric": **change one constant at the
top of the file, re-run, and verify a related feature moved with it.**
If nothing moved that should have, that constant isn't actually wired
in — it's just a label sitting next to a literal somewhere else.

## When to use this skill (and when not to)

| Situation | Use this skill? | Why |
|-----------|-----------------|-----|
| You have an STL and want to tweak one dimension | ✅ Yes | The whole point. Rebuild parametric, change the parameter. |
| You have a STEP file and want to tweak one dimension | ✅ Yes | STEP is much easier than STL — see § STEP path below. |
| You have a 3D scan of a real object | ✅ Yes (with a caveat) | Scans are noisy; lean heavier on bounding-box + reference photos than on the mesh itself. |
| You just want to print the existing STL once, unchanged | ❌ No | Slice it. You don't need build123d. |
| The STL is generative / topology-optimised / organic | ⚠️ Avoid | Primitive decomposition won't work; consider keeping it as a mesh and only modelling the mounting interface. |

## The Cardinal Rule #1: STL is lossy

An STL is a list of triangles. It has **no** notion of:

- faces (a "flat top" is hundreds of coplanar triangles)
- edges (a fillet is a strip of small triangles)
- holes (a "round hole" is a ring of triangles forming a cylinder)
- features (a "boss" is just more triangles)
- units (no header — *assume mm* and verify with bounding box)

Everything above must be **inferred**. If a measurement disagrees with
common sense (a "6.03 mm" hole that's clearly meant to be M6 → 6.0 mm),
**round to the design intent**, don't preserve mesh noise.

STEP files don't have this problem — they carry BREP geometry with real
faces, edges, and (sometimes) features. Always prefer STEP if available.

---

## 1. Pick the right loader

| Library | Best for | Notes |
|---------|----------|-------|
| `trimesh` | Quick measurement of an STL: bounding box, volume, face normals, splitting into connected components, primitive fitting | `pip install trimesh` (pulls `numpy`). Pure-Python-friendly. |
| `numpy-stl` | Just reading triangles into NumPy arrays | Lower-level than trimesh; rarely needed if you have trimesh |
| `cadquery-ocp` / build123d's OCCT bindings | Loading **STEP** as real BREP and re-using its faces in a parametric script | This is the gold path for STEP. STL via OCCT is possible but you get a Shell of triangles, not real faces. |
| `pymeshlab` | Cleaning bad meshes (non-manifold edges, flipped normals, duplicated vertices) before measurement | Heavy dependency; only pull in if `trimesh.is_watertight` is False. |

### Loading STL with trimesh (measurement-first)

```python
import trimesh

mesh = trimesh.load("input.stl", force="mesh")  # force= avoids Scene wrapper
print(f"vertices: {len(mesh.vertices)}, faces: {len(mesh.faces)}")
print(f"watertight: {mesh.is_watertight}")
print(f"bbox (mm): {mesh.bounding_box.extents}")   # (X, Y, Z) extents
print(f"volume: {mesh.volume / 1000:.2f} cm³ "
      f"(meaningful only if watertight)")
```

If `is_watertight` is False, run `mesh.fill_holes()` and
`mesh.fix_normals()` before trusting volume or any inside/outside test.
If that doesn't fix it, fall back to pymeshlab.

### Loading STEP with build123d (structural-first)

```python
from build123d import import_step

shape = import_step("input.step")
bb = shape.bounding_box()
print(f"bbox: {bb.size}")
for face in shape.faces():
    n = face.normal_at(face.center())
    print(f"  face area={face.area:.2f}  normal={n}  center={face.center()}")
```

A STEP import gives you a `Solid` you can keep using directly in
build123d — `face.fillet(...)`, `face.hole(...)`, etc. all work. You can
treat it as the starting point for a parametric model rather than
rebuilding from scratch.

---

## 2. Align to a sane coordinate system FIRST

Reverse engineering is much easier when the part is axis-aligned with
its longest dimension along +X (or whatever your `ORIENTATION` map says
"front-back" is). Don't try to measure features on a part that's tilted
30° in space.

```python
# If the part isn't already axis-aligned:
mesh.apply_obb()   # orient by oriented bounding box (longest axis to X)

# Re-centre on origin so measurements are symmetrical:
mesh.apply_translation(-mesh.bounding_box.centroid)

# Save the cleaned-up mesh so you can diff against it later:
mesh.export("input.aligned.stl")
```

After this step, write down the orientation in the same friendly terms
you'd use in `cad-build123d-general` § 8a:

```
ORIENTATION (inferred):
  +X = "long axis" (165 mm)
  +Y = "wide axis" (111 mm)
  +Z = "tall axis" (38 mm), open side
```

Confirm with the user before you start measuring features — half the
reconstruction effort comes from getting orientation wrong.

---

## 3. The measure → propose → diff loop

Reverse engineering is iterative. Don't try to model everything in one
pass.

### Step 1: Measure the obvious

Print, in this order:

1. **Outer bounding box** — round to a sensible precision (0.1 mm for
   printed parts, 0.01 mm for machined). Propose nice round numbers if
   the mesh is close (`165.03` → `165.0`).
2. **Wall thickness** — for an enclosure, find the difference between
   outer and inner bounding box at the floor. With trimesh:

   ```python
   # crude: slice the mesh just above the floor and look at section width
   section = mesh.section(plane_origin=[0, 0, mesh.bounds[0, 2] + 1.0],
                          plane_normal=[0, 0, 1])
   if section is not None:
       paths_2d, _ = section.to_planar()
       outer = paths_2d.bounds  # (xmin, ymin, xmax, ymax)
       # measure inner the same way at a higher Z
   ```

3. **Symmetry** — reflect the mesh across X=0, Y=0 and check overlap.
   If high, the part is symmetric and you only need to model half.

### Step 2: Identify primitives

Walk through the mesh looking for things that are clearly one shape:

| Mesh signature | Likely feature |
|----------------|----------------|
| Cluster of coplanar triangles forming a flat region | Face |
| Ring of triangles whose normals rotate around a single axis | Cylinder (hole or boss) |
| Strip of small triangles between two faces, normals rotating ~90° | Fillet |
| Strip of small triangles between two faces, normals rotating <45° | Chamfer |
| Identical triangle pattern repeated at offset positions | Pattern (array) |

trimesh helpers:

```python
# Find clusters of coplanar faces
adjacency = mesh.face_adjacency
# group faces whose adjacent normal angles are < 0.01 rad
groups = trimesh.graph.connected_components(
    edges=adjacency[mesh.face_adjacency_angles < 0.01]
)

# Detect cylindrical regions (good for holes / bosses)
# trimesh.primitives.Cylinder has a .from_mesh() heuristic in some forks;
# alternatively, fit per-cluster:
import numpy as np
for group in groups:
    normals = mesh.face_normals[group]
    if np.std(np.linalg.norm(normals, axis=1)) > 0.1:
        # normals point in many directions — possibly cylindrical
        ...
```

### Step 3: Propose a build123d reconstruction

Write a build123d script that produces the **simplest** primitive that
matches what you measured. Round dimensions to design intent. Use the
same `EXPORT_MODE` / `ORIENTATION` / `FeatureRegistry` scaffolding from
`cad-build123d-general` § 8a from the start — don't bolt it on later.

Per Cardinal Rule #0, every measured dimension goes in a named constant
at the top of the file, and everything else is derived. Compare:

❌ **Not parametric** (a copy with literals scattered through the script):

```python
with BuildPart() as part:
    Box(165.5, 111.47, 38.4)            # measured outer
    with BuildSketch(part.faces().sort_by(Axis.Z)[-1]):
        Rectangle(160.0, 105.97)        # measured inner
    extrude(amount=-35.65, mode=Mode.SUBTRACT)
    with Locations((82.75, 0, 26.4)):
        Box(8.25, 38.19, 24.0, mode=Mode.SUBTRACT)   # notch
```

Change `INNER_L` later? You'll touch four numbers in three places and
forget one.

✅ **Parametric** (one source of truth per dimension, derived where
possible):

```python
# --- Source-of-truth constants (everything else derives from these) ---
INNER_L = 160.0       # interior length, holds the inserted notes
INNER_W = 105.97
INNER_H = 35.65       # interior depth (open-top tray)
WALL    = 2.75        # uniform side-wall thickness
FLOOR   = 2.75        # bottom thickness

NOTCH_W = 38.19       # finger-pull notch
NOTCH_D = 24.0

# --- Derived (do not edit; change the source above instead) ---
OUTER_L = INNER_L + 2 * WALL
OUTER_W = INNER_W + 2 * WALL
OUTER_H = INNER_H + FLOOR

with BuildPart() as part:
    Box(OUTER_L, OUTER_W, OUTER_H)
    # interior cavity
    with BuildSketch(part.faces().sort_by(Axis.Z)[-1]):
        Rectangle(INNER_L, INNER_W)
    extrude(amount=-INNER_H, mode=Mode.SUBTRACT)
    # finger-pull notch on +X wall, flush with rim
    with Locations((OUTER_L / 2, 0, OUTER_H - NOTCH_D / 2)):
        Box(WALL * 3, NOTCH_W, NOTCH_D, mode=Mode.SUBTRACT)
```

Now bumping `INNER_L` from 160 to 180 stretches the box, moves the
notch wall outward, and keeps the wall thickness intact — all from one
edit. That's the litmus test from Cardinal Rule #0.

### Step 4: Diff against the original

Export your reconstruction to STL and compare:

```python
import trimesh, numpy as np

original = trimesh.load("input.aligned.stl", force="mesh")
rebuilt  = trimesh.load("rebuilt.stl",       force="mesh")

# Hausdorff-ish distance: closest-point distance from rebuilt to original
closest, dist, _ = trimesh.proximity.closest_point(original, rebuilt.vertices)
print(f"max  deviation: {dist.max():.3f} mm")
print(f"mean deviation: {dist.mean():.3f} mm")
print(f"95th percentile: {np.percentile(dist, 95):.3f} mm")
```

Targets for a good reconstruction:

- **mean < 0.1 mm** — the bulk shape matches
- **95th percentile < 0.3 mm** — most features captured
- **max < 1.0 mm** — the worst miss is a single fillet radius or a
  rounding choice

If `max` is huge (5+ mm), there's a missing feature — find the vertex
with the worst distance and look at that region in your slicer.

---

## 4. Holes and fillets are the hardest part

These two features account for ~80% of the headache.

### Holes

If you can spot a cylindrical region (§ 3 step 2), measure:

- **Centre axis** — fit a line through the cluster centroids
- **Diameter** — `2 × mean distance from axis to cluster vertices`
- **Depth** — distance from face entry to the deepest cluster point

Then **round to the nearest standard size**:

| Measured (mm) | Likely intended | Why |
|---------------|-----------------|-----|
| 3.05–3.25 | M3 clearance (3.2) | M3 screws need 3.2 |
| 3.95–4.15 | M4 clearance (4.0) | |
| 4.95–5.15 | M5 clearance (5.0) | |
| 5.95–6.15 | M6 clearance (6.0) | |
| 6.95–7.15 | M7 — rare; check if M6 + clearance | |
| Anything `.5` ± 0.1 | Rounded design number | |

Don't preserve `5.97 mm` in your build123d source. Write `M5_CLEAR =
5.0` and use that constant.

### Fillets

Almost always design-intent radii: **R0.5, R1, R2, R3, R5**. Measure
the fillet strip width (perpendicular to the fillet axis) and
back-calculate:

```
strip_width ≈ R × π/2     (for a 90° fillet)
so R ≈ strip_width × 2/π ≈ strip_width × 0.637
```

A 3.14 mm wide fillet strip → R2. A 4.71 mm strip → R3. If your
back-calculated R is 1.97 or 3.04, **round to 2 or 3**.

Apply fillets *last* in the build123d script (per
`cad-build123d-general` § 3) so they don't fight with the rest of the
geometry.

---

## 5. Common reconstruction mistakes (from experience)

### Building a copy instead of a parametric model

The biggest mistake. Symptoms: literals scattered through the script,
no constants section at the top, related dimensions stored independently
(both `INNER_L = 160` and `OUTER_L = 165.5` instead of deriving one).
Bumping a single dimension requires touching the script in five places
and you forget two of them.

Fix: re-read Cardinal Rule #0. Pull every measured number into a named
constant at the top, derive everything else, and apply the litmus test:
change one constant, re-run, confirm related features moved with it.

### Preserving mesh noise

The STL has every triangle at floating-point precision. Your build123d
source should have **clean numbers**: 160.0, not 160.0327. If a
dimension doesn't round to something nice, double-check whether it's
actually `outer = inner + 2 × wall` (a derived value), and store the
source-of-truth instead.

### Modelling the wrong side as primary

For shells (enclosures, cases): the **inner** dimensions are usually
the design intent (they're sized to fit something), and outer is
derived. For solid blocks the opposite. Pick correctly per part. See
`cad-build123d-general` § 8a — when in doubt, ask the user.

### Forgetting orientation

A reconstructed model that prints upside-down is no better than the
STL it came from. Fill in the `ORIENTATION` map before any feature
work, and pick a `BED_FACE` early.

### Trying to capture every feature in one pass

Build the outer shell first. Diff it. Then add the biggest cutout.
Diff again. Keep iterating; commit each working pass. If you try to
add a notch + holes + text + fillets all at once and the diff explodes,
you won't know which one broke it.

### Skipping the diff step

If you don't measure deviation, you don't know what you missed. The
diff loop (§ 3 step 4) is the whole point of this skill.

---

## 6. Quick reference

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| trimesh `is_watertight` is False | Mesh has holes / non-manifold edges | `mesh.fill_holes()`, `mesh.fix_normals()`, then pymeshlab if still bad |
| `volume` looks wildly wrong | Mesh isn't watertight, or wrong units | Check bounding box matches expected mm; if 25.4× off, it's inches |
| Diff `max` >> `95th percentile` | One missing feature | Find the worst-deviation vertex and look at that area |
| Diff is high everywhere | Wrong orientation or wrong scale | Re-run `apply_obb()` and re-measure bounding box |
| Holes don't line up by exactly 0.05–0.2 mm | You preserved mesh noise instead of rounding | Use `M3_CLEAR = 3.2` constants, not raw measurements |
| Changing one dimension breaks unrelated features | Not actually parametric — you have copy-paste literals | Pull all measured numbers into a constants block; derive everything else (Cardinal Rule #0) |
| Fillet radii feel "off" | Same — preserving noise | Round to R0.5 / R1 / R2 / R3 / R5 |
| Reconstruction is 25.4× too big or too small | Inch ↔ mm confusion | Multiply by `25.4` or `1/25.4` and re-bound |

## See Also

- `cad-build123d-general` — once you have a working reconstruction,
  this is your home. Use its export modes, orientation map, feature
  inventory, and print-settings sidecar.
- `cad-feature-inventory` — register the features you reconstructed so
  the model is self-describing as you iterate.
- trimesh docs: <https://trimesh.org/>
- build123d STEP import:
  <https://build123d.readthedocs.io/en/latest/import_export.html>
