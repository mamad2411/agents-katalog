---
name: cad-partcad-repository
description: 'PartCAD — package manager + public repository of community CAD parts and assemblies (https://partcad.org/repository). Browse hundreds of parts (electrical, electronics, electromechanics, furniture, medical, robotics, std, storage), import them into build123d via `pc.get_part_build123d(...)`, publish your own packages. Covers install, CLI (`pc list/info/inspect/export`), Python API (build123d / CadQuery / generic), partcad.yaml package authoring, AI-generated parts (Google / OpenAI), assembly composition (.assy). USE FOR: PartCAD, partcad, find a community part, browse part catalog, public CAD repo, import community part into build123d, pc.get_part_build123d, pc inspect, pc export, pc list parts, AI-generated CAD model, ai-cadquery, ai-openscad, publish CAD package, OpenVMP robot.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["partcad","build123d","part-library","package-manager","cad"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# PartCAD — Public CAD Repository for build123d

> **Prerequisite:** Load `cad-build123d-general` first if the user is going
> to consume PartCAD parts in a build123d script.
>
> **Sibling skill:** `cad-build123d-bd-warehouse` covers Gumyr's
> bd_warehouse part library directly (and is what an agent should reach
> for first for nuts/bolts/bearings). PartCAD's repository *includes*
> bd_warehouse parts, but is much broader — load this skill when the
> user wants a community part outside the bd_warehouse scope, wants to
> publish their own CAD package, or wants to use PartCAD's AI-generated
> part workflow.

## Purpose

PartCAD is a **package manager and public repository for parametric CAD
models**. It treats CAD parts and assemblies the way npm treats
JavaScript packages or pip treats Python packages: a versioned
namespace, a CLI to install/inspect/export, and a public catalog at
<https://partcad.org/repository> with hundreds of community-published
items.

This skill covers:

- Installing PartCAD and using the CLI (`pc list`, `pc info`,
  `pc inspect`, `pc export`).
- Browsing the public repository (online and from the CLI).
- **Importing PartCAD parts into a build123d script** —
  `pc.get_part_build123d(...)` and `pc.get_assembly_build123d(...)`.
- **Authoring** your own PartCAD package: `partcad.yaml`, `.assy` files,
  the supported part `type:` values (file formats, CAD scripts, AI
  generation).
- Publishing a package to the public index.

## When to Use This Skill

- The user asks for a **community CAD part** that isn't a basic fastener
  (e.g. "an OpenVMP robot arm", "an IKEA-like desk", a published
  electronics enclosure model).
- The user wants to **browse the catalog** at
  <https://partcad.org/repository>.
- The user wants to **install and use PartCAD's CLI** to inspect or
  export models without opening a CAD GUI.
- The user wants to **import a PartCAD part into a build123d script**.
- The user wants to **publish their own build123d/CadQuery/OpenSCAD
  models** as a PartCAD package.
- The user wants **AI-generated CAD models** (CadQuery or OpenSCAD)
  as a starting point.

For just a hex bolt or socket-head cap screw, do NOT load this skill —
use `cad-build123d-bd-warehouse` instead. PartCAD has more setup overhead.

---

## Install

```bash
pip install partcad
```

PartCAD is a real PyPI package (unlike bd_warehouse which is git-only).
The install brings the `pc` CLI plus the `partcad` Python module.

> **Optional configuration** for the AI-part-generation feature
> (`type: ai-cadquery` / `type: ai-openscad`):
>
> ```yaml
> # ~/.partcad/config.yaml
> googleApiKey: <...>
> openaiApiKey: <...>
> ```

## Browse the public repository

| Method | URL / command |
|---|---|
| Web UI | <https://partcad.org/repository> |
| VS Code extension | Search "PartCAD" in the marketplace ([OpenVMP.partcad](https://marketplace.visualstudio.com/items?itemName=OpenVMP.partcad)) |
| CLI | `pc list packages -r` |

The web UI groups packages by top-level category:

| Top-level package | Examples |
|---|---|
| `electrical` | Switches, terminals, batteries |
| `electromechanics` | Motors, actuators, solenoids |
| `electronics` | PCBs, microcontrollers, sensor modules |
| `examples` | Reference projects (cubes, simple assemblies) |
| `furniture` | Desks, chairs, tables |
| `medical` | Medical-device exemplars |
| `robotics` | OpenVMP robots, arms, grippers, common platforms |
| `std` | Industry-standard hardware (ISO/DIN/ASME) — bd_warehouse-equivalent |
| `storage` | Bins, racks, shelves |
| `svc` | Service / infrastructure parts |

A part path looks like
`//pub/<package-tree>:<part-name>`, for example
`//pub/std/metric/cqwarehouse:hexhead-din931`.

## CLI Reference

```bash
# Initialize a new PartCAD package in the current folder (creates partcad.yaml)
pc init

# List things across all available packages
pc list packages -r
pc list parts -r
pc list assemblies -r
pc list sketches -r
pc list interfaces -r
pc list mates -r            # known matings of interfaces

# Inspect a single part — prints info without opening a viewer
pc info //pub/std/metric/cqwarehouse:fastener/hexhead-din931

# Display in the OCP CAD Viewer (in VS Code)
pc inspect //pub/std/metric/cqwarehouse:fastener/hexhead-din931

# Display with parameters
pc inspect \
    -p length=30 \
    -p size=M4-0.7 \
    //pub/std/metric/cqwarehouse:fastener/hexhead-din931

# Render projections to image files
pc render -t svg <part-path>
pc render -t png <part-path>

# Export to a file
pc export -t stl  <part-path>
pc export -t step <part-path>
pc export -t 3mf  <part-path>
pc export -t step -a <assembly-path>
```

Supported export targets: STEP, BREP, STL, 3MF, ThreeJS, OBJ, GLTF, IGES.

## Consuming PartCAD parts in build123d

This is the entry point most CAD-Builder agents need.

```python
# part.py
import build123d as b3d
import partcad as pc

part = pc.get_part_build123d(
    "//pub/std/metric/cqwarehouse:hexhead-din931",
)
show_object(part)
```

```python
# assembly.py
import build123d as b3d
import partcad as pc

assembly = pc.get_assembly_build123d(
    "//pub/furniture/workspace/basic:imperial-desk-1",
)
show_object(assembly)
```

The returned `part` is a regular build123d `Part` (or `Compound` for
assemblies) — fuse it, position it, integrate it with your own geometry
the same way you would any other build123d part.

### Passing parameters

Many parts in the repository are parametric. The CLI `-p key=value` and
the Python API's keyword arguments serve the same purpose. Check the
part's repository page for valid parameters.

### Generic Python API (no CAD framework)

```python
import partcad as pc
part = pc.get_part("//pub/std/metric/cqwarehouse:hexhead-din931")
part.show()
```

### CadQuery API (when not on build123d)

```python
import cadquery as cq
import partcad as pc
part = pc.get_part_cadquery(
    "//pub/std/metric/cqwarehouse:fastener/hexhead-din931",
)
show_object(part)
```

## Authoring your own package

Every PartCAD package is a folder with a `partcad.yaml` manifest.

### Parts from a CAD file

```yaml
# partcad.yaml
parts:
    part1:
        type: step          # part1.step is used
    part2:
        type: brep          # part2.brep is used
    part3:
        type: stl           # part3.stl is used
    part4:
        type: 3mf           # part4.3mf is used
    part5:
        type: obj           # part5.obj is used
```

### Parts from a Python script (build123d / CadQuery)

PartCAD intercepts `show_object()` calls (CQGI) — your script just
calls `show_object(part)` like normal:

```yaml
# partcad.yaml
parts:
    optional-path/part1:
        type: build123d     # optional-path/part1.py is used
    part2:
        type: cadquery      # part2.py is used
```

### Parts from OpenSCAD

```yaml
# partcad.yaml
parts:
    part1:
        type: scad          # part1.scad is used
```

> OpenSCAD parameters are **not yet** propagated by PartCAD as of the
> current docs. If you need a parametric SCAD part, factor parameters
> into a wrapper build123d/CadQuery script.

### AI-generated parts (Google / OpenAI)

The fastest "from scratch" bootstrap:

```yaml
# partcad.yaml
parts:
    part1:
        type: ai-cadquery   # part1.py is created by the AI
        desc: A cube
        provider: google
    part2:
        type: ai-openscad   # part2.scad is created by the AI
        desc: A flat screen TV
        provider: openai
        images:
          - product_photo.png
```

Workflow: generate → empty the file and re-generate with refined prompts
→ at some point drop the `ai-*` prefix and continue improving the
script manually.

### Assemblies (.assy)

A `partcad.yaml` lists assemblies that point to `.assy` files.

```yaml
# partcad.yaml
assemblies:
    logo:
        type: assy
```

```yaml
# logo.assy — hierarchical composition with positioning
links:
  - part: /produce_part_cadquery_logo:bone
    location: [[0, 0, 0], [0, 0, 1], 0]
  - part: /produce_part_cadquery_logo:bone
    location: [[0, 0, -2.5], [0, 0, 1], -90]
  - links:
      - part: /produce_part_cadquery_logo:head_half
        location: [[0, 0, 2.5], [0, 0, 1], 0]
      - part: /produce_part_cadquery_logo:head_half
        location: [[0, 0, 0], [0, 0, 1], -90]
    location: [[0, 0, 25], [1, 0, 0], 0]
  - part: /produce_part_step:bolt
    location: [[0, 0, 7.5], [0, 0, 1], 0]
```

Each `location` is `[[x, y, z], [axis_x, axis_y, axis_z], angle_degrees]`.

## Publishing to the public repository

1. Push your package as a public GitHub repo.
2. Open a pull request against
   [partcad/partcad-index](https://github.com/partcad/partcad-index)
   adding a reference to your repo.
3. Once merged, your package is browsable at
   <https://partcad.org/repository> and importable via `pc.get_part(...)`.

## Caching

PartCAD aggressively caches intermediate and final compilation results.
First fetch of a part triggers a download + build; subsequent runs
return instantly from the local cache. See
<https://partcad.readthedocs.io/en/latest/features.html#caching>.

## When NOT to use PartCAD

- For a single hex bolt / nut / washer in a personal project →
  `bd_warehouse.fastener` is one `pip install` and one import; PartCAD
  adds package-manager overhead that isn't worth it for one bolt.
- For pure GUI workflows in FreeCAD/Fusion → there's no PartCAD plugin
  for these GUIs yet. Export the model to STEP/3MF first
  (`pc export -t step ...`) and import the file.
- For your own one-off model that won't be shared → build123d alone is
  simpler. Reach for PartCAD when you're publishing or when you're
  consuming a published part.

---

## Quick Reference

| I want to … | Command / API |
|---|---|
| Browse the catalog (web) | <https://partcad.org/repository> |
| Browse from VS Code | install the OpenVMP.partcad extension |
| List all parts | `pc list parts -r` |
| Inspect a part | `pc inspect <path>` |
| Render a part to PNG | `pc render -t png <path>` |
| Export a part to STL | `pc export -t stl <path>` |
| Export an assembly to STEP | `pc export -t step -a <path>` |
| Use a part in build123d | `pc.get_part_build123d("//pub/...")` |
| Use an assembly in build123d | `pc.get_assembly_build123d("//pub/...")` |
| Author a build123d part | `partcad.yaml` with `type: build123d` |
| Generate a part with AI | `partcad.yaml` with `type: ai-cadquery` + `desc:` |
| Compose an assembly | `.assy` file with `links:` and `location:` |
| Publish a package | PR against `partcad/partcad-index` |

## See Also

- PartCAD docs: <https://partcad.readthedocs.io/en/latest/>
- Use cases: <https://partcad.readthedocs.io/en/latest/use_cases.html>
- Public repository: <https://partcad.org/repository>
- Source: <https://github.com/partcad/partcad>
- Index repo (for publishing): <https://github.com/partcad/partcad-index>
- VS Code extension: <https://marketplace.visualstudio.com/items?itemName=OpenVMP.partcad>
- Sibling skill: `cad-build123d-bd-warehouse` (use first for standard hardware)
- Sibling skill: `cad-build123d-tools` — references PartCAD as one of many
  ecosystem tools; this skill is the authoritative deep-dive
