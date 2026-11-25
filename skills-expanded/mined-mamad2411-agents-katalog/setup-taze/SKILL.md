---
name: follow-tool-taze-setup-taze
description: Install and use taze — major/minor checks, monorepo recursive scan
argument-hint: "[scope]"
related:
  - follow-monorepo
  - run-install
  - run-verify
---

## Goal

Install and use taze to check and update dependencies — `major`/`minor`/`latest` modes, recursive monorepo scan, and package scripts

## Scope

Use for projects/workspaces that need to keep dependencies up-to-date with the taze CLI — run modes, monorepo usage, validation flow

## Execute

### 1. Check And Run

> Goal: Run taze to check dependencies

1. Run `bunx taze` — scans dependencies and shows available updates (no install needed; or `bun add -D taze` to pin it)
2. Use `bunx taze --json` for machine-readable output (agents/CI)
3. See more options in [references/taze.md](../../references/taze.md)

### 2. Update Modes

> Goal: Pick the update mode by risk

1. `bunx taze patch` — patch updates only (safest)
2. `bunx taze minor` — minor + patch
3. `bunx taze major` — includes major bumps (review breaking changes)
4. `bunx taze latest` — update everything to latest

### 3. Write And Install

> Goal: Apply updates to the project

1. Use `-w` to write versions into `package.json`
2. Use `-i` to install dependencies after the bump
3. Use `-I` interactive mode to pick packages one by one
4. Full update example: `bunx taze latest -w -i`

### 4. Monorepo Usage

> Goal: Scan every workspace

1. Use `-r` to recursively scan every workspace package
2. Run `bunx taze major -r` to check the whole monorepo before writing
3. Check compatibility across workspaces — internal packages must have consistent versions
4. For a complex config → create `taze.config.ts` (`exclude`, `include`, `packageMode`, `depFields`, `ignorePaths`, `maturityPeriodExclude`)

### 5. Validate Updates

> Goal: Confirm the updates don't break the project

1. Run install after writing (`bun install`, or `-i` already covers it)
2. Run tests, lint, typecheck — do `/run-verify`
3. Review the `package.json` diff before committing — major bumps require reviewing changelog/breaking changes
4. If something breaks → revert `package.json` + lockfile, then report

## Rules

### 1. Usage

- `bunx taze` for one-off runs; `-r -w -i` for a full monorepo update
- `--json` for agents/CI

### 2. Safety

- Always review the diff before committing — major updates require review
- Run tests after updating; never update in a production branch without review
- One mode at a time — patch/minor before major to isolate breakage

### 3. Monorepo

- Always use `-r` in a monorepo; use `ignoreOtherWorkspaces` in `taze.config.ts` when only one scope is wanted

- Use /follow-monorepo if needed
- Use /run-install if needed

## Expected Outcome

- Dependencies checked and updated with the appropriate mode
- The monorepo scan covers every workspace
- Updates pass tests/lint/typecheck before committing
