---
name: development-branch-closeout
description: "Use after implementation and required verification when PM/coordinator must choose merge, pull request, preserve, discard, or workspace cleanup handling for the current branch."
---

# Development Branch Closeout

Use this after required reviews and verification have evidence. It turns branch handling into an explicit, safe PM decision.

## Preconditions

- Required implementation, review, and verification evidence is present or explicitly blocked.
- Current branch, worktree state, base branch, and dirty status are known.
- Top-level session or PM/coordinator owns the user-facing decision.

## Detect

- `git status --short`
- `git branch --show-current`
- `git rev-parse --git-dir`
- `git rev-parse --git-common-dir`
- `git rev-parse --show-toplevel`
- Candidate base: `main`, `master`, or PM-provided base branch.

## Decision Surface

Use native ask UI when available. Follow the Native Ask Contract from `core-workflow-contract` for structured ask UI requirements. Present only applicable options:

- `merge_local`: merge to the selected base branch after verification on the merge result.
- `open_pr`: push the branch and create a pull request; preserve the worktree for review follow-up.
- `keep_branch`: leave branch/worktree as-is and report path, branch, and next manual command.
- `discard`: destructive path; requires explicit typed confirmation and a list of commits/files/worktree path that would be removed.

If native ask UI is unavailable and a choice is required, follow the Native Ask Contract from `core-workflow-contract` for fallback behavior.

## Safety Rules

- Do not merge, push, delete, or discard unless the user explicitly chose that action.
- Do not offer merge/PR as complete when verification is failed or blocked.
- Cleanup only worktrees known to be project-created, such as under `.worktrees/`, `worktrees/`, or a `workspace-isolation` artifact. Never remove harness-owned or unknown workspaces.
- For `open_pr` and `keep_branch`, preserve the worktree.
- For `discard`, require exact typed confirmation before deleting anything.

## Output

Return:

- `branch_state`
- `base_branch`
- `dirty_status`
- `verification_summary`
- `decision_options`
- `selected_action`
- `cleanup_scope`
- `residual_risk`
