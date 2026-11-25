---
name: cad-build123d-tools
description: 'Catalog of external tools for the build123d ecosystem: editors, viewers, CAM toolpath generation, Blender integration, topology optimization, browser-based CAD, package management, and CI/publishing. USE FOR: OCP CAD Viewer, ocp-vscode, view model, preview CAD, CNC toolpath, CAM, Blender, blendquery, nething, generative AI CAD, topology optimization, dl4to4ocp, OCP.wasm, browser CAD, PartCAD package manager, MakerRepo, makerrepo-cli, publish model, share model, Yet Another CAD Viewer.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["build123d","tooling","viewers","cam","ecosystem"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# Build123d External Tools

> **Prerequisite:** Load `cad-build123d-general` first — all tools below
> operate on build123d objects and assume familiarity with the API.

## Purpose

Before recommending a workflow change, custom script, or manual export step,
check whether one of the community tools already solves the problem.  This
skill is a catalog of every tool listed on the official build123d
[External Tools and Libraries](https://build123d.readthedocs.io/en/latest/external.html)
page (Editors & Viewers + Tools sections), with installation commands,
quick-start usage, and guidance on when to reach for each tool.

## When to Use This Skill

- The user asks how to **view / preview / inspect** a build123d model.
- The user wants to **generate CNC toolpaths** from a build123d part.
- The user asks about **Blender integration** for rendering or animation.
- The user wants to **share, publish, or package** a build123d model.
- The user mentions **topology optimization** or **generative design**.
- The user wants to **run build123d in a browser** (WebAssembly).
- The user asks "is there a tool for …?" in the build123d ecosystem.

---

## Editors & Viewers

### 1  OCP CAD Viewer for VS Code (ocp-vscode)

The **primary viewer** for build123d development.  A VS Code extension that
renders CadQuery / build123d objects in a 3D panel with measurement tools,
face/edge/vertex selection, PBR materials, and visual debugging.

| Field | Value |
|-------|-------|
| **Repo** | <https://github.com/bernhard-42/vscode-ocp-cad-viewer> |
| **PyPI** | `ocp-vscode` |
| **VS Code** | Search "OCP CAD Viewer" in Extensions |
| **License** | Apache-2.0 |
| **Latest** | 3.3.4 (as of writing) |

#### Install

```bash
# Option A — VS Code Quickstart button (installs build123d + ocp_vscode + deps)
# Open sidebar → OCP CAD Viewer → "Quickstart build123d"

# Option B — CLI (pip)
pip install ocp-vscode

# Option C — CLI (uv)
uv add ocp-vscode
```

#### Quick start

```python
from build123d import *
from ocp_vscode import *

b = Box(10, 20, 30)
show(b)
```

#### Key features

- **Jupyter integration** — run cells, see results in the viewer panel.
- **Visual debugging** — step through code; all CAD `locals()` auto-display.
- **Measurement mode** — select faces/edges/vertices and measure distances.
- **PBR Studio** — physically based rendering with MaterialX materials,
  environment maps, shadows, and ambient occlusion.
- **Standalone mode** — `python -m ocp_vscode` starts a Flask server at
  `http://127.0.0.1:3939` — no VS Code required.
- **Camera control** — `reset_camera=Camera.CENTER` (keeps rotation, re-centers),
  `Camera.KEEP` (keeps pan too), `Camera.RESET` (full reset).
- **`set_defaults()`** — set per-file defaults for `helper_scale`,
  `reset_camera`, `transparent`, etc.

#### Best practices

- Use `# %%` cell markers with the Jupyter extension for interactive work.
- Name your `BuildPart` / `BuildSketch` / `Location` contexts so the visual
  debugger labels them.
- Don't use the OCP logo to verify settings — it overrides your config.
- If models are invisible, clear the VS Code browser cache (stale WebGL
  shader compilation).

---

### 2  cq-editor (jdegenstein fork)

A GUI editor based on PyQT, forked with build123d-friendly changes.
Useful if you prefer a standalone IDE-like experience outside VS Code.

| Field | Value |
|-------|-------|
| **Repo** | <https://github.com/jdegenstein/jmwright-CQ-Editor> |

> **When to use:** Only if the user explicitly doesn't want VS Code.
> Otherwise, recommend ocp-vscode — it's better maintained and more
> feature-rich.

---

### 3  Yet Another CAD Viewer (YACV)

A **web-based** CAD viewer for OCP models that runs in any modern browser.
Supports static site deployment, interactive inspection, measurement,
per-model clipping planes, transparency, and hot reloading via `yacv-server`.

| Field | Value |
|-------|-------|
| **Repo** | <https://github.com/yeicor-3d/yet-another-cad-viewer> |
| **PyPI** | `yacv-server` |
| **License** | MIT |
| **Demo** | <https://yeicor-3d.github.io/yet-another-cad-viewer/> |

#### Install

```bash
pip install yacv-server
```

#### Key features

- **Browser playground** — edit and run build123d code entirely in the browser
  (powered by OCP.wasm).
- **Static deployment** — upload the viewer + GLTF models to any web server.
- **Hot reload** — `yacv-server` watches for file changes and pushes updates.
- **GLTF 2.0** — full support for textures, PBR materials, animations.
- **Measurement** — bounding box size and distance measurement on selection.

> **When to use:** sharing models with others who don't have VS Code, embedding
> previews on a website, or running build123d in a browser without any local
> install.

---

### 4  PartCAD VS Code Extension

A wrapper around `ocp-vscode` that requires build123d scripts to be packaged
with PartCAD.  Adds UI controls for exporting models and passing parameters,
plus AI-based generative design tools.

| Field | Value |
|-------|-------|
| **VS Code** | Search "PartCAD" in Extensions |
| **Docs** | <https://partcad.readthedocs.io/> |

> **When to use:** only if the user is already using PartCAD for package
> management.  Otherwise, ocp-vscode alone is simpler.

---

## Tools

### 5  blendquery — Blender Integration

CadQuery and build123d integration for Blender.  Import CAD objects directly
into Blender for rendering, animation, or further modeling.

| Field | Value |
|-------|-------|
| **Repo** | <https://github.com/uki-dev/blendquery> |

#### When to use

- The user wants to **render a photorealistic image** of a build123d model
  using Blender's Cycles/EEVEE renderer.
- The user wants to **animate** an assembly.
- The user needs to **combine CAD geometry with artistic 3D work**.

> Note: For quick renders, ocp-vscode's PBR Studio mode may be sufficient
> without bringing in Blender.

---

### 6  nething — Generative AI for CAD

A 3D generative AI platform for CAD modeling.  Describe what you want in
natural language and get a 3D model.

| Field | Value |
|-------|-------|
| **Website** | <https://nething.xyz/> |

> **When to use:** the user wants to quickly bootstrap a shape from a text
> description before refining it parametrically in build123d.  Treat the
> output as a starting point, not a final model — it won't be parametric.

---

### 7  ocp-freecad-cam — CNC Toolpath Generation

Generates CNC toolpaths from build123d / CadQuery / OCP shapes by leveraging
FreeCAD's Path workbench through a fluent Python API.  Spiritual successor
of `cq-cam`.

| Field | Value |
|-------|-------|
| **Repo** | <https://github.com/voneiden/ocp-freecad-cam> |
| **PyPI** | `ocp-freecad-cam` |
| **Docs** | <https://ocp-freecad-cam.readthedocs.io/> |
| **License** | Apache-2.0 |
| **Latest** | 1.1.0 |

#### Prerequisites

- FreeCAD ≥ 1.0.1 must be importable by your Python environment.
- On Linux: extract the AppImage, create a venv from its interpreter, add
  FreeCAD's `lib` to a `.pth` file.
- On Windows: use the 7z portable build; create a `.pth` pointing at `src`.

#### Install

```bash
pip install ocp-freecad-cam
```

#### When to use

- The user wants to **machine a build123d part on a CNC router or mill**.
- The user asks about **G-code generation** from a parametric model.

#### Limitations

- **Experimental** — always double-check generated G-code.
- `Pocket3D` doesn't work; use `Surface3D` instead.
- `VCarve` can produce unstable toolpaths (openvoronoi bug).

---

### 8  PartCAD — Package Manager for CAD Models

A package manager and repository for CAD models. Build123d is the most
supported framework; CadQuery and OpenSCAD are also supported.

| Field | Value |
|-------|-------|
| **Repo** | <https://github.com/partcad/partcad> |
| **Docs** | <https://partcad.readthedocs.io/> |
| **Public repo** | <https://partcad.org/repository> |
| **PyPI** | `partcad` |
| **VS Code extension** | <https://marketplace.visualstudio.com/items?itemName=OpenVMP.partcad> |

#### When to use

- Find / reuse a community-published CAD part beyond the basic
  hardware that `bd_warehouse` covers.
- Publish your own build123d / CadQuery / OpenSCAD models.
- Use AI-generated CAD scripts (Google / OpenAI) as a starting point.

> **Deep dive lives in the `cad-partcad-repository` skill.** That
> skill covers install, the full CLI (`pc list / info / inspect /
> render / export`), the build123d / CadQuery / generic Python APIs
> (`pc.get_part_build123d`, `pc.get_assembly_build123d`),
> `partcad.yaml` package authoring, AI-generated parts, `.assy`
> assembly files, and publishing to the public index. Load that
> skill when the user actually wants to use PartCAD; this `tools`
> entry is just the catalog pointer.

---

### 9  MakerRepo — Manufacturing-as-Code

A lightweight Python library (`mr`) that provides decorators to annotate
build123d model functions for discovery by `makerrepo-cli` or MakerRepo.com CI.

| Field | Value |
|-------|-------|
| **Library repo** | <https://github.com/LaunchPlatform/makerrepo> |
| **CLI repo** | <https://github.com/LaunchPlatform/makerrepo-cli> |
| **Docs** | <https://docs.makerrepo.com/makerrepo-library/> |
| **PyPI** | `makerrepo` (library), `makerrepo-cli` (CLI) |

#### Install

```bash
pip install makerrepo makerrepo-cli
```

#### Decorators

| Decorator | Purpose |
|-----------|---------|
| `@artifact` | Mark a function that produces a CAD model to be built/published. Optional: `sample`, `cover`, `desc`, `export_step`, `export_3mf`. |
| `@customizable` | Parametric model — users tweak parameters via a Pydantic model. |
| `@cached` | Cache expensive sub-builds by arguments for reuse. |

#### Quick start

```python
import makerrepo as mr
from build123d import *

@mr.artifact(desc="A simple box", export_step=True)
def my_box():
    return Box(10, 20, 30)
```

```bash
mr list        # discover artifacts
mr build       # build all artifacts
mr snapshot    # snapshot outputs
```

#### When to use

- The user wants a **CI/CD pipeline** for their build123d models.
- The user wants to **publish parametric models** on MakerRepo.com.
- The user wants **build caching** for complex multi-part projects.

> **Non-intrusive:** decorators have zero effect on normal build123d scripts
> until discovered by MakerRepo tooling.

---

### 10  dl4to4ocp — Topology Optimization

Perform topology optimization on OCP-based CAD models using the `dl4to`
deep-learning library.

| Field | Value |
|-------|-------|
| **Repo** | <https://github.com/yeicor-3d/dl4to4ocp/> |

#### When to use

- The user wants to **minimize material** while maintaining structural strength.
- The user mentions **topology optimization**, **generative design** (structural),
  or **lightweighting**.

> **Experimental** — requires `dl4to` and its deep-learning dependencies
> (PyTorch).  Best for users already comfortable with ML tooling.

---

### 11  OCP.wasm — Build123d in the Browser

Ports OCP (OpenCASCADE for Python) and supporting libraries to WebAssembly,
enabling full in-browser CAD model generation.  Powers the build123d
playground in Yet Another CAD Viewer.

| Field | Value |
|-------|-------|
| **Repo** | <https://github.com/yeicor/OCP.wasm> |

#### When to use

- The user wants to **run build123d without a local Python install**.
- The user wants to **embed a live build123d editor** on a website.
- The user is building a **web-based CAD application**.

> For a ready-made frontend, use Yet Another CAD Viewer (§3 above) rather
> than integrating OCP.wasm directly.

---

## Quick Decision Table

| Need | Tool |
|------|------|
| View model interactively in VS Code | **ocp-vscode** (§1) |
| View model in a web browser | **Yet Another CAD Viewer** (§3) |
| Run build123d with no local install | **OCP.wasm** via YACV playground (§3, §11) |
| Photorealistic render / animation | **blendquery** (§5) or ocp-vscode PBR Studio |
| Generate shape from text description | **nething** (§6) |
| CNC toolpath / G-code from model | **ocp-freecad-cam** (§7) |
| Find / reuse community parts | **PartCAD** (§8, deep dive in `cad-partcad-repository` skill); for nuts/bolts/bearings see `cad-build123d-bd-warehouse` |
| Publish models with CI/CD | **MakerRepo** (§9) |
| Topology optimization | **dl4to4ocp** (§10) |
| Standalone GUI editor (no VS Code) | **cq-editor fork** (§2) |

---

## See Also

- Official page: <https://build123d.readthedocs.io/en/latest/external.html>
- Related skill: `cad-build123d-bd-warehouse` (deep dive on Gumyr's
  comprehensive part library — fasteners, bearings, gears, threads, etc.)
- Related skill: `cad-partcad-repository` (deep dive on PartCAD: install,
  CLI, build123d / CadQuery / generic Python APIs, package authoring,
  AI-generated parts, publishing)
- Related skill: `cad-build123d-general` (foundational build123d API reference)
