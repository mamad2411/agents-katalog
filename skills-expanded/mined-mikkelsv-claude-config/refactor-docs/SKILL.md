---
name: refactor-docs
description: Review and update project documentation to match code changes
disable-model-invocation: true
---

# Documentation Sync

Check if docs match current code. Update what's stale.

## Step 1: Scope

If orchestrator provided scope, skip to Step 2.

**Mode A** (no args): run `pwsh -NoProfile -File ".claude/scripts/git-diff-scope.ps1"` if that file exists, else `pwsh -NoProfile -File "$HOME/.claude/scripts/git-diff-scope.ps1"`. Abort if `MODE: none`.
**Mode B** (path/area): Glob relevant files, cross-reference with docs.
**Mode C** (`all`): read all docs, cross-reference full codebase.

## Step 2: Read Relevant Docs

Scope the reading to the mode — a full sweep on every invocation is wasted context when the diff only touches one area.

- **Scoped modes (A or B, diff-based)**: read only the docs relevant to the changed areas.
- **Full-review mode (C)**: read in full `CLAUDE.md`, all `docs/` files, all `.claude/rules/` files.

## Step 3: Cross-Reference

For each changed file, check if changes affect documented info: solution structure, module descriptions, build commands, API surfaces, type definitions, conventions. Look for: new files/modules not in CLAUDE.md, renamed types/functions docs reference, new undocumented APIs, changed behavior contradicting docs, removed features still documented.

## Step 4: Apply

Update only what's stale. Match existing style. Keep concise.

Create a `docs/<area>.md` when content in `CLAUDE.md` fails the where-vs-how test in `arch-claude-md-is-an-index` — move the how-it-works prose across, leave a one-line index entry behind. One area per file.

**Not a restructure pass.** First-time `docs/` splits and whole-tree reorganization are a deliberate manual operation. `/audit-branch` spawns this skill diff-scoped on every branch audit, so a whole-tree restructure must never be reachable from here — note the need in the report and stop.

## Step 5: Report

Files updated and why. Gaps needing attention. Borderline items left alone.
