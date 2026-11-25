---
name: ki-stack-pcb
description: |
  Flagship PCB workflow skill for KiCad agents. Use for board-level work:
  current board inspection, selected items, footprints, pads, tracks, vias,
  zones, layers, board metadata, PCB rendering, DRC, fabrication exports, and
  PCB editor automation through kicad-python IPC.
license: MIT
compatibility: opencode
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---
<!-- AUTO-GENERATED from SKILL.md.tmpl. Regenerate with scripts/gen-skill-docs. -->

# ki-stack-pcb

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

This is the flagship KiCad board skill. It should make agents good at the thing KiCad agents most often need: inspect and change a PCB using code, then prove the board still works.

PCB editor interactions use `kicad-python` IPC first. The CLI proves and exports. File surgery is fallback for deterministic offline board-file changes.

## Route Fast

| Task | Route |
| --- | --- |
| Current board, selected item, highlighted footprint/track/via/zone | `ki-stack-live` with `kicad-python` |
| Inspect nets, footprints, tracks, vias, zones, layers | `kicad-python` examples first |
| Move/update/create/delete board objects | `kicad-python` commit session |
| Render board top/bottom/layers/3D | `kicad-cli` via `ki-stack-render` |
| DRC, schematic parity, refill/save-board check | `kicad-cli pcb drc` |
| Gerbers, drill, pick/place, IPC-2581, ODB++, STEP, GLB, STL | `kicad-cli pcb export ...` |
| Metadata-only offline board transform | `kiutils-rs` if supported |
| Need a missing real part or KiCad artifacts | `https://pcbparts.dev/` |

## Start Here

```bash
KI_STACK_DIR="${KI_STACK_DIR:-skills/ki-stack}"
"$KI_STACK_DIR/bin/kicad-project-find" .
"$KI_STACK_DIR/bin/kicad-version"
"$KI_STACK_DIR/bin/kicad-python-smoke"
"$KI_STACK_DIR/bin/kicad-python-smoke" connect
```

If the task is about a file path, use that board. If the user says "current board" or "selected", IPC is required.

## First Five Commands

```bash
python3 skills/ki-stack/examples/ipc/hello_kicad.py
python3 skills/ki-stack/examples/ipc/board_inventory.py
python3 skills/ki-stack/examples/ipc/layer_overview.py
python3 skills/ki-stack/examples/ipc/selection_dump.py
python3 skills/ki-stack/examples/ipc/footprint_report.py
```

Do this before writing custom code. It gives the agent board name, counts, layers, selected objects, and footprints.

## Board Inspection Recipes

### Current selection

```bash
python3 skills/ki-stack/examples/ipc/selection_dump.py
```

Use for:

- "selected footprint"
- "these traces"
- "highlighted vias"
- "current item"

### Inventory and risk scan

```bash
python3 skills/ki-stack/examples/ipc/board_inventory.py
python3 skills/ki-stack/examples/ipc/layer_overview.py
python3 skills/ki-stack/examples/ipc/footprint_report.py
```

Use for:

- board summary
- layer-aware work
- footprint lookup
- deciding render layers

### Save a checkpoint

```bash
python3 skills/ki-stack/examples/ipc/save_board_copy.py /tmp/before-edit.kicad_pcb
```

Use before:

- bulk edits
- footprint movement
- route/zone work
- any script that creates/removes items

## Board Mutation Recipe

1. Save a copy if risk is non-trivial.
2. Inspect current state.
3. Begin IPC commit.
4. Mutate.
5. Refill zones if copper changed.
6. Push commit with clear message.
7. Save only if intended.
8. Render.
9. DRC.

Skeleton:

```python
from kipy import KiCad

with KiCad() as k:
    board = k.get_board()
    commit = board.begin_commit()
    try:
        # inspect target first
        # create/update/remove items here
        # board.refill_zones() if copper changed
        board.push_commit(commit, "Describe PCB edit")
        board.save()
    except Exception:
        board.drop_commit(commit)
        raise
```

## Render Proof

### Top copper/silkscreen/outline SVG

```bash
skills/ki-stack/bin/kicad-render pcb-svg board.kicad_pcb /tmp/pcb-svg --layers F.Cu,F.SilkS,Edge.Cuts --mode-single --fit-page-to-board
```

### Bottom side SVG

```bash
skills/ki-stack/bin/kicad-render pcb-svg board.kicad_pcb /tmp/pcb-bottom-svg --layers B.Cu,B.SilkS,Edge.Cuts --mirror --mode-single --fit-page-to-board
```

### 3D PNG

```bash
skills/ki-stack/bin/kicad-render pcb-render board.kicad_pcb /tmp/board-top.png --width 1800 --height 1200 --side top
```

## DRC Proof

```bash
skills/ki-stack/bin/kicad-drc-json board.kicad_pcb /tmp/drc.json
```

For parity-sensitive work:

```bash
kicad-cli pcb drc --format json --exit-code-violations --schematic-parity --output /tmp/drc.json board.kicad_pcb
```

If zones changed and the board should be saved after refill:

```bash
kicad-cli pcb drc --refill-zones --save-board --format json --output /tmp/drc.json board.kicad_pcb
```

## Fabrication And Mechanical Exports

Use `kicad-cli` instead of custom scripts:

```bash
kicad-cli pcb export gerbers --output fab/gerbers board.kicad_pcb
kicad-cli pcb export drill --output fab/drill board.kicad_pcb
kicad-cli pcb export pos --output fab/position.csv board.kicad_pcb
kicad-cli pcb export ipc2581 --output fab/board.xml board.kicad_pcb
kicad-cli pcb export odb --output fab/odb board.kicad_pcb
kicad-cli pcb export step --output mech/board.step board.kicad_pcb
kicad-cli pcb export glb --output mech/board.glb board.kicad_pcb
```

Run `kicad-cli pcb export <target> -h` when flags matter. The CLI docs are current source of truth.

## Parts Search

When a board task needs a real component, footprint, symbol, JLC/LCSC/CSE data, lifecycle clue, or vendor artifact:

1. Search `https://pcbparts.dev/`.
2. Record manufacturer part number and vendor/source.
3. Use KiCad artifacts from source when available.
4. Verify symbol/footprint visually before use.

Do not invent footprints or pinouts from memory when a part source is available.

## Offline Board File Surgery

Use only when live IPC is unnecessary or unavailable and the edit is deterministic.

```bash
skills/ki-stack/bin/kiutils-inspect board.kicad_pcb --show-unknown --show-diagnostics --show-canonical
```

Then use `kiutils-rs` typed setters/upserts/removals if the stable API supports the edit. If the task is really schematic or symbol S-expression work, route to `kicad-skip` or `ki-stack-file-surgery`.

## Stop Conditions

- User says "selected/current/open board" but IPC cannot connect: `BLOCKED`.
- Board geometry changed but no render: `DONE_WITH_CONCERNS`.
- Electrical geometry changed but DRC not run: `DONE_WITH_CONCERNS`.
- DRC has violations: report exact count/path and classify as new, pre-existing, or unknown.
- Part data is guessed without source: not acceptable.

## Report

```text
PCB REPORT
Target: <live board|board file>
Route: <IPC|CLI|file surgery|parts search>
Actions: <scripts/commands>
Artifacts: <renders/exports>
Checks: <DRC/ERC/file inspect>
Parts: <pcbparts.dev/source evidence if used>
Status: DONE|DONE_WITH_CONCERNS|BLOCKED|NEEDS_CONTEXT
```
