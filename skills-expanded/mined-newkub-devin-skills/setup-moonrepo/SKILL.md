---
name: follow-tool-moonrepo-setup-moonrepo
description: Install moon and init the `.moon/` workspace for a first-time monorepo
argument-hint: "[scope]"
related:
  - follow-monorepo
  - follow-tool-mise
  - run-install
  - run-verify
---

## Goal

Install the moon CLI and initialize `.moon/` workspace configuration so the monorepo is ready to use moonrepo — first-time setup

## Scope

For projects that choose moonrepo as the orchestrator (supports Bun, Node, Rust) — it doesn't cover task tuning (see `workflows/config-pipeline/SKILL.md`)

- If `.moon/` already exists → verify only, no re-setup

## Execute

### 1. Check Prerequisites

> Goal: check the current state before setup

1. Check whether `.moon/workspace.yml` or `moon.yml` already exists — if yes → skip to verify
2. Identify the project's stack: `package.json` (JS/Bun), `Cargo.toml` workspace (Rust), or mixed
3. Identify the package manager from the lockfile (`bun.lockb`, `pnpm-lock.yaml`, etc.)

### 2. Install moon

> Goal: install the moon CLI per environment

1. Install with the appropriate package manager:
   - Bun project: `bun add -D @moonrepo/cli`
   - npm/pnpm/yarn project: use the project's package manager
   - PowerShell: `irm https://moonrepo.dev/install/moon.ps1 | iex`
   - macOS/Linux/WSL: `bash <(curl -fsSL https://moonrepo.dev/install/moon.sh)`
   - proto: `proto install moon`
   - mise: `mise use -g moon` (per `global_rules` — prefer mise for global tools)
2. Check the version with `moon --version`

### 3. Initialize Workspace

> Goal: create the `.moon/` configuration

1. Run `moon init` in the repo root to scaffold, or create `.moon/workspace.yml` by hand
2. Define project globs in `.moon/workspace.yml`:
   - JS/Bun: `packages/*`, `apps/*`
   - Rust: `crates/*`
3. Create `.moon/toolchains.yml` per the detected stack (Bun, Node, Rust)
4. Create `.moon/tasks/all.yml` for shared task config
5. Verify every project is detected — use `moon query projects` or check `moon.yml` per project

### 4. Migrate From Turborepo (If Needed)

> Goal: move off turborepo if the project previously used turbo

1. Delete `turbo.json` and remove `turbo` from devDependencies
2. Change root scripts from `turbo run` → `moon run`
3. Update README, AGENTS, and `rules/` that reference turborepo — run `/update-references`

### 5. Verify

> Goal: confirm the workspace works

1. Run `moon run :build` or `moon check` — the project graph must build
2. If verification fails → run `/resolve-errors` max 3 rounds, then stop and report

## Rules

### 1. Idempotent

- If `.moon/` already exists → verify only
- Don't add `turbo` dependencies back into a moon repo

### 2. Toolchain

- Set `.moon/toolchains.yml` per the actually detected stack — don't enable unused toolchains
- Prefer `mise use -g moon` for the global install per `global_rules`

### 3. Layout

- Project globs must cover every workspace without being too broad (JS/Bun = package, Rust = crate)

- Use /follow-monorepo if needed
- Use /follow-tool-mise if needed

## Expected Outcome

- moon CLI installed and `moon --version` works
- `.moon/` config created with correct project globs
- `moon run :build` passes — the project graph builds
