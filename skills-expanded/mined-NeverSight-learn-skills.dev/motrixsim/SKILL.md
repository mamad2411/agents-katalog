---
name: motrixsim
description: Use when writing, debugging, or reviewing MotrixSim Python programs, simulation scripts, or MJCF XML models. The agent must use the versioned motrixsim-docs-md documentation as the source of truth for Python API and MJCF XML details, especially when choosing classes, methods, attributes, canonical MJCF paths, defaults behavior, or validation commands.
---

# MotrixSim

Use this skill for MotrixSim Python programming and MJCF XML model construction.

## Documentation source

Use `motrixsim-docs-md` as the source of truth. Do not guess API signatures or MJCF attributes from memory.

Find the docs in this order:

1. `<current-repo>/motrixsim-python/motrixsim-docs-md`
2. `<current-repo>/motrixsim-docs-md`
3. determine the target MotrixSim version, then check `~/.motrixsim/docs-md/<version>/`
4. if that versioned local directory is missing, download the matching tag from `https://github.com/Motphys/motrixsim-agent-docs.git`

Expected layout:

- `api_md/index.md` - Python API registry
- `mjcf_md/index.md` - MJCF XML canonical path registry

Before reading from `~/.motrixsim`, identify the target version from the user request or the current project. Do not scan global docs and pick an arbitrary installed version.

When using the GitHub fallback, do not use an arbitrary latest checkout. If the exact tag is missing, list available tags and pick the closest version that does not exceed the target, then inform the user of the version mismatch. If no reasonable match exists, report the exact blocker before inventing API or XML details.

## Task routing

- Installation, environment setup, or missing dependency: read the official installation guide at `https://motrixsim.readthedocs.io/zh-cn/latest/user_guide/getting_started/installation.html`.
- Python program or API usage: read [references/python-workflow.md](references/python-workflow.md), then use `api_md/index.md`.
- MJCF XML model, XML attributes, defaults, or tags: read [references/mjcf-workflow.md](references/mjcf-workflow.md), then use `mjcf_md/index.md`.
- Combined task, such as loading MJCF from Python: read both workflow references.
- Docs repo layout or version question: read [references/docs-layout.md](references/docs-layout.md).

## Core workflow

1. Locate the version-correct `motrixsim-docs-md`.
2. Read the relevant index before target docs.
3. Resolve the exact API symbol or canonical MJCF path before editing.
4. Read only the needed documentation block or file.
5. Implement the script/model using documented names and constraints.
6. Validate with the narrowest runnable check available.

## Validation expectations

- For Python scripts, run the script or a focused Python test when dependencies are available.
- For MJCF models, parse or load the XML through MotrixSim when possible.
- If validation cannot run because MotrixSim, Python dependencies, or docs are unavailable, state the exact blocker.
- If MotrixSim is not installed, consult the official installation guide before proposing package-manager commands.

## Rules

- Prefer exact names from `motrixsim-docs-md` over recalled API names.
- For MJCF, always use canonical paths such as `body/joint`, `equality/joint`, and `tendon/fixed/joint`; never treat bare `joint` as an unambiguous element.
- For `default/<tag>` MJCF entries, read `Defaults Target` before deciding which real element semantics apply.
- Keep generated XML and Python examples minimal unless the user asks for a complete project.
- Do not edit generated docs by hand; regenerate them from the owning repository when asked to update docs.
