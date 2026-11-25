---
name: git-branch-clean
description: 'Audit, archive, rename or delete Git branches without losing work, with plan-hash-bound cleanup helpers. Use for stale or integrated branches, branch archival, or pruning local and remote refs. RU: очистка веток, архив ветки, удалить ветки.'
disable-model-invocation: true
---

# Git branch cleanup and archival

Use to audit, archive, rename or delete branches. Verify the exact source, destination, checkout, worktrees, tip and recovery boundary first. A branch rename does not switch the active checkout. Preserve paused work and historical blockers, never delete a dirty worktree, and verify any separately authorized remote change.

Inventory actual local refs, remote refs and linked worktrees before selecting candidates. Compare ancestry, patch equivalence and available review evidence; verify unique work and dirty worktrees rather than trusting a single signal. Deletion requires applicable authorization and recoverable state; remote deletion is a separate action.

For a read-only local-branch comparison against a chosen base, run [the local audit helper](scripts/audit-local-branches.py) with Python 3 and `--base <commit-or-ref>`. Resolve the skill location through the current runtime's plugin interface. The helper fetches nothing, performs no deletions, snapshots branch tips and reports ancestry, patch equivalence and checked-out state as separate evidence; it fails if a comparison fails or observed refs change. Patch equivalence alone is not authorization or proof that a branch is safe to delete. Review remote and pull-request evidence separately when relevant.

To delete branches that are already integrated into the remote default branch, use [the cleanup helper](scripts/git-branch-clean.sh) only with authorization for those branches. It is a two-step, plan-bound operation:

1. The default dry-run runs `git fetch --prune` (unless `--no-fetch`), classifies branches as merged (ancestor, patch-equivalent, or a merged GitHub PR into the default branch when `gh` works), lists the unmerged and the protected ones, and prints `plan_sha256`. The default branch, `dev`, `main`, `master`, the checked-out branch, branches checked out in a worktree and `backup/*` are never candidates.
2. `--apply --plan-sha256 <hash>` recomputes the plan from the current refs and deletes nothing if any branch tip, classification, scope or the base moved. Before deleting, it records `<scope> <branch> <sha>` in `<git-dir>/branch-cleanup/deleted-<UTC>.tsv` (restore with `git branch <branch> <sha>`), reads the record back and re-checks each tip.

The default scope is `local`. Remote branches are deleted only with an explicit `--scope remote|both` that was part of the reviewed dry-run, and only if they still point at the reviewed commit (`git push --force-with-lease`). A hash is valid only for the scope it was printed for. Run `python3 test/test_git_branch_cleanup.py` from the skill directory after changing the helper.

Read [branch history and retirement](../git-repo-run/references/branch-history-and-retirement.md). For linked-worktree inclusion, use [content coverage](../git-repo-run/references/worktree-content-coverage.md). Follow the user, project and runtime authorization for each operation; this skill does not grant additional authority.
