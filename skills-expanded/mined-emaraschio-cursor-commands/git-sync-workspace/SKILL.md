---
name: git-sync-workspace
description: >-
  Sync every git repo in a Cursor multi-root workspace to its remote default
  branch: discover roots, preflight each repo, fetch --all --prune, checkout
  default, pull --ff-only. Skips dirty or unsafe repos with a clear report.
  Use for "sync workspace", "update all repos", "back to main", or reset
  workspace repos to remote HEAD without losing uncommitted work.
user-invocable: false
---
# Git sync workspace

## Role

You sync multiple git repositories in a Cursor workspace to the latest remote default branch (`main` or `master`). This is the safe "back to base state" routine: fetch, checkout default, fast-forward pull, not a destructive reset.

## When to use

Use when the user wants every repo in a multi-root workspace updated after context-switching, before cross-repo assessments, or when starting fresh work from remote HEAD. For a single broken repo (merge conflict, detached HEAD), use `fix-git-issues` instead.

## Workflow

Run phases in order. **Preflight every repo before any write.**

### Phase 0: Discover repos

1. **Workspace file (preferred):** find `*.code-workspace` under the Cursor workspace root(s). Parse `folders[].path` and resolve relative paths against the workspace file location.
2. **Host profile (fallback):** if no workspace file, read optional `profiles/repos.yaml` beside this skill (see [Host overlay](#host-overlay)).
3. **Ask (last resort):** if discovery yields nothing, ask the user which paths to include. Do not scan arbitrary `~/code/*` without direction.
4. De-duplicate paths. Keep only directories that contain a `.git` directory.
5. If the user scopes the request (e.g. "only repo1 and repo2"), filter to matching paths only.

### Phase 1: Preflight (read-only, every repo)

Before modifying any repo, show a preflight table:

| Path | Current branch | Default branch | Working tree | Ahead / behind |
|------|----------------|----------------|--------------|----------------|

Collect:

- **Path**: repository root (absolute or workspace-relative).
- **Current branch**: `git branch --show-current` (note detached HEAD).
- **Default branch**: from `git symbolic-ref refs/remotes/origin/HEAD` (strip `refs/remotes/origin/`), else `main`, else `master`.
- **Working tree**: `git status --porcelain` (empty = clean).
- **Ahead / behind**: `git rev-list --left-right --count @{u}...HEAD` when upstream exists.

Also detect **in-progress operations** (merge, rebase, cherry-pick) via `git status` or `.git/MERGE_HEAD` / `.git/rebase-merge`. Treat these as **unsafe**; skip with reason `skipped_unsafe`.

**Dirty policy (hard rule):** if the working tree is not clean, or checkout to default would strand unpushed commits the user has not explicitly accepted losing, **do not modify that repo**. Record `skipped_dirty` or `skipped_unsafe` and continue other repos.

### Phase 2: Sync (clean repos only)

For each repo that passed preflight:

1. Record `old_sha`: `git rev-parse HEAD` (when on default) or note branch switch.
2. `git checkout <default_branch>`. If local branch missing, create tracking branch from `origin/<default>`.
3. `git fetch --all --prune`
4. `git pull --ff-only`. If no upstream is set, use `git merge --ff-only origin/<default>` instead.

**Concurrency:** run `git fetch --all --prune` across repos in parallel with a cap of **≤ 6** concurrent shell sessions. **Serialize** checkout and pull per repo (one repo at a time for those steps) to avoid races.

If `pull --ff-only` fails (diverged local commits on default), mark the repo **failed**, capture stderr, and do not merge or rebase without explicit user approval.

### Phase 3: Report

Emit a workspace summary with three sections:

**Synced**: path, branch, `old_sha` → `new_sha` (short)

**Skipped**: path, status (`skipped_dirty`, `skipped_unsafe`, `no_remote`), reason

**Failed**: path, failing command, stderr excerpt

## Safety

- Never `git reset --hard`, `git clean`, or **force-push** unless the user explicitly requests it in the same turn with per-repo confirmation.
- Never checkout over a **dirty** working tree.
- Never discard stashes or delete branches without approval.
- Redact credentials in `git remote -v` output if shown to the user.

## Host overlay

When no `.code-workspace` file is present, the host workspace may provide a repo list. Copy the template from `profiles/repos.yaml` in this skill directory:

```yaml
repos:
  - path: ../repo1
  - path: ../repo2
```

Paths are relative to the file location or absolute. The agent reads this file only when workspace-file discovery fails.

## Distinction from other commands

- **`fix-git-issues`**: reactive troubleshooting (conflicts, detached HEAD), not bulk workspace sync.
- **`commit`** / **`commit-same-branch`**: start new work on a branch; this ends on default at remote HEAD.
- **`merge-open-prs`**: merges PRs then syncs one repo, not a workspace-wide default-branch sync.
- **`scoped-audit`**: read-only orchestration across a surface, not git checkout/pull.

## Guardrails

- Preflight every repo and skip any dirty working tree (record `skipped_dirty`); never checkout or pull over uncommitted changes.
- Use `pull --ff-only` and never `git reset --hard` or force-push without explicit per-repo approval.
- Discover repos from the workspace file or user scope; do not guess paths outside discovery.
