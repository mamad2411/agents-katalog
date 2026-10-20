---
name: follow-monorepo
description: Check and follow monorepo conventions, workspace scripts, dependencies, and build pipelines
argument-hint: "[workspace-or-command]"
related:
  - ship
  - run-build
  - run-verify
  - follow-tool-vite
  - follow-tool-moonrepo
  - follow-tool-mise
  - follow-tool-mr-boxington
  - follow-tool-linter
  - follow-tool-formatter
  - follow-tool-gitleaks
  - update-license-md
  - update-contributing
  - update-astgrep-rules
  - update-gitignore
  - update-dot-vscode
  - update-dot-devin
  - improve
  - setup-cicd
  - deep-review-codebase
  - report
  - suggest-next-action
  - run-test
---

## Goal

Check and follow monorepo conventions, workspace scripts, dependencies, and build pipelines

## Scope

Use with monorepos that use `moon`, `turbo`, `pnpm workspace`, `bun workspace`, or `nx` — detect the tool, verify workspace conventions, run commands, and manage dependencies

## Execute

### 1. Detect Monorepo Tool

> Goal: know which monorepo tool is used

1. Check the root `package.json` for `workspaces`, `packageManager`
2. Check `moon.yml`, `turbo.json`, `nx.json`, `pnpm-workspace.yaml`
3. Check `moon --version`, `turbo --version`, `pnpm --version`, `bun --version`
4. Record the tool used

### 2. List Workspaces

> Goal: know what workspaces exist

1. If `moon` → run `moon query projects`
2. If `turbo` → read the `package.json` workspaces
3. If `pnpm` → run `pnpm -r list`
4. If `bun` → read the `package.json` workspaces
5. Build a list: name, path, type (app/package/integration/tool)

### 3. Verify Workspace Conventions

> Goal: check that each workspace follows conventions

1. Check `package.json` has `name`, `type: module`, `scripts`
2. Check `moon.yml` if moon is used
3. Check whether `tsconfig.json`, `biome.jsonc` exist
4. Check for `README.md` or `AGENTS.md` in the workspace
5. Check `.vscode/` and `.devin/` in each workspace (settings, hooks, skills, MCP)
6. Record workspaces missing conventions
7. Sync convention layers when missing or drifted:
   - `/follow-tool-moonrepo` (default orchestrator) or `/follow-tool-mr-boxington` per the tool used
   - `/follow-tool-mise` for toolchain/runtime versions
   - `/follow-tool-linter` + `/follow-tool-formatter` for lint/format wiring
   - `/follow-tool-gitleaks` for the secrets scanning hook (e.g. pre-push)
   - `/setup-cicd` if there is no pipeline yet or the config drifted
   - `/update-license-md`, `/update-contributing`, `/update-astgrep-rules`, `/update-gitignore` for repo hygiene files
   - `/update-dot-vscode`, `/update-dot-devin` for the workspace's `.vscode`/`.devin` config
   - `/improve config` when the config works but can still be improved

### 4. Run Workspace Command

> Goal: run a command across workspaces

1. Use the suitable tool command:
   - moon: `moon run :<task> --concurrency 1`
   - turbo: `turbo run <task>`
   - pnpm: `pnpm -r <command>`
   - bun: `bun run --filter <workspace> <script>`
2. Record results and errors
3. If it fails → run `/resolve-errors`

### 5. Check Dependencies

> Goal: check dependencies across workspaces

1. Check `package.json` dependencies in each workspace
2. Check whether external dependencies are duplicated
3. Check internal workspace dependencies (`workspace:*`)
4. If there are duplicates or version mismatches → run `/update-version-to-latest`

### 6. Verify Build Pipeline

> Goal: confirm the build pipeline works

1. Run `bun install` or the package manager install
2. Run `moon run :build` or `turbo run build`
3. Run `moon run :typecheck` or `turbo run typecheck`
4. Run `moon run :lint` or `turbo run lint`
5. If it fails → run `/resolve-errors`

### 7. Report

> Goal: summarize the status of every workspace including `.vscode`/`.devin`

1. Run `/report table` with columns: `No.`, `Workspace`, `Type`, `Conventions`, `.vscode`, `.devin`, `Deps`, `Status`
2. A workspace missing `.vscode` → run `/update-dot-vscode`; missing `.devin` → run `/update-dot-devin`
3. Run `/suggest-next-action`

### Workflows

> Goal: dispatch specialized work to a more detailed workflow

| Topic | Workflow |
|-------|----------|
| Move a single repo → monorepo — workspace config, dep hoisting, git history | `workflows/migrate-to-monorepo/SKILL.md` |
| Configure workspaces for bun/npm/pnpm + moon/turbo | `workflows/config-workspaces/SKILL.md` |

## Rules

### 1. Tool Agnostic

- Support moon, turbo, pnpm, bun, nx
- Use the command the tool recommends
- Don't assume every project uses the same tool

### 2. Workspace Conventions

- Every workspace must have a `package.json` with `name`
- Every workspace should have a `README.md`
- Every app should have an `AGENTS.md` if there are global rules

### 3. Consistent Dependencies

- Use `workspace:*` for internal packages
- Avoid duplicate external versions
- Update `bun.lock` or `pnpm-lock.yaml` when dependencies change

### 4. Parallel Safety

- Run commands with suitable concurrency
- Never run a destructive command on every workspace at once
- Use dry-run if a command has side effects

### 5. Minimal Impact

- Don't change the tool unless necessary
- Don't refactor all workspaces in one pass
- Fix only the workspaces with problems

- Use /ship if needed
- Use /run-build if needed
- Use /run-verify if needed
- Use /follow-tool-vite if needed
- Use /deep-review-codebase if needed
- Use /report if needed
- Use /suggest-next-action if needed
- Use /run-test all if needed
- Use /update-dot-vscode if needed
- Use /update-dot-devin if needed

## Expected Outcome

- Monorepo tool is detected
- Workspaces listed and conventions verified
- Dependencies consistent
- Build/typecheck/lint pass
- Report table summarizes every workspace including `.vscode`/`.devin` (`/update-dot-vscode`, `/update-dot-devin`)
