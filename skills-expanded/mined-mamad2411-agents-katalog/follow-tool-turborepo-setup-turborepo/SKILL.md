---
name: follow-tool-turborepo-setup-turborepo
description: Install Turborepo and arrange the workspace structure for a monorepo for the first time
argument-hint: "[scope]"
related:
  - follow-monorepo
  - run-install
  - run-verify
---

## Goal

Install the `turbo` CLI and arrange the monorepo workspace structure to be ready for Turborepo — first-time setup, not ongoing maintenance

## Scope

Use for a project that wants to start using Turborepo fresh — install, root `package.json`, directory layout, smoke check

- If `turbo.json` already exists → verify only, no re-setup needed
- Pipeline/tasks details → see `workflows/config-pipeline/SKILL.md`

## Execute

### 1. Check Prerequisites

> Goal: Check the current state before setup

1. Check the root `package.json` — it must have `private: true`, `packageManager`, and `workspaces`
2. Check whether a `turbo.json` or the `turbo` dependency already exists — if so → skip to verify
3. Identify the package manager the project uses (`bun`, `pnpm`, `npm`, `yarn`) from the lockfile

### 2. Install Turbo

> Goal: Install the turbo CLI

1. Install with `bun add -D turbo` (or the project's package manager)
2. Verify the version with `bunx turbo --version`
3. Add root scripts such as `"build": "turbo run build"`, `"dev": "turbo run dev"`

### 3. Arrange Workspace Layout

> Goal: Organize the directory structure per Turborepo conventions

1. Arrange directories with `apps/*` for applications and `packages/*` for shared libraries
2. Avoid nested packages that complicate the workspace globs
3. Verify each package has a `package.json` with a unique `name` and `exports` if it is a library
4. Configure `workspaces` in the root `package.json` to cover `apps/*` and `packages/*`

### 4. Create Minimal turbo.json

> Goal: Create a minimal working `turbo.json`

1. Create `turbo.json` at the root with `$schema`
2. Define basic `tasks` for `build`, `dev`, `lint`, `test` — the full details continue in `workflows/config-pipeline/SKILL.md`

### 5. Verify

> Goal: Confirm the setup works

1. Run `bunx turbo run build` or a basic task — it must pass and create the cache in `.turbo/`
2. Run `bunx turbo run build` again — you must see a cache hit (`FULL TURBO` or cache replay)
3. If verification fails → do `/resolve-errors` max 3 rounds, then stop and report

## Rules

### 1. Idempotent

- If the setup already exists (`turbo.json` + the turbo dependency) → verify only, never reinstall
- Don't change the project's package manager just to install turbo

### 2. Layout

- Use `apps/*` + `packages/*` as the standard layout
- Every package must have a `package.json` with a unique `name`

### 3. Verification

- The cache must be seen working (a repeat run is faster) before the setup counts as successful
- Report the result with `/report-before-after`

- Use /follow-monorepo if needed
- Use /run-install if needed
- Use /run-verify if needed

## Expected Outcome

- `turbo` is installed and `turbo.json` is created at the root
- The workspace layout `apps/*` + `packages/*` is ready to use
- `turbo run <task>` runs and caches properly
