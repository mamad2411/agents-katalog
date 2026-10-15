---
name: stale-pr-reminder
description: |
  Use this skill when the user wants to check for stale PRs, "find old pull requests",
  "stale PRs", "PRs needing attention", or wants to identify pull requests that have
  been inactive for too long. This skill scans repositories for PRs that need action
  and generates a prioritized reminder report. Requires Gitee MCP Server to be configured.
version: 2.0.0
requires:
  mcp-servers:
    - gitee
---

# Stale PR Reminder

Scan repositories for stale Pull Requests and generate a prioritized action report.

## What is a "Stale PR"?

A stale PR is a Pull Request that:
- Has been open for a long time without updates
- Has not received reviewer attention
- Has merge conflicts that haven't been resolved

## Staleness Levels

| Level | Age | Action |
|-------|-----|--------|
| 🔴 Critical | > 28 days | Close or rework |
| 🟠 Severe | > 14 days no update | Ping author |
| 🟡 Moderate | > 7 days no review | Assign reviewer |
| 🟢 Mild | > 3 days no activity | Monitor |
| ✅ Fresh | < 3 days | No action |

## Steps

### Step 1: Fetch Open PRs

Call `list_repo_pulls` to retrieve all open PRs:

```
INPUT:
  - owner: repository owner
  - repo: repository name
  - state: "open"
  - sort: "created"
  - direction: "asc"
  - per_page: 100
```

### Step 2: Get PR Details

For each PR, call `get_pull_detail`:

```
EXTRACT:
  - number: PR number
  - title: PR title
  - user.login: author username
  - created_at: creation timestamp
  - updated_at: last update timestamp
  - mergeable: false = has conflicts
  - draft: is draft PR
```

### Step 3: Get Comments (Optional)

Call `list_pull_comments` to check review activity:

```
ANALYZE:
  - has_reviewer_comments: any comment from non-author
  - last_comment_date: most recent comment timestamp
```

### Step 4: Calculate Staleness

No code execution needed. The AI can parse timestamps directly.

**Today's date**: 2026-03-17

For each PR:

1. Parse `created_at` (format: `YYYY-MM-DDTHH:MM:SSZ`, e.g., `2026-01-15T10:30:00Z`)
2. Parse `updated_at` the same way
3. Calculate days between created_at and today (2026-03-17)
4. Calculate days between updated_at and today
5. Check if `mergeable: false` (has conflicts)
6. Check if `draft: true`

**Classification rules**:
- `critical`: age > 28 days
- `severe`: age > 14 days AND days_since_update > 14
- `moderate`: age > 7 days AND no reviewer comments
- `mild`: age > 3 days AND days_since_update > 3
- `fresh`: otherwise

### Step 5: Generate Report

Create a grouped report with links:

```markdown
## Stale PR Report: {owner}/{repo}

### Critical (> 28 days)
| PR | Title | Age | Author |
|----|-------|-----|--------|
| [#{num}](https://gitee.com/{owner}/{repo}/pulls/{num}) | {title} | {age}d | @{author} |

### Severe (> 14 days no update)
| PR | Title | Age | Last Update |
|----|-------|-----|-------------|
| [#{num}](https://gitee.com/{owner}/{repo}/pulls/{num}) | {title} | {age}d | {days}d ago |

### Moderate (> 7 days no review)
| PR | Title | Age |
|----|-------|-----|
| [#{num}](https://gitee.com/{owner}/{repo}/pulls/{num}) | {title} | {age}d |

### Summary
- Critical: {count}
- Severe: {count}
- Moderate: {count}
- Fresh: {count}
```

## Usage Examples

### Example 1: Basic Check

```
User: "Check for stale PRs in myrepo"

AI: Scanning myrepo...
Found 10 open PRs:
- 2 Critical (> 28 days)
- 3 Severe (> 14 days)
- 5 Moderate (> 7 days)

[Shows report]
```

### Example 2: Check Specific Author

```
User: "Are there any stale PRs from @alice?"

AI: Found 2 stale PRs from @alice:
- PR #42: 25 days old, needs rebase
- PR #45: 12 days old, waiting for review
```

## Notes

- Be diplomatic when mentioning stale PRs
- Exclude bot PRs (dependabot, renovate) by default
- Respect "wip", "draft", "on-hold" labels
