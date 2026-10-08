---
name: git-merge-expert
version: 2.0.0
description: |
  Run a git merge, PR merge, conflict resolution, or rollback safely — readiness-checked and BACKED
  UP before anything touches shared history. Assesses branch/CI/review state and conflict risk, tags
  a backup point before non-trivial merges, resolves conflicts without dropping either side
  (regenerating lockfiles, not hand-editing), validates the result, then cleans up or rolls back —
  routing to the worktree specialist when isolated execution is safer. Never claims success with
  unresolved conflicts or failing validation, prefers `git revert` over `reset` on shared branches,
  and requires explicit confirmation before destructive rollback, force-push, or branch deletion.
  Use only when the user explicitly asks to merge, resolve conflicts, or roll back.
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Skill
disable-model-invocation: true
user-invocable: true
argument-hint: "[PR number, source branch, target branch, or merge task]"
arguments:
  - request
when_to_use: |
  Use only when the user explicitly asks to merge a branch or PR, resolve git conflicts, review
  merge readiness, or roll back a bad merge — "/git-merge-expert", "merge this branch", "resolve
  these conflicts", "roll back that merge". Do NOT use for read-only git inspection or unrelated
  code changes, and hand off to the worktree specialist (git-merge-expert-worktree) when the merge
  should run in an isolated worktree; explicit-user-only, confirm before destructive cleanup.
---

<EXTREMELY-IMPORTANT>
This skill mutates git state and must stay disciplined.

Non-negotiable rules:
1. Check merge readiness before merging: branch state, CI, reviews, and conflict risk.
2. Create a backup point before non-trivial merges or destructive recovery.
3. Validate after merging before declaring success.
4. Prefer isolated worktree execution for risky or explicitly isolated merges.
5. Get explicit user confirmation before destructive rollback or branch cleanup.
</EXTREMELY-IMPORTANT>

# Git Merge Expert

## Inputs

- `$request`: PR number, source branch, target branch, merge method, rollback target, or conflict-resolution goal

## Goal

Perform safe git merges by:

- assessing readiness and merge method
- isolating risk when needed
- resolving conflicts without dropping intent
- validating the result
- cleaning up or rolling back safely

## Step 0: Resolve the requested merge operation

Determine whether the user wants to:

- merge a PR
- merge one branch into another
- resolve conflicts from an in-progress merge
- assess merge readiness before executing
- roll back a bad merge
- clean up merged branches

If the requested scope, merge method, or cleanup behavior is ambiguous, use `AskUserQuestion`
before mutating git state.

**Success criteria**: The source, target, merge method, and cleanup expectations are explicit.

## Step 1: Assess readiness and choose the execution mode

Inspect:

- current branch and working tree state
- source and target branch topology
- PR readiness when applicable
- CI and review status when applicable
- conflict likelihood

Then choose whether to:

- proceed inline for a straightforward merge
- route to `git-merge-expert-worktree` for isolated execution

Prefer the worktree specialist when:

- the user explicitly asks for worktree isolation
- the merge is risky or multi-step
- cleanup/retry safety matters more than speed

Load `references/merge-strategies.md` for merge-method and readiness rules.

**Success criteria**: The merge is either blocked, approved for inline execution, or redirected to the worktree specialist.

## Step 2: Create a backup point and perform the merge

Before non-trivial merges or destructive rollback, create a backup reference such as a tag.

Then perform the requested operation:

- PR merge via `gh` when appropriate
- branch merge with the selected strategy
- conflict resolution for an in-progress merge

Rules:

- do not merge with failing CI unless the user explicitly wants to override
- do not silently drop either side of a conflict
- regenerate lockfiles instead of hand-editing them
- use the smallest safe merge method that matches the request

Load `references/conflict-and-rollback.md` for conflict tiers and recovery patterns.

**Success criteria**: The merge or conflict-resolution step is complete and git state is coherent.

## Step 3: Validate before cleanup or push

Validate the result with the narrowest relevant checks:

- `git status`
- conflict-free state
- build/test/typecheck commands when appropriate
- branch topology inspection

Rules:

- do not claim success if unresolved conflicts or failing validation remain
- stop and recover before cleanup or push when validation fails
- if rollback is needed, use the recovery guidance instead of improvising

**Success criteria**: The merge result is validated or the failure state is clearly identified.

## Step 4: Report, clean up, or roll back safely

Depending on the result:

- report the merge outcome
- comment on the PR if needed
- clean up merged branches conservatively
- roll back using the safest method for the branch type

Rules:

- prefer `git revert` over `git reset` on shared branches
- do not delete branches unless they are confirmed merged or the user explicitly asked
- warn before destructive cleanup or force-push operations
- if the merge was delegated to the worktree specialist, report that routing clearly

Load `references/conflict-and-rollback.md` for rollback and cleanup rules.

**Success criteria**: The user can see the outcome, any cleanup performed, and the remaining git state.

## Guardrails

- Do not let the model invoke this skill proactively; it mutates git history and branch state.
- Do not add `context: fork`; if isolation is needed, use the worktree specialist instead.
- Do not add `paths:`; this is a generic git workflow skill.
- Do not keep giant examples, command encyclopedias, or long failure catalogs inline in `SKILL.md`.
- Do not merge with unresolved conflicts.
- Do not delete user branches or force-push shared branches without explicit approval.

## When To Load References

- `references/merge-expertise.md`
  Use at session start for role and domain expertise.

- `references/merge-strategies.md`
  Use for merge-method selection, PR readiness checks, GitHub CLI usage, and when to route to the worktree specialist.

- `references/conflict-and-rollback.md`
  Use for conflict tiers, lockfile handling, rollback choices, and cleanup rules.

## Output Contract

Report:

1. the requested merge or rollback operation
2. the chosen execution mode and merge strategy
3. the readiness/validation status
4. any conflicts resolved, backup refs created, or rollback actions taken
5. the final git state and any cleanup performed
