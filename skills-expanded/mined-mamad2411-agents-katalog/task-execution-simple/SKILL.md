---
name: task-execution-simple
description: Use when task-local spec or plan work is complete and a concrete docs/tasks task should be implemented through the repository's simple direct execution path.
---

# Task Execution Simple

Use after `task-preparation` has finished task-local docs and routine follow-up, and the task is ready for straightforward direct execution.

Owns branch/worktree isolation, readiness, implementation edits, verification, docs/status updates caused by implementation, implementation review, and branch closing. Does not own roadmap decomposition or task-local `spec.md` and `plan.md` authoring.

## Required Gates

| Gate | Required behavior |
|------|-------------------|
| Branch | Default never implement on the current branch; create a dedicated task branch by default unless the user explicitly chooses otherwise or a worktree workflow is specifically needed. |
| Readiness | Handle branch/worktree isolation and any other pre-code readiness work before implementation edits. |
| Verification | Verify implementation and update docs/status in the same round when behavior, API shape, or task state changed. |
| Review | Stop for implementation review before destructive cleanup or branch deletion. |
| Closing | Resolve only any remaining hard gate such as branch deletion or destructive cleanup after implementation review. |

After an implementation review pause, treat any clear forward-motion message as approval to follow the recommended non-destructive next step. Ask a separate approval question only for hard gates.

## Branch Isolation

- Default to creating a dedicated task branch in the current workspace.
- Use a worktree workflow only when the user explicitly wants one or when parallel or high-conflict execution makes a separate workspace specifically valuable.
- User explicitly asks to stay on current branch: proceed only with explicit user choice.

## Branch Closing

- Use `superpowers:finishing-a-development-branch` for merge/PR/keep/discard options.
- Use `superpowers:using-git-worktrees` cleanup rules; removing a worktree does not remove its task branch.
- Confirm before deleting any branch or worktree. If merge plus cleanup is chosen, confirm whether cleanup includes deleting the fully merged task branch.
- If the user asks to move forward, keep moving through non-destructive wrap-up steps, but stop before deleting a branch or worktree.

## Testing and Verification

- Follow the task-local `spec.md` and optional `plan.md` for testing and verification expectations.
- If relevant existing automated tests fail during the task, do not ignore them just because the task did not require adding new unit tests.
- Prefer fixing production code so existing tests keep expressing the same behavior.
- If existing tests need semantic changes because the task intentionally changes behavior, explain the reason and get user confirmation before changing what those tests assert.
- Small test-file repairs that preserve the original assertion intent do not need separate confirmation.

## Docs Boundaries

Code is source of truth when code and docs diverge. If implementation changes behavior, API shape, task status, architecture assumptions, or stable constraints, update the relevant docs in the same round. Move stable rules out of `docs/context/`.

## Detailed Rules and References

Use the existing execution references when needed:

- `references/task-execution-detailed-rules.md`

## Workflow

1. Receive handoff context from `task-preparation`.
2. Create branch/worktree isolation and complete readiness work before code edits.
3. Implement one concrete task.
4. Verify behavior and update docs/status affected by implementation.
5. Stop for implementation review.
6. Resolve branch closing and cleanup hard gates only when explicitly confirmed.

## When To Use

Use when a concrete task already has its task-local `spec.md` and optional `plan.md`, and the next work is direct implementation through the repository's simple execution path rather than delegated or specialized execution. Do not use before task-local docs are ready.

Do not use when:

- milestone/module/task structure is still being decided; use `milestone-planning`
- task-local `spec.md` or `plan.md` work still needs to be written or reviewed; use `task-preparation`
- the repository needs a delegated or specialized execution path instead of the simple direct path

## Common Mistakes

- Starting implementation before branch/worktree isolation is complete
- Treating a normal forward-motion message as approval for destructive cleanup
- Rewriting roadmap or task structure here instead of routing back to `milestone-planning`
