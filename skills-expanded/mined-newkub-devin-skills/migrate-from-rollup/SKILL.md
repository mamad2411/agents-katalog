---
name: follow-tool-rolldown-migrate-from-rollup
description: Migrate Rollup → Rolldown — plugin mapping, config translation, verify
argument-hint: "[project-path]"
related:
  - follow-tool-rolldown
  - scan-codebase
  - deep-impact
  - deep-review-codebase
  - report-before-after
---

## Goal

Move `rollup.config.*` to `rolldown.config.ts` with equivalent output — correct plugin map, complete config translation, rollback-ready

## Scope

- For projects with `rollup.config.js/ts/mjs` that want to move to standalone Rolldown
- Covers config translation, plugin mapping (`@rollup/plugin-*` → Rolldown equivalents), output verification
- If Rollup is used through Vite → use the `follow-tool-vite` workflow `migrate-to-vite8` instead (Vite 8 uses Rolldown by default)

## Execute

### 1. Inventory Current Setup

> Goal: map every affected point before moving

1. Read `rollup.config.*` — list `input`, `output` (dir/file/format/plugins), `external`, `plugins`, `treeshake`, `watch`
2. List all plugins with versions — separate official `@rollup/plugin-*` from community
3. Capture a baseline: run the rollup build and record the output file list + sizes
4. Read the official migration guide at `rolldown.rs` — run `/learn` (web) if unsure
5. Commit the current state before starting — the rollback path must be ready

### 2. Install And Create Config

> Goal: create `rolldown.config.ts` alongside the original

1. `bun add -D rolldown` — keep `rollup` until verification passes
2. Create the new `rolldown.config.ts` with `defineConfig` from `rolldown` — don't delete the original rollup config
3. Translate options block by block: `input` → `input`, `output.*` → `output.*` (mostly the same names), `plugins` → `plugins`

### 3. Map Plugins

> Goal: every plugin has an equivalent

1. Check Rolldown's official plugin list — many `@rollup/plugin-*` keep working or have a builtin/native replacement
2. Priority: builtin feature > official Rolldown plugin (`@rolldown/*` or as the docs state) > compatible Rollup plugin
3. A plugin with no equivalent → defer the migration or find an alternative — see official docs
4. Test plugins one at a time — comment the rest out, re-enable as the build passes

### 4. Translate Remaining Options

> Goal: every option has a destination

1. `external`, `globals`, `paths` → direct maps in `external`/`output.*`
2. `manualChunks` → `output.advancedChunks` (or the field named in official docs)
3. `watch`, `onwarn`, `treeshake` → check the docs for equivalents
4. Options with no counterpart → decide: drop (if Rolldown does it builtin) or find a plugin

### 5. Verify Output

> Goal: output equivalent to the Rollup build

1. Run `bunx rolldown -c` → the build passes
2. Compare file list, sizes, formats with the baseline — diff important files if needed
3. import/require every entry in a consumer → works as before; run the test suite
4. All pass → remove the `rollup` deps + the original config, in a separate commit
5. Fails and can't be fixed within 3 rounds → rollback and report what remains

## Rules

### 1. Safety

- One commit per migration step — never mix with feature work
- Keep the rollup config until verification fully passes — the rollback path must always be ready

### 2. Fidelity

- Output must be equivalent: formats, externals, globals, sourcemap — never let output differ unintentionally
- Any plugin that changes behavior must be flagged in the report

## Expected Outcome

- `rolldown.config.ts` fully replaces the rollup config
- The build passes with equivalent output and tests green
- The build is faster or the same speed
