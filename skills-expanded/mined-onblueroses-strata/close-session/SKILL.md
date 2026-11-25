---
name: close-session
description: Reconcile a primary DeepSeek run across relevant repository state, Linear, the repository's AGENTS.md, and OptMem. Use when the user asks to wrap up, end, close, hand off, or finish a work session cleanly.
---

# Close Session

Close the work actually done under the current role. Ordinary conversation needs no ledger update or handoff, and small completed tasks need no restart brief.

## Outcome contract

- Goal: make completed work, remaining work, evidence, and restart state agree across relevant durable ledgers.
- Success: applicable verification, repository, spec, issue, repository `AGENTS.md`, and accepted OptMem state are reconciled; unfinished work is restartable when it needs to be.
- Does not count: closing before success, a mechanical note, a material deferral left untracked, or a delegated agent settling memory.
- Stop: issues actually worked carry truthful outcomes, material follow-ups have an owner, and unfinished work has enough context to resume.

## Workflow

1. Read applicable `AGENTS.md`, any active spec, issues actually worked, `git status`, and the relevant diff.
2. Run the narrow verification required by the task and independent review when risk warrants it. Keep incomplete objectives open.
3. If there is an active spec, update it truthfully and close its Frontier only when its success conditions pass. Save a brief when unfinished work has context worth carrying forward.
4. Append an outcome signed `(deepseek, YYYY-MM-DD)` to issues actually worked. Name artifacts, verification results, unknowns, and follow-ups. Move an issue to `Done` only after that comment succeeds.
5. Track material deferrals and unresolved decisions that need follow-through with exactly one `for:` owner; passing ideas and quick questions need no ticket.
6. Re-read the `AGENTS.md` lines that concern the changed files. Add a line there only when it preserves knowledge a future agent cannot cheaply rediscover.
7. For each durable memory candidate, if this is the root user-facing DeepSeek primary and startup reported OptMem available, judge it under `knowledge-management.md`, append accepted notes, and verify by exact recall. Delegated DeepSeek agents return candidates instead.
8. Re-read `git status`. Commit scoped finished work unless the user said not to or dirty overlap prevents a safe commit. Never push without authority.

## Return

Lead with completed versus open. Name verification evidence, ledger updates, working-tree state, commit state, and the exact next action. Include proposed notes only for delegated or failed-append candidates.
