---
name: readable-github
description: Reads GitHub via the gh CLI — repo metadata / README / file tree, issues with comments and timeline, pull requests (diff, files, inline comments, GraphQL review threads with isResolved / isOutdated), discussions (GraphQL), code (file contents and code search), and releases (with tarball / zipball fallback). Routes by URL shape into references/{topic}.md so only the relevant command sheet is loaded. Use when the URL is on github.com.
---

# GitHub Reader

Uses the `gh` CLI (which calls the GitHub REST/GraphQL API) for everything. The CLI handles auth, pagination, and rate limiting; AUP exempts API access from its scraping clauses.

## Prerequisite

```bash
gh auth status
```

If not logged in: `gh auth login`.

## Pick the right reference

Identify what kind of GitHub URL the user supplied, then follow the matching reference file:

| URL shape | Reference |
|---|---|
| `github.com/{owner}/{repo}` (root, README, file tree) | [references/repo.md](references/repo.md) |
| `github.com/{owner}/{repo}/issues/...` | [references/issues.md](references/issues.md) |
| `github.com/{owner}/{repo}/pull/...` | [references/pulls.md](references/pulls.md) |
| `github.com/{owner}/{repo}/discussions/...` | [references/discussions.md](references/discussions.md) |
| `github.com/{owner}/{repo}/blob/...`, `tree/...`, code search | [references/code.md](references/code.md) |
| `github.com/{owner}/{repo}/releases/...` | [references/releases.md](references/releases.md) |

For Gist URLs (`gist.github.com/...`), use the [readable-gist](../readable-gist/SKILL.md) skill instead.

## General tips

- Prefer `gh` subcommands (`gh repo`, `gh issue`, `gh pr`, ...) where they exist; fall back to `gh api` for endpoints they don't cover.
- Use `--json {fields}` to keep responses small. Each subcommand documents its `--json` field set; run `gh {sub} view --help` to list them.
- Rate limit: 5,000 req/hour for authenticated users. `gh api rate_limit` reports current usage.
