---
name: edit-relative
description: Edit a file and update all related references, both relative paths and semantic relations
argument-hint: "[@files...]"
related:
  - update-references
  - resolve-errors
  - refactor
  - review-devin-global-harness
  - scan-codebase
  - report
---

## Goal

Edit the specified file and update the relative paths, imports, links, and semantic references in related files so they stay consistent

## Scope

Use when editing one file affects other files that reference it, e.g.:
- Renaming a function/class/variable requires updating call sites
- Moving or renaming a file requires updating imports
- Updating a skill requires updating `related`, body references, `AGENTS.md`, `global_rules.md`
- Changing a barrel/export requires updating consumers

## Execute

### 1. Identify Targets And Changes

> Goal: know the target files and what will change

1. Take `@files...` from the argument
2. Read the target files
3. Record a baseline: names, paths, imports, exports, public API
4. Identify the changes to make

### 2. Apply Edits

> Goal: edit the target files

1. Apply edits per the user request or `/refactor`
2. Preserve the public API unless a change is required
3. Do a dry run if there are destructive changes

### 3. Find Related Files

> Goal: find files that reference the target files

1. Run `/scan-codebase` to find imports, references, call sites
2. Find relative path references
3. Find semantic references: function names, class names, skill names, `related` lists
4. Collect the files that need updating into a list

### 4. Update Relative References

> Goal: update paths to be correct

1. Run `/update-references` for relative paths
2. If a file moved → update imports for the new directory
3. If a file was renamed → update its name in every reference
4. If there are markdown links → update the paths

### 5. Update Semantic References

> Goal: update renamed symbols

1. If a function/class/variable was renamed → update call sites
2. If a skill was renamed → update `related`, body, `AGENTS.md`, `global_rules.md`
3. If an API signature changed → update the consumers that call it
4. Use `/scan-codebase` + grep to find every occurrence

### 6. Validate

> Goal: no broken references

1. Run `/review-devin-global-harness`
2. Run `/resolve-errors` if there are build/lint/typecheck errors
3. If it fails → fix and recheck (max 3 rounds)

### 7. Report

> Goal: summarize results

1. Run `/report` summarizing the edited files, files with updated references, and validation results
2. Run `/suggest-next-action`

## Rules

1. Edit only the necessary files + affected related files
2. Never break the public API without stating it
3. Every rename/move must update references immediately
4. Use a dry run before destructive actions
5. If unsure about impact → run `/ask-me`

## Expected Outcome

- Target files are edited
- Related files have all references updated
- No broken references
- Lint/typecheck/test/build pass, if present
- The change report is complete
