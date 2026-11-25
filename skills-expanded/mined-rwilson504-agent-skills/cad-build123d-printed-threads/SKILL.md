---
name: cad-build123d-printed-threads
description: 'How to design 3D-printable screw threads, thumbscrews, and printed nuts in build123d using bd_warehouse.thread. Covers the right thread family for FDM (ISO vs Acme vs trapezoidal), pitch/diameter rules for layer-line resolution, the "shaft at minor diameter + add external thread" pattern, the printed-on-printed clearance trick, and the bd_warehouse SUBTRACT bugs that bite trapezoidal threads. USE FOR: 3D-printed thumbscrew, printed nut, captive nut, lead screw, knob, threaded clamp, IsoThread, AcmeThread, MetricTrapezoidalThread, TrapezoidalThread, threaded bore, helix, FDM thread, printed-on-printed fit.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["build123d","threads","3d-printing","fdm","fasteners"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# CAD Build123d Printed Threads

> **Prerequisite:** Load `cad-build123d-general` and
> `cad-build123d-bd-warehouse` first. This skill is the *practical*
> companion to those — what thread libraries exist (bd_warehouse
> reference) vs how to actually use them for FDM-printed parts (this).

## Purpose

3D-printed screws, nuts, knobs, and lead screws are surprisingly easy
in build123d via `bd_warehouse.thread` — but only if you know the
gotchas. The library was built primarily for *visualizing* metal
fasteners, and the FDM use case (where male and female parts will
both be printed and need to mate with clearance) is a side road with
sharp edges. This skill is the map of the sharp edges + the patterns
that work.

## What you get from `bd_warehouse.thread`

The full API (signatures only — see
`cad-build123d-bd-warehouse` for the catalog overview):

| Class | Profile | Use it for | FDM friendly? |
|-------|---------|------------|---------------|
| `IsoThread(major_diameter, pitch, length, external, ...)` | 60° V (ISO/UTS) | Real bolts; ALSO the workaround for printed parts (see § Bugs) | ✅ at coarse pitch + large diameter |
| `AcmeThread(size, length, ...)` | 29° trapezoidal (imperial sizes like `"1/2"`) | Lead screws, vises | ✅ flat tops handle layer steps |
| `MetricTrapezoidalThread(size, length, ...)` | 30° trapezoidal (`"12x3"` etc.) | Metric lead screws, knobs | ⚠️ has SUBTRACT bug; see below |
| `TrapezoidalThread(diameter, pitch, thread_angle, length, ...)` | Generic trap | Custom angles | ⚠️ same SUBTRACT bug |
| `Thread(apex_radius, apex_width, root_radius, root_width, pitch, length, ...)` | Fully custom profile | Specialty / debug | n/a |
| `PlasticBottleThread(size, ...)` | SP-100 etc. | Bottle caps | n/a |

All threading classes are `BasePartObject`s — instantiating them
inside a `BuildPart` context auto-adds them to the current part
(don't call `add()` afterwards or you'll get a `TypeError` about
`unwrap`).

## FDM thread design rules (printed-on-printed)

A printed screw + printed nut is a different beast from metal
fasteners. The rules below assume a 0.4 mm nozzle at 0.2 mm layer
height on a Bambu / Prusa / Voron-class FDM printer. Looser nozzles
(0.6 mm) or coarser layers need the rules bumped further.

### Pick a coarse, large thread

| Goal | Rule | Why |
|------|------|-----|
| Thread crests print as flat-topped material, not staircased pixels | **`major_diameter ≥ 12 mm`** for V-threads, ≥ 8 mm for trapezoidal | Smaller and the 60°-V crests turn into knife edges that the nozzle can't form |
| Each thread face has enough layers to look like a face | **`pitch ≥ 1.5 mm`** (preferably ≥ 2 mm) | At 0.2 mm layer height, 2 mm pitch = 10 layers per turn = visible smooth helix |
| Tactile threads the user feels turning | pitch 2-4 mm | Below 1.5 mm → looks like a smooth shaft; above 4 mm → user feels each "step" |
| Travel per turn covers the clamp/mating range in a few seconds | (range_mm) / pitch ≈ 5-15 turns | 30 mm travel ÷ 3 mm pitch ≈ 10 turns of the knob |

**Default starting point for a hobbyist clamp / knob: ISO M16 × 3.**
This skill's reference project (`cad/headphone-hook-desk-clamp/`)
uses exactly this.

### Clearance: female thread is OVERSIZED

Both male and female threads will print 0.1-0.3 mm fatter than you
designed because of nozzle over-extrusion + cooling bulge. If you
design them as exact mates (`major_diameter` identical for both),
the printed parts will jam.

**Pattern:** make the female thread's `major_diameter` larger by
`2 * THREAD_CLEAR` (typically `2 × 0.4 = 0.8 mm`):

```python
THREAD_CLEAR = 0.4   # radial; tune per printer in a test print

# Male — exact target diameter
IsoThread(major_diameter=16,           pitch=3, length=35, external=True,  ...)

# Female — oversized to leave room for the male
IsoThread(major_diameter=16 + 2*0.4,   pitch=3, length=12, external=False,
          mode=Mode.SUBTRACT, ...)
```

Tune `THREAD_CLEAR`:
- Too tight (won't thread by hand): increase by 0.1 mm and reprint just the nut
- Too loose (wobbles, no grip): decrease by 0.1 mm
- Most printers settle at **0.3-0.5 mm radial**

### Print orientation

| Part | Bed face | Why |
|------|----------|-----|
| **Thumbscrew / bolt** | knob flat on bed; thread axis vertical (+Z) | Helix layers wrap around the axis → strong against the axial clamping load |
| **Nut** | hex/square face on bed; thread axis vertical (+Z) | Same reason; bore prints upward, no support needed |
| **Lead screw** | one end on bed, axis vertical | Same |

**Never print a thread on its side.** The helix becomes a sequence of
horizontal arcs that don't bond well, and supports inside the threads
are a nightmare to remove.

### Slicer settings

- **Layer height: 0.16 mm or finer** for the threaded parts. 0.2 mm
  works but the helix surface is more obviously stepped.
- **4+ perimeters** so the thread crest material is solid instead of
  hollow.
- **30%+ infill** on the nut so thread-engagement loads don't deform it.
- Skip supports — vertical-axis threads are self-supporting.

## The "shaft at minor diameter" pattern

For external threads, `bd_warehouse` produces a shape that fills
**from minor diameter outward to major diameter**. To make a complete
threaded shaft you need a cylinder underneath.

❌ **Wrong** — shaft at major diameter, thread sits flush on top:

```python
with BuildPart() as bolt:
    Cylinder(radius=12/2, height=35)          # shaft at MAJOR — too big
    IsoThread(major_diameter=12, pitch=3, length=35, external=True)
    # Result: solid cylinder + thread crests poking BELOW the surface
    # → no actual thread profile, just a fat shaft with helix scars
```

✅ **Right** — shaft at minor diameter, thread fills out to major:

```python
with BuildPart() as bolt:
    pitch = 3
    major = 12
    minor = major - pitch        # rule of thumb for ISO/Acme/Trap (close enough for FDM)
    Cylinder(radius=minor/2, height=35,
             align=(Align.CENTER, Align.CENTER, Align.MIN))
    IsoThread(major_diameter=major, pitch=pitch, length=35, external=True,
              align=(Align.CENTER, Align.CENTER, Align.MIN))
```

The default `interference=0.2` parameter on the thread classes pushes
the thread body inward by 0.2 mm so it overlaps the shaft and fuses
cleanly. Don't change `interference` unless you know what you're
doing — for FDM, increasing `THREAD_CLEAR` (above) is what you want.

## bd_warehouse bugs to know about

These are bugs in `bd_warehouse.thread` (verified against version
shipped circa 2026). All of them produce **two disconnected solids**
in your STL — the box + a "ghost" thread floating inside the box —
which usually slices fine but is conceptually wrong, fails
booleans, and can cause weird slicer behavior at the edges.

The **diagnostic signal** for all of these bugs:

```python
import trimesh
m = trimesh.load("your_part.stl", force="mesh")
parts = m.split(only_watertight=False)
print(f"{len(parts)} solids")
# If you expected 1 solid and got 2+, one of the bugs below bit you.
```

### Bug 1: `MetricTrapezoidalThread + Mode.SUBTRACT` doesn't subtract

**Symptom:**

```python
with BuildPart() as nut:
    Box(20, 20, 10)
    MetricTrapezoidalThread(size="12x3", length=10,
                            external=False, mode=Mode.SUBTRACT)
# STL has 2 solids: solid box + free-floating female thread
```

**Root cause:** the `MetricTrapezoidalThread` (and the underlying
`TrapezoidalThread`) returns a hollow shell whose walls are too thin
for OCCT to register as overlapping the box. Boolean subtract finds
no intersection volume, so it does nothing — but the thread itself
still gets added to the part as an unrelated solid.

**Detection:** see the diagnostic above. Will reliably reproduce
with `Box(20, 20, 10) + MetricTrapezoidalThread(size="12x3", length=10,
external=False, mode=Mode.SUBTRACT)` → 2 solids.

**Fix:** **use `IsoThread` instead** for the female thread. ISO has
a slightly worse profile for FDM but at coarse pitch + large diameter
(see "FDM thread design rules" above) it prints fine, and `IsoThread`
+ `Mode.SUBTRACT` works correctly.

If you specifically need the trapezoidal profile, use a manual
Helix + `sweep` to build the thread shape yourself, or build the
female thread as ADD material *inside* a pre-bored cylinder in the
nut. (Both are more work; only do this if Iso isn't acceptable.)

### Bug 2: `IsoThread + end_finishes=("fade", "fade") + Mode.SUBTRACT` loses the subtract

**Symptom:** `IsoThread + Mode.SUBTRACT` works fine until you ask
for `end_finishes=("fade", "fade")`. Then it produces 2 solids
(the box and a ghost thread, same as Bug 1).

```python
# WORKS — 1 solid:
with BuildPart() as nut:
    Box(20, 20, 10)
    IsoThread(major_diameter=12, pitch=3, length=10,
              external=False, mode=Mode.SUBTRACT)

# BROKEN — 2 solids:
with BuildPart() as nut:
    Box(20, 20, 10)
    IsoThread(major_diameter=12, pitch=3, length=10,
              external=False,
              end_finishes=("fade", "fade"),    # ← this triggers the bug
              mode=Mode.SUBTRACT)
```

**Detection:** same diagnostic as Bug 1. Toggle `end_finishes` off
to confirm.

**Fix:** **don't pass `end_finishes` when using `external=False +
Mode.SUBTRACT`**. The default end finishes (`("fade", "square")`)
work correctly. End-of-thread aesthetics on the inside of a bore
don't matter much anyway — no one sees them.

For external threads you can still use any `end_finishes` you want;
this only bites the SUBTRACT case.

### Bug 3: `with Locations(...): IsoThread(..., Mode.SUBTRACT)` loses the subtract

**Symptom:** wrapping the thread in a `Locations` context to position
it (instead of letting it default to z=0..length) causes Mode.SUBTRACT
to fail the same way.

```python
# WORKS:
with BuildPart() as nut:
    Box(20, 20, 10, align=(Align.CENTER, Align.CENTER, Align.MIN))
    IsoThread(major_diameter=12, pitch=3, length=10,
              external=False, mode=Mode.SUBTRACT)

# BROKEN — 2 solids:
with BuildPart() as nut:
    Box(20, 20, 10, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    with Locations((0, 0, -5)):                  # ← the wrap breaks it
        IsoThread(major_diameter=12, pitch=3, length=10,
                  external=False, mode=Mode.SUBTRACT)
```

**Fix:** build the nut with the thread at the thread's *natural*
position (bottom at z=0), then translate the **entire nut** afterward:

```python
with BuildPart() as nut:
    # Match the thread's natural z=0..length frame: bottom-aligned.
    Box(NUT_OD, NUT_OD, NUT_HEIGHT,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    IsoThread(major_diameter=THREAD_DIA + 2*THREAD_CLEAR,
              pitch=THREAD_PITCH, length=NUT_HEIGHT,
              external=False, mode=Mode.SUBTRACT)

# Now move the nut wherever your assembly needs it:
nut_solid = nut.part.translate((0, 0, -NUT_HEIGHT/2))
export_stl(nut_solid, "nut.stl")
```

This isn't pretty but it's the cleanest fix that doesn't fight the
library.

### Bug 3, second variant: tapping a bore inside a LARGER existing part

The translate-the-whole-thing trick works when the threaded part is
its own standalone object (a separate nut). It **breaks down** when
you want to cut an internal thread into one specific spot of a much
larger part — like tapping an M16 hole through one corner of a clamp
body that's already 150 × 25 × 60 mm with a dozen other features.
Translating the entire body to put the bore at z=0 would also move
all the other features off-position.

**Pattern that works:** build the thread cutter in **its own
`BuildPart` context** at origin, capture the resulting Part, `.move()`
it to the desired position, then `add(..., mode=Mode.SUBTRACT)` it
inside the host part's BuildPart context. The `Locations` wrapper
is never used; positioning is via `.move()` on the Part itself.

```python
# ── Build the thread cutter outside the host part ──
# Slight axial overshoot guarantees a clean through-hole even with
# floating-point rounding at the housing top/bottom faces.
OVERSHOOT = 1.0
with BuildPart() as _thread_cutter:
    IsoThread(
        major_diameter=BORE_DIA + 2 * THREAD_CLEAR,
        pitch=THREAD_PITCH,
        length=BORE_LENGTH + 2 * OVERSHOOT,
        external=False,
        align=(Align.CENTER, Align.CENTER, Align.MIN),  # bottom at z=0
    )

# Position it where the host part wants the bore.
thread_cutter = _thread_cutter.part.move(
    Location((BORE_CX, BORE_CY, BORE_BOT_Z - OVERSHOOT))
)

# ── Subtract it from the host part ──
with BuildPart() as body:
    # ... lots of other features at their natural positions ...
    Box(150, 25, 60, ...)
    Box(...)            # spine, top jaw, arm, gusset, etc.
    add(thread_cutter, mode=Mode.SUBTRACT)   # ← tapped bore
    # ... fillets, chamfers, etc.
```

Why this works: the `IsoThread` constructor is called with no
ambient `Locations`, so the buggy code path is never entered. The
buggy code path is specifically the one that combines an external
location override with the internal-thread end-handling — neither
`.move()` on a finished Part nor `add(...)` triggers it.

> ⚠️ **But:** the `.move() + add(SUBTRACT)` pattern shown above
> can leave the bore non-watertight or, in busy multi-primitive
> bodies, can leave the inner cylinder volume **un-removed** —
> only the helical thread profile gets cut. See **Bug 4** below
> for the canonical "host body + IsoThread material as a
> `Compound`" pattern that we now recommend instead.

Bug-3 fix recap:

| You want | Use |
|----------|-----|
| Internal-threaded standalone part (a nut) | Build at origin, `.translate()` the whole part. |
| Internal-threaded bore inside a much larger part | **Use Bug 4's Compound pattern (recommended)** — single-`BuildPart` boolean fusion of host + internal `IsoThread` is unsafe. |
| External thread at any position | Plain `with Locations(...): IsoThread(external=True, ...)` works fine — bug only bites SUBTRACT. |

### Bug 4: combining a host body with an internal `IsoThread` via boolean fusion destroys the host

**Symptom (in any of three flavors):**

1. **Bore plugged.** In a tapped hole through a complex body
   (multi-`Box` body composed of top jaw + spine + housing + arm,
   etc.), helical thread crests are visible at the top and bottom
   faces of the housing — the screw started to bite — but the
   **inner cylindrical bore is solid**. Looking down the bore from
   above, you see solid material where you expected open air.
2. **Bore open, no threads.** "Cylinder SUBTRACT, then IsoThread
   ADD" produces an open through-hole but no helical thread crests
   inside it.
3. **Body destroyed entirely.** Same single-BuildPart chain as
   (2) — the IsoThread `mode=Mode.ADD` step silently *consumes the
   host body* and leaves only the helical thread material as the
   final result. The exported STL still passes a "watertight"
   check, which is what makes this so deceptive.

```python
# BROKEN — three different broken outcomes from very similar code

# Variant A: one-shot subtract — bore plugged
with BuildPart() as _cutter:
    IsoThread(major_diameter=BORE_DIA, pitch=PITCH, length=L,
              external=False, align=(Align.CENTER, Align.CENTER, Align.MIN))
cutter = _cutter.part.move(Location((CX, CY, BOT_Z)))
with BuildPart() as body:
    Box(...); Box(...); Box(...)
    add(cutter, mode=Mode.SUBTRACT)     # threads visible, bore plugged

# Variant B: cylinder cut + IsoThread ADD inside ONE BuildPart — BODY DESTROYED
with BuildPart() as body:
    Box(...); Box(...); Box(...)
    Cylinder(radius=BORE_DIA/2, height=L, mode=Mode.SUBTRACT, ...)
    IsoThread(major_diameter=BORE_DIA, pitch=PITCH, length=L,
              external=False, ...)      # ← this step EATS the host body
```

**Volume audit on a bare 20×20×16 box host (synthetic minimal repro):**

| step | operations                                            | volume   | what survives                          |
|------|-------------------------------------------------------|----------|----------------------------------------|
| 1    | `Box(20,20,16)`                                       | 6400     | host ✓                                 |
| 2    | step 1 + `Cylinder(r=8.4, SUBTRACT)`                  | 2855     | hollow box, smooth bore ✓              |
| 3    | step 1 + `IsoThread(external=False, ADD)`             | 6484     | solid box + ~84 mm³ crests in the wall (no bore) |
| 4    | step 2 + `IsoThread(external=False, ADD)`             | **876**  | ✗ host body destroyed; only the thread material survives |
| 5    | `IsoThread(external=False)` alone                     | 876      | matches step 4 — confirms the host was eaten |

Reproduces for both `Box` and `Cylinder` host shapes. The
destruction is reproducible in `bd_warehouse` circa 2026.

**Root cause / interpretation.** The `IsoThread(external=False)`
solid is, geometrically, the helical thread *material* between the
minor and major radii of an internal thread (~875 mm³ for M16×3 ×
16 mm long). Its default `interference=0.2` mm is designed to
overlap with the bore wall *of the host body* so that a slicer
(union semantics) fuses thread + bore wall into a single watertight
solid. When you instead try to merge them inside one `BuildPart`
via OCCT's algebraic boolean (the implicit `fuse()` that
`mode=Mode.ADD` runs), the OCCT operation gets the topology badly
wrong against a freshly-carved cylindrical wall and discards the
host body. **The fix is to NOT do the boolean fusion at all** —
keep host and thread as siblings in a `Compound` and let the
slicer fuse them.

**Fix — canonical Compound pattern (matches bd_warehouse docs):**

The bd_warehouse documentation states:

> *interference – Amount the thread will overlap with nut or bolt
> core. Used to help create valid threaded objects where the
> thread must fuse with another object.* **For threaded objects
> built as Compounds, this value could be set to 0.0.** Defaults
> to 0.2.

That is, multi-body Compound is an explicitly-supported authoring
pattern for internal threads. **Recommended:** keep the default
`interference=0.2` so the slicer fuses thread + bore wall; only
drop to `0.0` if you are doing downstream OCCT work that requires
non-overlapping siblings.

```python
from build123d import (BuildPart, Box, Cylinder, Compound, Locations,
                       Align, Mode)
from bd_warehouse.thread import IsoThread

# 1. Host body — bore carved at the THREAD MAJOR diameter (not minor).
#    The bore is plain cylindrical; the thread crests will sweep
#    inward from this wall toward the screw axis.
with BuildPart() as body_with_bore:
    Box(...); Box(...); Box(...)        # housing, top jaw, spine, arm, ...
    with Locations((CX, CY, BORE_BOT_Z)):
        Cylinder(radius=BORE_DIA / 2,
                 height=BORE_LEN,
                 align=(Align.CENTER, Align.CENTER, Align.MIN),
                 mode=Mode.SUBTRACT)

# 2. Thread material — a SEPARATE BuildPart, default mode=Mode.ADD
#    (no SUBTRACT, no fuse with the host). Default interference=0.2 mm
#    means the thread crests overlap into the bore wall by 0.2 mm.
with BuildPart() as body_thread_only:
    with Locations((CX, CY, BORE_BOT_Z)):
        IsoThread(major_diameter=BORE_DIA,
                  pitch=PITCH,
                  length=BORE_LEN,
                  external=False,
                  end_finishes=("fade", "fade"),
                  align=(Align.CENTER, Align.CENTER, Align.MIN))

# 3. Combine. TWO valid options:
#    (a) Algebra-mode fuse — produces ONE watertight solid.
#        REQUIRED if the .3mf will be loaded into Bambu Studio,
#        PrusaSlicer multi-body modes, or any slicer that treats
#        each .3mf object as a separate gcode-planner entity.
body_part = body_with_bore.part + body_thread_only.part

#    (b) Compound (no boolean fuse) — produces a multi-body STL/3MF.
#        Fine for STL-only workflows where the slicer auto-unions
#        overlapping shells.
# body_part = Compound(children=[body_with_bore.part,
#                                body_thread_only.part])
export_stl(body_part, "body.stl")
```

> ✅ **`Part + Part` (algebra) is the slicer-friendly default.**
> Earlier this skill recommended `Compound(children=[host, thread])`
> based on the bd_warehouse note that *"For threaded objects built
> as Compounds, [interference] could be set to 0.0."* That works for
> *STL inspection* but produces a **multi-body `.3mf`** (Mesher
> emits two `<vertices>` blocks and two `<object>` definitions).
> Bambu Studio loads such a `.3mf` as **two separate objects** and
> emits *"Conflicts of gcode paths at layer N"* + *"floating
> regions"* + *"floating cantilever"* warnings for the overlapping
> shells.
>
> The algebra-mode `Part + Part` operator runs OCCT's `fuse()`
> between two **finished** Solids. Unlike the destructive
> single-`BuildPart` `Cylinder(SUBTRACT) + IsoThread(ADD)` chain at
> the top of this section, fusing two already-built parts via `+`
> **preserves the IsoThread material**. Verified on the SKILL Bug 4
> minimal repro: `host(2853) + thread(730) → fused(3457)`, single
> watertight solid (volume = sum − 126 mm³ overlap from the 0.2 mm
> default interference).
>
> Use Compound only when you specifically want a multi-body file
> (e.g. for trimesh STL-level inspection of host vs. thread
> separately). For anything that hits a slicer, use `+`.

> ⚠️ **`end_finishes` matters for length compliance.** The IsoThread
> default `end_finishes=("fade", "square")` does NOT cleanly clip the
> thread material at `z=length` on internal threads — measured bbox
> for `IsoThread(length=16, external=False, end_finishes=("fade",
> "square"))` extends to `z=18.621`, a **2.621 mm overrun above the
> nominal length**. (Confirmed against bd_warehouse circa 2026.)
>
> Use `end_finishes=("fade", "fade")` for internal threads inside a
> bounded host — measured top is `z=15.621` (0.379 mm UNDER the
> nominal length). This matches the AcmeThread / MetricTrapezoidalThread
> default and is the safest choice when the thread sits inside a
> host body whose top face must stay flush.
>
> | end_finishes        | bbox z (length=16)        | top overrun |
> |---------------------|---------------------------|-------------|
> | `("fade", "square")` (IsoThread default) | `[0.000, 18.621]` | **+2.621** |
> | `("fade", "fade")` (recommended) | `[0.000, 15.621]` | -0.379 |
> | `("square", "square")` | `[0, 16.000]` | 0 (but emits "Boolean unable to clean" warning) |
> | `("chamfer", "chamfer")` | `[0, 16.000]` | 0 (entry chamfer for screw alignment) |
> | `("raw", "square")` | `[-2.810, 18.810]` | +2.810 (and -2.810 below) |
>
> You CANNOT boolean-trim the IsoThread material after the fact via
> `Part - Box` (algebra), `Box(SUBTRACT)` inside the same BuildPart,
> or `cut()` — all yield zero volume. The IsoThread Solid is
> "fragile" against any **subtractive** boolean. The fuse via `+`
> works because the IsoThread is the **second operand** of an
> additive op against an already-finished host. Pick the right
> `end_finishes` up front.

The fused STL is a single watertight solid. Slicer preview should show
the bore region as one solid with thread profile, not two disjoint
shells. If the slicer reports "Conflicts of gcode paths" or "floating
regions", you accidentally exported a Compound instead of the algebra
fuse — re-check the line that produces `body_part`.

**Detection — top-down section in WORLD coordinates:**

```python
import trimesh, matplotlib.pyplot as plt, numpy as np
m = trimesh.load("body.stl", force="mesh")
parts = [p for p in m.split(only_watertight=False) if p.volume > 1]
# Multiple Z planes inside the thread span:
for z in z_planes_inside_bore:
    for part in parts:
        sec = part.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        if sec is None: continue
        # IMPORTANT: do NOT use sec.to_2D() — it strips the world XY offset
        # and centers everything on origin, hiding where the bore actually is.
        for ent in sec.entities:
            pts = sec.vertices[ent.points]      # world coords
            plt.plot(pts[:, 0], pts[:, 1], '-')
```

Expect at each Z inside the thread span: the host perimeter PLUS one
or two inner loops near the screw axis. The inner loops are the bore
wall (around major radius) and the helical thread sweep (between
minor and major radii). With the algebra-fuse pattern these merge
into a single non-circular inner loop with thread crests visible as
inward bumps; with the Compound pattern they appear as two distinct
concentric loops. ZERO inner loops = plugged bore. ONE perfectly
circular inner loop with no inward bumps = open bore but no threads.

**Visual gold-standard:** a `pyvista.Plotter().add_mesh(mesh.clip(...))`
half-cut through the screw axis. An open bore with horizontal
banding visible inside the cut = real threads.

**Guardrail:** add the section check OR a cutaway render to your
project's auto-rebuild workflow. The reference project's verification
pattern lives in [`cad/headphone-hook-desk-clamp/headphone_hook.py`](../../../cad/headphone-hook-desk-clamp/headphone_hook.py)
and a worked Compound implementation lives in
[`cad/headphone-hook-desk-clamp/decisions/0007-captured-pad-and-tapped-housing.md`](../../../cad/headphone-hook-desk-clamp/decisions/0007-captured-pad-and-tapped-housing.md).

## Pattern: complete thumbscrew + captive nut + clamp body

End-to-end pattern from the reference project. Adapt the constants
to your part. (Imports, exports, and shared helpers omitted; see
`cad/headphone-hook-desk-clamp/headphone_hook.py` for the full file.)

```python
from build123d import *
from bd_warehouse.thread import IsoThread

# ── Source-of-truth constants ──
THREAD_NOMINAL_DIA = 16.0    # M16 — coarse for FDM
THREAD_PITCH       = 3.0     # 3 mm/turn, 15 layers per turn at 0.2 mm
THREAD_LENGTH      = 35.0    # full thread length on the screw
THREAD_CLEAR       = 0.4     # radial clearance for printed-on-printed
NUT_OD             = 26.0    # square nut across-flats
NUT_HEIGHT         = 12.0    # >= 4 × pitch for solid engagement
KNOB_DIA           = 40.0
KNOB_HEIGHT        = 12.0
KNOB_FLUTE_COUNT   = 16
KNOB_FLUTE_DEPTH   = 1.5
PAD_DIA            = 28.0
PAD_THICKNESS      = 6.0

# ── Captive nut: square outer, internal ISO thread ──
with BuildPart() as nut:
    Box(NUT_OD, NUT_OD, NUT_HEIGHT,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    IsoThread(
        major_diameter=THREAD_NOMINAL_DIA + 2 * THREAD_CLEAR,
        pitch=THREAD_PITCH, length=NUT_HEIGHT,
        external=False, mode=Mode.SUBTRACT,
        # no end_finishes! triggers Bug 2
    )
nut_part = nut.part.translate((0, 0, -NUT_HEIGHT / 2))

# ── Thumbscrew: knob + threaded shaft + pad ──
import math
with BuildPart() as thumbscrew:
    # Knob with finger flutes
    Cylinder(radius=KNOB_DIA / 2, height=KNOB_HEIGHT,
             align=(Align.CENTER, Align.CENTER, Align.MIN))
    for i in range(KNOB_FLUTE_COUNT):
        ang = 2 * math.pi * i / KNOB_FLUTE_COUNT
        fx = (KNOB_DIA / 2) * math.cos(ang)
        fy = (KNOB_DIA / 2) * math.sin(ang)
        with Locations((fx, fy, KNOB_HEIGHT / 2)):
            Cylinder(radius=KNOB_FLUTE_DEPTH * 1.2, height=KNOB_HEIGHT + 0.2,
                     mode=Mode.SUBTRACT,
                     align=(Align.CENTER, Align.CENTER, Align.CENTER))

    # Threaded shaft — built at MINOR diameter
    minor_dia = THREAD_NOMINAL_DIA - THREAD_PITCH
    with Locations((0, 0, KNOB_HEIGHT)):
        Cylinder(radius=minor_dia / 2, height=THREAD_LENGTH,
                 align=(Align.CENTER, Align.CENTER, Align.MIN))

    # External thread fills out to major diameter
    with Locations((0, 0, KNOB_HEIGHT)):
        IsoThread(
            major_diameter=THREAD_NOMINAL_DIA, pitch=THREAD_PITCH,
            length=THREAD_LENGTH, external=True,
            end_finishes=("fade", "fade"),    # OK on external threads
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )

    # Pad on top of the threaded shaft
    with Locations((0, 0, KNOB_HEIGHT + THREAD_LENGTH)):
        Cylinder(radius=PAD_DIA / 2, height=PAD_THICKNESS,
                 align=(Align.CENTER, Align.CENTER, Align.MIN))

# ── Body with captive-nut pocket and screw clearance hole ──
# (only the pocket + clearance hole; outer body shape is project-specific)
NUT_POCKET_TOL = 0.3
with BuildPart() as body:
    Box(50, 30, 50)         # placeholder body
    # Captive-nut pocket — square hole sized to slip the printed nut in
    Box(NUT_OD + 2 * NUT_POCKET_TOL,
        NUT_OD + 2 * NUT_POCKET_TOL,
        NUT_HEIGHT + 1,                 # +1 for slide clearance
        mode=Mode.SUBTRACT,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Vertical clearance hole through the rest of the body for the screw
    Cylinder(radius=(THREAD_NOMINAL_DIA + 2 * THREAD_CLEAR + 0.5) / 2,
             height=100, mode=Mode.SUBTRACT,
             align=(Align.CENTER, Align.CENTER, Align.CENTER))
```

Print all three parts in their natural orientation
(`Align.MIN` z = bed face). They assemble by hand: drop nut into
pocket, thread thumbscrew up from below.

## Quick reference

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Female thread comes out as a separate solid floating in the nut | Bug 1 (MetricTrapezoidalThread + SUBTRACT), Bug 2 (IsoThread + fade,fade + SUBTRACT), or Bug 3 (Locations wrapper) | Switch to IsoThread / drop end_finishes / unwrap Locations and translate after |
| External thread sits flush on a fat shaft, no thread visible | Shaft built at major diameter | Build shaft at `minor = major - pitch`; the thread fills the gap |
| Printed screw won't thread into printed nut, jams immediately | No clearance | Bump female `major_diameter` by `2 × THREAD_CLEAR` (start 0.4 mm) |
| Printed thread strips out under load | Pitch too fine for FDM, or nut too thin | Use coarser pitch (≥ 2 mm), or `NUT_HEIGHT ≥ 4 × pitch` |
| Thread looks like a smooth corkscrew, no defined crests | Pitch too coarse for diameter, or layer height too thick | Reduce pitch, or use 0.16 mm layers |
| Helix appears valid in viewer but breaks downstream booleans | OCCT helix self-intersection | Per `cad-build123d-general` § Quick reference, split into ≤180° segments — usually means using `bd_warehouse` instead of hand-rolling the helix |
| `add(MetricTrapezoidalThread(...))` raises `TypeError: ... missing 1 required positional argument: 'length'` | You called `add()` on a `BasePartObject` that auto-adds inside `BuildPart` | Just instantiate it (no `add()`); inside `BuildPart` it auto-adds |

## See Also

- bd_warehouse threads docs:
  <https://bd-warehouse.readthedocs.io/en/latest/thread.html>
- `cad-build123d-bd-warehouse` — the bd_warehouse reference, including
  the thread classes section that points you here
- `cad-build123d-general` — Helix/thread "self-intersection" gotcha
  in the Quick Reference table
- `print-bambu-studio` *(separate plugin)* — slicer settings (layer height,
  walls, infill) for printed-thread parts
- Reference project: `cad/headphone-hook-desk-clamp/` — full
  thumbscrew + captive nut + clamp body, where every bug above
  was discovered and worked around
