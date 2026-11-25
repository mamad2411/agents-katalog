---
name: ki-stack-footprints
description: |
  Footprint-focused KiCad workflows built on top of the Phase 1 substrate skills.
  Use when the task is about footprint libraries, footprint inspection, footprint
  rendering, or proving footprint-side changes with deterministic exports.
license: MIT
compatibility: opencode
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# ki-stack-footprints

## Purpose

This Phase 2 domain skill orchestrates footprint-focused work by composing:

- `ki-stack-render`
- `ki-stack-file-surgery`
- `ki-stack-verify`
- `ki-stack-live` when the footprint is being inspected from a placed board context

Use it when the user's intent is specifically about footprints or footprint libraries.

## What it covers

- footprint rendering
- footprint library inspection
- footprint-side offline edits
- visual proof of footprint changes
- placed-footprint inspection through board context when relevant

## Routing rules

### Use `ki-stack-render` when

- the user wants a visual of a footprint
- the goal is export, inspection, or before/after proof

### Use `ki-stack-file-surgery` when

- the task is a deterministic footprint-library edit
- the change is offline and file-structural

### Use `ki-stack-live` when

- the footprint is being investigated as a placed object on a live board
- selection or board context matters

### Use `ki-stack-verify` after

- any footprint change that should be proven visually

## Phase 1: Orient

1. Confirm the task is footprint-scoped.
2. Identify the `.pretty` library directory and the exact footprint name, or identify the placed footprint on a board.
3. If the footprint name is unclear, stop and ask or inspect the library contents first.

## Phase 2: Inspect

For library-side tasks, the first useful step is usually a visual export.

Canonical command:

```bash
skills/ki-stack/bin/kicad-render footprint-svg my.pretty out_dir --footprint SOIC-8_3.9x4.9mm_P1.27mm
```

For placed-footprint tasks on a live board, start with the PCB examples in `ki-stack-live` and `ki-stack-pcb`.

## Phase 3: Execute

For footprint tasks in v1, prefer deterministic offline library workflows unless the request is explicitly about a placed footprint in a board context.

Common execution path:

1. identify footprint library and footprint name
2. render the baseline footprint
3. apply the footprint-side change offline or via board context
4. render again
5. report before/after artifacts

## Phase 4: Verify

The main proof for footprint tasks is visual.

Prefer:

1. render before
2. change footprint
3. render after
4. report both artifact paths

If the footprint change affects a placed board design, also route through PCB verification where relevant.

## Common footprint workflows

### Workflow: inspect a footprint visually

1. render the footprint as SVG
2. convert to PNG if a raster artifact is needed
3. report the artifact path

### Workflow: verify a footprint edit

1. render before
2. apply edit
3. render after
4. if needed, inspect the placed footprint in PCB context too

## Helper assets

Skills to compose:

- `skills/ki-stack/ki-stack-render/SKILL.md`
- `skills/ki-stack/ki-stack-file-surgery/SKILL.md`
- `skills/ki-stack/ki-stack-verify/SKILL.md`
- `skills/ki-stack/ki-stack-live/SKILL.md`

References:

- `skills/ki-stack/references/render-recipes.md`

Helpers:

- `skills/ki-stack/bin/kicad-render`
- `skills/ki-stack/bin/kicad-svg-to-png`

## Guardrails

- Distinguish clearly between a library footprint and a placed footprint instance on a board.
- Do not assume the footprint name if it is not specified.
- If the task is really board-scoped, route to `ki-stack-pcb`.

## Completion states

- `DONE`: footprint task completed and visually verified
- `DONE_WITH_CONCERNS`: completed but verification is partial or board placement effects were not fully checked
- `BLOCKED`: file, footprint name, or tooling issue prevented completion
- `NEEDS_CONTEXT`: footprint library path, placed-board context, or footprint identifier is missing
