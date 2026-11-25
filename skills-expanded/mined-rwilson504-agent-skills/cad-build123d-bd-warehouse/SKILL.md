---
name: cad-build123d-bd-warehouse
description: 'bd_warehouse — the comprehensive parametric part library for build123d (by the build123d author Gumyr). Covers fasteners (nuts/screws/washers + ClearanceHole/TapHole/InsertHole), bearings, gears, sprockets, threads, pipes, flanges, OpenBuilds parts. USE FOR: bolt, screw, nut, washer, hex nut, socket-head cap screw, clearance hole, tap hole, threaded hole, heat-set insert, ball bearing, press-fit hole, simple gear, sprocket, pipe, flange, OpenBuilds; also points to py_gearworks / bd_vslot / bd_beams_and_bars / superellipses for niches outside bd_warehouse.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["build123d","bd-warehouse","fasteners","bearings","gears","threads"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# bd_warehouse — Parametric Part Library for build123d

> **Prerequisite:** Load `cad-build123d-general` first — bd_warehouse parts
> are returned as build123d `Part` objects and follow the same API conventions.

## Purpose

Before modeling a common mechanical component from scratch, check whether
`bd_warehouse` already provides a parametric version. It is the
most-comprehensive build123d-native part library, written by the build123d
author (Gumyr), and covers the vast majority of "I need a standard part"
requests an agent will see.

This skill is the **bd_warehouse reference**. The `Other build123d-compatible
libraries` appendix at the end points to a handful of niche libraries
(py_gearworks for advanced gears, bd_vslot for V-Slot rails, etc.) and the
separate `cad-partcad-repository` skill for the wider community-parts
catalog.

## When to Use This Skill

- The user asks for a **bolt, screw, nut, washer, bearing, simple gear,
  sprocket, pipe, flange, helical thread, or heat-set insert hole**.
- The user says *"is there already a part for …?"* or *"I don't want to
  model X from scratch"*.
- You're about to hand-model a standard mechanical component — check here
  first.
- Need an *advanced* gear (helical, bevel, cycloid, profile shift, backlash
  control)? Bounce out to py_gearworks via the appendix below.
- Need a community part that isn't on bd_warehouse (e.g. an OpenVMP robot
  arm, a piece of furniture)? Bounce out to `cad-partcad-repository`.

---

## Install

```bash
pip install git+https://github.com/gumyr/bd_warehouse
```

> ⚠️ Install from git — `bd_warehouse` is not currently published to PyPI.
> The git source tracks build123d's API closely; pinning a commit is wise
> for reproducibility.

## Sub-packages

| Sub-package | What it provides | Key classes |
|-------------|-----------------|-------------|
| `fastener` | Nuts, screws, washers, custom holes | `HexNut`, `SocketHeadCapScrew`, `CounterSunkScrew`, `PlainWasher`, `HeatSetNut`, `ClearanceHole`, `TapHole`, `InsertHole`, `ThreadedHole` |
| `bearing` | Ball bearings, press-fit holes | `SingleRowDeepGrooveBallBearing`, `PressFitHole` |
| `gear` | Parametric gears (simple) — for helical/bevel/cycloid go to py_gearworks | (see docs) |
| `flange` | NPS / class-rated pipe flanges | (see docs) |
| `pipe` | NPS-standard parametric pipes | (see docs) |
| `thread` | Helical threads (ISO, Acme, Metric Trapezoidal, Plastic Bottle) | `IsoThread`, `AcmeThread`, `MetricTrapezoidalThread`, `PlasticBottleThread` |
| `sprocket` | Parametric sprockets | `Sprocket` |
| `open_builds` | OpenBuilds V-slot ecosystem parts | (see docs) |

> **For practical FDM-printable threads** (thumbscrews, captive nuts,
> printed-on-printed fits) load `cad-build123d-printed-threads` after
> this skill — it covers the patterns and the bd_warehouse thread bugs.

## Fastener Quick Reference

### Discovering available parts

```python
from bd_warehouse.fastener import Nut, HexNut, Screw, SocketHeadCapScrew

# List all nut subclasses
Nut.__subclasses__()

# List types for a class
HexNut.types()          # {'iso4033', 'iso4032', 'iso4035'}

# List sizes for a type
HexNut.sizes("iso4032") # ['M1.6-0.35', 'M2-0.4', ..., 'M48-5']

# Find all fasteners that come in M6
Nut.select_by_size("M6-1")
Screw.select_by_size("M6-1")
```

### Creating fasteners

```python
from build123d import *
from bd_warehouse.fastener import HexNut, SocketHeadCapScrew, SetScrew

nut       = HexNut(size="M3-0.5", fastener_type="iso4032")
screw     = SocketHeadCapScrew(size="M6-1", fastener_type="iso4762", length=16)
setscrew  = SetScrew(size="M6-1", fastener_type="iso4026", length=10 * MM)

# Imperial sizes work too
cap_screw = SocketHeadCapScrew(
    size="#6-32", fastener_type="asme_b18.3", length=(1/2) * IN
)
```

### Custom holes (the real power feature)

```python
from bd_warehouse.fastener import (
    ClearanceHole, TapHole, InsertHole, HeatSetNut, SocketHeadCapScrew,
)

screw = SocketHeadCapScrew(size="M2-0.4", length=16)

with BuildPart() as block:
    Box(50, 50, 10)
    with Locations((0, 0, 10)):
        # Clearance hole sized to the screw — no manual dimensions needed
        ClearanceHole(fastener=screw, fit="Normal")

# For 3D-printed heat-set inserts
insert = HeatSetNut(size="M3-0.5-Standard", fastener_type="McMaster-Carr")
with BuildPart() as post:
    Cylinder(radius=5, height=10)
    with Locations((0, 0, 10)):
        InsertHole(fastener=insert)
```

### Pillow block example (bearing + fasteners)

```python
import copy
from bd_warehouse.bearing  import PressFitHole, SingleRowDeepGrooveBallBearing
from bd_warehouse.fastener import ClearanceHole, SocketHeadCapScrew
from build123d import *

cap_screw = SocketHeadCapScrew(size="M2-0.4", length=16, simple=False)
bearing   = SingleRowDeepGrooveBallBearing(size="M8-22-7")

with BuildPart() as pillow_block:
    with BuildSketch():
        RectangleRounded(50, 30, 2)
    extrude(amount=10)
    with Locations((0, 0, 10)):
        PressFitHole(bearing=bearing, interference=0.025 * MM)
        with GridLocations(38, 18, 2, 2):
            ClearanceHole(fastener=cap_screw)
```

## Class Reference

### Nut Classes

| Class | Standards |
|-------|-----------|
| `DomedCapNut` | din1587 |
| `HeatSetNut` | McMaster-Carr, Hilitchi |
| `HexNut` | iso4032, iso4033, iso4035 |
| `HexNutWithFlange` | din1665 |
| `UnchamferedHexagonNut` | iso4036 |
| `SquareNut` | din557 |

### Screw Classes

| Class | Standards |
|-------|-----------|
| `ButtonHeadScrew` | iso7380_1 |
| `ButtonHeadWithCollarScrew` | iso7380_2 |
| `CheeseHeadScrew` | iso14580, iso7048, iso1207 |
| `CounterSunkScrew` | iso2009, iso14582, iso14581, iso10642, iso7046 |
| `HexHeadScrew` | iso4017, din931, iso4014 |
| `HexHeadWithFlangeScrew` | din1662, din1665 |
| `PanHeadScrew` | asme_b_18.6.3, iso1580, iso14583 |
| `PanHeadWithCollarScrew` | din967 |
| `RaisedCheeseHeadScrew` | iso7045 |
| `RaisedCounterSunkOvalHeadScrew` | iso2010, iso7047, iso14584 |
| `SetScrew` | iso4026 |
| `SocketHeadCapScrew` | iso4762, asme_b18.3 |

### Washer Classes

| Class | Standards |
|-------|-----------|
| `PlainWasher` | iso7094, iso7093, iso7089, iso7091 |
| `ChamferedWasher` | iso7090 |
| `CheeseHeadWasher` | iso7092 |
| `InternalToothLockWasher` | din6797, asme_b18.21.1 |

### Hole Types

| Hole Class | Purpose | Key params |
|------------|---------|------------|
| `ClearanceHole` | Through-hole for bolt to pass freely | `fastener`, `fit` (Close/Normal/Loose), `counter_sunk`, `captive_nut` |
| `TapHole` | Pre-drilled for tapping threads | `fastener`, `material` (Soft/Hard), `fit` |
| `ThreadedHole` | Hole with internal threads | `fastener`, `material`, `depth` (required) |
| `InsertHole` | Sized for heat-set inserts (3D print) | `fastener` (HeatSetNut only), `manufacturing_compensation` |

### Thread Classes

`IsoThread`, `AcmeThread`, `MetricTrapezoidalThread`, `TrapezoidalThread`,
`PlasticBottleThread`, plus the base `Thread` class for arbitrary helical
profiles.

> See `cad-build123d-printed-threads` for the FDM-printable patterns,
> the `interference` parameter, the `end_finishes` length-overrun gotcha,
> the algebra-fuse vs Compound multi-body trade-off, and the bugs that
> bite trapezoidal-thread `Mode.SUBTRACT` operations.

## Performance Tip

All fastener classes accept `simple=True` (default) which omits thread
geometry for dramatically faster rendering. Only set `simple=False` for
final renders or assembly validation.

## Docs

- Full docs: <https://bd-warehouse.readthedocs.io/en/latest/>
- Fasteners: <https://bd-warehouse.readthedocs.io/en/latest/fastener.html>
- Bearings: <https://bd-warehouse.readthedocs.io/en/latest/bearing.html>
- Gears: <https://bd-warehouse.readthedocs.io/en/latest/gear.html>
- Threads: <https://bd-warehouse.readthedocs.io/en/latest/thread.html>
- Source: <https://github.com/gumyr/bd_warehouse>

---

## Other build123d-compatible part libraries

Brief pointers to libraries that handle niches `bd_warehouse` does not.
Listed here so the agent has the catalog in one place; load the linked
external docs for full API details.

### py_gearworks (advanced gears)

By GarryBGoode. Use this when `bd_warehouse.gear` isn't enough.

| Capability | bd_warehouse `gear` | py_gearworks |
|---|:---:|:---:|
| Spur | ✓ | ✓ |
| Helical | limited | ✓ |
| Bevel | ✗ | ✓ |
| Cycloid | ✗ | ✓ |
| Profile shift | ✗ | ✓ |
| Backlash control | ✗ | ✓ |
| `mesh_to(other)` positioning | ✗ | ✓ |

```bash
pip install git+https://github.com/GarryBGoode/py_gearworks
```

```python
from py_gearworks import SpurGear

g1 = SpurGear(number_of_teeth=12, module=2, height=4, profile_shift=0.3)
g2 = SpurGear(number_of_teeth=23, module=2, height=4)
g1.mesh_to(g2, target_dir=UP, backlash=0.1, angle_bias=1)

part_1 = g1.build_part()  # build123d Part
part_2 = g2.build_part()
```

Docs: <https://gggears.readthedocs.io/en/latest/>

**Rule of thumb:** Use `bd_warehouse` for sprockets and simple gears
alongside fasteners. Use `py_gearworks` for anything with profile shift,
bevel gears, helical meshing, or backlash control.

### bd_vslot (V-Slot 2020 linear motion)

By James Keal. V-Slot 2020 rails, wheels, sliding T-nuts, end caps, build
plates, common bearings (625, 688, 105).

```bash
pip install bd-vslot
```

Docs: <https://bd-vslot.readthedocs.io/>

### bd_beams_and_bars (structural sections)

By ExperimentsLabs. Flat bars, IPE/HEA/HEB/HEM/IPN beams, L bars,
rectangle/round tubes, T bars, UPE/UAP/UPN beams.

```bash
pip install git+https://gitlab.com/experimentslabs/3d/bd_beams_and_bars.git
```

```python
from bd_beams_and_bars.profiles.flat_bars import Bar, Standards, Definition

part   = Bar(Standards.LFL.LFL_160x5, 500)
custom = Bar(Definition(w=43, h=9), 500)
```

Docs: <https://bd-beams-and-bars.3d.experimentslabs.com/>

> For round pipes specifically, `bd_warehouse.pipe` is usually a better
> fit — NPS-standard parametric pipes with joints.

### Superellipses & superellipsoids

By fanf2. Single-file Python module, not a pip package — copy
[`superellipse.py`](https://github.com/fanf2/kbd/blob/model-b/keybird42/superellipse.py)
into your project. Smooth alternative to rounded rectangles, useful for
typeface-style key caps, app-icon-style clipping, organic phone-case
shapes.

### Public PartCAD repository

A package-manager-style ecosystem with hundreds of community-published
parts and assemblies (electrical, electromechanics, electronics,
furniture, medical, robotics, std, storage). Includes bd_warehouse parts,
plus much more. Browse: <https://partcad.org/repository>.

> **Don't use this skill for PartCAD specifics.** The
> [`cad-partcad-repository`](../cad-partcad-repository/SKILL.md) skill
> covers `pip install partcad`, `pc.get_part_build123d(...)`, the
> CLI, and the AI-generated-part workflow. This entry is here only as
> a pointer.

---

## Quick Decision Table

| "I need a …" | Library | Skill |
|---|---|---|
| Bolt / screw / nut / washer | `bd_warehouse.fastener` | this skill |
| Heat-set insert hole (3D print) | `bd_warehouse.fastener.InsertHole` | this skill |
| Ball bearing / press-fit hole | `bd_warehouse.bearing` | this skill |
| Simple spur gear / sprocket | `bd_warehouse.gear` / `bd_warehouse.sprocket` | this skill |
| Helical / bevel / cycloid gear, profile shift, backlash | `py_gearworks` | this skill (appendix) |
| Pipe / flange (NPS) | `bd_warehouse.pipe` / `bd_warehouse.flange` | this skill |
| Helical thread (ISO, Acme, …) | `bd_warehouse.thread` | this skill + `cad-build123d-printed-threads` |
| Practical FDM-printable thread / thumbscrew / captive nut | `bd_warehouse.thread` (with project patterns) | `cad-build123d-printed-threads` |
| V-Slot 2020 rail / wheel / nut | `bd_vslot` | this skill (appendix) |
| Structural beam / bar | `bd_beams_and_bars` | this skill (appendix) |
| Superellipse / squircle shape | `superellipse.py` (copy into project) | this skill (appendix) |
| Browse / install community parts | PartCAD package manager + repo | `cad-partcad-repository` |

---

## See Also

- Official build123d listing: <https://build123d.readthedocs.io/en/latest/external.html#part-libraries>
- `cad-build123d-general` — foundational build123d API + idioms (load first)
- `cad-build123d-printed-threads` — practical FDM-printable thread patterns + bd_warehouse thread bugs
- `cad-partcad-repository` — sibling skill, covers the PartCAD ecosystem in depth
