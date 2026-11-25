---
name: pr-trends
description: Generate weekly and monthly pull request trend tables for a git repository, including created PRs, merged PRs, average days to merge, and lines changed. Use when a user asks for PR throughput trends, repo contribution trends, weekly or monthly PR summaries, merge velocity, or a table like Created/Merged/Avg Days/Lines Δ.
---

# PR Trends

Use this skill when the user wants a repo-level pull request trend report.

## Quick start

Run the bundled script from the target repository:

```bash
node .agents/skills/pr-trends/scripts/report-pr-trends.mjs
```

Useful options:

```bash
node .agents/skills/pr-trends/scripts/report-pr-trends.mjs --repo /path/to/repo
node .agents/skills/pr-trends/scripts/report-pr-trends.mjs --mode gh
node .agents/skills/pr-trends/scripts/report-pr-trends.mjs --mode git
```

## Source selection

- `--mode auto`: try `gh pr list` first for exact PR `createdAt`, `mergedAt`, and line counts. Fall back to `git` if `gh` is unavailable or offline.
- `--mode gh`: require GitHub CLI data. Use this when the user needs exact PR creation trends and accurate days-to-merge.
- `--mode git`: use only local mainline history. This gives reliable merged counts and merged lines changed, but it cannot recover exact PR creation timestamps or closed-unmerged PRs.

## Output

The script prints:

1. A weekly summary table
2. A monthly summary table
3. A short note describing which data source was used

## Interpretation

- `Created` is grouped by PR creation time when GitHub metadata is available.
- `Merged`, `Avg Days`, and `Lines Δ` are grouped by merge time.
- In `git` fallback mode, `Created` and `Avg Days` are shown as `-` because local git history does not preserve complete PR lifecycle metadata.

## Notes

- Run from the repo root unless `--repo` is provided.
- The script reads first-parent history so the report reflects the mainline branch.
- If the fallback note mentions missing PR numbers, treat those as likely closed, unmerged, or otherwise not reconstructable from local git alone.
