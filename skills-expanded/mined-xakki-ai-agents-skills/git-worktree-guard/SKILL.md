---
name: git-worktree-guard
description: 'Preserve other actors'' staged, unstaged and untracked work in a shared checkout. Use when the tree has changes you did not make, when several writers touch one repository, or before any step that could discard or overwrite local work. RU: грязное дерево, чужие изменения, параллельные агенты.'
---

# Git worktree guard

Use when a checkout holds changes you did not make, when more than one writer touches the repository, or before any step that could discard or overwrite local work.

- Establish the current actor's permitted baseline before mutation. Keep the index, working bytes and untracked files distinct; preserve opaque content within its authorized boundary. Never overwrite or discard another actor's changes merely to obtain a clean tree. If damage occurs, stop and recover only from verified, authorized evidence.
- Separate read-only discovery from writers. Serialize conflicting writes and index or ref changes, or run authorized gates against a complete immutable snapshot when unrelated concurrent edits are allowed. Preserve landed partial work and wait for actual writer completion before review.

Read [preservation and index guidance](../git-repo-run/references/preservation-and-index.md) and [workstream coordination](../git-repo-run/references/workstream-coordination.md). If a shared-worktree race occurs, use [concurrent writer recovery](../git-repo-run/references/concurrent-writer-recovery.md). For linked-worktree inclusion use [content coverage](../git-repo-run/references/worktree-content-coverage.md); for interrupted selective staging use [selective index and recovery](../git-repo-run/references/selective-index-and-recovery.md); for investigating saved changes use [stash provenance](../git-repo-run/references/stash-evidence.md). When protected dirty content constrains an authorized integration, see [isolated squash integration](../git-repo-run/references/isolated-squash-integration.md). Follow the user, project and runtime authorization for each operation; this skill does not grant additional authority.
