---
name: ki-stack-live
description: |
  Control a running KiCad session through the official kicad-python IPC bindings.
  Use for PCB editor interactions, open-board state, current selection, live
  footprint/track/via/zone/layer work, undoable board mutations, and scripts that
  chain many KiCad IPC calls together.
license: MIT
compatibility: opencode
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---
<!-- AUTO-GENERATED from SKILL.md.tmpl. Regenerate with scripts/gen-skill-docs. -->

# ki-stack-live

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

This is the main action space for a running KiCad PCB editor.

Use `kicad-python` IPC for:

- current board
- current selection
- PCB editor state
- footprints, pads, tracks, vias, zones, layers
- undoable edits
- fast inspect/edit/render loops

Do not use this for schematic S-expression surgery. Use `kicad-skip`, `kiutils-rs`, or another structured file parser for offline schematic/library/project edits.

## Run First

```bash
KI_STACK_DIR="${KI_STACK_DIR:-skills/ki-stack}"
"$KI_STACK_DIR/bin/kicad-python-smoke"
"$KI_STACK_DIR/bin/kicad-python-smoke" connect
```

Interpret failures plainly:

- `kipy_import=failed`: install or fix `kicad-python`.
- `ipc_connect=failed`: no reachable KiCad API server, API disabled, busy KiCad, bad socket/token, or version mismatch.
- `board_open=failed`: KiCad is reachable but no board is open.

KiCad 9/10 usually means GUI-backed IPC. KiCad 11+ may support `kicad-cli api-server` and `KiCad(headless=True, ...)`.

## Golden Path

1. Prove import/connect.
2. Inspect board or selection.
3. Copy the closest example.
4. If editing, use `begin_commit()`.
5. Push or drop the commit.
6. Save only when intended.
7. Render with `kicad-cli`.
8. Run DRC if electrical or geometry risk exists.

## Copy These First

```bash
python3 skills/ki-stack/examples/ipc/hello_kicad.py
python3 skills/ki-stack/examples/ipc/board_inventory.py
python3 skills/ki-stack/examples/ipc/layer_overview.py
python3 skills/ki-stack/examples/ipc/selection_dump.py
python3 skills/ki-stack/examples/ipc/footprint_report.py
```

Mutation examples:

```bash
python3 skills/ki-stack/examples/ipc/update_title_block.py --title "Agent Edited Board"
python3 skills/ki-stack/examples/ipc/save_board_copy.py /tmp/board-copy.kicad_pcb
```

## Minimal Inspect Script

```python
from kipy import KiCad

with KiCad() as k:
    print(k.get_version())
    board = k.get_board()
    print(board.name)
    print("nets", len(board.get_nets()))
    print("footprints", len(board.get_footprints()))
    print("tracks", len(board.get_tracks()))
    print("vias", len(board.get_vias()))
    print("zones", len(board.get_zones()))
```

## Selection First

If the user says "selected", "this footprint", "these traces", "current item", or "the highlighted thing", inspect selection before searching.

```python
from kipy import KiCad

with KiCad() as k:
    board = k.get_board()
    selection = list(board.get_selection())
    print("selection_count", len(selection))
    print(board.get_selection_as_string())
```

This avoids the classic mistake: inventing a search heuristic when the user already selected the object.

## Undoable Mutation Pattern

Use this for every multi-step board edit:

```python
from kipy import KiCad

with KiCad() as k:
    board = k.get_board()
    commit = board.begin_commit()

    try:
        title = board.get_title_block_info()
        title.title = "Agent Edited Board"
        board.set_title_block_info(title)

        board.push_commit(commit, "Update board title")
        board.save()
    except Exception:
        board.drop_commit(commit)
        raise
```

Rules:

- `begin_commit()` before grouped edits.
- `push_commit()` only after local checks pass.
- `drop_commit()` on exceptions or bad detected state.
- `save()` only when the user asked for persistence or the workflow requires it.

## Useful Board Calls

Inspection:

- `get_open_documents()`
- `get_board()`
- `get_project()`
- `get_as_string()`
- `get_nets()`
- `get_tracks()`
- `get_vias()`
- `get_footprints()`
- `get_pads()`
- `get_zones()`
- `get_items()`
- `get_items_by_id()`
- `get_items_by_net()`
- `get_item_bounding_box()`
- `get_selection()`
- `get_selection_as_string()`
- `get_stackup()`
- `get_title_block_info()`

Mutation/editor state:

- `begin_commit()`
- `push_commit()`
- `drop_commit()`
- `create_items()`
- `update_items()`
- `remove_items()`
- `set_active_layer()`
- `set_visible_layers()`
- `set_origin()`
- `set_title_block_info()`
- `refill_zones()`
- `save()`
- `save_as()`

Prefer `kicad-cli` for export/check proof even when IPC exposes export helpers. The CLI is easier to run repeatably and compare.

## Verification

After any live edit:

```bash
KI_STACK_DIR="${KI_STACK_DIR:-skills/ki-stack}"
"$KI_STACK_DIR/bin/kicad-render" pcb-svg board.kicad_pcb /tmp/after-svg --layers F.Cu,F.SilkS,Edge.Cuts --mode-single
"$KI_STACK_DIR/bin/kicad-drc-json" board.kicad_pcb /tmp/drc.json
```

Use DRC when:

- tracks, vias, zones, pads, footprints, net ties, or board outline changed
- zones were refilled
- the edit could affect clearance/connectivity

Render-only is enough for:

- title block changes
- layer visibility experiments
- pure visual annotation if no electrical geometry changed

## Stop Conditions

- No `kicad-python` import: `BLOCKED`, unless an offline file route can satisfy the user.
- No IPC connection: `BLOCKED` for current-board/current-selection tasks.
- No board open: `NEEDS_CONTEXT` unless a file path was provided.
- Three failed script attempts: stop and report attempted scripts/errors.
- Electrical edit without DRC: `DONE_WITH_CONCERNS`, not `DONE`.

## Report

```text
LIVE IPC REPORT
Connection: <import/connect/board status>
Script: <path or inline summary>
Commit: <pushed|dropped|none>
Saved: <yes|no|copy path>
Evidence: <render paths, DRC path, script output>
Status: DONE|DONE_WITH_CONCERNS|BLOCKED|NEEDS_CONTEXT
```
