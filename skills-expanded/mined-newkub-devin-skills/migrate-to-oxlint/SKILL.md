---
name: follow-tool-eslint-migrate-to-oxlint
description: Migrate ESLint → oxlint — coverage check, side-by-side, switch, rollback
argument-hint: "[project-path]"
related:
  - follow-tool-eslint
  - run-lint
  - deep-review-codebase
  - report-before-after
---

## Goal

Move linting from ESLint to oxlint safely — check rule coverage first, run side by side during transition, switch when ready, keep a rollback

## Scope

- Use in projects with an ESLint setup that want to cut lint time with oxlint
- Covers coverage assessment, `.oxlintrc.json`, side-by-side run, CI switch, rollback
- oxlint does not cover every ESLint rule/plugin — the migration may end as "oxlint primary + ESLint for the remaining rules"

## Execute

### 1. Assess Coverage

> Goal: know which rules oxlint covers

1. List the ESLint rules/plugins enabled in `eslint.config.*` — use `eslint --print-config` for the effective rules
2. Check oxlint rule coverage in the official docs — oxlint supports rules from eslint, typescript, react, unicorn, import, etc. but not all
3. Split rules into covered / not covered / partial — write a mapping table
4. If a critical rule is not covered → plan a hybrid or delay the migration

### 2. Install And Configure oxlint

> Goal: oxlint runs in parallel with ESLint

1. `bun add -D oxlint` or the package manager the project uses
2. Create `.oxlintrc.json` — map plugins/categories/rules from the ESLint config (see official docs for config fields and migration aids)
3. Use `eslint-plugin-oxlint` in the ESLint config to disable rules oxlint already covers — prevents double-reporting during transition (see oxlint's official docs or `/follow-create-oxlint-plugin`)

### 3. Run Side-By-Side

> Goal: compare diagnostics before switching

1. Run `bunx oxlint` + `bunx eslint .` → compare findings
2. Findings oxlint misses but ESLint catches = coverage gaps — decide per rule
3. Measure lint time for both — keep the numbers for the report
4. During transition: CI runs both — oxlint as the fast gate, ESLint only for still-needed rules

### 4. Switch

> Goal: oxlint becomes the primary linter

1. Update package scripts: `"lint": "oxlint"` (and `lint:eslint` if keeping a hybrid)
2. Update CI: run oxlint as a required check — if hybrid, keep ESLint as a separate job
3. Set up editor integration per official docs (oxlint extension/LSP)
4. Coverage sufficient → remove ESLint deps/config in a separate commit; hybrid → document which rules ESLint still owns

### 5. Verify And Rollback Path

> Goal: the lint gate is at least as strong as before

1. Run lint over the whole codebase → no regression in the findings meant to be covered
2. Test `--fix` behavior if auto-fix is used
3. Rollback path = restore scripts/CI to ESLint (the old config stays in git history) — verify it works
4. Report via `/report-before-after`: lint time, rule coverage, decisions

## Rules

### 1. Coverage First

- never switch before checking coverage — oxlint is not a 100% drop-in replacement
- rules oxlint does not cover need an explicit plan: ESLint hybrid or acceptance

### 2. Transition

- always run side by side before switching — `eslint-plugin-oxlint` disables the duplicates
- separate commits: add oxlint → switch scripts/CI → remove ESLint
- if oxlint findings differ a lot from ESLint → stop and review before switching

## Expected Outcome

- oxlint runs as the primary linter — lint time drops significantly
- coverage mapping is clear — rules still on ESLint (if any) are documented
- rollback path verified
