---
name: ps1-modeling
description: "Use when modeling, refining or reviewing a PS1/PSX-style low-poly character or prop in Blender — a retro game asset, a low-poly portrait from a turnaround reference, a faceted-hair game mesh, anything that has to match the poly budget and conventions of PlayStation 1 assets, or any low-poly body that has to be welded into one surface at the shoulders, hips, wrists and neck. Covers the procedural build-script workflow, the loft/bridge library, measuring a reference for proportions, budgets, and the failure modes that cost the most time."
---

# PS1 / PSX low-poly modeling

## What the style is

PS1 style = **small poly budget + one painted texture atlas**. It is *not* flat shading.
The body is smooth-shaded; only hair and hard props stay faceted. Flat-shading the whole
model reads as 2005 low-poly, not 1997. Detail lives in the texture, so the mesh is judged
on silhouette and edge flow — never on surface detail.

## Conventions (measured from real PS1-era reference models, not guessed)

- +Z up, character faces **−Y**, feet on **Z=0**, metres.
- One object — or, from the next character on, one object for the body and one per
  garment — one material, one texture atlas. In the reference models the clothes *are*
  the mesh; the next character here splits them: a complete closed body plus one closed
  shell per garment (see the separate-mesh note under the traps). Either way there are no
  intersecting tubes and no clothes painted onto a naked limb you never model.
- 100% smooth shading, except hair and hard-surface props.
- No normal maps, no PBR, no shape keys.
- One connected surface for the body: no loose vertices, no loose edges, no zero-area
  faces, no non-manifold edges, no coincident vertices. Quads for shells, triangles only
  where a shape needs them (joint bands, tips).
- **Build** in a T-pose — level rings make every cut and weld trivial — then **pose the
  finished, welded mesh** before saving: a rigid per-ring drop of the arms (35° about the
  shoulder socket, ramped along the arm) and a rigid hand turn about the wrist seam (25°).
  Every reference ships A-pose at rest, and a T-pose base reads as an unshipped blockout.

Budgets from five reference models:

| model | verts | tris | notes |
|---|---|---|---|
| rigged male basemesh | 772 | 1540 | 84 bones, 256² atlas, A-pose, 1.98 m |
| Walking (PSXProp) | 349 | 645 | all tris, 512² atlas, T-pose, 1.77 m |
| LE0GAR | 548 | 943 | 9 objects, one 256² atlas, Rigify, 2.4 m |
| PSX_Char_Male_Base v2 | 447 | 880 | 47-bone UE4 rig, untextured, A-pose, 1.82 m |
| Retro_Char_Base_Female v2 | 451 | 880 | same rig and budget, A-pose, 1.71 m |

That is a rigged **bare body**. Hair volume and accessories legitimately push past it — a
1100 v / 2200 tri character with a full mane, belt and boots is still a PS1 character.
Never cut silhouette to hit a number derived from a bare body.

The two `*_version_2` base meshes are also the useful counter-example: 880 tris each on a
47-bone rig, and **not clean**. They carry 6 boundary edges, 2 non-manifold edges, 2
pentagons and 8–14 coincident vertices; the female has 4 loose verts marking the eyes. Each
hand — 82 verts, 18 % of the mesh — is a separate shell overlapping the wrist under rigid
weights, i.e. a visible cuff, while its head, arms and legs are one welded 283-vert
surface. The bar these assets clear is lower than the gate this skill enforces: weld what
deforms, let a cuff hide what does not. (Digits there are 3 chains per hand — thumb, index,
one fused middle/ring/pinky — because that is what 880 tris buys.)

## Setup

`scripts/psx_build.py` is the library; the harnesses are config-at-the-top scripts.

```
scripts/psx_build.py           ring / ring_dir / Build / bridge / finish / check / report
scripts/preview.py             ortho clay renders, shots derived from the bbox
scripts/compare.py             stats table + side-by-side against reference FBX/OBJ models
scripts/measure_silhouette.py  width-vs-height scan of a reference PNG
```

Put `scripts/` on `sys.path` and import, or copy a harness next to your build script.
Everything runs inside Blender:

```python
import sys
sys.path.insert(0, r"…/scripts")
from psx_build import Build, ring, ring_dir, bridge, finish, check
```

## The API

```python
ring(cx, cy, cz, rx, ry, n=12, e=2.0, axis="Z", phase=0.0, yoff=None)
```
One closed cross-section. `e` is the superellipse exponent: 2 = circle, higher = boxier.
Useful: 2.1 limbs and head, 2.2 legs, 2.3 torso and belt, 2.6 palm. `axis="X"` lays the
ring in YZ for limbs along X. `yoff={index: dy}` pushes single vertices — that is how a
bust bulge, lumbar curve or seat is made without adding rings.

```python
Build.loft(rings, cap_start=..., cap_end=..., flat=..., part="…")
Build.extrude(base_indices, [(dir, length, scale), …], part="…")   # welded digit
Build.add_faces(faces, part="…")          # stitch vertices that already exist
Build.add(verts, faces, flat=..., part="…")
Build.tube(path, rx, ry, n=4, e=2.0, caps=True, part="…")
Build.box(cx, cy, cz, sx, sy, sz, flat=True, part="…")
Build.mark() → Build.mirror_x(mark)      # returns the mirrored vertex offset
bridge(verts, loop_a, loop_b, ref_face)  # stitch two open loops
```

`tube()` takes a path and orients each ring along the tangent — good for chains, straps,
loose props. It builds **its own** rings, so it cannot weld anything: for a digit that
must be part of a hand, use `extrude()` on vertices that already exist.

`finish()` merges builds into one object, applies smooth flags, welds coincident verts,
triangulates n-gons, recalculates normals, makes the material, adds placeholder UVs and
prints the report. `check()` is the gate; `bridge()`'s `ref_face` argument is what keeps
its winding honest.

## One surface, not a bag of parts

The default low-poly habit is to model each part as its own tube and push them into each
other. It is fast, and it is wrong in three ways: the crossing surfaces show as a jagged
seam in close-up, the interior faces are wasted, and every joint tears when it deforms.

Build the body as **one welded surface** instead. Four techniques cover every joint:

1. **Split a rim into limbs (hips, shoulders of a four-legged animal).** The pelvis's
   lowest ring is not a cap: each leg takes *six of its twelve verts* plus two crotch
   verts shared by both legs, and the two gaps left (front and back) are one triangle
   each. The legs then loft from that loop down. Nothing is bridged, nothing overlaps —
   the hip is simply one surface. Order each leg's loop by angle around its own thigh
   axis before lofting, or the first band twists.
2. **Cut a socket and stitch (shoulders, wrists, ankles, neck).** Write the parent's
   faces out by hand instead of calling `loft()`, skipping the quads where the limb
   attaches. That leaves an opening whose boundary is a known loop of vertex indices.
   `bridge(b.v, socket_loop, limb_first_ring, neighbouring_face)` fills it with a band —
   unless the rim's count already equals the limb's ring count, in which case use
   technique 4 instead and skip the band entirely.
3. **Extrude a welded quad (fingers, thumbs).** Take four existing vertices — four
   corners of the palm's end ring, or one wall quad left open in the palm — and
   `extrude()` them. Adjacent digits share their side edge, so the knuckles are one
   surface with a crease, not tubes in a box.
4. **Share a ring outright (wrist, ankle).** If both sides are the same vertex count and
   the same place, use the parent's ring *as* the child's first ring. Costs no geometry.

Two numbers decide whether a stitched joint looks professional:

- **Cut the socket to the joint's real size, and let the hole BE the limb's first ring.**
  A shoulder is as tall as the deltoid: a 2×2 quad cut (two columns × two ring bands,
  ~110 mm tall on a 1.8 m figure) leaves an 8-vert rim, exactly the arm's ring count, so
  technique 4 applies — copy the rim's coordinates as ring 0 and weld. No band, no fan, no
  shelf. A one-band (40 mm) slot forces a small first ring and a deltoid that swells
  afterwards, and the deltoid's top then has to land level with the parent's shelf: that is
  the shoulder-pad step, and it took a second character to get rid of it.
- **Where the socket cannot be sized to the joint** (a wrist, an ankle), the older rule
  holds: two quads wide, the limb's ring at the socket plane, a small ring that swells one
  or two rings later. Three quads wide was worse, never better.
- **A 2×2 cut orphans the vert at the hole's centre** — it belonged to all four deleted
  quads. Delete loose verts in the tidy *before* `remove_doubles`, or the gate fails on two
  loose verts and the socket weld still looks fine.

## Workflow

1. **Measure the reference before modelling.** Run `scripts/measure_silhouette.py` on the
   turnaround; write the width-at-height table down. Eyeballing proportions is the single
   biggest source of rounds lost.
2. **Block with lofts, then weld.** Torso grid first (its face list is hand-written so
   sockets can be cut), then pelvis split → legs → feet, sockets → arms → hands, neck →
   head. Read the printed PARTS log after every build.
3. **Render clay, and render close-ups of every joint.** Full-body ortho hides joints
   completely. Shoot each seam at 0.20–0.32 ortho from two angles before believing it.
4. **Compare against reference models**, not just the image. `compare.py` scales
   everything to one height and prints verts/tris side by side.
5. **Audit numerically** (see below), then save a copy.

## Verifying a weld

"It looks attached" is not evidence. Count:

```python
from psx_build import check
check(ob)                 # closed body: every count 0, boundary 0
check(ob, boundary=32)    # when you ship single-sided decals on purpose
```

`boundary` is the number of edges with only one face. A closed body is 0. This is the
test that catches the expensive bug: a digit whose base ring was *copied* instead of
shared looks welded in a render and shows up here as four boundary edges per digit.

Also worth printing once per session:

```python
bm = bmesh.new(); bm.from_mesh(me)          # after bm.from_mesh:
len(bm.verts) - len({tuple(round(c, 5) for c in v.co) for v in bm.verts})   # coincident
sum(1 for f in bm.faces if len(f.verts) > 4)                                # n-gons
# symmetry: every vert with |x| > 0 should have a partner at -x
```

Check symmetry **globally**, not per part: a mirrored part has no partner inside itself,
so a per-part check reports 100 % asymmetric for a perfectly symmetric model. Hair is the
one part that should be allowed to be asymmetric — an identical mirror looks like a wig.

## Traps — each one of these cost at least one round trip

1. **A copied base ring is not a weld.** `tube()`/`ring_dir()` build new vertices, so
   feeding them a digit's four corner *coordinates* silently duplicates the ring. The
   digit renders as attached, `boundary` is nonzero, and a whole review pass can be spent
   polishing a joint that does not exist. Pass indices; use `extrude()`.
2. **Decide a seam's winding from a neighbouring face, not from a normal vote.** For a
   band that wraps a limb the face normals sum to about zero, so an inward/outward vote
   is noise and half the band ends up inverted. A seam edge must be walked in opposite
   directions by the two faces that share it — that is one comparison, and it is exact.
3. **Rings of different counts need `bridge()`; same counts do not need anything.** Two
   8-vert loops at the same place can simply share vertices. Reaching for a stitch band
   where a shared ring would do adds triangles and a visible crease.
4. **Radii at a stitched junction must be monotonic.** Neck thinner than the skull's
   opening, opening wider than the neck: if the surface goes out→in→out, the groove
   catches shadow and reads as a crack across the throat. Same rule under a jaw, a cuff,
   a boot top.
5. **Keep the head and its accessories in one register.** Put the head's vertical offset
   in a single constant (`HEAD_DZ`) and apply it to skull, nose, eyes and hair together.
   Moving "the head" by editing the skull table alone leaves the fringe floating.
6. **Hair: don't cut the face slot out of the shell.** For each row, columns inside the
   slot get a radial scale around 0.45 plus a small +Y push, ramping to full radius
   roughly 10° past the slot half-angle (26–34° by row). A 30° ramp puts hair over the
   whole face; shrink without the push leaves a pale inner wall beside the cheek. **This
   only works on a thick mane.** At ~20 mm of short hair the quad that crosses from a
   sunk column to the frame column lies in front of the cheek and reads as a dark slab
   across the cheekbone; fold the slot columns straight back into the head instead (spread
   across the slot in x, `y = centre + 18 mm`) so the hairline is the column at the rim.
7. **Never alternate a fringe hem by column parity.** `j % 2` on an even column count
   puts a tooth notch dead centre. Use a smooth function of the column angle.
8. **A single-apex pyramid is not a nose.** Read as a thin sliver from the front. Use a
   six-vertex wedge with a separate bridge point and tip point, base closed so the head
   stays watertight.
9. **Frame the whole pose.** A wide pose spans about the character's height; an ortho scale
   that frames the torso crops the hands off and hides every hand problem. Set the render
   width from the bbox, not from habit — and re-frame after posing, because the bounds
   move (1.86 ortho for the T-pose became 1.80 at 820 × 900 for the A-pose).
10. **Normalise every direction vector** before scaling by a length. An unnormalised one
    produced a 1 m thumb.
11. **`mirror_x` takes `(len(v), len(f))` from `mark()`**, reverses the mirrored winding,
    and returns the copy's vertex offset — keep its return value if you want to stitch a
    seam to the mirrored limb.
12. **Never `join()` without deselecting all first.** A leftover default cube gets
    absorbed into the character. Filter selection by object name.
13. **Reference FBX imports**: read posed bones from the evaluated depsgraph
    (`ob.evaluated_get(dg).pose.bones[name]`), not rest-pose `bone.head_local` — rigs
    ship in an A-pose and the rest positions are metres away from what you see. Clear
    parents before deleting an armature, and delete the imported objects afterwards:
    a leftover reference model renders into your previews for the rest of the session.
14. **Elevated preview cameras**: the horizontal offset must scale by `cos(elev)`, or the
    shot frames empty background.
15. **Run the gate on geometry, not on the render.** A degenerate quad looks fine in a
    front view and wrecks the wireframe.
16. **Pose the welded mesh, don't model it posed.** Build level (easy cuts, easy welds),
    then rotate the finished blocks: an arm drop whose angle ramps along x, plus a rigid
    hand turn about the wrist seam. Limb rings lie in planes of constant x, so a per-ring
    angle cannot pinch a loop — the stitch bands take the rest, and mirroring *after*
    posing gives the other side for free. The wrist break is what makes a hanging hand read
    as a hand instead of a paddle continuing the forearm.
17. **Crotch points belong in the cleft.** A rear crotch point sitting several cm forward of
    the seat closes the buttock with a quad that folds edge-on and renders as a sharp fin
    on the seat. Put it on the buttock line (y ≈ 0.07, z ≈ 0.89, front point mirrored in y)
    and the seat closes with a small triangle instead.
18. **Never let a temp study scene stay active.** A ref-study run that died between
    `scenes.new()` and its cleanup left that scene active; the next build landed in it —
    no lights, no camera — and a render pass came out black. Tear temp scenes down in a
    `finally` at the call site, no global `orphans_purge`, and check the live scene's
    object list afterwards.
19. **Check that a socket cut matches the table it indexes.** The comment said the slot was
    cut from the armpit band (rings 8–9); the code cut band 9 — the one above it — so the
    arm was stitched into the shoulder shelf. Every render showed a valley with a flap and
    two rounds of re-depthing the deltoid changed nothing. When a junction looks wrong,
    print the rim vertices and compare their z with the limb's first ring *before* tuning
    the limb.
20. **Faces are structural, not optional.** A blank face still needs vertices where the
    eyes go: 8 columns give a centre line and ±45° (the cheek), so a socket has nowhere to
    be. 12 columns with a pair at ±22.5°, a brow ring set ahead of the eye ring, and ±2 mm
    socket/cheek offsets carry painted features. Keep offsets small — 3.5 mm on top of a
    10 mm ring step turned the brow into a shelf, because on a 12-column face a 4 mm offset
    over a 20 mm gap already folds. All five references are 100% smooth-flagged yet render
    faceted: their FBX carries baked split normals, so flags don't prove flat shading — and
    don't flat-shade a skull to fake structure the texture should paint.
21. **Mark hair by its flat shading, not by "the last N faces".** A join plus a tidy pass
    reorders polygons; a stored face count drifts and a "dark hair" render pass recolours
    scattered faces across the whole body. Faceted geometry above the waist is the hair.
22. **Workbench shadow acne looks like z-fighting.** A dotted line under a belt overhang
    read as coplanar faces; the vertices were 8–11 mm apart. Check the numbers before
    moving geometry.
23. **A 2×2 socket cut orphans the vert at the hole's centre.** It belonged to all four
    deleted quads, so it survives with no faces and the gate fails on two loose verts (one
    per side) while the socket weld itself looks perfect. Delete loose verts in the tidy
    *before* `remove_doubles`.
24. **Garments are radius steps in the same surface.** A tee hem, a jacket hem and a
    trouser cuff are 10–15 mm outward jumps between two rings 10–20 mm apart, plus one
    ring turning back in at the very bottom so the edge drapes instead of ending as a
    cut-off pipe. A raised zip bead (a 4-vert loft down the front, flat-shaded) is what
    makes a closed jacket read as a jacket rather than a vest. A hard part inside a
    garment — a sole and welt — can be a second loft that *shares* its boundary ring: the
    tidy welds the duplicate and the flat-shaded band reads as leather.

**Separate body and clothing meshes.** The current characters carry the clothes *in* the
body surface, which is why their sleeves, hems and trouser legs are radius steps and why
the jacket cannot be removed. That was the right call while the weld doctrine was being
figured out (one surface means one set of seams to get right) and the wrong call going
forward: the next character should keep **a complete closed body underneath and each
garment as its own closed shell**, offset 4–8 mm from the skin, so clothes can be swapped,
hidden or weighted separately, and so a hem or a lapel can be opened without re-modelling
the torso. Keep the welds *within* each garment (a sleeve is welded to its jacket, a
trouser leg to its waist) and keep the body welded to itself; the two sets never share a
vertex. Budget for it: sleeves and legs then exist twice, so a 2400-tri character becomes
~3000 under this scheme — and the body can be blocked coarser because it is mostly hidden.

## Review pass

Render, then look, in this order:

- **Close-ups first** — every seam at 0.20–0.32 ortho, two angles each. Joints are where
  the errors are; a full-body shot at 1.80 ortho cannot show a 10 mm fold.
- Body front / side / back / three-quarter at an ortho scale that fits the whole pose.
- Hand and head separately, against the reference art at matched scale.
- Wireframe or `check()` output next to every render pass.

Then the numbers: `check()` clean, `z.min == 0`, height, tri count, smooth flags, one
material, UVs inside 0–1, object transform identity.

## Worked example — one real character

A 1.72 m gothic girl, mesh only, built and welded with this library in T-pose, then posed
to A-pose (35° arm drop, 25° wrist break) after the last weld:
**1167 verts / 1267 faces / 2308 tris — 1041 quads, 226 tris, 0 n-gons, 0 boundary
edges, 0 non-manifold edges, 0 coincident verts.** Torso, pelvis, both legs, both boots,
both arms, both hands, neck and head are one closed shell; the mane is a second closed
shell. The skull is 12 columns (a pair at ±22.5° for the eyes, brow ring ahead of the eye
ring) so painted features have form; the neck bridge is 12↔12.

The second character — a 1.81 m male in a leather jacket, tee, bootcut jeans and slim
boots — reused the same library and settled the shoulder question: **1202 verts / 1285
faces / 2372 tris**, same gate, all zero. Its shoulder is a 2×2 socket cut whose eight rim
verts *are* the arm's first ring (no stitch band), its short hair folds the slot columns
back into the skull instead of sinking them, and its clothes are still part of the surface —
the next one should not be (see the separate-mesh note in the traps).

What the welding pass changed, in the order it was done:

| joint | before | after |
|---|---|---|
| shoulders | arm tube butted into the chest | 2-quad socket cut in the armpit band, arm stitched in |
| wrists | hand ended inside the forearm | arm's wrist ring stitched to the hand's 10-vert ring |
| hips | torso stub buried in the trouser tubes | pelvis rim split six-and-six, crotch = 2 shared verts + 2 triangles |
| ankles | hem over a separate boot | hem stitched to the boot's shaft ring |
| neck | head floating in the neck tube | neck rim stitched to the skull's lowest ring |
| fingers | capped tubes pushed into the palm | 3-segment `extrude()` off the knuckle ring |

Measured widths from its reference sheet (z → silhouette width in metres):

| z | width | | z | width |
|---|---|---|---|---|
| 1.66 | 0.245 | | 1.05 | 0.242 |
| 1.575 | 0.322 | | 0.96 | 0.295 |
| 1.49 | 0.349 | | 0.875 | 0.314 |
| 1.40 | 0.403 | | 0.61 | 0.330 |
| 1.225 | 0.265 | | 0.26 | 0.452 |
| 1.14 | 0.180 | | 0.0525 | 0.449 |

The numbers matter less than the method: one table, one pass of lofts, one welding pass,
then numeric corrections driven by close-up renders. Two things needed the reference
*models* rather than the image: arm length (the image's arms droop ~20°, so its horizontal
span understates the true length) and hand size (the image's hand is 154 mm wrist-to-tip
on a 1.74 m figure; a reference rig with finger bones gave 3 phalanges per finger and
~168 mm, which is what the model uses).

## Out of scope here

Texturing, rigging and export. Placeholder UVs from `smart_project` are islands, not a
real atlas. When texturing starts: one 256² or 512² atlas, keep the hair's inner surfaces
on a dark region so the shell edges read as depth, and paint the face — the mesh stays a
mask. A welded surface is what makes the later rig survive; a bag of intersecting shells
is what makes it tear.
