---
name: ki-stack-symbols
description: |
  Symbol-focused KiCad workflows built on top of the Phase 1 substrate skills.
  Use when the task is about symbol libraries, symbol inspection, symbol rendering,
  or proving symbol-side changes with deterministic exports.
license: MIT
compatibility: opencode
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# ki-stack-symbols

## Purpose

This Phase 2 domain skill orchestrates symbol-focused work by composing:

- `ki-stack-render`
- `ki-stack-file-surgery`
- `ki-stack-verify`

Use it when the user's intent is specifically about symbols or symbol libraries.

## What it covers

- symbol rendering
- symbol library inspection
- symbol-side offline edits and regeneration workflows
- symbol verification through exports

## Routing rules

### Use `ki-stack-render` when

- the user wants to inspect or compare a symbol visually
- the task is to export symbol artifacts

### Use `ki-stack-file-surgery` when

- the symbol task is a deterministic library or file transform
- preserving file structure and tokens matters

### Use `ki-stack-verify` after

- any symbol edit that should be proven visually

## Phase 1: Orient

1. Confirm the task is symbol-scoped.
2. Identify the `.kicad_sym` file and exact symbol name.
3. If the symbol name is missing, stop and ask for it or search the library contents first.

## Phase 2: Inspect

The most useful first step is usually rendering the target symbol.

Canonical command:

```bash
skills/ki-stack/bin/kicad-render symbol-svg library.kicad_sym out_dir --symbol Device:R
```

If the task is an offline edit, inspect the relevant library files before mutation.

## Phase 3: Execute

For symbol work in v1, prefer deterministic offline workflows over speculative live APIs.

Common execution path:

1. identify the symbol library file
2. render the baseline symbol
3. apply the symbol-side change offline
4. render the symbol again
5. report before/after artifacts

## Phase 4: Verify

The main proof for symbol tasks is visual and export-based.

Prefer:

1. render before
2. change symbol
3. render after
4. report both artifact paths

If the task affects downstream library behavior, note any limits in verification.

## Common symbol workflows

### Workflow: inspect a symbol visually

1. render the symbol as SVG
2. convert to PNG if a raster artifact is needed
3. report the artifact path

### Workflow: verify a symbol edit

1. render before
2. apply edit
3. render after
4. report the before/after paths and any file-level transform used

## Helper assets

Skills to compose:

- `skills/ki-stack/ki-stack-render/SKILL.md`
- `skills/ki-stack/ki-stack-file-surgery/SKILL.md`
- `skills/ki-stack/ki-stack-verify/SKILL.md`

References:

- `skills/ki-stack/references/render-recipes.md`

Helpers:

- `skills/ki-stack/bin/kicad-render`
- `skills/ki-stack/bin/kicad-svg-to-png`

## Guardrails

- Do not assume a symbol name if the user did not specify one.
- Prefer export-based proof over prose description.
- If the task is really about footprints or schematics, route to those skills.

## Completion states

- `DONE`: symbol task completed and visually verified
- `DONE_WITH_CONCERNS`: completed but verification is partial
- `BLOCKED`: file, symbol name, or tooling issue prevented completion
- `NEEDS_CONTEXT`: symbol library path or symbol identifier is missing
