---
name: git-stats
description: Shows contribution stats, hotspot files, and commit patterns for the repo
argument-hint: [author] [--since=30days]
user-invocable: true
allowed-tools: Bash(git *)
effort: low
---

## Git Repository Stats

```bash
# Overall stats
git shortlog -sn --no-merges | head -20

# Recent activity
git log --oneline --since="30 days ago" | wc -l

# Most changed files (hotspots)
git log --name-only --no-merges --pretty=format: | sort | uniq -c | sort -rn | head -20

# Commit frequency by day of week
git log --format="%ad" --date=format:"%A" | sort | uniq -c | sort -rn

# Lines changed per author (if requested: $ARGUMENTS)
git log --no-merges --author="$1" --shortstat | grep -E "file|insertion|deletion" | awk '{files+=$1; ins+=$4; del+=$6} END {print "Files:", files, "Insertions:", ins, "Deletions:", del}'
```

Present findings as a readable report:
- Top contributors
- Most active files (high churn = technical debt candidates)
- Commit patterns (which days/times are most active)
- Any observations about code health
