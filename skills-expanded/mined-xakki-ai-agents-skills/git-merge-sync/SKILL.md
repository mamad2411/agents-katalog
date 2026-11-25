---
name: git-merge-sync
description: 'Reconcile merges and divergent histories while keeping both sides'' behavior and a recoverable source state. Use when resolving conflicts, reviewing a merge against both parents, squashing, rebasing or reconciling diverged branches. RU: слияние, конфликты, ребейз, расхождение истории.'
disable-model-invocation: true
---

# Git merge and history reconciliation

Use for conflict resolution, merge review, squash or rebase integration, and reconciling divergent histories.

- Identify the exact source, target, topology, merge bases and requested result before integration. Preserve adequate authorized recovery artifacts before history or ref mutations, account for additions and deletions, and compare the final candidate with the retained source. A local rewrite does not authorize remote publication or force updates.
- Resolving conflicts: apply existing owner decisions to each conflict, preserve both compatible behaviors, regenerate derived artifacts through supported tools, and report unresolved material policy choices. A clean or marker-free merge alone does not prove that both parents' behavior survived.
- Reviewing a pinned merge (read-only): compare affected files and contracts against each parent, verify relevant tests and the actual conflict context, and report precise findings.

Read [branch history and retirement](../git-repo-run/references/branch-history-and-retirement.md) and [merge and parent review](../git-repo-run/references/merge-and-parent-review.md). For parent-by-parent and generated-artifact checks use [merge parent evidence](../git-repo-run/references/merge-parent-evidence.md); for linked-worktree inclusion after squash integration use [content coverage](../git-repo-run/references/worktree-content-coverage.md); for protected dirty content during an authorized squash use [isolated squash integration](../git-repo-run/references/isolated-squash-integration.md). Follow the user, project and runtime authorization for each operation; this skill does not grant additional authority.
