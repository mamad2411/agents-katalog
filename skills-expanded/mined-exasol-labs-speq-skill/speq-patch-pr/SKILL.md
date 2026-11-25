---
name: speq-patch-pr
description: "Ships a bug fix, small feature, or tweak as one ready PR: runs /speq-patch on the patch/patch-name branch, bumps the version, commits, and opens a ready pull request. Run again to resume. Arg: change intent text."
---

# Patch, PR flow (Orchestrator)

## User Arguments

$ARGUMENTS

This skill runs `/speq-patch` on its own branch and ships the result as a ready PR. `/speq-patch` writes the code, tests, specs, and docs. You run every git/`gh` action yourself, per `/speq-git-operations`. Stop on the first failed step and report it. Running it again resumes the work.

## Required Skills

Invoke before starting:
- `/speq-writing-guardrails`: prose style for GitHub text
- `/speq-git-operations`: git/`gh` writes, PR title, version bump

`/speq-patch` invokes its own required skills.

## Workflow

### 1. Check Prerequisites and Name

1. The GitHub CLI is not authenticated, or the repository has no `origin` remote → stop before any edit and name the missing piece.
2. Run `/speq-patch` steps 1 to 3: prerequisites, discovery, the patch name, and the first size check.
3. Derive the PR title from `<patch-name>` per `/speq-git-operations` § PR title and version bump.

### 2. Branch

Run `checkout` with `patch/<patch-name>`.
- **Found:** the latest commit `HEAD` is not on `origin/<default-branch>`, has the PR title as subject, and `git status --porcelain` lists nothing outside the patch folder, new files included → go to step 5. Otherwise go to step 3.
- **Not found:** run `create-branch` with `patch/<patch-name>` and `base: origin/<default-branch>`. Uncommitted changes the user assigned to the patch carry over.

### 3. Patch

Run `/speq-patch` steps 4 to 8, but keep the patch folder: step 8 deletes it. Keep the report for the PR body. Skip its closing line.

### 4. Bump Version

Bump the version file and sync the lockfile per `/speq-implement-pr` step 3, at the level `/speq-git-operations` § PR title and version bump gives.

### 5. Ship

1. Run the suites and the lint command once more per `/speq-patch` step 4, so the PR reports the tree it ships. Red → stop and report as in `/speq-patch` step 4.
2. A run that resumed here reads the ADR and architecture lines from the commit's diff, and the affected plans from `speq plan list`.
3. Ship:

```
Run operation: ship-ready (per /speq-git-operations)
  paths: every file /speq-patch changed, the version file, and the lockfile; never the patch folder
  message: <the PR title>
  title: <the PR title>
  body: per references/pr-body-template.md
```

4. Delete the patch folder `specs/_plans/<patch-name>/`.

Never merge the PR.

### 6. Report

Give the PR link, the new version, and the `/speq-patch` report.
