---
name: ki-stack-schematic
description: |
  Schematic-focused KiCad workflows built on top of the Phase 1 substrate skills.
  Use when the task is about schematic pages, ERC, project text variables, sheet
  rendering, or proving schematic-side changes with exports and checks.
license: MIT
compatibility: opencode
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# ki-stack-schematic

## Purpose

This Phase 2 domain skill orchestrates schematic-focused work by composing:

- `ki-stack-render`
- `ki-stack-file-surgery`
- `ki-stack-verify`
- `ki-stack-live` when schematic-side IPC support is relevant in the environment

Use this skill when the user's intent is clearly about schematics rather than boards.

## What it covers

- rendering schematic sheets and full schematics
- schematic ERC
- project text variable workflows
- schematic file discovery and inspection
- proof-oriented schematic change verification

## Routing rules

### Use `ki-stack-render` when

- the user wants to see a schematic page or export it
- the task is primarily visual
- the goal is proof, documentation, or comparison

### Use `ki-stack-file-surgery` when

- the schematic-side task is a deterministic file transformation
- the task is project-file or metadata oriented
- no live editor context is required

### Use `ki-stack-live` when

- the environment exposes the needed schematic-side API surface
- the task genuinely benefits from live project/editor state

### Use `ki-stack-verify` after

- schematic changes that could affect electrical correctness
- any schematic edit that needs before/after proof

## Phase 1: Orient

1. Confirm the task is schematic-scoped.
2. Identify the relevant `.kicad_sch` and `.kicad_pro` files.
3. Probe the environment:

   ```bash
   skills/ki-stack/bin/kicad-version
   skills/ki-stack/bin/kicad-project-find <root>
   ```

4. Decide the path:

- render-only
- offline file/proj transform
- live API path if the environment supports it

## Phase 2: Inspect

For schematic tasks, inspect the available files and identify page scope before editing.

Helpful checks:

```bash
skills/ki-stack/bin/kicad-project-find <root>
```

For project-side text variables, the `kicad-python` project object exposes:

- `get_text_variables()`
- `set_text_variables()`
- `expand_text_variables()`

If the task is visual, render a baseline artifact first.

## Phase 3: Execute

### Render/export path

Use:

```bash
skills/ki-stack/bin/kicad-render schematic-svg design.kicad_sch out_dir
skills/ki-stack/bin/kicad-render schematic-pdf design.kicad_sch design.pdf
```

### File-based path

For deterministic project-side edits, modify the relevant files carefully, then verify with render plus ERC.

### Live path

Only use the live path if the needed schematic or project APIs are clearly available in the environment. Avoid inventing undocumented live flows.

## Phase 4: Verify

For schematic changes, verify with:

1. render after change
2. run ERC
3. report exact artifact and check paths

Preferred ERC command:

```bash
skills/ki-stack/bin/kicad-erc-json design.kicad_sch erc.json
```

## Common schematic workflows

### Workflow: render a schematic for inspection

1. render SVG or PDF
2. if there are multiple pages, scope the output using `--pages`
3. report the output paths

### Workflow: verify a schematic change

1. render before
2. apply change
3. render after
4. run ERC
5. report both artifacts and the ERC result

### Workflow: inspect project variables

1. identify the project file
2. use the project API or file-based path to inspect variables
3. verify any variable-driven output by rendering the schematic again

## Helper assets

Skills to compose:

- `skills/ki-stack/ki-stack-render/SKILL.md`
- `skills/ki-stack/ki-stack-file-surgery/SKILL.md`
- `skills/ki-stack/ki-stack-verify/SKILL.md`
- `skills/ki-stack/ki-stack-live/SKILL.md`

References:

- `skills/ki-stack/references/render-recipes.md`
- `skills/ki-stack/references/version-matrix.md`

Helpers:

- `skills/ki-stack/bin/kicad-render`
- `skills/ki-stack/bin/kicad-erc-json`
- `skills/ki-stack/bin/kicad-project-find`

## Guardrails

- Do not assume the same live API richness on schematics that exists on boards.
- Prefer deterministic render plus ERC workflows.
- If the task is really about symbols or footprints, route to those domain skills.
- If page scope matters, specify it explicitly in the render command.

## Completion states

- `DONE`: schematic task completed and verified
- `DONE_WITH_CONCERNS`: completed but verification or API support is partial
- `BLOCKED`: environment or version prevented completion
- `NEEDS_CONTEXT`: missing schematic path, page scope, or intended outcome
