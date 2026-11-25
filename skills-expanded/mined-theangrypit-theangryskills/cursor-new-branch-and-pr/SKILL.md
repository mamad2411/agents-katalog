---
name: cursor-new-branch-and-pr
description: Create a fresh branch, complete work, and open a pull request
---

## Runtime selection

Before runtime-dependent work, read [execution selection](references/runtime/selection.md). In a verified T3 host follow [the T3 contract](references/runtime/t3.md) and its method reference; the inline section below is the native Codex branch, not literal T3 dispatch. Outside T3, native Codex follows that inline branch unchanged. If the host is ambiguous or a required capability is unavailable, report the gap; a permission refusal never authorizes switching branches.

## Native Codex branch

## Codex publication boundary

Treat repository review, local edits, pushing a branch, opening or updating a PR, and merging as distinct effects. Verify the target repository and current user authorization for each external write. If push or PR publication is not yet authorized, complete the local branch, diff, checks, and draft PR text so approval is the final step. Do not merge unless separately requested. Preserve the upstream review and CI workflow within those boundaries.

# New branch and PR

## Trigger

Starting work that should be shipped through a clean branch and pull request workflow.

## Workflow

1. Ensure the working tree is clean or explicitly handled.
2. Create a descriptive branch from the latest main.
3. Complete implementation and tests.
4. Commit focused changes and push.
5. Create a concise PR with summary and test notes.

## Guardrails

- Keep branch scope focused on one change set.
- Include verification notes before requesting review.

## Output

- New branch name
- PR summary and test notes
- PR URL
