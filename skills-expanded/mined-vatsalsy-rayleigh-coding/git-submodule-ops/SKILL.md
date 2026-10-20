---
name: git-submodule-ops
description: >-
  Use when the user mentions submodules, gitlinks, or `.gitmodules` — add,
  convert, sync, repair, change remote/branch — or `git submodule` commands
  fail with mapping, auth, or lock-file errors. Generic commit/PR work is
  git-master.
---

# Git Submodule Ops

## Overview

Use this skill for submodule-specific work. It is for repos where one path is a gitlink, or where a folder should be converted into a submodule and kept in sync with its upstream. Use `git-master` for generic commit and PR work after the submodule state is settled.

## Workflow

1. Identify the layer:
   - Outer repo that tracks the gitlink.
   - Submodule repo that owns the actual files.
2. Check current state:
   - `git status --short`
   - `git submodule status --recursive`
   - `git diff --submodule=log`
3. If converting an existing folder:
   - Ensure the folder is clean or committed.
   - Add the upstream remote.
   - Use `git submodule add <url> <path>` or convert the path into a gitlink.
   - Commit `.gitmodules` and the gitlink together.
4. If changing the submodule remote or branch:
   - Edit `.gitmodules`.
   - Run `git submodule sync -- <path>`.
   - Run `git submodule update --init --recursive --checkout <path>` unless the workflow explicitly wants a different merge or remote mode.
5. If the submodule itself needs a commit:
   - Work inside the submodule repo first.
   - Commit there.
   - Return to the outer repo and stage the updated submodule pointer.
   - **Bad:** pointer-bump commit message `update submodule`. **Good:** `Bump skills submodule to a1b2c3d for updated trigger descriptions` — name the submodule, the new SHA, and why.
6. For a skills repo mirrored into another repo:
   - Treat the upstream skills repo as the source of truth.
   - Keep the outer repo pinned to a specific submodule commit unless the user explicitly wants a branch-tracking workflow.
   - If branch tracking is desired, set the branch in `.gitmodules` and document that the superproject still records commit SHAs.
7. Verify:
   - `git status --short`
   - `git diff --submodule=log`
   - `git submodule status --recursive`

## Optional resources

- `scripts/` for deterministic helpers
- `references/` for detailed docs loaded as needed
- `assets/` for templates/static files used in outputs

## Gotchas

1. Deleting the worktree directory is not enough. Use `git submodule deinit` or `git submodule sync` plus `git submodule update` so `.git/modules/...` stays consistent.
2. `fatal: no submodule mapping found in .gitmodules` usually means the outer repo and `.gitmodules` disagree. Fix both, then resync.
3. `index.lock` and `HEAD.lock` errors usually mean another git process was left open. Remove the stale lock only after confirming no git command is still running.
4. An outer repo can look dirty even when the submodule worktree is clean; the dirty state may just be the gitlink moving to a new commit.
5. Auth failures against private submodule remotes usually mean the submodule remote is using the wrong protocol or missing access. Prefer the repo's standard SSH URL if available.
