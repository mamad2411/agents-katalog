---
name: follow-tool-rolldown-optimize bundle
description: Tune the Rolldown bundle — code splitting, treeshaking, advancedChunks
argument-hint: "[target-area]"
related:
  - follow-tool-rolldown
  - run-bench
  - deep-review-codebase
  - report-before-after
---

## Goal

Reduce size and tune the layout of Rolldown output — code splitting, tree-shaking, and `output.advancedChunks` — always measuring before and after

## Scope

- For standalone Rolldown (`rolldown.config.ts`) — inside Vite, use the `follow-tool-vite` workflows instead
- Covers `output.advancedChunks`, `treeshake`, `external`, minify, and sourcemap options
- These optimizations focus on output quality — not dev-server speed

## Execute

### 1. Baseline

> Goal: measure before editing; never guess the bottleneck

1. Run `bunx rolldown -c` and record build time and file size per chunk
2. Identify abnormally large chunks or modules that shouldn't be bundled — run `/deep-optimize`
3. Save the baseline for comparison (use `/report-before-after` at the end)

### 2. Tree-shaking

> Goal: dead code is actually removed

1. `treeshake` is on by default — check nobody disabled it
2. Set `sideEffects` in `package.json` or `treeshake.moduleSideEffects` correctly — flag only files with real side effects
3. A library that won't tree-shake → mark it `external` or import specific paths

### 3. Code Splitting

> Goal: split chunks for a reason

1. Dynamic `import()` in the source creates chunk boundaries — use for lazy features
2. A multi-entry `input` object shares common modules via `output.advancedChunks`
3. Use `advancedChunks` groups, e.g. a `vendor` group by `test`/`minSize`/`priority` — see official docs for all fields
4. Avoid overly small chunks or circular imports between chunks

### 4. Output Tuning

> Goal: minify and output options fit the target

1. `output.minify` — on for production, tune `compress`/`mangle` per official docs
2. `output.sourcemap` — pick a strategy per deployment (external map, hidden)
3. `external` for deps the consumer installs itself — libraries must never bundle `peerDependencies`
4. Set `entryFileNames`/`chunkFileNames` with a content hash when the output is a cacheable app bundle

### 5. Verify

> Goal: compare, no regressions

1. Rebuild → compare size/chunk count/build time against the baseline
2. import/require the output at every entry → no missing modules or lost side effects
3. If a regression → revert that point and report the diff

## Rules

### 1. Correctness First

- A wrong tree-shake/chunk split = broken runtime — verify the output after every change
- Never put files with real side effects under `sideEffects: false`

### 2. Options

- Use only options from the official docs (`rolldown.rs`) — the Rolldown API changes fast, never guess

## Expected Outcome

- A smaller bundle or better layout compared to the baseline
- Output importable at every entry with no behavior changes
