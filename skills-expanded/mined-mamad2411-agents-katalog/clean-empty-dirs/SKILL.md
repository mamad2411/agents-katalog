---
name: clean-empty-dirs
description: Remove empty directory trees with a dry-run preview and git-aware detection
argument-hint: "[path] [--dry-run]"
related:
  - delete
  - report
  - run-clean
  - run-cleanup
---

## Goal

Find and remove empty directories — including nested empty trees — with a dry run before any real deletion, for a clean repo/filesystem

## Scope

- Scan directory trees for empty dirs (no files at all, counted recursively)
- Git-aware: watch out for dirs git does not track but that are still needed (e.g. `logs/` created by the app itself) — flag them separately from plain empty dirs
- Default: always dry-run — real deletion requires confirmation

## Execute

### 1. Scan For Empty Dirs

> Goal: find every empty dir

1. Scan recursively from the given path — a dir is empty when it contains no files at all (empty subdirs still count)
2. Include nested empty trees — deleting the children leaves the parent empty too
3. Skip hidden/system dirs (`.git`, `node_modules`) unless explicitly specified

### 2. Classify Before Delete

> Goal: separate safe-to-delete empty dirs from ones that may be needed

1. Safe to delete: empty dirs with no purpose marker
2. Suspicious: dirs that code might expect (`logs/`, `tmp/`, `uploads/`, `data/`) — search the code for references to the path
3. Git-ignored: dirs listed in `.gitignore` — they may be intentionally empty (git does not track empty dirs)
4. Keep markers: dirs with `.gitkeep`/`.keep` are meant to be kept — never delete

### 3. Preview

> Goal: show the list before deleting

1. Report via `/report`: `No.`, `Path`, `Depth`, `Classification`, `Action`
2. Summarize counts: safe to delete vs flagged vs kept
3. Ask the user to confirm — dry-run is the default

### 4. Delete (Confirmed Only)

> Goal: delete only what was confirmed

1. Delete deepest first (children before parents) — nested empty trees clear away in one pass
2. Delete only dirs classified `safe` — flagged ones are the user's choice
3. Report how many were actually deleted

## Rules

### 1. Dry-Run Default

- Always show a preview — delete only after the user confirms
- Never delete flagged dirs without an explicit choice

### 2. Purpose Aware

- Dirs referenced by code (log dirs, upload targets) must be flagged — deleting them can break the app
- `.gitkeep`/`.keep` = a deliberate signal — always respect it

### 3. No Partial Deletes

- Delete all-or-nothing per tree — never leave a parent weirdly half-empty from a partial delete
- Windows: beware locked dirs — skip with a note instead of failing the whole batch
- Use /run-clean if needed
- Use /run-cleanup if needed

## Expected Outcome

- A list of empty dirs with their classification
- Only safe, confirmed dirs get deleted
- A cleaner filesystem without destroying the dirs that are needed
