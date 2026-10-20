---
name: "bitbucket-cloud"
description: "Handle Bitbucket Cloud PR operations. Use for \"PR\", \"pull request\", \"review\" when repo is on bitbucket.org."
---

# Bitbucket Cloud PR Operations

## Platform Detection

Run `git remote -v` to verify this is Bitbucket Cloud (bitbucket.org):
- SSH format: `git@bitbucket.org:workspace/repo.git`
- HTTPS format: `https://bitbucket.org/workspace/repo.git`
- Extract: workspace = `workspace`, repository = `repo`

## Status Indicators

When listing or displaying PRs, use these status emojis based on PR state:

| Condition | Status |
|-----------|--------|
| Draft | 📝 Draft |
| Open | ✅ Open |
| Merged | 🔀 Merged |
| Declined | ❌ Declined |

## Output Format

Display PRs in a table with columns: `| # | Title | Author | Branch | Status | Updated |`

Example:
```
| 42 | Add authentication feature | alice | feature/auth | ✅ Open | 1/22/2026 |
| 41 | Update dependencies | bob | chore/deps | 📝 Draft | 1/20/2026 |
```

## PR Review

When reviewing a PR:
1. Fetch PR details and diff
2. Analyze for bugs, security issues, performance, and code quality
3. Present findings as: `## PR Review: #<NUM> - <TITLE>`
4. List issues with file references: `file_path:line_number`
5. Provide verdict: APPROVE, REQUEST_CHANGES, or COMMENT
6. Post comments/approve via MCP tools if requested
