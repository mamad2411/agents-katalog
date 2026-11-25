---
name: git-rewrite-commit-dates
description: Rewrite commit timestamps from a specified commit (inclusive) to HEAD with evenly spaced times, with the newest commit set to current time. Use when the user asks to batch-adjust git commit times, normalize commit history timestamps, or change dates after a specific commit SHA.
entrypoint: scripts/rewrite_commit_dates.py
---

# Git Rewrite Commit Dates

Rewrite git commit timestamps from a specified commit to HEAD with evenly spaced dates.

## Arguments

Arguments are passed directly to the underlying Python script:

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--start-commit <SHA>` | **Yes** | - | Starting commit SHA (inclusive) |
| `--step-minutes <N>` | No | 5 | Minutes between consecutive commits |
| `--dry-run` | No | false | Preview changes without actually rewriting |

## Usage Examples

### Basic usage - rewrite from specified commit with default 5-min step
```
skill: git-rewrite-commit-dates
args: --start-commit abc1234
```

### Custom step interval
```
skill: git-rewrite-commit-dates
args: --start-commit abc1234 --step-minutes 10
```

### Preview changes only (dry run)
```
skill: git-rewrite-commit-dates
args: --start-commit abc1234 --step-minutes 5 --dry-run
```

## User-Facing Slash Commands

Users can also trigger this skill via slash commands:

```
/git-rewrite-commit-dates --start-commit abc1234 --step-minutes 5
```

## Safety Rules

1. **Backup created automatically** - Script creates `backup/rewrite-dates-<timestamp>` branch
2. **Require explicit confirmation** - For destructive operations not using `--dry-run`
3. **Warn about force push** - If commits were already pushed to remote, user needs force push

## Workflow

1. Verify current directory is a git repository
2. Validate start commit exists
3. Create backup branch: `backup/rewrite-dates-<timestamp>`
4. Calculate evenly spaced timestamps (newest = current time)
5. Run `git filter-branch` to rewrite dates
6. Show summary of rewritten commits

## Verification

After execution, verify with:
```bash
git log --date=iso --pretty=format:'%h %ad %s' -n 20
```

Expected output: commits should have evenly spaced timestamps, with the newest at current time.

## Notes

- Both `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` are modified
- If `start_commit` is the root commit, the entire history is rewritten
- Rewriting history invalidates old commit SHAs
- This operation uses `git filter-branch` which is destructive
