---
name: git-merge-expert-worktree
version: 2.0.0
description: |
  Run merges and conflict resolution inside a dedicated git worktree so the MAIN tree is never
  touched — isolation is the whole point. Lists existing worktrees and current context first,
  creates or reuses the right isolated workspace, tags a backup and performs the merge/rebase/
  cherry-pick there, validates the result, then closes the lifecycle with `git worktree remove` +
  `prune` and verifies the main tree stayed clean. Uses `git worktree remove` (never `rm -rf`) for
  normal cleanup, never auto-deletes non-ephemeral branches, and requires explicit confirmation
  before force-removing a dirty worktree. Use only when the user explicitly wants merge work done in
  an isolated worktree.
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
disable-model-invocation: true
user-invocable: true
argument-hint: "[merge target, source branch, or worktree task]"
arguments:
  - request
when_to_use: |
  Use only when the user explicitly asks for worktree-based merge operations — "merge this in a
  worktree", "create an isolated merge workspace", "resolve conflicts in a worktree", "clean up
  stale worktrees". Do NOT use for a standard in-place merge (git-merge-expert), read-only git
  inspection, or normal non-worktree editing; explicit-user-only, confirm before force cleanup.
---

<EXTREMELY-IMPORTANT>
This skill mutates git state and must stay disciplined.

Non-negotiable rules:
1. Start by listing existing worktrees and identifying the current worktree context.
2. Keep merge operations isolated from the main working tree whenever a worktree is being used.
3. Use `git worktree remove`, not `rm -rf`, for normal cleanup.
4. Never delete non-ephemeral branches automatically.
5. Get explicit user confirmation before force-removing dirty worktrees or performing ambiguous branch cleanup.
</EXTREMELY-IMPORTANT>

# Git Merge Expert — Worktree Specialist

## Inputs

- `$request`: Merge target, source branch, worktree name, cleanup task, or conflict-resolution goal

## Goal

Perform safe worktree-based git operations by:

- discovering existing worktrees and current context
- creating or selecting the right isolated workspace
- doing merge/conflict work in the worktree
- validating the result before integration
- cleaning up worktrees and ephemeral branches correctly

## Step 0: Resolve the requested operation

Determine whether the user wants to:

- create a worktree
- perform a merge in a worktree
- resolve merge conflicts in a worktree
- validate an existing worktree merge
- clean up stale or finished worktrees

If the requested source/target branches or cleanup scope are ambiguous, use `AskUserQuestion`
before mutating git state.

**Success criteria**: The intended worktree action, branch scope, and cleanup expectations are explicit.

## Step 1: Discover current worktree state

Before creating or removing anything, inspect:

- `git worktree list`
- current repository root
- current branch and working tree state
- whether the target branch is already checked out in another worktree

Load `references/worktree-conventions.md` for path, naming, and lifecycle rules.

Rules:

- always list worktrees first
- verify whether you are already inside a linked worktree or the main tree
- do not attempt to check out the same branch in two worktrees

**Success criteria**: Existing worktrees, branch occupancy, and current context are known.

## Step 2: Create or prepare the isolated worktree

Create or reuse the right worktree for the task.

Typical decisions:

- managed worktree path vs sibling-path worktree
- ephemeral session branch vs existing branch
- setup needs such as dependency install, symlinks, or env-file propagation

Load `references/worktree-conventions.md` for path and branch conventions.

Rules:

- prefer isolated worktrees over doing merge work in the main tree
- verify creation with `git worktree list`
- only run setup steps that make sense for the detected project

**Success criteria**: The worktree exists, is on the intended branch, and is ready for merge work.

## Step 3: Perform the merge or conflict operation in the worktree

Inside the worktree:

- create a backup tag when appropriate
- run the merge, rebase, cherry-pick, or cleanup operation requested
- resolve conflicts carefully without silently dropping either side

Load `references/merge-playbook.md` for:

- conflict tiers
- lockfile handling
- abort-and-recreate recovery
- stale-worktree cleanup patterns

Rules:

- do not merge in the main tree if the user asked for worktree isolation
- regenerate conflicted lockfiles rather than hand-editing them
- abort and recreate the worktree when recovery is cleaner than patching a broken merge state

**Success criteria**: The git operation is complete in the worktree and the result is coherent.

## Step 4: Validate before final integration

Validate the worktree result with the narrowest relevant checks:

- `git status`
- conflict-free state
- project build/test/typecheck commands when appropriate
- branch topology review when needed

Rules:

- do not claim merge success if unresolved conflicts or failing validation remain
- keep validation scoped to the project/tooling reality
- if validation fails, stop or recover before cleanup/push

**Success criteria**: The worktree result is clean enough to integrate or push.

## Step 5: Cleanup and verify the main tree remains untouched

When the operation is complete:

- return to the main repository context if needed
- remove the worktree with `git worktree remove`
- delete only ephemeral session branches when appropriate
- run `git worktree prune`
- verify the remaining worktree list and main-tree state

Load `references/merge-playbook.md` for cleanup and recovery rules.

Rules:

- never auto-delete non-session branches
- warn before force-removing a dirty worktree
- explicitly verify the main working tree was not unintentionally modified

**Success criteria**: The worktree lifecycle is closed cleanly and the user can see the final git state.

## Guardrails

- Do not let the model invoke this skill proactively; it mutates git and worktree state.
- Do not add `context: fork`; this workflow already creates git isolation explicitly.
- Do not add `paths:`; this is a generic git workflow skill.
- Do not keep giant walkthroughs, command tables, or recovery encyclopedias inline in `SKILL.md`.
- Do not use `rm -rf` for normal worktree cleanup.
- Do not delete user branches unless the user explicitly asked.
- Do not use force cleanup silently on dirty worktrees.

## When To Load References

- `references/worktree-expertise.md`
  Use at session start for role and domain expertise.

- `references/worktree-conventions.md`
  Use for branch naming, path layout, lifecycle, setup conventions, and destroy safety.

- `references/merge-playbook.md`
  Use for merge execution, conflict-resolution tiers, lockfile handling, stale-worktree cleanup, and abort-and-recreate recovery.

## Output Contract

Report:

1. the requested operation and resolved branch/worktree scope
2. the worktrees created, reused, or removed
3. the merge/conflict outcome and validation status
4. any branches or tags created or deleted
5. the final `git worktree list` and main-tree safety status
