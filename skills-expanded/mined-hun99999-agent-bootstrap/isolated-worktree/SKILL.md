---
name: isolated-worktree
description: Use only when the user explicitly requests an isolated Git worktree or explicitly approves isolation for overlapping writable work.
---

# Isolated Worktree

## Result

Provide one task-specific workspace with a known path and branch while preserving the original checkout and its unrelated work.

## Route

1. Resolve the repository root, current branch, linked-worktree state, and current changes.
2. Reuse the current workspace when it is already an isolated worktree suitable for the task.
3. Prefer the host's native worktree capability. Otherwise use `git worktree add` with a `codex/<task>` branch and the repository's declared worktree location. When no location is declared, use a task-specific sibling directory outside the tracked tree.
4. Resolve branch or path collisions from observed Git state before creation.
5. Run only the setup or baseline check needed to begin the requested task.
6. Report the absolute workspace path, branch or detached state, and readiness evidence.

## Stop

Return a concrete blocker when isolation requires destructive cleanup, overwriting an existing path, changing unrelated work, or new authority. Leave worktree removal and branch deletion to a separately authorized cleanup task.
