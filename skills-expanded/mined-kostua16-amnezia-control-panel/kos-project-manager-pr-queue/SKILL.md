---
name: kos-project-manager-pr-queue
description: Project-manager PR queue rules: action priority, stale Code Review rebases, finalizer fallback, workflow failure escalation, and one mutation per PR per run.
user-invocable: true
when_to_use: "When implementing or reviewing project-manager PR queue behavior."
category: workflows
keywords: [project-manager, pr-queue, rebase, finalizer, fix-review, direct-merge]
metadata:
  author: project-manager
  license: repo
  version: "1.0"
---

# Project Manager PR Queue

The PR queue route runs when open PRs are greater than the configured threshold. It inspects the latest PRs and computes at most one action per PR per run.

## Priority

1. Escalate failed repair workflows with a deduped `@claude fix ...`.
2. Resolve merge conflicts via exact `/rebase`.
3. Rebase stale current-head Code Review when the head commit is older than 5 hours and the latest current-head rebase was not a no-op.
4. Trigger `/fix` for failed checks.
5. Trigger `/fix-review` for review blockers (in alignment enforce mode, a Dependabot PR whose only blocker is `deps-review-manual` skips this and goes to the alignment review instead).
6. Dispatch `pr-finalizer.yml` for ready PRs.
7. If ready for more than 1 hour and still open, file a workflow issue, `/fix` it, then direct-merge only after project-manager review says `merge`.
8. For manual-only PRs: with `PM_ALIGNMENT_MODE=enforce`, run the alignment review on the next cycle and act on its `merge` / `request_fixes` / `hold` verdict (see `kos-project-manager-direct-merge`); otherwise direct-merge only after review says `merge` and either approval exists or 8 hours passed without maintainer rejection.

## Loop prevention

- Use the project-manager sticky state as cooldown memory, but always recompute live GitHub state.
- Reset head-specific state when the head SHA changes.
- A rebase no-op is `Pushed: no (no changes after rebase)` or `rebase_moved_head=false`; do not repeat stale-CR `/rebase` after that signal.

## Critical constraints

- Use existing workflows as the first path: finalizer before direct merge, fix-review before manual repair, rebase-pr for branch refresh.
- Direct merge is a fallback, never the default happy path.
- Do not make project-manager a required check.
