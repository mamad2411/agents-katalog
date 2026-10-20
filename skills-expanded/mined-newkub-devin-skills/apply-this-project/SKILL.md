---
name: apply-this-project
description: Apply an action (choose/validate/delete from /apply) to the current project with verification gates
argument-hint: "[action-or-mode]"
related:
  - apply
  - apply-projects-in-drive-d
  - scan-codebase
  - check-should-update
  - dont-over-engineer
  - all-workspace
  - all-this-patterns
  - ask-me
  - run-check
  - deep-validate
  - resolve-errors
  - update-references
  - report
  - suggest-next-action
---

## Goal

Apply a decided action to the current project end to end — mode from `/apply` (`choose`/`validate`/`delete`), scoped to this workspace, verified before done

## Scope

- In: the current project/workspace only — its files, config, docs the action touches
- Out: another single project or several drive-D repos → `/apply-projects-in-drive-d`; a bare pick-from-N-options or generic apply with no project target → `/apply` directly
- The project's `AGENTS.md` / `README.md` conventions win over generic steps here

## Execute

### 1. Capture Action And Mode

> Goal: know exactly what to apply and under which mode

1. Take the action from the argument/context; unclear → run `/ask-me` to pin target + expected outcome
2. Detect the mode from `/apply`: several options → `choose`; needs confirmation before applying → `validate`; removing files/folders → `delete` (dry-run + confirm gates stay mandatory there)

### 2. Scope Targets In The Project

> Goal: concrete file list inside this project, nothing else

1. Run `/scan-codebase` to find the affected files/patterns; check `git status` — record any in-progress work, do not clobber it
2. Run `/check-should-update` per candidate target — skip targets that don't actually need the action
3. Plan the minimal change set with `/dont-over-engineer`; the action reaching several places → `/all-this-patterns` inside this project

### 3. Apply

> Goal: execute the action on this project only

1. Apply target by target, one responsibility per change; mix no refactor with behavior changes in one pass
2. `delete`-mode targets → follow `/apply` `## Mode: Delete` fully (identify → impact → dry run → backup → delete) before any reference updates
3. After editing, run `/update-references` when files moved/renamed/deleted

### 4. Verify And Report

> Goal: the project is left green

1. Run `/run-check` (lint/typecheck/scan) for the detected ecosystem; skill/config-level changes → `/deep-validate`
2. Failure → fix with `/resolve-errors` (max 3 rounds → stop and report); then re-verify
3. `/report` the result table (No., Target, Action, Status, Evidence) → run `/suggest-next-action`

## Rules

### 1. Scope Discipline

- Touch only this project's files — never reach outside the workspace root
- Follow the project's own `AGENTS.md` for commands, architecture, and gates
- No commit/push unless the user asked — this skill ends at verified state

### 2. Safety

- Destructive sub-actions always go through dry-run + user confirmation first
- Uncommitted work in the target area → back it up before overwriting and state the backup path

## Expected Outcome

- The action is applied across the current project with every touched target verified
- Checks pass with no regressions; deleted/moved targets leave zero broken references
- One report table with per-target status and the next action
