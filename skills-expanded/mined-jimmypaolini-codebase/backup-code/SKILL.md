---
name: backup-code
description: "Create a safety backup before potentially destructive actions. Use when running risky git commands (reset, rebase, clean, restore, checkout with overwrite, force push), applying large sweeping edits, mass refactors, broad search-and-replace, generator rewrites, or any operation that may be hard to undo. Produces a recoverable snapshot via backup branch, stash, or both, and verifies recovery commands."
user-invocable: true
argument-hint: "Describe what risky operation you are about to run and whether you prefer branch backup, stash backup, or both."
compatibility:
   environments:
      - vscode
      - github-copilot
      - copilot-cli
license: MIT
---

# Backup Code Before Risky Changes

Create a recoverable snapshot of local work before any potentially destructive operation.

## When to Use This Skill

- Before git operations that can discard or rewrite work
- Before large sweeping code changes across many files
- Before automated codemods, generator rewrites, or bulk renames
- Before cleanup commands touching untracked files
- Any time rollback confidence is low

Keywords: backup branch, safety checkpoint, stash snapshot, destructive git command, recover changes.

## Risky Operations Covered

- `git reset --hard`
- `git clean -fd` / `git clean -fdx`
- `git rebase` / `git rebase --onto`
- `git restore --source ... --worktree --staged`
- `git checkout` or `git switch` paths/branches that overwrite local work
- `git push --force` / `git push --force-with-lease`
- Large multi-file edits where undo history is insufficient

## Prerequisites

- Run from repository root
- Working tree state is inspectable with `git status --short`
- `git` is available

## Decision Flow

1. If current changes are meaningful and may be needed intact, create a backup branch snapshot.
2. If quick temporary rollback is needed, create a named stash.
3. If operation is highly destructive or uncertain, do both.
4. If no local changes exist, still create a backup branch for pre-operation baseline.

## Step-by-Step Workflow

### 1. Inspect Current State

Run:

```bash
git status --short
git branch --show-current
```

Record:

- Current branch name
- Whether there are tracked modifications
- Whether there are untracked files

### 2. Create Backup Artifact

Choose one strategy.

#### Strategy A: Backup Branch Snapshot (recommended)

```bash
iso_timestamp="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
current_branch="$(git branch --show-current)"
backup_branch="backup/${current_branch}/${iso_timestamp}"

git switch -c "$backup_branch"
git add -A
git commit -m "chore(codebase): 🔧 create safety backup before risky changes"
git switch "$current_branch"
```

Use this when you need a durable, auditable checkpoint.

#### Strategy B: Named Stash Snapshot

```bash
timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
stash_name="backup:${timestamp}:before-risky-change"

git stash push --include-untracked -m "$stash_name"
```

Use this when you need a quick local rollback point.

#### Strategy C: Maximum Safety (both)

Run Strategy A first, then Strategy B if additional local-only checkpointing is desired.

### 3. Verify Recovery Paths

For branch backups:

```bash
git branch --list "backup/*"
```

For stash backups:

```bash
git stash list --date=local
```

### 4. Print Recovery Commands

Branch recovery:

```bash
git switch <backup-branch>
```

Stash recovery:

```bash
git stash apply "stash@{N}"
```

### 5. Proceed With Risky Operation

Only continue after backup artifact and recovery commands are confirmed.

## Completion Criteria

- Backup branch exists, or stash entry exists, or both
- Backup includes all intended tracked and untracked changes
- Recovery command is printed and verified
- Risky operation starts only after all checks pass

## Troubleshooting

| Problem | Cause | Fix |
| --- | --- | --- |
| `nothing to commit` on backup branch | No file changes staged | Keep branch as baseline checkpoint or proceed with stash-only if needed |
| `No local changes to save` from stash | Clean worktree | Create branch checkpoint only |
| Cannot switch branches | Ongoing merge/rebase/cherry-pick | Resolve or abort in-progress operation first, then create backup |
| Backup commit rejected by hooks | Strict hooks on commit | Use stash strategy for local checkpoint, then revisit backup commit approach |

## Notes

- Never use destructive commands before creating at least one checkpoint artifact.
- Prefer backup branch for long-running or high-risk tasks because it survives stash pruning and improves traceability.
- Backup branch naming convention: `backup/{branch_name}/{iso_timestamp}`.
