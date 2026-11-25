---
name: git-worktree-playbook
description: >-
  Use when the user mentions worktrees, /worktree, worktree-merge, .worktrees,
  or OpenCode/comphy-code worktree tooling, or asks to create, clean up,
  reset, or troubleshoot a git worktree.
---

# Worktree Playbook

Use this skill to compare and guide worktree usage in three layers:
1) Git worktrees (core git feature)
2) OpenCode native worktree service (internal runtime)
3) comphy-code worktree tool + slash commands (plugin layer)

## Quick intake

- Determine which layer the user cares about (git vs OpenCode native vs comphy tool).
- Confirm desired mode: new branch, existing branch, or detached.
- Confirm desired location (repo-local `.worktrees` vs OpenCode data path).
- Confirm whether auto-cleanup or manual cleanup is preferred.

## Canonical facts

### Git worktree basics

- `git worktree add` creates a linked working tree for a branch or detached HEAD.
- A branch can be checked out in only one worktree at a time.
- Removing a worktree does not automatically delete a branch unless explicitly done.
- Stale entries can be cleaned via `git worktree prune`.

Core commands:

```sh
git worktree list --porcelain
git worktree add -b <branch> <path> <base>
git worktree add <path> <branch>
git worktree add --detach <path> <base>
git worktree remove <path>
git worktree prune
git branch -d <branch>
```

### OpenCode native worktrees (internal runtime)

- Lives under OpenCode data dir: `Global.Path.data/worktree/<projectId>`.
- Name is auto-generated (adjective-noun). Optional input is slugged; branch is `opencode/<name>`.
- Uses `git worktree add --no-checkout` then `git reset --hard` to populate the new worktree.
- Bootstraps a project instance and may run project start commands and optional extra start command.
- Emits readiness and failure events on the global bus.
- Remove flow uses `git worktree remove --force` and deletes the worktree branch.
- Reset flow finds default branch (remote HEAD or main/master), fetches if needed, hard-resets,
  cleans, updates and resets submodules, then asserts a clean status. It cannot reset the primary worktree.

### comphy-code worktree tool

- Creates repo-local worktrees in `.worktrees/<name>`.
- Requires explicit `name` and `mode` (`new`, `existing`, `detach`).
- Validates name and branch characters for safety; base ref defaults to `HEAD`.
- Uses `git worktree add` with mode-specific args.
- Optional auto-cleanup via session tracking (unless `keep=true` or no session ID).
- No bootstrap, reset, or branch deletion is performed by the tool.

### comphy-code slash commands

- `/worktree` generates worktree and branch names from a prompt if flags are not provided,
  then calls the worktree tool.
- `/worktree-merge` guides merging a worktree back and cleaning up interactively.
- Built-ins are declared in `src/features/commands/loader.ts`.

## Guidance patterns

- Prefer comphy `/worktree` for quick repo-local isolation with auto-cleanup.
- Prefer OpenCode native worktrees when the runtime needs bootstrapping/start commands
  and centralized storage outside the repo.
- For git-only usage, provide a minimal command sequence and safety checks.

## Troubleshooting cues

- "Worktree already exists" or path errors: pick a new path or remove/prune.
- "Branch is already checked out": choose another branch or remove the other worktree.
- "Detached" surprises: use `--detach` explicitly or create a branch at the HEAD.
- Dirty worktree on merge: commit or stash before merge-back.


## Gotchas

1. **A branch can only be checked out in one worktree at a time** -- attempting `git worktree add` for a branch already checked out elsewhere fails with 'already checked out'. Solution: either remove the existing worktree first, or use `--detach` and checkout the branch manually.
2. **Stale worktree entries survive `rm -rf`** -- removing the worktree directory without running `git worktree remove <path>` or `git worktree prune` leaves a stale entry that blocks future adds to the same path.
3. **OpenCode native worktrees live outside the repo** -- they are stored under the OpenCode data dir, not `.worktrees/`. Cleaning `.worktrees/` manually will NOT remove OpenCode-managed worktrees; use the OpenCode remove flow instead.
4. **Dirty worktree blocks merge-back** -- always commit or stash before attempting `/worktree-merge`; uncommitted changes in the worktree will cause the merge to fail or silently drop changes.

## Expected assistant behavior

- Ask which layer the user intends to use if unclear.
- When comparing systems, separate by layer and mention storage path, branch naming,
  bootstrap behavior, and cleanup/reset capabilities.
- If asked to run commands, suggest the safest order and call out branch deletions explicitly.
