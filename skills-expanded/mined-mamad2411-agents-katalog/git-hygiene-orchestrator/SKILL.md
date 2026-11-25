---
name: git-hygiene-orchestrator
description: Audit and clean Git branches, remote-tracking refs, and worktrees safely. Use when Codex is asked to inspect Git hygiene, stale branches, merged branches, remote refs, worktrees, dirty work, merge conflicts, branch cleanup, pruning, repository cleanup commands, or when the task should be finished through validation, commit, push, pull request creation, and merge if gates allow.
---

# Git Hygiene Orchestrator

## Mission

Audit Git branches, remote-tracking refs, and worktrees before recommending or executing cleanup. Protect uncommitted work, detect conflicts, classify stale or merged branches using evidence, and separate low-risk metadata pruning from higher-risk branch, worktree, and remote deletion.

Default to audit-first and conservative. Prefer preserving work over deleting it. Never hide uncertainty. When cleanup is safe, recommend exact commands. When cleanup is risky, explain why and require explicit approval.

## Finish Workflow Authority

Treat the repository's blanket finish approval, or a user instruction of `finish it`, as explicit authorization to run the repository finish workflow for the current task whenever the user has not explicitly limited scope to read-only, no-commit, no-push, or local-only work:

1. Inspect status and confirm the intended work scope.
2. Run the relevant tests, lint, contract checks, or smoke checks for the changed surface.
3. Stage only task-owned files.
4. Commit with a concise task-scoped message.
5. Fetch and rebase or otherwise sync using the repo-approved safe path.
6. Push the task branch.
7. Open a pull request against the repo's default branch.
8. Merge the pull request only when branch protection, required checks, required reviews, and repo policy allow it.

Do not treat `finish it` as permission to bypass safety gates, force-push, merge red checks, delete user work, skip required review, or push directly to protected branches. If any step is blocked, complete all earlier safe steps and report the exact blocker and next required action.

## Intake

Start every task by reading repository instructions such as `AGENTS.md`, `CONTRIBUTING.md`, `.codex/`, `.github/`, and local workflow docs when present.

Create a work item with:

- Objective
- Acceptance criteria
- Out-of-scope items
- Risks
- Definition of Done

When the runtime and current instructions allow delegation, split independent audit work into:

- Branch Topology Auditor
- Worktree Auditor
- Dirty Work / Conflict Auditor
- Cleanup Executor, only after approval

If delegation is unavailable or not allowed, perform those roles directly.

## Task and Artifact Links

For every task this skill performs, coordinates, or reports on, carry forward relevant direct links when they are available:

- Azure Boards work items, Tasks, Bugs, User Stories, Features, or Epics that track the objective or repo action.
- Pull requests, branches, commits, builds, releases, deployments, validation logs, and worktree paths that provide evidence for the task.
- Delegated agent or task handoffs when the runtime exposes a durable task, thread, or handoff link.

Resolve links through the repository's source of truth first, such as Azure DevOps for Azure Repos or GitHub for GitHub remotes. Do not fabricate URLs. Use connector or CLI-returned URLs when available, or construct Azure DevOps work item links only from confirmed organization, project, and work item IDs.

Always include relevant task and artifact links in status updates and final output. If a relevant link should exist but cannot be resolved, state `link unavailable` with the exact blocker instead of omitting it.

## Hard Safety Rules

- Do not run `git reset --hard`, `git clean`, `git checkout --`, `git restore`, `git branch -D`, `git push --force`, or remove worktrees with dirty changes unless the user explicitly approves that exact action.
- Prefer `git branch -d` over `git branch -D`.
- Do not delete branches checked out by any active worktree.
- Do not remove a worktree with uncommitted, untracked, staged, or conflicted files unless the user explicitly approves that exact action.
- Do not delete unmerged local or remote branches unless the user explicitly approves after seeing unique commits.
- Do not assume a branch is safe because it is old. Use merge-base, ahead/behind, upstream status, and diff evidence.
- Treat remote branch deletion as higher risk than local branch deletion.
- Avoid plain `git prune`; use `git worktree prune` and `git remote prune` for this task.

## Pull Request Defaults

When this skill creates or completes a pull request, default to the repository's protected-branch completion path unless the user or repo policy explicitly requires something else:

- Enable squash merge.
- Enable auto-complete after required policies, checks, and reviews pass.
- Enable source-branch deletion after completion.
- In Azure Repos, pass those options when creating the PR:

```powershell
az repos pr create --source-branch <branch> --target-branch <base> --auto-complete true --squash true --delete-source-branch true --transition-work-items true
```

- If the PR already exists, set the same defaults immediately:

```powershell
az repos pr update --id <pr-id> --auto-complete true --squash true --delete-source-branch true --transition-work-items true
```

If the repository does not support one of those settings, or policy prevents auto-complete, leave the PR open in the safest available state and report the exact blocker. Do not silently fall back to a merge commit or leave source-branch cleanup unspecified.

## Inventory

Run read-only checks first. Detect the primary branch if `main` is not confirmed:

```powershell
git symbolic-ref --quiet --short refs/remotes/origin/HEAD
```

Use the detected branch, usually `main`, in the inventory commands:

```powershell
git status --short --branch
git remote -v
git worktree list --porcelain
git branch -vv --all
git branch --merged main
git branch --no-merged main
git branch -r --merged origin/main
git branch -r --no-merged origin/main
git for-each-ref --sort=-committerdate --format="%(refname:short)|%(objectname:short)|%(committerdate:iso8601)|%(authorname)|%(upstream:short)|%(upstream:track)|%(contents:subject)" refs/heads refs/remotes
git worktree prune --dry-run --verbose
git remote prune origin --dry-run
```

If the primary branch is not `main`, replace `main` and `origin/main` with the detected branch and its remote-tracking ref.

## Worktree Audit

For every path from `git worktree list --porcelain`, run:

```powershell
git -C <worktree-path> status --short --branch
git -C <worktree-path> diff --stat
git -C <worktree-path> diff --cached --stat
git -C <worktree-path> ls-files --others --exclude-standard
```

Classify each worktree:

- `Clean`: no staged, unstaged, untracked, deleted, or conflicted files.
- `Dirty`: staged, unstaged, untracked, or deleted files exist.
- `Conflicted`: Git reports unmerged paths.
- `Missing/prunable`: Git reports `prunable` or the path no longer exists.
- `Locked`: worktree metadata has a lock reason.

Record path, branch or detached HEAD, current commit, upstream, lock/prune state, cleanliness, whether the commit is merged into the primary branch, and inferred purpose from the path or branch name.

## Conflict Audit

Detect conflict state with:

```powershell
git status --short
git diff --name-only --diff-filter=U
git ls-files -u
rg "<<<<<<<|=======|>>>>>>>" .
git diff --check
```

If conflicts exist:

- List each conflicted file.
- Identify whether the conflict is content, rename/delete, add/add, delete/modify, or binary.
- Inspect both sides with safe commands:

```powershell
git diff
git diff --ours -- <file>
git diff --theirs -- <file>
git show :1:<file>
git show :2:<file>
git show :3:<file>
```

Recommend one resolution per file: keep ours, keep theirs, manually merge, delete file, or split into a follow-up. Apply a resolution only when it is obvious or user-approved.

After resolving conflicts, run:

```powershell
git diff --check
git status --short
```

Also run project tests or focused validation when available.

## Branch Analysis

For every local branch, collect:

- Current commit
- Upstream
- Ahead/behind
- Merged into primary branch
- Checked out by a worktree
- Remote exists or is gone
- Last commit date and author
- Duplicate tip with other branches
- Unique commits versus primary branch

Use evidence commands such as:

```powershell
git rev-list --left-right --count origin/main...<branch>
git log --oneline origin/main..<branch>
git diff --stat origin/main...<branch>
git merge-base --is-ancestor <branch> origin/main
git branch --contains <commit>
```

Replace `origin/main` with the detected primary remote-tracking ref when needed.

Classify branches:

- `Keep`: default branch, unmerged branch, active worktree branch, dirty worktree branch.
- `Delete local`: merged into primary, not checked out, no unique work, or upstream gone but already merged.
- `Review`: duplicate branch, clean checked-out branch, unusual remote/upstream state.
- `High risk`: unmerged branch, dirty worktree branch, remote-only branch with unique commits.

## Cleanup Rules

Treat cleanup categories as different risk levels:

- Metadata pruning: `git worktree prune` and `git remote prune origin` are acceptable after dry-run review.
- Local branch deletion: use `git branch -d` only for merged branches that are not checked out by any worktree.
- Worktree removal: use `git worktree remove <path>` only for clean, reviewed worktrees that are clearly obsolete.
- Remote branch deletion: require explicit user approval unless the user already gave clear cleanup authorization and policy permits it.

Use remote branch deletion only when all are true:

- The branch is merged into `origin/<primary>`.
- The branch has no unique commits.
- The user requested remote cleanup or explicitly approves it.
- Repository policy allows remote branch deletion.

Command:

```powershell
git push origin --delete <branch>
```

Dirty or conflicted worktrees must be preserved unless the user explicitly approves removal.

## Execution Sequence

Use this sequence:

1. Run inventory.
2. Report planned cleanup grouped by risk.
3. Execute safe metadata cleanup:

```powershell
git worktree prune --verbose
git remote prune origin
```

4. Delete safe merged local branches with `git branch -d`.
5. Remove only clean worktrees that are clearly obsolete.
6. Delete remote merged branches only after explicit user approval or clear instruction.
7. Re-run verification.

Never claim cleanup succeeded without command output confirming it.

## Verification

After cleanup, run:

```powershell
git worktree list --porcelain
git worktree prune --dry-run --verbose
git remote prune origin --dry-run
git branch -vv --all
git status --short --branch
```

## Final Output

Lead with the result. Include:

1. Relevant task and artifact links, or `link unavailable` with the blocker.
2. What was cleaned.
3. What was intentionally preserved.
4. Remaining dirty, conflicted, or unmerged work.
5. Commands that failed or were skipped.
6. Exact next recommended commands, if any.
7. Final risk assessment.
