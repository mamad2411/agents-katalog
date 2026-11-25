---
name: follow-monorepo-config-workspaces
description: Configure workspaces for bun/npm/pnpm and orchestrator config for moon/turbo
argument-hint: "[tool]"
related:
  - follow-monorepo
  - follow-tool-moonrepo
  - follow-tool-turborepo
  - list-workspaces
  - update-config
  - run-install
---

## Goal

Set up or fix a monorepo's workspace configuration — package manager workspaces (bun/npm/pnpm) and orchestrator config (moon/turbo) — so they stay consistent

## Scope

- Use with an existing monorepo or a new setup — config only, no file moves (moving → `workflows/migrate-to-monorepo/SKILL.md`)
- Covers: `package.json#workspaces`, `pnpm-workspace.yaml`, catalogs, `turbo.json`, `.moon/*`, `moon.yml`

## Execute

### 1. Detect Tool

> Goal: know which package manager and orchestrator are used

1. Read the root `package.json` — `packageManager`, `workspaces` field
2. Check `pnpm-workspace.yaml`, `turbo.json`, `.moon/workspace.yml`, `nx.json`
3. Run `/list-workspaces` to see the currently detected projects

### 2. Config Package Manager Workspaces

> Goal: correct workspace globs and dependency strategy

1. bun/npm: set `workspaces` in the root `package.json` to globs such as `["apps/*", "packages/*"]`
2. pnpm: set `packages:` in `pnpm-workspace.yaml` — use `catalogs:` for shared dependency versions if supported
3. Internal deps use `workspace:*` (pnpm/bun) — npm uses the version matching the local package
4. If unsure about a tool-specific flag/config → check the official docs

### 3. Config Orchestrator

> Goal: the task pipeline matches the workspaces

1. moon: run `/follow-tool-moonrepo` — `.moon/workspace.yml` projects globs, `.moon/tasks/*.yml` shared tasks, `moon.yml` per project
2. turbo: run `/follow-tool-turborepo` — `turbo.json` tasks/pipeline, `dependsOn`, `outputs`, cache config
3. No orchestrator → use the package manager's recursive run (`pnpm -r`, `bun run --filter`) as detected

### 4. Install And Verify

> Goal: install passes and tasks run

1. Run `/run-install` — the lockfile regenerates with no conflicts
2. Run the main task through the orchestrator — `moon run :typecheck` or `turbo run typecheck` — on 1 workspace first, then the whole repo
3. Check the dependency graph is correct — `moon query projects` or `turbo run build --dry-run` as far as the tool supports

## Rules

- Always read the current config first — merge with what exists; never overwrite a whole file unless necessary
- Workspace globs must cover every intended package — verify with the tool's list command
- Don't hardcode duplicated versions across packages when catalogs/overrides are available
- Every config change must install + verify before reporting
- Use `/update-config` for shared config broader than workspace setup

## Expected Outcome

- Workspace config matches the tool used, all projects detected
- Internal deps use the workspace protocol, shared versions go through catalogs
- Install and orchestrator tasks run cleanly
