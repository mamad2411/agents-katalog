---
name: delete-project-temp
description: Safely delete a project's .devin/temp/ (reports, plans) with dry-run + confirm
argument-hint: ""
related:
  - delete
  - cleanup
  - cleanup-artifact
  - create-plan-in-dot-devin
  - create-report-in-dot-devin
  - deep-review-codebase
  - ask-me
  - report
  - suggest-next-action

---

## Goal

Safely delete the entire `.devin/temp/` directory in the project — covering `report/` and `plan/` artifacts created by `/create-report-in-dot-devin` and `/create-plan-in-dot-devin` — with dry-run and user confirmation before deletion

## Scope

- single target: `.devin/temp/` at the project root only
- use when you want to clear all temp artifacts (reports, plans) in the project
- does not cover other parts of `.devin/` (`rules/`, `hooks/`, `skills/`, `mcp_config.json`)
- not for deleting a single file or a single subdir — for selective deletion use `/delete`

## Execute

### 1. Locate And Inspect

> Goal: Confirm `.devin/temp/` exists and see what is inside

1. Check that `.devin/temp/` exists at the project root
2. If missing → report that there is nothing to delete and finish
3. List all contents (`report/`, `plan/`, and other files) with file counts
4. Measure the total size via `/deep-review-codebase` scope `size` or `du -sh .devin/temp`

### 2. Dry Run And Confirm

> Goal: Show what will be deleted and ask for confirmation

1. Show the full tree/list of items to be deleted with the total size
2. Warn that plan files in `.devin/temp/plan/` not yet implemented will be permanently lost
3. Do `/ask-me` to confirm — `proceed` or `cancel`
4. If in `/dont-ask-me` mode → skip the confirmation but still show the dry-run
5. If the user cancels → finish without deleting anything

### 3. Delete

> Goal: Delete all of `.devin/temp/`

1. Recursive delete per platform:
   - bash: `rm -rf .devin/temp`
   - PowerShell: `Remove-Item -Recurse -Force .devin/temp`
2. If deletion fails (file locked, permission denied) → report the error and stop
3. If an empty `.devin/temp` or residue remains → delete it all

### 4. Validate And Report

> Goal: Confirm the deletion succeeded and summarize

1. Check that `.devin/temp/` no longer exists
2. Do `/report` summarizing the number of files and size deleted
3. Do `/suggest-next-action`

## Rules

### 1. Safety

- Always dry-run + confirm before deleting — never delete without showing the list first
- Scope is `.devin/temp/` only — never expand to `.devin/` or other project files
- Never delete `.git`, config, secrets, or files outside `.devin/temp/`
- If `.devin/temp/` is a symlink/junction → remove the link only, never follow it into the target

### 2. No Backup Needed

- temp artifacts are disposable by design — no backup needed
- if a plan/report is still needed, the user must cancel at the confirmation or move it out first

## Expected Outcome

- `.devin/temp/` is fully deleted, or nothing changed if the user cancels
- A report of the count and size of deleted items
- No residue or partial delete left behind
