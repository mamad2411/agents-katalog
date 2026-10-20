---
name: preset-debugger
description: "Diagnose and fix broken dotclaude presets and their bundled plugin scripts. ONLY for dotclaude preset/plugin artifacts in this dotclaude repo — do NOT invoke for general TypeScript debugging, npm package issues, or non-dotclaude tools. Invoke only when called from /preset-wizard or when the user explicitly requests help with a dotclaude preset that fails to build, typecheck, or pass tests."
---

# preset-debugger

Diagnose and fix failures in dotclaude preset artifacts: YAML files, sidecar files,
plugin builds, and generated vitest stubs. Follow phases in order.

**Rules:**
- Never fix errors silently — always show the proposed change and get user approval before applying.
- Never attempt fixes outside of `presets/`, `claudekit/`, `scripts/`, and `plugins/` — do not modify unrelated code.
- After applying a fix, always re-run the full verify suite before reporting success.

---

## Input Context

This skill may be invoked with context from `/preset-wizard`. If provided, use it directly
rather than re-running diagnosis from scratch:

- **Failed step**: which command failed (`pnpm typecheck` / `pnpm build-plugin` / `pnpm test`)
- **Error output**: exact stderr/stdout from the failed command
- **Files created**: list of files created in the current session

If invoked manually without context, run the full diagnosis phase.

---

## Phase 1 — Diagnosis

### Step 1a — Identify scope

Ask the user (or infer from context):
- Which preset name? (to know which YAML + plugin to check)
- Which step is failing, if known?

### Step 1b — Run the verify suite

Run all three checks and capture exact output:

```bash
pnpm typecheck
pnpm build-plugin <preset-name>
pnpm test
```

For each command, record: pass ✓ / fail ✗ + exact error message.

### Step 1c — Parse errors and identify root cause

Match the error output against known failure patterns:

#### Pattern A — Preset YAML schema violation
Symptoms: `ZodError`, `validation failed`, `does not match schema`

Common causes:
- Missing required field (`name`, `kind`, `description`, `version`)
- `name` not kebab-case (`/^[a-z][a-z0-9-]*$/`)
- `version` not SemVer (`X.Y.Z`)
- `external_setup` entry has `standalone: false` but no `install_hint`
- Component listed in `components.*` does not exist in `claudekit/`
- `settings_patch` contains nested object that conflicts with schema

Fix direction: edit the preset YAML to satisfy the schema.

#### Pattern B — Component not found during build
Symptoms: `ENOENT`, `component not found`, `locateComponent failed`

Common causes:
- Component name in preset YAML is misspelled
- Component exists in claudekit as a folder but was referenced as file (or vice versa)
- Component was renamed or moved in claudekit

Fix direction: correct the component name in the preset YAML, or vendor the missing component.

#### Pattern C — Sidecar validation failure
Symptoms: `sidecar.schema.json`, `invalid sidecar`, `commit must be full 40-char SHA-1`

Common causes:
- `source.commit` is not a full 40-char hex SHA (e.g., short hash)
- `imported_at` is not `YYYY-MM-DD` format
- Required field missing (`source`, `license`, `modified`)
- `modifications` is non-null but `modified: false`

Fix direction: correct the `.source.yaml` or `SOURCE.yaml` file for the affected component.

#### Pattern D — TypeScript error in scripts
Symptoms: `error TS...` from `pnpm typecheck`

Common causes:
- `exactOptionalPropertyTypes` violation: accessing a field that could be `undefined` without a guard
- `noUncheckedIndexedAccess` violation: indexing an array without checking bounds
- Missing `external_setup` field in a test fixture that constructs a `Preset` object directly
- Type mismatch after schema change (new required field not added to existing code)

Fix direction: edit the TypeScript file at the reported location.

#### Pattern E — Vitest test failure
Symptoms: test file fails, `AssertionError`, `TypeError` in a test

Common causes:
- A test fixture constructs a `Preset` object without the newly added `external_setup` field
- A generated stub has a syntax error

Fix direction: add missing fields to test fixtures, or fix stub syntax.

#### Pattern F — Plugin build crash (not component-not-found)
Symptoms: unhandled exception in `pnpm build-plugin`, not Pattern B

Common causes:
- `plugins/<name>/` directory has stale files from a previous failed build — clean and retry
- YAML parse error in a preset file (tab instead of spaces, bad indentation)

Fix direction: run `pnpm build-plugin <name> --clean`, or fix YAML indentation.

---

## Phase 2 — Fix

### Step 2a — Propose the fix

For each identified error, show the user:
1. Root cause (one sentence)
2. The exact change to make (diff or before/after)
3. Which file will be edited

Ask: **"Apply this fix? (yes / skip / modify)"**

Handle multiple errors in sequence — propose one at a time if they are in different files.

### Step 2b — Apply approved fixes

Apply only changes the user has approved. Use Edit/Write tools — do not use sed or awk.

Keep changes minimal: fix the reported error and nothing else. Do not refactor surrounding code.

---

## Phase 3 — Re-verify

After all approved fixes are applied, re-run the full suite:

```bash
pnpm typecheck
pnpm build-plugin <preset-name>
pnpm test
```

If new errors surface (not present in Phase 1), treat them as a new diagnosis cycle — go back to Phase 1c with the new output.

---

## Phase 4 — Report

### If all checks pass

Report:
- Fixes applied (list files changed + one-line summary per fix)
- Build: ✓
- Tests: ✓
- Ready for install:
  ```
  pnpm install:user <preset-name> --force --symlink
  # or
  pnpm install:project <preset-name> --force --symlink
  ```

### If errors remain after fix attempts

Report:
- What was fixed (if anything)
- What remains broken (exact error, file, line)
- Whether it requires manual intervention (e.g., missing upstream component that must be vendored, env config that must be set up outside this repo)
- Suggested next step (e.g., "vendor the missing component using `/dotclaude-component-picker`")
