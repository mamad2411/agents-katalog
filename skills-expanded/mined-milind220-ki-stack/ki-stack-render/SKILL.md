---
name: ki-stack-render
description: |
  Render KiCad schematics, PCBs, symbols, and footprints into visual artifacts.
  Use when asked to view a KiCad object, generate SVG/PDF/PNG/JPEG outputs,
  inspect a design visually, produce before/after evidence, or prepare images
  for a vision-capable model.
license: MIT
compatibility: opencode
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# ki-stack-render

## Purpose

This skill teaches the agent how to turn KiCad design artifacts into visual outputs.

It is the canonical `ki-stack` skill for:

- schematic rendering
- PCB 2D rendering
- PCB 3D raster rendering
- symbol rendering
- footprint rendering
- SVG to PNG conversion when raster images are needed
- before/after visual verification

## When to use it

Use this skill when the user asks to:

- render a schematic sheet or whole schematic
- render a board or a specific layer set
- get a visual look at a symbol or footprint
- export PDF or SVG deliverables
- generate a PNG/JPEG screenshot-like artifact
- verify that a change actually looks correct

## Shared assumptions

- Prefer `kicad-cli` as the default render path.
- Prefer deterministic exports over GUI screenshots.
- If the model needs raster images and the CLI emits SVG, convert the SVG to PNG.
- Always report exact command lines and output paths.

## Phase 1: Orient

1. Locate `kicad-cli`:

   ```bash
   skills/ki-stack/bin/kicad-cli-path
   ```

2. Detect the version:

   ```bash
   skills/ki-stack/bin/kicad-version
   ```

3. If the input path is unclear, find likely KiCad files:

   ```bash
   skills/ki-stack/bin/kicad-project-find <root>
   ```

## Phase 2: Identify render target

Choose one of these target classes:

- schematic
- pcb-2d
- pcb-3d
- symbol
- footprint

Map the request to the target class before choosing the command.

Examples:

- "Show me this board" -> `pcb-2d` or `pcb-3d`
- "Render this symbol" -> `symbol`
- "Give me a screenshot of the footprint" -> `footprint`
- "Visualize page 2 of the schematic" -> `schematic`

## Phase 3: Render

Use the helper wrapper whenever possible.

### Schematic SVG

```bash
skills/ki-stack/bin/kicad-render schematic-svg design.kicad_sch out_dir
```

### Schematic PDF

```bash
skills/ki-stack/bin/kicad-render schematic-pdf design.kicad_sch design.pdf
```

### PCB SVG

```bash
skills/ki-stack/bin/kicad-render pcb-svg board.kicad_pcb out_dir --layers F.Cu,F.SilkS,Edge.Cuts --mode-single
```

### PCB PDF

```bash
skills/ki-stack/bin/kicad-render pcb-pdf board.kicad_pcb board.pdf --layers F.Cu,F.SilkS,Edge.Cuts --mode-single
```

### PCB 3D PNG/JPEG

```bash
skills/ki-stack/bin/kicad-render pcb-render board.kicad_pcb board.png --width 1800 --height 1200 --side top
```

### Symbol SVG

```bash
skills/ki-stack/bin/kicad-render symbol-svg library.kicad_sym out_dir --symbol Device:R
```

### Footprint SVG

```bash
skills/ki-stack/bin/kicad-render footprint-svg my.pretty out_dir --footprint SOIC-8_3.9x4.9mm_P1.27mm
```

## Phase 4: Convert if needed

If the output is SVG but the downstream model needs PNG:

```bash
skills/ki-stack/bin/kicad-svg-to-png input.svg output.png
```

## Phase 5: Verify

For render tasks, verification means:

- the command succeeded
- the output file exists
- the output format matches what the user asked for
- if this is a before/after check, both paths are preserved and clearly labeled

Prefer a before/after loop for edit verification:

1. render before
2. perform edit
3. render after
4. report both artifact paths

## Phase 6: Report

Always report:

- render target type
- command used
- output path(s)
- any conversion steps used
- any version-specific caveats

## Helper assets

References:

- `skills/ki-stack/references/render-recipes.md`
- `skills/ki-stack/references/version-matrix.md`

Helpers:

- `skills/ki-stack/bin/kicad-cli-path`
- `skills/ki-stack/bin/kicad-version`
- `skills/ki-stack/bin/kicad-project-find`
- `skills/ki-stack/bin/kicad-render`
- `skills/ki-stack/bin/kicad-svg-to-png`

## Guardrails

- If `kicad-cli` is unavailable, stop and report `BLOCKED`.
- If the input type is ambiguous, identify the file type before rendering.
- If a command fails, capture stderr and try a narrower invocation rather than guessing.
- If the user wants a GUI screenshot specifically, say that this skill produces deterministic exports rather than true live GUI screenshots.

## Completion states

- `DONE`: artifact created and path reported
- `DONE_WITH_CONCERNS`: artifact created but format conversion or version caveat exists
- `BLOCKED`: no CLI or render command failed irrecoverably
- `NEEDS_CONTEXT`: missing input path, missing target symbol/footprint name, or output format is unspecified
