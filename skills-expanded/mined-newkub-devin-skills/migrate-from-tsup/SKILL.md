---
name: follow-tool-tsdown-migrate-from-tsup
description: Migrate tsup → tsdown — config translation, verify build
argument-hint: "[project-path]"
related:
  - follow-tool-tsdown
  - follow-tool-rolldown
  - deep-review-codebase
  - report-before-after
---

## Goal

Move a tsup config to tsdown with equivalent output — use the migration tool first, fix the rest manually, with a rollback path

## Scope

- Applies to library projects with `tsup.config.*` or `tsup` in `package.json`
- Covers `tsdown-migrate`, config option mapping, output verification
- New projects that never used tsup → use `workflows/setup-tsdown/SKILL.md`

## Execute

### 1. Baseline And Plan

> Goal: capture the original state before migrating

1. Read `tsup.config.*` / the `tsup` field in `package.json` — list `entry`, `format`, `dts`, `external`, `esbuildOptions`, `onSuccess`, hooks
2. Run the `tsup` build and save the `dist/` file list + sizes as the baseline
3. Read the official migration guide in the tsdown docs — do `/learn` (web) if unsure
4. Commit the state before starting — the rollback path must be ready

### 2. Run tsdown-migrate

> Goal: use the official migration tool before manual edits

1. Run `bunx tsdown-migrate` — the tool converts `tsup.config.*` → `tsdown.config.ts` and adjusts `package.json`
2. Review the whole diff the tool made — don't trust it unverified
3. Install `tsdown` as the tool specifies (`bun add -D tsdown`)

### 3. Manual Config Translation

> Goal: options the tool didn't cover

1. Map the remaining options: `esbuildOptions` → rolldown/hooks equivalents per docs, `onSuccess` → a hook tsdown supports, `define`/`env` → check counterparts
2. tsup's esbuild plugins → must become Rolldown/unplugin plugins — see official docs
3. Options with no counterpart → flag them clearly in the report

### 4. Update Package Metadata

> Goal: scripts/exports point at tsdown

1. scripts: `tsup` → `tsdown`, `tsup --watch` → `tsdown --watch`
2. Check `exports`/`main`/`types` match the output tsdown produces — naming may differ from tsup
3. Remove the `tsup` dep only after verification passes

### 5. Verify Output

> Goal: output equivalent to the tsup build

1. Run `bun run build` → passes
2. Compare `dist/` with the baseline: file list, formats, `.d.ts` complete
3. import/require every entry in a consumer + run tests
4. Passes → delete the tsup config + dep in a separate commit, report via `/report-before-after`
5. Fails within 3 rounds → rollback (the tsup setup is still in git history), then report

## Rules

### 1. Safety

- Always use `tsdown-migrate` before manual edits
- Keep the migration in its own commit — never mix in feature work

### 2. Fidelity

- Output formats/`.d.ts`/sourcemap must equal the original tsup ones
- esbuild plugins don't work on tsdown directly — map them, don't copy

- Use /follow-tool-tsdown if needed
- Use /follow-tool-rolldown if needed
- Use /deep-review-codebase if needed

## Expected Outcome

- `tsdown.config.ts` replaces the tsup config, build passes with equivalent output
- The `tsup` dep is removed, scripts point at tsdown
