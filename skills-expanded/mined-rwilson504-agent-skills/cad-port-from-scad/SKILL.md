---
name: cad-port-from-scad
description: 'Port an OpenSCAD parametric script to build123d (Python) cleanly and incrementally. Covers OpenSCAD↔build123d operator equivalence, the SCAD idioms that trip up a literal port (hull/loft, intersection, taper, ternary chains), phased-bundle workflow with a deferred-features tracker, sentinel-based smoke testing for parametric scripts, and naming hygiene when source labels are misleading. USE FOR: "port this SCAD to build123d", "convert OpenSCAD to Python", "rewrite this .scad file", "I have a community OpenSCAD generator I want to extend in Python", "translate hull() to loft()", "bridge SCAD scale=[sx,sy] to build123d taper".'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["openscad","build123d","porting","migration","python"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# CAD: Port from OpenSCAD to build123d

> **Prerequisite:** Load `cad-build123d-general` first. Everything in this
> skill assumes you already know build123d's `BuildPart` / `BuildSketch`
> idioms, the sketch-on-face + extrude pattern, and the export workflow.

## Purpose

OpenSCAD has a huge community library — Thingiverse, Printables, GitHub —
of parametric generators that you'd love to extend or fix but the SCAD
syntax is its own little world. Porting one to build123d gives you:

- Real Python (loops, dicts, helpers, type hints)
- A modern OCCT kernel (better booleans, fewer mysterious failures)
- Integration with the rest of your repo's CAD toolchain (companion
  scripts, layout maps, six-view checks, CI smoke tests)

The catch: a **literal line-by-line port will not work**. SCAD's
`hull()`, `union()`, and `linear_extrude(scale=...)` operate on
different mental models than build123d's `loft()`, `add()`, and
`extrude(taper=...)`. This skill is the bag of tricks I learned the
hard way porting a 950-line SCAD generator (Harbor Freight bin
generator v26 → `cad/harbor-freight-bins/hf_bin.py`).

## Cardinal Rule #0: Phase the port, don't one-shot it

A complex SCAD source is a kitchen sink. The Harbor Freight bin
generator had:

- 2 output modes (replacement bin / factory liner)
- 5 base styles
- 2 lip styles
- 3 fill modes
- Optional scoops, label flanges, tall dividers, sacrificial supports
- 2 system depths × 5 preset bin sizes
- Stack-count math

If you try to port everything at once, you'll have a 1500-line Python
file you can't review and 12 silently-broken toggles.

**Do this instead:**

1. Read the SCAD file end-to-end first. Don't write any Python.
2. Build a **deferred-features tracker** as a markdown table mapping
   every SCAD knob/module to a feature ID (F01, F02, …) with its SCAD
   line anchor. Live document; commit it on day one.
3. Pick a Phase 1 minimum-viable subset (~25% of features) and ship
   the rest as `NotImplementedError` guards that point back to the
   tracker. Smoke-test Phase 1 hard.
4. Group remaining features into bundles (3–5 features that share
   plumbing). Each bundle = one session = one decision record.
5. Move features from "Deferred" → "Shipped" as you land them.

The end state is the same as one-shot, but every commit is reviewable
and every variant has a passing smoke test by construction.

## Operator equivalence — the foundation

These are not 1:1. Some are close enough that you can mechanically
translate; others need real thought.

| OpenSCAD | build123d | Notes |
|---|---|---|
| `union() { a; b; }` | `add(a); add(b)` (default `Mode.ADD`) | SCAD union accepts disjoint solids; build123d's `add()` requires they fuse cleanly. **Free-floating bodies are a real problem in build123d.** See `cad-build123d-general` §4. |
| `difference() { a; b; }` | `add(a); add(b, mode=Mode.SUBTRACT)` | build123d is **stateful** — the active builder is the "subject" of every op. SCAD is declarative. Different mental model. |
| `intersection() { a; b; }` | `add(a); add(b, mode=Mode.INTERSECT)` | Same reasoning. |
| `hull() { a; b; }` | `loft()` over the section sketches | **NOT EQUIVALENT.** SCAD `hull` builds a convex hull of all points in `a` and `b`. build123d `loft` builds a swept surface between *aligned planar sections*. See "Hull → Loft" below. |
| `linear_extrude(h) { ... }` | `extrude(amount=h)` on a `BuildSketch` | OK. |
| `linear_extrude(h, scale=[sx, sy]) { ... }` | `extrude(amount=h, taper=°)` | **NOT EQUIVALENT.** build123d's `taper` is **uniform** (same shrinkage in X and Y). SCAD's per-axis scale has no direct port. See "Anisotropic taper" below. |
| `rotate_extrude() { ... }` | `revolve()` | Close enough. |
| `translate([x,y,z]) child;` | `child.moved(Location((x,y,z)))` *or* `with Locations((x,y,z)): ...` | Two patterns; pick whichever reads cleaner. `Locations` is for sketches/builders; `.moved()` is for finished parts. |
| `rotate([rx,ry,rz]) child;` | `Plane(origin=..., x_dir=..., z_dir=...)` *or* `child.rotate(...)` | SCAD's Euler angles do not survive translation cleanly. Re-express the intent as a target plane (its origin + X/Z axes) and life is much easier. |
| `mirror([1,0,0]) child;` | `child.mirror(Plane.YZ)` | OK. |
| `cube([w,d,h], center=true)` | `Box(w, d, h)` | build123d boxes are centered by default. |
| `cylinder(h=h, r=r, $fn=60)` | `Cylinder(radius=r, height=h)` | build123d auto-tessellates. `$fn` has no equivalent (and you almost never need one). |
| `polygon(points)` then extrude | `with BuildLine(): Polyline(points); make_face(); extrude(...)` | OK. |
| Top-level `if (cond) { a; } else { b; }` block | An `if` branch inside `build_bin()` deciding which helper to call | SCAD's top-level `if` chooses between whole geometry trees. build123d expects a single `BuildPart` context, so the conditional moves down into the assembly. |
| `module foo(args) { ... }` | `def _build_foo(args): with BuildPart() as p: ...; return p.part` | OK. Convention: prefix internal builder functions with `_build_`. |
| `function foo(args) = expr;` | regular Python `def` | OK. |
| `$fn`, `$fa`, `$fs` | (none, automatic) | Drop. |

### Hull → Loft

SCAD's `hull()` is the most-misused operator in the SCAD-to-build123d
port. People assume it's the same as `loft()` because both produce a
"smooth blend between two shapes". **They are not the same operation.**

| Property | SCAD `hull()` | build123d `loft()` |
|---|---|---|
| Input | Any number of disjoint 3D solids | An ordered list of planar sections (sketches), all in the same builder |
| Behavior | Convex hull of every vertex in every input | Swept surface connecting consecutive sections in order |
| Tolerates degenerate input | Yes (silently ignores collinear / coincident points) | **No** — coincident sections raise `OCP.OCP.StdFail.StdFail_NotDone: BRep_API: command not done` |
| Result for 2 cubes touching at an edge | A single chamfered solid | Often fails or produces wrong topology |

**The translation pattern that mostly works:**

```python
# SCAD
# hull() {
#   translate([0, 0, 0])  rounded_rect(wb, db, 0.1, cr_b);
#   translate([0, 0, h])  rounded_rect(wt, dt, 0.1, cr_t);
# }

# build123d
with BuildPart() as p:
    with BuildSketch(Plane.XY):
        RectangleRounded(wb, db, cr_b)
    with BuildSketch(Plane.XY.offset(h)):
        RectangleRounded(wt, dt, cr_t)
    loft()
```

**The trap:** if `wb == wt` and `db == dt` and `cr_b == cr_t`, the two
sketches are coincident and `loft()` fails. This actually happened in
the Harbor Freight port: insert mode forced `LIP_OVERHANG = 0`, which
made the chamfer ramp's two sections identical, which crashed OCCT
deep inside an unrelated-looking call site.

**Defensive code for the coincident-section case:**

```python
if section_a == section_b:        # or any equality test that fits
    # Degenerate: just extrude the section
    with BuildSketch(Plane.XY):
        Section()
    extrude(amount=h)
else:
    with BuildSketch(Plane.XY):
        SectionA()
    with BuildSketch(Plane.XY.offset(h)):
        SectionB()
    loft()
```

### Anisotropic taper

SCAD: `linear_extrude(height=H, scale=[sx, sy])` shrinks the section
by `sx` along X and `sy` along Y independently. build123d's
`extrude(taper=θ)` uses a **single angle**, applied uniformly.

For a thin support line that's wide at the bed and narrow at the top
(SCAD's pattern for sacrificial supports), there's no perfect
equivalent. Pragmatic options:

1. **Use uniform taper.** Compute the taper angle that matches the
   thin-axis shrinkage; the long axis ends up slightly tapered too.
   For a support that snaps off, this is fine. The Harbor Freight port
   went this route — the line that used to be `[w, line_w]` becomes a
   uniformly-tapered slab.

2. **Build the per-axis shape via two lofts.** Loft from a wide
   rectangle at the bed to a narrow rectangle at the top, where the
   "narrow" only changes the X dimension. Repeat orthogonally. More
   accurate but doubles the loft count.

3. **Do an XY-anisotropic scale of a uniformly-tapered prism.**
   `tapered.scale((sx, 1, 1))`. Works for symmetric shapes; fails
   if the prism has features that move with the scale.

Which to choose depends on whether the geometry is structural or
cosmetic. Document the choice in a decision record so future-you
remembers there was an option.

### Ternary chains

SCAD source frequently looks like this (from the HF generator):

```scad
pre_w = (preset == "HF_20_Small") ? p20_s_w :
        (preset == "HF_20_Med")   ? p20_m_w :
        (preset == "HF_20_Large") ? p20_l_w :
        (preset == "HF_8_Small")  ? p8_s_w  :
        (preset == "HF_8_Large")  ? p8_l_w  : 53;
```

This is a dictionary lookup wearing a fancy hat. **Always convert to a
`dict`** in Python:

```python
PRESETS = {
    "HF_20_Small": (38.0, 53.5),
    "HF_20_Med":   (78.5, 53.5),
    # ...
}
final_w_top, final_d_top = PRESETS[preset]
```

The dict gives you:

- `KeyError` for typos (SCAD silently falls through to the default)
- A single source of truth (SCAD often duplicated the chain for `pre_w`,
  `pre_d`, `int_w_target`, `int_d_target` …)
- Easy iteration when you want to e.g. validate every preset

## Workflow: turning a SCAD file into a working Python file

### Step 1 — read the source, then write a tracker

Don't open a Python editor yet. Read the SCAD file end-to-end and
build a markdown table:

```markdown
## Deferred features

| # | Feature | SCAD anchor | Notes |
|---|---|---|---|
| F01 | HF 8 Deep system (97 mm slots, 4.5 mm taper) | `case_type == "HF_8_Deep"`, constants `TAPER_8`, `WALL_8`, `HEIGHT_8` | HF8 presets in Phase 1 produce HF20-tapered bins of right footprint. |
| F02 | Insert / liner mode | `is_insert`, `auto_internal_dims`, `int_w_target` | Forces Flat base + Standard lip + no overhang automatically. |
| ... |
```

Each row is a feature ID, a one-line description, the SCAD
identifier(s) that implement it, and any notes. **This is the most
important file you'll create.** It's your roadmap and your "remaining
work" list.

### Step 2 — capture the source as a reference artifact

Copy the SCAD file into `<project>/reference/<name>.scad` so it lives
under version control alongside the port. This lets reviewers compare
SCAD lines to Python lines without leaving the repo, and it pins the
exact source version you ported (the upstream may evolve).

Mark the file read-only in your README — you don't edit the reference,
you edit the Python.

### Step 3 — Phase 1: minimum viable port

Pick the smallest subset that produces an interesting STL. For the HF
generator that was: replacement bin, one slot system, one base style,
one lip style, one fill mode, the default preset. ~400 lines of
Python including all the design/test/production scaffolding.

Add a guard block near the top of the script:

```python
if OUTPUT_TYPE != "Replacement_Bin":
    raise NotImplementedError(
        f"OUTPUT_TYPE={OUTPUT_TYPE!r} is deferred "
        "(see decisions/0002-deferred-scad-features.md F02 'Insert mode')."
    )
```

The pointer to the deferred-features doc is the key — when someone
flips a knob you haven't ported, they should not have to grep the SCAD
source to figure out why it broke.

### Step 4 — bundle remaining features into reviewable phases

Group features that share plumbing. From the HF port:

- **Bundle A** (Systems + fill): HF8 system + Solid_Block fill +
  Custom_Depth fill + global height adjust. ~80 lines.
- **Bundle B** (Bases): Peg holes + Flat base + pegs-only diagnostic.
  ~60 lines.
- **Bundle C** (Scoops). ~100 lines, all geometry.
- **Bundle D/E/F/G/H** for the more complex remaining features.

3–5 bundles is the sweet spot. Each bundle is one session, gets one
decision record (`NNNN-phaseX-bundle-description.md`), and ships with
the smoke test extended to cover its variants.

### Step 5 — write the smoke test FIRST when adding a bundle

For parametric scripts, you cannot tell if a bundle landed correctly
just by running the default config. The HF port has 25+ variants;
each bundle adds 2–4. Add the variants to the smoke test
**before** you write the geometry, so the moment a bundle compiles you
have something to validate.

See "Sentinel-based smoke test" below for the pattern.

### Step 6 — close the loop with cross-checks

When the SCAD source has hand-calipered measurements and you can find
the original product's spec sheet (manufacturer page, retail listing,
PDF), cross-check the calibrated numbers. You will sometimes find:

- The SCAD calibration is correct (good — pin it down with a comment
  citing the spec).
- The SCAD calibration is off by ~1 mm (ask: print tolerance, or did
  the SCAD author measure a different revision of the part?).
- The SCAD generator is missing a variant (e.g. the HF "Small case"
  was missing entirely from the SCAD; only adding the spec data
  surfaced this).

This step also unlocks **better names** — the SCAD's `HF_20_*` /
`HF_8_*` made sense to its author but obscured that the "8" case is
the **Large** physical case (it has fewer bins because each is
bigger). Spec-data-informed renaming is its own small phase.

## Sentinel-based smoke test for parametric scripts

A SCAD-style parametric script has many top-level parameters that
cascade through validators and derived dimensions. To test variants
you cannot just `import` the module and patch attributes — the
derived block already ran with the defaults.

The pattern that works:

```python
# tests/smoke_test.py
from pathlib import Path
import subprocess, sys, os

PROJECT_DIR = Path(__file__).resolve().parent.parent

# A line that appears EXACTLY ONCE and AFTER all default parameter
# assignments. Pick something distinctive in your script.
SENTINEL = 'BED_FACE = "-Z"'

VARIANTS = [
    ("01 default", "test_01_default.stl", ""),
    ("02 alt preset", "test_02_alt.stl", "PRESET = 'OTHER'"),
    ("03 multi-knob", "test_03_combo.stl",
     "BASE_STYLE = 'Flat'\nLIP_STYLE = 'Gridfinity_Flange'"),
]

SHIM = r"""
import sys
sys.path.insert(0, r"{project_dir}")
src_path = r"{src_path}"
src = open(src_path, "r", encoding="utf-8").read()
sentinel = {sentinel!r}
overrides = {overrides!r}
injected = sentinel + "\n# --- smoke test overrides ---\n" + overrides + "\n"
src = src.replace(sentinel, injected, 1)
import types
mod = types.ModuleType("the_script")
mod.__file__ = src_path
mod.__name__ = "__main__"          # so the script's main() block runs
sys.modules["the_script"] = mod
sys.modules["__main__"] = mod
exec(compile(src, src_path, "exec"), mod.__dict__)
"""

def run_variant(label, stl_name, overrides):
    full = (f"EXPORT_MODE = 'production'\n"
            f"STL_NAME = {stl_name!r}\n" + (overrides + "\n" if overrides else ""))
    shim = SHIM.format(project_dir=str(PROJECT_DIR),
                       src_path=str(PROJECT_DIR / "the_script.py"),
                       sentinel=SENTINEL, overrides=full)
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run([sys.executable, "-c", shim],
                          capture_output=True, text=True,
                          encoding="utf-8", env=env)
    return proc.returncode == 0

# ... iterate, report pass/fail ...
```

### Why this and not unittest / pytest fixtures

- Re-importing a module after `setattr(mod, key, value)` does **not**
  re-run the module body, so derived dimensions aren't recomputed.
- `importlib.reload()` re-runs the module body but with the
  *original* defaults, so your patches don't apply.
- Each variant in its own subprocess means a hard crash in one
  variant doesn't poison the rest.
- The shim works on any parametric script that has a sentinel and
  a `main()` body gated on `__name__ == "__main__"`.

### Pitfalls when first wiring up the test

| Symptom | Cause | Fix |
|---|---|---|
| All variants run with default params | Sentinel placed BEFORE some default assignment in the script (the late default re-binds your override) | Pick a sentinel near the END of the parameter block |
| `main()` doesn't run, so STL never exports | `__name__ == "__main__"` guard fails because the shim left `__name__ == "the_script"` | Set `mod.__name__ = "__main__"` and `sys.modules["__main__"] = mod` in the shim |
| Subprocess fails silently | `print()` raises `UnicodeEncodeError` on Windows when stdio is `cp1252` | Set `env["PYTHONIOENCODING"] = "utf-8"` |
| Sentinel "found" but overrides don't take effect | Your `replace()` was a no-op because the sentinel was inside an `f-string` or a comment | Pick a sentinel that's a real assignment statement |
| Multi-knob overrides splice mid-line | You used an unquoted multiline string with a single `replace()` | Use `repr()` (`{overrides!r}`) so the multiline string is properly quoted |

## Naming hygiene during the port

The SCAD authors' names are not your names. Translate them as you go:

1. **Drop SCAD-specific abbreviations** that don't survive into Python
   convention. SCAD's `$fn`, `$fs`, `$fa` go away entirely. SCAD's
   `_$_` prefix on private vars (when present) becomes Python's
   leading underscore.

2. **Resist re-using cryptic SCAD names** just because the SCAD source
   used them. `HF_8_Med` makes sense once you read the SCAD's intro
   comment; it's hostile to anyone who didn't. Better:
   `LARGE_CASE_MEDIUM_BIN`. Document the rename in a decision record.

3. **Add aliases for back-compat** when renaming user-facing constants
   that may be in someone's notebook or snippet:

```python
# Old SCAD-era names still work as aliases
TAPER_20 = SHALLOW_SLOT_TAPER
TAPER_8  = DEEP_SLOT_TAPER
PRESETS["HF_20_Med"] = PRESETS["MEDIUM_CASE_MEDIUM_BIN"]
```

4. **Helper functions named after the wrong thing** are worse than
   ones named after nothing. The HF port had `_is_hf8()` — the test
   actually meant "is this the deep slot system?" but the name made it
   look like it tested for "the 8-bin case". Renamed to
   `_is_deep_slot_system()` with the old name kept as alias.

5. **One commented ASCII-art table at the top of the file** beats ten
   tiny per-constant comments scattered through the file. The HF
   port's two tables (case lineup + bin types catalog) made the rest
   of the file readable without context.

## Defensive validation up front

SCAD silently does nothing when given a bad knob value. build123d
either raises a deep OCCT error or — worse — produces wrong geometry
silently. Always add validators near the top of the script:

```python
_VALID_BASE_STYLES = ("Standard_Pegs", "Standard_Pegs_With_Support",
                      "Peg_Holes", "Gridfinity_Chamfer", "Flat")
if BASE_STYLE not in _VALID_BASE_STYLES:
    raise ValueError(
        f"Unknown BASE_STYLE={BASE_STYLE!r}; valid: {_VALID_BASE_STYLES}"
    )

# Cross-knob constraints
if IS_INSERT and DIMENSION_MODE != "Presets":
    raise NotImplementedError(
        "Insert mode currently requires DIMENSION_MODE = 'Presets' "
        "(needs the calibrated PRESET_INTERNALS table)."
    )
```

The error messages should:

- Echo the bad value (`{X!r}`)
- List the valid values
- Point at the deferred-features doc when the answer is "we haven't
  built that yet"

A good validator block at the top saves more debugging time than any
amount of geometry-helper polish.

## Cascading "active" parameters

SCAD frequently has lines like:

```scad
active_base_style    = (is_insert) ? "Flat"     : base_style;
active_lip_overhang  = (is_insert) ? 0          : lip_overhang;
active_lip_style     = (is_insert) ? "Standard" : lip_style;
active_corner_radius = (is_insert) ? corner_radius
                                   : max(0.5, corner_radius - active_factory_wall);
```

Each setting cascades from a single user choice. Two bad ports of this
pattern:

- **Bad #1:** sprinkle `if IS_INSERT:` checks throughout `build_bin()`.
  The cross-cutting concern bleeds into every helper.
- **Bad #2:** rebind the user-facing constant
  (`BASE_STYLE = "Flat"`). Now `print(BASE_STYLE)` lies about what the
  user asked for.

**The right pattern:** centralize the cascade in the validator block,
right after the cross-knob constraints. Be explicit that a setting was
overridden:

```python
IS_INSERT = (OUTPUT_TYPE == "Insert_For_Factory_Bin")
if IS_INSERT:
    BASE_STYLE = "Flat"            # forced by insert mode
    LIP_STYLE = "Standard"         # forced
    LIP_OVERHANG = 0.0             # forced (insert hugs factory wall)
```

Document the forced values in the param's docstring so users grepping
"why is my LIP_OVERHANG ignored" land in the right place.

## Map the conditional assembly

SCAD's top-level `if (generate_pegs_only) { ... } else { union() { ... } }`
chooses between whole geometry trees. build123d wants a single
`BuildPart`, so the conditional moves down:

```python
def main():
    if GENERATE_PEGS_ONLY:
        layout = _build_pegs_only_layout()
        export_stl(layout, EXPORT_DIR / "pegs_only.stl")
        return     # short-circuit; skip the bin assembly entirely
    bin_part = build_bin()
    # ... export, inventory, sidecar ...
```

If a SCAD module is invoked from multiple places (`generate_pegs(...)`
inside both the body and the supports branch), the Python equivalent
is: **one `_build_pegs()` helper, called from `build_bin()` everywhere
the SCAD did**. Keep the geometry source single-sourced; let the
`build_bin()` flow control choose where it goes.

## Quick reference — common SCAD-port bugs and their fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| `OCP.OCP.StdFail.StdFail_NotDone: BRep_API: command not done` deep in `loft()` | Two `BuildSketch` sections in the loft are coincident (often when a parameter goes to 0) | Branch the helper: when sections are equal, `extrude` instead of `loft` |
| Geometry "looks right" but slicer reports floating bodies | Direct port of SCAD `union()` of touching solids; build123d didn't fuse them | Sketch-on-face + extrude (see `cad-build123d-general` §4) |
| Off-centre feature ends up mirrored | SCAD `translate([0, -d, 0])` ported to a `Plane` whose normal flipped Y | Verify with a six-view check; negate the local Y in `Locations(...)` |
| Variant works in isolation, fails in smoke test | Smoke test's sentinel is BEFORE the default that gets re-bound | Move sentinel to end of param block |
| Smoke variant prints inventory but exports a stale STL | Subprocess shim didn't trigger `main()` because `__name__ != "__main__"` | Set `mod.__name__ = "__main__"` and `sys.modules["__main__"] = mod` |
| Validator says "unknown PRESET" for a name the user copied from the SCAD source | You renamed the preset but didn't add the back-compat alias | `PRESETS[old_name] = PRESETS[new_name]` in a `_PRESET_ALIASES` loop |
| Sacrificial support lines look right at the bed but wrong at the top | `linear_extrude(scale=[sx, sy])` doesn't translate to uniform `taper=` | Pick: uniform taper (lossy), two orthogonal lofts, or post-extrude scale |
| Print orientation summary missing a base style | New base style added in a bundle but `bed_note` dict in `main()` not extended | Extend the dict and add the case to the smoke test |

## Anti-patterns to call out before they happen

1. **"I'll just port the modules in source order"** — you'll write
   helpers for features Phase 1 doesn't use, then break them when
   Phase 2 actually needs them. Port driven by the assembly tree, not
   by SCAD line order.

2. **"I'll skip the smoke test, it's a 5-knob script"** — by Phase 3
   it's a 25-knob script and the cross-feature interactions
   (insert-mode forcing zero overhang breaking the lip loft) only
   show up in the variant matrix.

3. **"I'll preserve the SCAD names so people can find things"** —
   you'll preserve the SCAD's *bad* names that took you a week to
   decode. Rename, document the rename, alias the old name. Your
   future-self contributors are users too.

4. **"`hull()` is just `loft()` with rounding"** — see Hull → Loft
   above. The OCCT crashes when you act on this assumption are not
   informative.

5. **"I'll defer the deferred-features doc until later"** — without
   it, every new contributor to your port has to read the SCAD source
   from scratch. The doc IS the port plan; write it day one.

## See Also

- Foundational build123d patterns: `cad-build123d-general`
- Reading existing meshes (different problem, similar discipline):
  `cad-reverse-engineer-stl`
- Real-world example: `cad/harbor-freight-bins/` — full port of a
  950-line SCAD generator, with phase decisions in `decisions/`
- OpenSCAD docs: <https://openscad.org/documentation.html>
- build123d docs: <https://build123d.readthedocs.io/>
