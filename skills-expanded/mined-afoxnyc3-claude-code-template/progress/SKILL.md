---
name: progress
description: Generate visual progress report showing implementation status
allowed-tools: Bash, Read, Glob
---

# Progress Report

Generate a visual progress report showing current implementation status.

## Instructions

### 1. Collect Current State

```bash
# Recent commits
git log --oneline -10

# Current branch status
git status --short

# Open PRs (if using GitHub)
gh pr list --state open --json number,title,headRefName 2>/dev/null || echo "No gh CLI or not a GitHub repo"

# Recently merged PRs (last 5)
gh pr list --state merged --limit 5 --json number,title,mergedAt 2>/dev/null || echo "No gh CLI"
```

### 2. Map Component Status

Check each major directory/component:

| Component | Status | Notes |
|-----------|--------|-------|
| [Component A] | done/wip/planned | Based on directory existence and recent commits |
| [Component B] | done/wip/planned | ... |
| ... | ... | ... |

### 3. Generate Summary

```markdown
## Progress Report - YYYY-MM-DD

### Completed
- [x] Item 1
- [x] Item 2

### In Progress
- [ ] Item 3 (PR #X open)
- [ ] Item 4

### Planned
- [ ] Item 5
- [ ] Item 6

### Blockers
- None / [Describe any blockers]
```

### 4. Output Format

Present the summary in a clear, scannable format suitable for status updates or team communication.
