---
name: cleanup-files-in-project
description: Clean up unnecessary source files in the project, not build artifacts or dependency caches
argument-hint: "[target]"
related:
  - report
  - report-file-structure
  - check-reference
  - run-clean
  - run-cleanup
---

## Goal

Delete unnecessary source files in the project — unused, duplicated, or dead-code files — without touching build artifacts or dependency caches

## Scope

Applies to source files in the project workspace — excludes `node_modules`, `dist`, `target`, `.next`, `.nuxt`, `.output`, `coverage`, logs, caches, and generated build files

## Execute

### 1. Identify Candidates

> Goal: Find unnecessary source files

1. Run `/follow-tool-knip` to find unused files
2. Run `/follow-tool-knip` to find unneeded dependencies
3. Find duplicate files with `glob` and `exec` (hash comparison)
4. Find empty files, orphan test fixtures, abandoned stubs

### 2. Analyze Impact

> Goal: Assess impact before deleting

1. Use `grep` to find each file's imports or references
2. Check whether the file is in `.gitignore`
3. Identify real source files (`.ts`, `.js`, `.rs`, `.py`, `.go`, `.vue`, `.svelte`, etc.)
4. Exclude build artifacts, lock files, config files, `.env`, `AGENTS.md`, `README.md`

### 3. Confirm With User

> Goal: Get explicit confirmation before deleting

1. Produce a `/report` of candidates with reasons and paths
2. Run `/report-file-structure` to show the top-level files to be deleted
3. Ask the user with `ask_user_question` whether to delete

### 4. Remove Source Files

> Goal: Delete only approved files

1. Delete files one at a time with `Remove-Item` or `rm`
2. Update the imports/references that used each file with `edit`
3. Update `README`, `AGENTS.md` if needed

### 5. Validate

> Goal: Check after deleting

1. Run `git status` to review the deleted files
2. Run `/check-reference` to catch broken references
3. Run the project tests or build if available

## Rules

### 1. Source Only

- Delete only source files such as `.ts`, `.js`, `.tsx`, `.jsx`, `.vue`, `.svelte`, `.rs`, `.py`, `.go`
- Never delete build artifacts (`dist`, `target`, `.output`), dependency caches (`node_modules`, `.bun/install/cache`), logs, coverage
- Never delete lock files, config files, `.env`, `AGENTS.md`, `README.md`

### 2. Explicit Confirmation

- Never delete automatically
- Require user approval before deleting
- If unsure, ask first

### 3. Safe Impact

- Check references with `grep` before deleting
- Update all imports/exports after deleting
- Verify `git status` before and after

### 4. Ecosystem Aware

- Follow the language/framework conventions
- Update barrel exports if present
- Use /run-clean if needed
- Use /run-cleanup if needed

## Expected Outcome

- Unnecessary source files removed
- No build artifacts or dependency caches touched
- Imports/exports updated correctly
- Before/after report table and file structure
