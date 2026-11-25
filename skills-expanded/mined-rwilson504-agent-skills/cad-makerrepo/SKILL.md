---
name: cad-makerrepo
description: 'MakerRepo manufacturing-as-code: annotate build123d scripts with @artifact, @customizable, @cached decorators for CI/CD publishing on MakerRepo.com; BuildEnv for version marks; Result for versioned models; repository config; makerrepo-cli for local build/export/snapshot. USE FOR: MakerRepo, makerrepo, makerrepo-cli, publish model, share model, manufacturing as code, CI for CAD, build version mark, parametric generator, @artifact, @customizable, @cached, mr artifacts, mr generators, mr cache, annotate build123d script for MakerRepo.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["makerrepo","build123d","ci-cd","publishing","parametric"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# MakerRepo — Manufacturing-as-Code

> **Prerequisite:** Load `cad-build123d-general` first — MakerRepo decorators
> wrap build123d model functions and assume familiarity with the API.

## Purpose

MakerRepo turns build123d scripts into publishable, discoverable CAD
artifacts.  This skill covers:

1. The **`makerrepo` Python library** (`import mr`) — decorators and helpers
   that annotate existing build123d functions without changing their behavior.
2. The **`makerrepo-cli`** — a local CLI (`mr`) that discovers, builds,
   views, exports, and snapshots those annotated functions.
3. **Repository configuration** — `.makerrepo/config.yaml` for repo-level
   defaults.
4. The **"annotate an existing script" recipe** — how to take a plain
   build123d script and make it MakerRepo-ready with minimal changes.

The decorators are **non-intrusive**: they have zero effect on a normal
build123d script until discovered by MakerRepo tooling.

## Source of Truth

This skill is the canonical reference for MakerRepo decorator APIs,
CLI commands, and repository configuration.  The `cad-build123d-tools`
skill has a brief entry (§9) pointing here for the deep dive.

Official docs: <https://docs.makerrepo.com/>

---

## 1  Installation

```bash
# Library (decorators + helpers)
pip install makerrepo          # or: uv add makerrepo

# CLI (local build / export / view / snapshot)
uv tool install makerrepo-cli  # global install — available as `makerrepo-cli` or `mr`
uv add makerrepo-cli           # project-local — use `uv run mr`
uvx makerrepo-cli              # run without installing (one-shot)
```

Import convention:

```python
import makerrepo as mr
# or selective imports:
from mr import artifact, customizable, cached, BuildEnv, Result
```

---

## 2  `@artifact` — Fixed-Geometry Models

Mark a function that returns a build123d `Build` object as a publishable
artifact.

### Minimal example

```python
from build123d import *
from mr import artifact

@artifact(short_desc="A simple box")
def my_box():
    with BuildPart() as part:
        Box(10, 20, 30)
    return part
```

### Decorator arguments

| Argument | Type | Default | Purpose |
|----------|------|---------|---------|
| `sample` | `bool` | `False` | Mark as a test/dev artifact — not shown to end-users |
| `cover` | `bool` | `False` | Use this artifact's snapshot as the repository cover image |
| `desc` | `str` | docstring | Markdown description (overrides the function docstring) |
| `short_desc` | `str` | — | Short description (<128 chars) for lists and previews |
| `export_step` | `bool` | repo default | Export as STEP file |
| `export_3mf` | `bool` | repo default | Export as 3MF file |

### Rules

- The function **must return** a build123d `Build` object (e.g. `BuildPart`)
  or a `Result` (see §5).
- The function takes **no arguments** (unlike generators).
- `desc` and `short_desc` are optional but recommended — they appear on
  MakerRepo.com and in `mr artifacts list`.

---

## 3  `@customizable` — Parametric Generators

Mark a function as a **generator** — a parametric model whose parameters
are defined by a Pydantic `BaseModel`.  End-users (or the CLI) pass a JSON
payload to customize the output.

### Minimal example

```python
from pydantic import BaseModel
from build123d import *
from mr import customizable

class BoxParams(BaseModel):
    width: float = 10
    height: float = 20
    depth: float = 30

@customizable(
    short_desc="Parametric box",
    sample_parameters=BoxParams(),
)
def parametric_box(parameters: BoxParams):
    with BuildPart() as part:
        Box(parameters.width, parameters.height, parameters.depth)
    return part
```

### Decorator arguments

| Argument | Type | Default | Purpose |
|----------|------|---------|---------|
| `desc` | `str` | docstring | Markdown description |
| `short_desc` | `str` | — | Short description (<128 chars) |
| `sample_parameters` | `BaseModel` | — | Default parameter values used for preview builds and `mr generators list` |

### Rules

- The function's **first positional argument** must be the Pydantic model
  instance (typically named `parameters`).
- `sample_parameters` provides the default values used when the CLI builds
  a preview or when no payload is supplied.

### Custom validation

Raise `GeneratorValidationError` with a list of `FieldError` objects:

```python
from mr import GeneratorValidationError, FieldError

@customizable(sample_parameters=BoxParams())
def validated_box(parameters: BoxParams):
    errors = []
    if parameters.width < 1:
        errors.append(FieldError(field="width", message="Must be >= 1"))
    if errors:
        raise GeneratorValidationError(errors=errors)
    # ... build the model ...
```

---

## 4  `@cached` — Expensive Sub-Builds

Cache the result of an expensive build123d operation (e.g. threading,
complex boolean) so it's reused across artifact/generator builds.

### Example

```python
from build123d import *
from mr import cached

@cached(short_desc="M3 × 10 ISO thread")
def m3_thread():
    # expensive thread generation...
    with BuildPart() as part:
        # ... thread geometry ...
        pass
    return part
```

### Decorator arguments

| Argument | Type | Default | Purpose |
|----------|------|---------|---------|
| `desc` | `str` | docstring | Markdown description |
| `short_desc` | `str` | — | Short description (<128 chars) |

### Cache behavior

- Cached results are stored as BREP files under a local cache directory
  (organized as `<module>/<function>/<cache_key>.brep`).
- **No automatic invalidation** — if you change the function body, the old
  cache is still used.  Prune manually:
  ```bash
  mr cache prune --all           # remove everything
  mr cache prune --dangling      # remove orphaned entries only
  mr cache prune mymod/myfunc    # remove specific function's cache
  ```
- The cached function must be **deterministic** (same args → same geometry)
  for the cache to be meaningful.

---

## 5  `Result` — Primary + Versioned Models

When an artifact or generator needs to produce both a **clean model**
(for publishing) and a **development variant** (with a version mark),
return a `Result`:

```python
from mr import Result

return Result(model=clean_model, versioned=model_with_version_text)
```

### Definition

```python
@dataclasses.dataclass(frozen=True)
class Result:
    model: typing.Any           # primary model — what gets published
    versioned: typing.Any = None  # optional variant with version mark
```

### Usage pattern

```python
from build123d import *
from mr import artifact, BuildEnv, Result

@artifact(short_desc="Post clip")
def clip():
    with BuildPart() as model:
        # ... build the clip ...
        Box(20, 10, 5)

    build_env = BuildEnv.from_local_git_repo()
    if not build_env.versioned_model_enabled:
        return model

    with BuildPart() as versioned:
        add(model)
        version_mark = build_env.get_build_version()
        with BuildSketch(
            versioned.faces()
            .filter_by(lambda f: abs(f.normal_at().Y) > 0.98)
            .sort_by(Axis.Y)[-1]
        ):
            Text(version_mark, font_size=7 * MM, rotation=-90)
        extrude(amount=-0.1 * MM, mode=Mode.SUBTRACT)

    return Result(model=model, versioned=versioned)
```

### How tools consume `Result`

- **`mr artifacts export`** — exports `model` by default; pass `--versioned`
  to export the versioned variant.
- **`mr artifacts view`** — views `model` by default; `--versioned` for the
  variant.
- **MakerRepo.com CI** — publishes `model`; shows `versioned` in the
  development build UI.
- If you return a plain `Build` object instead of `Result`, that's fine —
  there's simply no versioned variant.

---

## 6  `BuildEnv` — Build Environment

Access CI and git metadata from within an artifact or generator function.

### Construction

```python
from mr import BuildEnv

# In CI (MakerRepo.com) — populated from environment variables:
env = BuildEnv.from_env()

# Local development — reads from the local git repo:
env = BuildEnv.from_local_git_repo()
```

### Fields

| Field | Type | Source |
|-------|------|--------|
| `build_id` | `str` | CI build identifier |
| `build_number` | `str` | Incrementing build number from CI |
| `build_version` | `str` | Explicit version override (env var) |
| `versioned_model_enabled` | `bool` | Whether to produce versioned variants |
| `git_commit` | `str` | Full commit SHA |
| `git_ref` | `str` | Git ref (e.g. `refs/tags/v1.0`) |
| `git_ref_name` | `str` | Short ref name (e.g. `v1.0`, `main`) |
| `repository_name` | `str` | Repository name |
| `repository_username` | `str` | Repository owner |
| `repository_url` | `str` | Repository URL |

### `get_build_version()` precedence

Returns a sensible version string for stamping on models:

1. `build_version` env var (explicit override)
2. Git tag (if on a tagged commit)
3. `build_number` (CI build counter)
4. First 4 characters of `git_commit` hash
5. `"unknown"` (fallback)

---

## 7  Repository Configuration

### File location

```
<repo-root>/.makerrepo/config.yaml
```

### Schema

```yaml
# .makerrepo/config.yaml
pythonpaths:
  - src              # prepended to sys.path before loading modules
  - libs/shared

artifacts:
  default_config:
    export_step: true   # default for @artifact(export_step=...)
    export_3mf: true    # default for @artifact(export_3mf=...)
```

| Key | Type | Purpose |
|-----|------|---------|
| `pythonpaths` | `list[str]` | Paths prepended to `sys.path` before importing repo code.  Use for `src/` layouts. |
| `artifacts.default_config.export_step` | `bool` | Default `export_step` when not set on `@artifact`. Default: `true`. |
| `artifacts.default_config.export_3mf` | `bool` | Default `export_3mf` when not set on `@artifact`. Default: `true`. |

Omit the file entirely if defaults are fine (both exports enabled, no
extra Python paths).

---

## 8  MakerRepo CLI (`mr`)

The CLI discovers `@artifact`, `@customizable`, and `@cached` functions
by scanning Python packages/modules under the current working directory.
**Run all commands from the repository root.**

### Artifacts commands

```bash
mr artifacts list                          # table of all artifacts
mr artifacts list -o json                  # JSON output
mr artifacts view [NAME...]                # open in OCP CAD Viewer
mr artifacts view --versioned              # view versioned variant
mr artifacts export [NAME...] -o part.step # export to STEP
mr artifacts export -f 3mf -o ./out/      # export all as 3MF to dir
mr artifacts snapshot [NAME...] -o img.png # headless screenshot
```

Supported export formats: **STEP, STL, BREP, glTF, 3MF, SVG, DXF**.
Format is inferred from the `-o` file extension or set explicitly with `-f`.

### Generators commands

```bash
mr generators list                                          # table of all generators
mr generators view my_gen -p '{"width": 10}'                # view with inline JSON
mr generators view -p @params.json                          # load payload from file
mr generators export my_gen -p '{"width": 10}' -o out.step  # export
mr generators snapshot my_gen -p '{}' -o snap.png           # screenshot
```

### Cache commands

```bash
mr cache list                          # list cached functions + files
mr cache view <path>                   # view a .brep in OCP Viewer
mr cache prune                         # interactive selection
mr cache prune --all                   # remove all cache files
mr cache prune --dangling              # remove orphaned files only
mr cache prune mymodule/myfunc         # remove specific function's cache
```

---

## 9  Recipe: Annotate an Existing build123d Script

When the user has a working build123d script and wants to make it
MakerRepo-ready, follow these steps:

### Step 1 — Install dependencies

```bash
pip install makerrepo
# Optional for local testing:
uv tool install makerrepo-cli
```

### Step 2 — Add `@artifact` to the main build function

**Before:**
```python
from build123d import *

with BuildPart() as part:
    Box(100, 80, 50)

export_stl(part, "box.stl")
```

**After:**
```python
from build123d import *
from mr import artifact

@artifact(
    short_desc="Simple box",
    desc="A 100 × 80 × 50 mm box.",
    export_step=True,
    export_3mf=True,
)
def simple_box():
    with BuildPart() as part:
        Box(100, 80, 50)
    return part

# Keep the local export for standalone use:
if __name__ == "__main__":
    result = simple_box()
    export_stl(result, "box.stl")
```

**Key changes:**
1. Wrap the build in a **named function** — MakerRepo discovers functions,
   not top-level code.
2. **Return** the `BuildPart` object (don't just export it).
3. Add `from mr import artifact` and the decorator.
4. Move the `export_stl()` call into an `if __name__` guard so the script
   still runs standalone.

### Step 3 — (Optional) Add parameters to make it a generator

If the model has named constants that users might want to tweak:

```python
from pydantic import BaseModel
from build123d import *
from mr import customizable

class BoxParams(BaseModel):
    length: float = 100
    width: float = 80
    height: float = 50

@customizable(
    short_desc="Parametric box",
    sample_parameters=BoxParams(),
)
def parametric_box(parameters: BoxParams):
    with BuildPart() as part:
        Box(parameters.length, parameters.width, parameters.height)
    return part
```

### Step 4 — (Optional) Add version marking

See §5 above for the `Result` + `BuildEnv` pattern.

### Step 5 — (Optional) Add repository config

If the script lives in a `src/` layout or you want to change export
defaults, create `.makerrepo/config.yaml` (see §7).

### Step 6 — Test locally

```bash
mr artifacts list           # should show the new artifact
mr artifacts view           # should open in OCP Viewer
mr artifacts export -o .    # should produce .step and/or .3mf files
```

### Step 7 — Publish

1. Create a repository on [MakerRepo.com](https://makerrepo.com/).
2. Push code to the linked Git remote.
3. MakerRepo CI builds artifacts automatically and hosts them for
   viewing/download.

---

## 10  Real-World Reference: TinyRack Pattern Library

The public TinyRack repository is a strong reference for how to organize a
MakerRepo-native build123d project:

- Repository: <https://makerrepo.com/r/fangpenlin/tinyrack/home/master>
- Artifacts page: <https://makerrepo.com/r/fangpenlin/tinyrack/artifacts/master>
- Generators page: <https://makerrepo.com/r/fangpenlin/tinyrack/generators/master>

### 10.1  Project structure that scales

TinyRack uses a package layout instead of one giant script:

```text
<repo-root>/
    .makerrepo/
        config.yaml
    pyproject.toml
    tinyrack/
        assembly.py
        panel.py
        post.py
        notched_post.py
        handle.py
        ...
        tools/
            manual_nut_connector_tool.py
            nut_connector_tool.py
            screw_driver_tool.py
```

Why this matters for MakerRepo:
- Discovery IDs become predictable and readable (`tinyrack.post post`,
    `tinyrack.panel custom_panel`, etc.).
- Each module owns one concept and can expose multiple artifacts/generators.
- Shared constants/utilities stay centralized (e.g., `constants.py`, cached
    thread builders).

### 10.2  Python file pattern used across modules

Across TinyRack modules (`panel.py`, `post.py`, `handle.py`, `mount.py`,
`notch.py`, `nut_connector.py`, `tools/*.py`), the pattern is:

1. Define a reusable geometry class (`class Panel(BasePartObject)`, etc.)
2. Expose one or more thin MakerRepo wrappers via decorators:
     - `@artifact(...)` returning default model variants
     - `@customizable(...)` for parameterized variants
     - `@cached(...)` for expensive sub-geometry builders

This class + wrapper split keeps CAD code reusable outside MakerRepo while
still giving MakerRepo clean discovery targets.

### 10.3  Artifact catalog strategy (what to publish)

TinyRack does not only publish final end-user parts. It also publishes:

- Primary parts (`post`, `panel`, `handle`, ...)
- Sample/debug artifacts (`top_screw_sample`, `notch`, `mount_cutter`, ...)
- Negative/cutter models as first-class artifacts (`*_cutter`)
- Assembly demo artifact (`assembly`, marked `sample=True`, `cover=True`)
- Tooling artifacts in subpackages (`tinyrack.tools.*`)

Recommended takeaway:
- Publish both manufacturing parts and helper/cutter geometries.
- Mark development-only artifacts as `sample=True`.
- Use one intentional `cover=True` artifact for repo thumbnail/first impression.

### 10.4  Generator robustness pattern

TinyRack generators (`custom_panel`, `custom_notched_post`, `custom_handle`)
use Pydantic schemas with constraints and clear descriptions.

Robustness details to copy:
- `Field(..., ge=..., gt=..., description=...)` for basic bounds
- Additional domain checks in code for geometric validity (e.g. non-overlap)
- `GeneratorValidationError` + `FieldError(path=(...))` for per-field,
    UI-friendly error feedback

This gives users actionable parameter errors instead of generic tracebacks.

### 10.5  Versioned model pattern at scale

TinyRack uses a consistent approach:
- `BuildEnv.from_local_git_repo()`
- Return base model when `versioned_model_enabled` is false
- Else return `Result(model=..., versioned=...)` with shallow engraved mark

Additional advanced detail from `post.py`:
- When returning a separate versioned part, propagate joints from the
    original model to the versioned model so assembly workflows still work.

### 10.6  Caching policy for expensive geometry

TinyRack applies `@cached` to thread-generation helpers (`make_top_screw`,
`make_bottom_thread`, `make_nut_connector_thread`) because those are expensive
and reused by multiple artifacts/generators.

Rule of thumb:
- Cache deterministic, expensive primitives.
- Keep cache boundaries at helper-function level, not whole artifacts.

### 10.7  Minimal MakerRepo config and dependency setup

TinyRack demonstrates a minimal `.makerrepo/config.yaml`:

```yaml
artifacts:
    default_config:
        export_3mf: false
```

And `pyproject.toml` includes both runtime and CLI dependencies in dev flow
(`makerrepo`, `makerrepo-cli`, `build123d`, etc.).

Practical takeaway:
- Use repo-level export defaults to control output volume.
- Keep decorator library + CLI available in the same environment for local
    validation.

### 10.8  Template to apply to our CAD projects

When adapting an existing CAD repo to MakerRepo, prefer this structure:

```text
myproject/
    .makerrepo/config.yaml
    pyproject.toml
    myproject/
        constants.py
        part_a.py
        part_b.py
        assembly.py
        tools/
            fixtures.py
```

Per part module:
1. Keep geometry in class/functions reusable outside MakerRepo
2. Add one or more `@artifact` wrappers with clear `short_desc`
3. Add `@customizable` wrappers where users need parameter control
4. Use `@cached` for heavy reusable primitives
5. Optionally add `Result`-based version stamping for traceability

This mirrors what works in TinyRack and yields clean artifact/generator pages
on MakerRepo.

---

## Quick Reference

| Want to… | Do this |
|----------|---------|
| Mark a model as publishable | `@artifact(short_desc="...")` |
| Make a model parametric | `@customizable(sample_parameters=Params())` |
| Cache an expensive sub-build | `@cached(short_desc="...")` |
| Return clean + versioned models | `return Result(model=..., versioned=...)` |
| Get build version for stamping | `BuildEnv.from_local_git_repo().get_build_version()` |
| Set repo-wide export defaults | `.makerrepo/config.yaml` |
| List all artifacts locally | `mr artifacts list` |
| Export an artifact | `mr artifacts export NAME -o file.step` |
| View in OCP Viewer | `mr artifacts view NAME` |
| Build a generator with params | `mr generators view NAME -p '{"key": val}'` |
| Clear stale cache | `mr cache prune --all` |

---

## See Also

- Official docs: <https://docs.makerrepo.com/>
- Library source: <https://github.com/LaunchPlatform/makerrepo>
- CLI source: <https://github.com/LaunchPlatform/makerrepo-cli>
- Philosophy: <https://docs.makerrepo.com/manufacturing-as-code/>
- Related skill: `cad-build123d-tools` (§9 has the brief catalog entry)
- Related skill: `cad-build123d-general` (foundational build123d API reference)
