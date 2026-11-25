---
name: multi-agent
description: Split work across agents without losing control, with one worktree and prompt file per task and a coordinator who integrates. Use when dispatching more than one agent or writing a brief for another agent.
---

# Multi-agent dispatch

Run agents in parallel only on independent tasks: two agents editing one interface produce two plausible diffs that cannot both be right. The unit is **one task, one branch, one worktree, one prompt file, one acceptance check**. Read-only reviewers may share a tree if writes are forbidden.

## Roles

- **Coordinator:** owns the task list, architecture, order, integration and the verification label. Creates and removes worktrees and picks each task's model. Never lets a worker redefine the product.
- **Worker:** does one bounded task in its own worktree and returns changed files, checks run, evidence and risks. Touches nothing outside its scope.
- **User:** decides product behavior and accepts the result.

## Setup

Use the worktree location and base the project names; do not assume the default branch holds the work the task needs. `git worktree add "$path" -b "$branch" "$base"`. Put the prompt in `WORKER_PROMPT.md` at that worktree's root, marked "Do not commit it". Remove the worktree only after its branch is integrated or abandoned.

## The prompt contract

A missing or contradictory field is a reason to challenge the task, not to start.

```text
Task ID:
Desired user-visible behavior:   what a person sees, not an implementation
Why it is needed:
Allowed files:                   a real list, plus a rule for the ragged edge
Forbidden scope:                 the specific temptations (adjacent refactors, coordinator files, publishing)
Dependencies already verified:
Acceptance test:                 numbered; each item can fail
Required checks:                 build flags, disk limits, commands never to run, what runs on CI
Return: summary, changed files, verification, risks, commit hash.
```

Put every binding constraint in the prompt: what cannot be verified here and the ceiling of what CI can prove; disk-heavy build flags; "report, do not patch" for observation tasks. When a null result is legitimate, say so ("if the only lever costs more than it buys, report that and close"), so the worker does not ship churn.

## Before dispatching

Serialize two tasks when their allowed files intersect, when they touch a shared runtime, protocol or permission contract still being reshaped, when they would exhaust one disk or CPU, or when they install to the same path or app home.

## Verification and integration

Label each result `user-verified` (the only "done"), `agent-verified`, or `unverifiable here` (name what would be needed); the ranking is in the [spec skill](../spec/SKILL.md#4-verify). Integrate one branch at a time and rerun the acceptance test on the merged tree.
