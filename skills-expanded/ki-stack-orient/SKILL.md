---
name: ki-stack-orient
description: |
  First-stop KiCad orientation skill. Use when starting any KiCad task, when the
  right substrate is unclear, when locating project files, when checking KiCad
  CLI or Python IPC availability, or when deciding between live IPC, kicad-cli,
  structured file edits, and parts search.
license: MIT
compatibility: opencode
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---
<!-- AUTO-GENERATED from SKILL.md.tmpl. Regenerate with scripts/gen-skill-docs. -->

# ki-stack-orient

## Preamble (run first)

Run this before choosing a KiCad workflow:

```bash
KI_STACK_DIR="${KI_STACK_DIR:-skills/ki-stack}"
"$KI_STACK_DIR/bin/ki-stack-update-check" 2>/dev/null || true
"$KI_STACK_DIR/bin/kicad-project-find" . 2>/dev/null | sed -n '1,80p' || true
"$KI_STACK_DIR/bin/kicad-version" 2>/dev/null || true
"$KI_STACK_DIR/bin/kicad-python-smoke" 2>/dev/null || true
```

Read these when the task touches the area:

- `skills/ki-stack/ETHOS.md`
- `skills/ki-stack/references/version-matrix.md`
- `skills/ki-stack/references/render-recipes.md`
- `skills/ki-stack/references/ipc-recipes.md`
- `skills/ki-stack/references/ipc-board-workflows.md`
- `skills/ki-stack/references/file-editing-recipes.md`

## Stack Rules

- PCB editor interaction or current selection: use `kicad-python` IPC.
- Render, import/export, DRC, ERC, fabrication, 3D outputs: use `kicad-cli`.
- Schematic/library/project file edits: use `kicad-skip`, `kiutils-rs`, or another structured parser. Do not hand-roll S-expression edits when a parser fits.
- Parts search and KiCad-ready vendor artifacts: check `https://pcbparts.dev/` early.
- File format truth: use KiCad developer file-format docs at `https://dev-docs.kicad.org/en/file-formats/`.
- No success claim without evidence: artifact path, DRC/ERC output, changed file list, or script output.

## Completion Status

- `DONE`: completed and verified.
- `DONE_WITH_CONCERNS`: completed but proof is partial, version-limited, or blocked by pre-existing issues.
- `BLOCKED`: prerequisite unavailable or command failed after a concrete attempt.
- `NEEDS_CONTEXT`: target file, object, board session, or intended result is unclear.

## Purpose

This is the first skill for KiCad work. It makes the agent stop guessing and quickly answer:

1. What KiCad files are present?
2. What KiCad version and CLI are available?
3. Are Python IPC bindings installed?
4. Is a live KiCad board reachable?
5. Which substrate should do the work?

## Decision Table

| User intent | First route | Why |
| --- | --- | --- |
| Current board, selected items, interactive PCB editor state | `ki-stack-live` / `ki-stack-pcb` with `kicad-python` | IPC sees the open editor and selection. |
| Move/inspect/update footprints, tracks, vias, zones, layers | `ki-stack-pcb` with `kicad-python` | This is PCB editor interaction. |
| Render board/schematic/symbol/footprint | `ki-stack-render` with `kicad-cli` | Deterministic visual artifact. |
| DRC/ERC, fabrication, 3D, BOM/netlist/export/import/upgrade | `ki-stack-verify` or `ki-stack-render` with `kicad-cli` | The CLI already owns these flows. |
| Schematic/project/library text-variable or symbol metadata edit | `ki-stack-file-surgery` with `kicad-skip` or `kiutils-rs` | Structured file edit beats raw S-expression surgery. |
| Need a new part, JLC/LCSC/CSE artifact, KiCad symbol/footprint | Search `https://pcbparts.dev/` first | Parts search is a solved external data problem. |
| Unsure what a token means | KiCad file-format docs | `https://dev-docs.kicad.org/en/file-formats/` is source of truth. |

## CLI Surface To Remember

`kicad-cli` covers much more than render:

- `api-server`: headless IPC server on newer KiCad.
- `fp`: footprint export and upgrade.
- `gerber`: convert, diff, inspect Gerber files.
- `jobset`: run `.kicad_jobset` outputs.
- `pcb`: DRC, import, upgrade, render, export.
- `sch`: ERC, upgrade, BOM, netlist, PDF/SVG/PNG/DXF/HPGL/PostScript.
- `sym`: symbol export and upgrade.
- `version`: version info.

High-value PCB exports:

- fabrication: Gerber, drill, position, IPC-D-356, IPC-2581, ODB++, GenCAD.
- documentation: PDF, SVG, PNG, DXF, HPGL, PostScript, statistics.
- 3D/mechanical: STEP, STEPZ, STL, GLB, VRML, PLY, U3D, BREP, XAO, 3D PDF.

## Orient Commands

```bash
KI_STACK_DIR="${KI_STACK_DIR:-skills/ki-stack}"
"$KI_STACK_DIR/bin/kicad-project-find" .
"$KI_STACK_DIR/bin/kicad-version"
"$KI_STACK_DIR/bin/kicad-python-smoke"
"$KI_STACK_DIR/bin/kicad-python-smoke" connect
```

If `connect` fails, do not force IPC. Use the error to decide:

- import failed: install or fix `kicad-python`.
- connect failed: KiCad GUI/API server not reachable.
- board failed: KiCad reachable but no board open.

## Evidence Contract

Before ending a KiCad task, produce at least one:

- rendered artifact path
- DRC/ERC JSON path and pass/fail summary
- IPC script output
- structured parser output or changed file diff
- part-search source URL or artifact path

## Completion

Report:

```text
KI-STACK ORIENT
Files: <found files or none>
KiCad: <version or unavailable>
IPC: <import/connect/board status>
Route: <live|cli|file-edit|parts-search|ask>
Next skill: <skill name>
Status: DONE|DONE_WITH_CONCERNS|BLOCKED|NEEDS_CONTEXT
```
