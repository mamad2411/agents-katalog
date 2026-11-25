---
name: git-repo-run
description: 'Perform scoped Git work safely: inspect, stage, commit, branch, push, prepare a pull request. Use for selective commits in a dirty or shared worktree, exact commit messages and trailers, multi-workstream commits, or reviewing a repair commit. RU: коммит, ветка, пуш, пулреквест, выборочный коммит.'
---

# Git work: scoped commits, branches, merges, pull requests

Use for Git operations that need a clear scope, preservation of existing work, or verification of a commit or ref. Follow the user, repository and runtime policy for the current task; loading this skill does not grant permission to commit, rewrite history, push, merge, deploy or contact others.

1. Resolve the exact repository, worktree, current branch, destination and requested operation. Preserve the current branch unless the task or project policy requires another; do not infer a branch, remote or publication target from an example.
2. Before mutation, inspect the authorized worktree and staged state at an appropriate scope. Distinguish existing changes, other agents' work and private files; do not read or stage content outside the permitted boundary. Coordinate overlapping writers (see `git-worktree-guard`) and preserve pre-existing index entries.
3. Stage only the authorized paths and changes. Check the complete staged diff and path list before committing: selecting paths to add does not remove other entries already staged. Handle mixed hunks and partially staged files without silently adding unrelated work.
4. Preserve the requested commit subject, body and trailers exactly; do not add attribution or other trailers unless requested or required by applicable project policy. Keep normal hooks and signing requirements enabled. Use [message and staging guidance](reference.md) when the message or index needs careful handling.
5. For an authorized commit, verify its ID, message, parents and affected paths against the intended result; separately report remaining work and failed or skipped checks. Do not amend or rewrite history without the necessary authorization.
6. For merge, rebase, push, PR or deployment, verify the actual source and target and the authorization for each effect. Recheck the relevant refs before an authorized publication and confirm its result. A successful commit or local check is not evidence of remote publication or deployment.

## Selective commits in a dirty or shared worktree

- An inventory is read-only and does not authorize a commit. For an authorized commit, record the original staged and working state, freeze the allowed paths and hunks, preserve existing foreign staging, include new files and both rename endpoints, and inspect the entire staged candidate and the resulting commit. A checkpoint is not acceptance.
- A successful add or a matching filename list does not prove the staged bytes are right: compare complete staged blobs, modes, deletions and rename endpoints with the approved candidate, and inspect normal hooks and the actual commit.
- Several workstreams: resolve the owner's approved scope, branch, commit count and order before staging; account for each workstream and each shared hunk; validate every requested intermediate candidate; preserve protected or unclassified content; verify the actual commit and the remaining state.
- Details: [preservation and index](references/preservation-and-index.md), [selective index and recovery](references/selective-index-and-recovery.md), [workstream coordination](references/workstream-coordination.md), [worktree content coverage](references/worktree-content-coverage.md).

## Reviewing a repair commit next to uncommitted tests

Capture the target commit, branch, relevant status and diffs, and the actual test scope before editing. Inspect the uncommitted tests, keep legitimate coverage, and report unrelated or uncertain work to its owner; never discard or rewrite a test just to make the tree look clean. Exercise the affected public behavior with project-sanctioned checks and discover the supported runtime instead of imposing a container, network mode or command. Distinguish passing, failing, blocked, skipped and unrun gates: a focused pass does not make a blocked full suite green. Make a test-only follow-up only when authorized, then verify the resulting commit, paths and excluded changes. Never claim runtime compatibility, clean state or acceptance beyond what the checks established.

## Preparing a pull request

Determine the actual base branch and requested scope from the task or repository; ask only if they cannot be established. Inspect the working tree, staged changes, branch history and the complete diff against that base, preserving unrelated staged and unstaged work, and look for accidental credentials or generated artifacts without adding them to the index. Run the relevant project-supported checks and report failures, skipped checks and limits. Draft a title and description that explain the problem, resulting behavior and useful validation evidence, following the project's template when one exists. Drafting does not authorize committing, pushing or creating the pull request. Do not assume a branch, trailer, agent configuration file or template.

Specialized work: use `git-path-run` for relocation, `git-merge-sync` for merges and history, `git-branch-clean` for branch pruning, the project's Kanban policy for card lifecycle, and the project's own review or test gates for acceptance. A skill name or a stated role does not grant additional authority.
