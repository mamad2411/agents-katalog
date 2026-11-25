---
name: pr-review
description: >-
  Review GitHub pull requests and post inline code review comments using the gh
  CLI. Use when the user asks to review a PR, provides a PR link, or wants
  automated code review with inline feedback on a pull request.
---

# PR Review

Review a GitHub pull request, analyze the diff, and post inline review comments using `gh`.

## Prerequisites

- **`gh` CLI** must be installed and authenticated (`gh auth status` to verify).
- The local repo should correspond to the PR's repository, or the user must provide the full PR URL.

## Workflow

### Step 1: Resolve the PR

Accept any of these formats from the user:
- Full URL: `https://github.com/owner/repo/pull/123`
- Short reference: `#123` (uses current repo)
- Owner/repo with number: `owner/repo#123`

Extract `OWNER`, `REPO`, and `PR_NUMBER`. If only a number is given, infer owner/repo from the current git remote:

```bash
gh repo view --json owner,name --jq '"\(.owner.login)/\(.name)"'
```

### Step 2: Fetch PR metadata

```bash
gh pr view PR_NUMBER --json title,body,baseRefName,headRefName,files,additions,deletions,changedFiles,author,state
```

Bail out if the PR is already merged or closed.

### Step 3: Fetch the diff

```bash
gh pr diff PR_NUMBER
```

Parse the unified diff to understand every changed file, hunk, and line.

### Step 4: Analyze the changes

Review each file's diff for:

| Category | What to look for |
|----------|-----------------|
| **Correctness** | Logic errors, off-by-one, null/undefined access, race conditions |
| **Security** | Hardcoded secrets, SQL injection, XSS, insecure deserialization |
| **Performance** | N+1 queries, unnecessary allocations, missing indexes |
| **Maintainability** | Dead code, duplicated logic, unclear naming, missing types |
| **Testing** | Untested paths, missing edge cases, brittle assertions |
| **Style** | Inconsistencies with the rest of the codebase |

**Do not flag:**
- Purely stylistic nitpicks that a linter would catch
- Changes outside the diff (pre-existing issues)
- Suggestions that would significantly alter the PR's scope

### Step 5: Post the review

Build and submit the review in a single API call so all comments are grouped into one review, rather than individual standalone comments.

Write the review payload to a temp file, submit it, then clean up:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews \
  --method POST \
  --input /tmp/review.json

rm /tmp/review.json
```

**Construct `/tmp/review.json`** with this structure:

```json
{
  "body": "Overall review summary here.",
  "event": "COMMENT",
  "comments": [
    {
      "path": "src/utils.py",
      "line": 42,
      "side": "RIGHT",
      "body": "**Suggestion**: Consider handling the `None` case here to avoid a potential `AttributeError`."
    },
    {
      "path": "src/api/views.py",
      "line": 15,
      "side": "RIGHT",
      "body": "**Issue**: This query runs inside a loop — could cause N+1 performance problems. Consider prefetching."
    }
  ]
}
```

**Field reference:**

| Field | Value | Notes |
|-------|-------|-------|
| `event` | `COMMENT` | Use `COMMENT` for neutral feedback. Use `REQUEST_CHANGES` only if the user explicitly asks to block the PR. Never use `APPROVE` unless the user explicitly asks. |
| `body` | Summary string | High-level summary of the review. |
| `comments[].path` | File path | Relative to repo root, as shown in the diff. |
| `comments[].line` | Line number | The line number in the **new** version of the file where the comment should appear. |
| `comments[].side` | `RIGHT` | Always `RIGHT` to comment on the new version of the file. Use `LEFT` only when commenting on deleted lines. |
| `comments[].body` | Comment text | The review feedback for that specific line. |

### Multi-line comments

For comments spanning a range of lines, add `start_line` and `start_side`:

```json
{
  "path": "src/models.py",
  "start_line": 10,
  "start_side": "RIGHT",
  "line": 18,
  "side": "RIGHT",
  "body": "This entire block could be simplified using a dictionary comprehension."
}
```

## Comment formatting

Prefix each inline comment with a severity tag:

- **Critical** — Must fix before merge (bugs, security issues, data loss)
- **Suggestion** — Recommended improvement (performance, readability, maintainability)
- **Nitpick** — Optional, low-priority (naming, minor style)
- **Question** — Needs clarification from the author

Example:

```
**Critical**: This opens a SQL injection vector. Use parameterized queries instead of string interpolation.
```

## Review summary format

The `body` field (overall review summary) should follow this template:

```
## PR Review Summary

**PR**: #NUMBER — TITLE
**Files reviewed**: N changed files (+additions, -deletions)

### Key findings
- Finding 1
- Finding 2

### Verdict
COMMENT / REQUEST_CHANGES rationale
```

## Edge cases

- **Large PRs (>20 files):** Focus on the most impactful files first. Flag that a full review may need multiple passes.
- **Binary files:** Skip binary files in the diff.
- **Generated / lockfiles:** Skip auto-generated files (lockfiles, migrations with only timestamps, minified bundles). Mention that they were skipped.
- **No issues found:** Still submit a `COMMENT` review with a summary confirming the PR looks good. Do not leave the PR without feedback.

## Error handling

- If `gh auth status` fails, tell the user to run `gh auth login`.
- If the PR number is invalid, report the error clearly.
- If the review API returns an error (e.g., stale diff, permission denied), show the raw error and suggest remediation.
