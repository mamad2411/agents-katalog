---
name: use-gh
description: Manages GitHub pull requests, issues, and CI runs using the gh CLI. Use when creating PRs, reviewing, merging, posting comments, checking CI status, or any gh operation.
compatibility: Requires gh CLI (brew install gh) and GitHub authentication
---

# use-gh

## Essential Principles

- **Always squash merge** and **delete the source branch** after merge
- **Detect PR templates** before creating a PR — check for `.github/pull_request_template.md` or templates in `.github/PULL_REQUEST_TEMPLATE/`
- **Inline review comments require `gh api`** — `gh pr comment` only posts top-level comments
- **Confirm before mutations** — don't create, merge, or comment without user approval

## Prerequisites

```bash
command -v gh >/dev/null 2>&1
```

If not found: `brew install gh`.

Verify authentication:

```bash
gh auth status
```

If not authenticated: `gh auth login`.

## Quick Start

```bash
gh pr create --title "Feature title" --fill
gh pr merge <NUMBER> --squash --delete-branch
gh pr comment <NUMBER> --body "Comment"
```

## PR Creation

### Step 1: Detect Templates

```bash
ls .github/pull_request_template.md .github/PULL_REQUEST_TEMPLATE/ 2>/dev/null
```

If a single template exists, use `--template` to apply it. If multiple exist in `PULL_REQUEST_TEMPLATE/`, list them and ask the user which to use.

### Step 2: Create PR

```bash
gh pr create \
  --title "Feature title" \
  --body "<description>" \
  --base main
```

When a template file is available, use `--template <filename>` instead of `--body` to pre-fill from the template.

| Flag | Purpose |
|------|---------|
| `--title` | PR title |
| `--body` | Description text |
| `--template` | Use a named template file as the starting body |
| `--fill` | Auto-fill title and body from commits (use when no template) |
| `--fill-first` | Use first commit for title/body |
| `--base` | Target branch (default: repo default branch) |
| `--draft` | Mark as draft |
| `--reviewer` | Request reviewers (comma-separated) |
| `--label` | Add labels (comma-separated) |
| `--assignee` | Assign to user(s) — use `@me` to self-assign |

## PR View and Merge

### View PR

```bash
gh pr view <NUMBER>                                             # summary
gh pr view <NUMBER> --comments                                  # with comments
gh pr view <NUMBER> --json title,state,reviews,statusCheckRollup  # structured data
gh pr diff <NUMBER>                                             # view diff
gh pr checks <NUMBER>                                           # CI status
```

### Merge

```bash
gh pr merge <NUMBER> --squash --delete-branch
```

Always squash and delete branch. Add `--auto` to merge automatically once CI passes.

## CI and Workflow Runs

```bash
gh run list --limit 10                          # recent runs
gh pr checks <NUMBER>                           # CI status for a PR
gh pr checks <NUMBER> --watch                   # watch until complete
gh run view <RUN_ID>                            # run details and failed steps
gh run view <RUN_ID> --log-failed               # logs for failed steps only
gh run rerun <RUN_ID> --failed                  # rerun only failed jobs
```

## Comments

### Top-Level Comment

```bash
gh pr comment <NUMBER> --body "Comment text"
```

### Inline Review Comment

Inline comments require the GitHub Reviews API via `gh api`.

**Step 1 — Find the head commit SHA:**

```bash
gh pr view <NUMBER> --json headRefOid --jq '.headRefOid'
```

**Step 2 — Write review JSON to temp file:**

```json
{
  "commit_id": "<HEAD_SHA>",
  "event": "COMMENT",
  "comments": [
    {
      "path": "src/file.ts",
      "line": 42,
      "body": "Comment text here"
    }
  ]
}
```

**`line` vs `position`:** Use `line` (the actual file line number). `position` is the offset within a diff hunk (lines down from `@@`) — it's fragile and error-prone. Prefer `line`.

| Field | When to use |
|-------|-------------|
| `line` | Comment on a specific line |
| `start_line` + `line` | Comment on a line range |
| `side`: `"RIGHT"` | Added/changed lines (default) |
| `side`: `"LEFT"` | Deleted lines |

**Step 3 — Post via API:**

```bash
gh api "repos/{owner}/{repo}/pulls/<NUMBER>/reviews" \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  --input /tmp/gh-review.json
```

**`event` values:** `COMMENT` (neutral), `APPROVE`, `REQUEST_CHANGES`.

## Issues

| Operation | Command |
|-----------|---------|
| List open issues | `gh issue list` |
| List my issues | `gh issue list --assignee @me` |
| View issue | `gh issue view <NUMBER>` |
| Create issue | `gh issue create --title "..." --body "..."` |
| Close issue | `gh issue close <NUMBER>` |
| Add labels | `gh issue edit <NUMBER> --add-label "bug,priority"` |

## JSON Output and Filtering

Most commands support `--json` with `--jq` for structured output:

```bash
gh pr list --json number,title,author --jq '.[] | "\(.number): \(.title) (\(.author.login))"'
gh pr view <NUMBER> --json reviews --jq '.reviews[] | "\(.author.login): \(.state)"'
gh issue list --json number,title,labels --jq '.[] | select(.labels | any(.name == "bug"))'
```

## Other PR Operations

| Operation | Command |
|-----------|---------|
| List open PRs | `gh pr list` |
| List my PRs | `gh pr list --author @me` |
| List PRs for review | `gh pr list --search "review-requested:@me"` |
| Close PR | `gh pr close <NUMBER>` |
| Reopen PR | `gh pr reopen <NUMBER>` |
| Mark ready | `gh pr ready <NUMBER>` |
| Edit PR | `gh pr edit <NUMBER> --title "..." --add-label "..."` |
