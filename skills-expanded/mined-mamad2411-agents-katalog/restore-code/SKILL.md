---
name: restore-code
description: "Restore code safely from backup artifacts created before risky changes. Use when undoing destructive operations, recovering from failed refactors or rebases, restoring deleted files, rolling back broad search-and-replace edits, or rehydrating work from backup branches and stashes. Supports preview-first recovery via backup branch, stash, or selective file restoration."
user-invocable: true
argument-hint: "Describe what needs to be restored and whether your source is a backup branch, stash entry, or specific files."
compatibility:
   environments:
      - vscode
      - github-copilot
      - copilot-cli
license: MIT
---

# Restore Code From Backup

Recover code from backup artifacts with a preview-first workflow that minimizes additional loss.

## When to Use This Skill

- After accidental destructive commands (`reset --hard`, `clean`, force-overwrite checkouts)
- After risky refactors or codemods introduced broad regressions
- After failed rebase or merge sequences where you need known-good state
- When files were deleted or overwritten and must be recovered quickly
- When a backup branch or stash exists and work must be restored safely

Keywords: restore code, recover backup, restore stash, recover branch snapshot, undo destructive change.

## Recovery Sources Supported

- Backup branches (`backup/*`)
- Named stashes created for safety snapshots
- Specific commit snapshots (including backup commits)
- Selective file restore from any source reference

## Prerequisites

- Run from repository root
- `git` is available
- Backup source exists or can be discovered
- Working tree state is inspectable

## Decision Flow

1. If full workspace rollback is required, restore from backup branch.
2. If local uncommitted work must be rehydrated, restore from stash.
3. If only selected files are needed, perform selective file restore.
4. If the target state is uncertain, preview diffs first and restore incrementally.
5. If current work may still be needed, run `backup-code` before restoring.

## Step-by-Step Workflow

### 1. Inspect Current And Recovery State

Run:

```bash
git status --short
git branch --show-current
git branch --list "backup/*"
git stash list --date=local
```

Record:

- Current branch
- Current uncommitted changes
- Available backup branches
- Candidate stash entry IDs

### 2. Choose Recovery Strategy

#### Strategy A: Restore Entire State From Backup Branch

Preview:

```bash
git diff --stat HEAD..backup/<source-branch>/<source-iso-timestamp>
```

Restore via reset to backup commit (destructive to current local state):

```bash
git reset --hard backup/<source-branch>/<source-iso-timestamp>
```

Alternative non-destructive approach:

```bash
git switch -c restore/<timestamp> backup/<source-branch>/<source-iso-timestamp>
```

Use this when broad rollback is needed.

#### Strategy B: Restore From Stash Snapshot

Preview stash contents:

```bash
git stash show --name-status "stash@{N}"
git stash show -p "stash@{N}" | head -n 120
```

Apply while keeping stash entry:

```bash
git stash apply "stash@{N}"
```

Apply and remove stash entry:

```bash
git stash pop "stash@{N}"
```

Use `apply` first when risk is unknown.

#### Strategy C: Restore Specific Files Only

From backup branch:

```bash
git restore --source backup/<source-branch>/<source-iso-timestamp> -- path/to/file.ts
```

From stash:

```bash
git restore --source "stash@{N}" -- path/to/file.ts
```

Use this when only partial recovery is needed.

### 3. Validate Recovery

Run:

```bash
git status --short
git diff --stat
```

Optional targeted checks:

```bash
pnpm exec nx affected --target=vitest --base=main
```

### 4. Finalize Recovery State

- Commit recovered changes if they are correct
- Keep source backup artifacts until recovery is confirmed
- Only delete backup branch/stash after verification

## Completion Criteria

- Recovery source identified and validated
- Restore executed with expected scope (full or selective)
- Post-restore diff matches intended files and content
- Validation checks pass or known residual issues are documented

## Troubleshooting

| Problem | Cause | Fix |
| --- | --- | --- |
| `unknown revision or path not in the working tree` | Wrong backup branch or stash reference | Re-list sources with `git branch --list "backup/*"` and `git stash list` |
| Stash apply conflicts | Current files diverged from stash base | Resolve conflicts, or apply into a temporary branch for safer merge |
| Restored too much content | Used full restore instead of selective restore | Revert unwanted files with `git restore -- path/to/file` and retry selectively |
| Lost current in-progress work during restore | Restore performed without checkpointing current state | Run `backup-code` before restoration in future; attempt recovery via reflog now |

## References

- Companion prevention workflow: `backup-code`
- Recovery history lookup: `git reflog`
- Safer partial restores: `git restore --source <ref> -- <path>`
