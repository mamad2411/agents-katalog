---
name: follow-monorepo-migrate-to-monorepo
description: Move a single repo into a monorepo — workspace config, dep hoisting, git history
argument-hint: "[tool]"
related:
  - follow-monorepo
  - check-monorepo
  - plan
  - run-verify
  - resolve-errors
  - ask-me
---

## Goal

Migrate a single-package repo into a monorepo safely — correct workspace config, hoisted dependencies, git history preserved, and rollback possible

## Scope

- Use when splitting one repo into `apps/*`, `packages/*`, or merging several repos together
- Supports bun/npm/pnpm workspaces and task orchestrators (moon, turbo)
- Does not cover configuring workspaces in an existing monorepo — use `workflows/config-workspaces/SKILL.md`

## Execute

### 1. Plan Layout And Tool

> Goal: fix the structure and tool before moving files

1. Run `/plan` — state the target layout (`apps/`, `packages/`, `tools/`) and the package manager + orchestrator to use
2. Pick the tool per the existing ecosystem — bun, pnpm, npm, moon, turbo — check official docs if unsure
3. Map every top-level directory/config to where it goes, or keep it at root

### 2. Preserve Git History

> Goal: don't lose history during the move

1. Always move files with `git mv` — never copy-delete
2. If merging several repos → use `git subtree` or merge with `--allow-unrelated-histories` to keep each repo's history — see official git docs
3. Separate the "move files" commit from the "edit config" commit so rename detection works

### 3. Setup Workspaces

> Goal: the workspace config works and install passes

1. Create the workspace config per the tool — `package.json#workspaces` (bun/npm), `pnpm-workspace.yaml` (pnpm)
2. Move shared devDependencies up to root; child packages use `workspace:*` (pnpm/bun) for internal deps
3. Check dep hoisting — external deps repeated across packages get one version, or use catalogs if the tool supports them
4. Run `install` and confirm the lockfile has no conflicts

### 4. Verify

> Goal: the monorepo works as before

1. Run `/run-verify` — build, typecheck, lint, test pass on every workspace
2. Run `/check-monorepo boundaries` to confirm no cross-import violates boundaries
3. If it fails → `/resolve-errors` for max 3 rounds, then stop and report

## Rules

- `/plan` and user confirm are required before moving — migration is a high-impact change
- One commit per step: move → workspace config → dep dedupe → verify, so bisect works
- Never delete the original repo/config until verify passes — keep a rollback path
- Internal deps use the workspace protocol, not published versions
- CI, scripts, and docs referencing old paths must be updated — run `/update-references`

## Expected Outcome

- The repo is a monorepo where install/build/test all pass
- Git history is preserved, deps are not duplicated
- Commit history is separated per step, making rollback possible
