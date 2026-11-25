---
name: apply-projects-in-drive-d
description: Run /apply-this-project across drive-D projects — matched by keyword or every discovered repo
argument-hint: "[action] [keyword|all]"
related:
  - apply-this-project
  - apply
  - search-project-in-drive-d
  - list-projects-git-in-drive-d
  - check-uncommit
  - follow-single-of-source
  - use-subagents
  - follow-parallel
  - run-check
  - ask-me
  - report
  - report-progress
  - commit-all-projects-in-drive-d
  - push-all-projects-in-drive-d
  - suggest-next-action
---

## Goal

Apply the same action to multiple git projects on drive D — the discovered set is either keyword-matched or all projects, depending on what the search finds — by dispatching `/apply-this-project` per project

## Scope

- In: drive-D project discovery, per-project dispatch, aggregated reporting; the action itself comes from the argument/context
- Out: the current project only → `/apply-this-project`; committing/pushing many repos → `/commit-all-projects-in-drive-d` / `/push-all-projects-in-drive-d`; the generic apply modes → `/apply`
- Batch runner only — never edits project files directly; every change goes through `/apply-this-project` inside each repo

## Execute

### 1. Discover Projects

> Goal: the concrete target list — match or all, per what is found

1. Keyword given → run `/search-project-in-drive-d` to get the matching project dirs
2. No keyword (or `all`) → run `/list-projects-git-in-drive-d` for every git project on drive D
3. Zero matches → widen the search or report and stop; never silently apply to an empty or guessed set
4. Record each target as an absolute path with its git status (`/check-uncommit` per repo flags dirty worktrees to protect)

### 2. Confirm The Batch Plan

> Goal: the user agrees before anything is touched

1. `/report table` of No., Project, Matched, Dirty?, Planned action
2. More than a few projects, or any `delete`-mode/destructive action → `/ask-me` to confirm the list and mode first
3. Order targets lowest-risk first; a project with uncommitted work relevant to the action → note it, do not clobber

### 3. Apply Per Project

> Goal: each repo is applied and verified independently

1. Run `/apply-this-project <action>` in each confirmed project — full gates inside every repo (scan → apply → `/run-check`)
2. Repos are disjoint directories → independent: batch them with `/use-subagents` (one `project-updater`-style worker per repo) or `/follow-parallel`; the parent collects every result
3. One project fails its verify gate → fix via that project's `/apply-this-project` retry (max 3), then continue the batch — never abandon the remaining targets
4. Track progress with `/report-progress` on long batches

### 4. Aggregate Report

> Goal: one table covering every project

1. `/report table`: No., Project, Action, Status (done/skipped/failed), Evidence
2. State source + date; list skipped projects with the reason
3. Run `/suggest-next-action` (e.g. per-repo commit via `/commit-all-projects-in-drive-d` when the user wants them committed)

## Rules

### 1. Batch Discipline

- Dispatch only — this skill makes no file edits itself (`/follow-single-of-source`: the workflow lives in `/apply-this-project`)
- Match-or-all is decided by discovery output, not guessed: keyword → matched set; no keyword → all git projects on drive D
- Never mix destructive `delete`-mode across the batch without a per-project dry-run + confirm

### 2. Safety

- Non-git or unreadable directories → skip and record, don't fail the whole batch
- Dirty worktree in a target → back up or stash-check with the user before applying
- No commit/push unless the user asked

## Expected Outcome

- Every discovered project ends applied-and-verified, or explicitly listed as skipped/failed with evidence
- No repo outside the confirmed set was touched
- One aggregate status table + next action
