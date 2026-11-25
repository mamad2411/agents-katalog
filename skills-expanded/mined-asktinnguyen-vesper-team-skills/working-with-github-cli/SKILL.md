---
name: working-with-github-cli
description: Uses GitHub CLI (gh) with minimal-output patterns to inspect repositories, pull requests, issues, checks, and workflow runs efficiently. Use when the user asks to review GitHub state, fetch PR/issue details, create PRs/issues, comment, merge, or debug CI while keeping token usage low.
alwaysAllow:
  - Bash
---

# Working with GitHub CLI

Use `gh` as the default interface for GitHub operations. Prefer concise commands and structured JSON queries to reduce output and token usage.

## Quick Start

Run these first to establish context:

```bash
gh auth status
gh repo view --json nameWithOwner,defaultBranchRef -q '{repo: .nameWithOwner, defaultBranch: .defaultBranchRef.name}'
```

If a specific repo is needed, add `--repo owner/name` to commands.

## Token-Efficient Rules

1. Prefer `--json ... -q ...` over full text output.
2. Request only required fields.
3. Limit result count with `--limit N`.
4. Avoid fetching full bodies unless explicitly needed.
5. Summarize status first, drill down only on flagged items.
6. For logs, fetch only failing jobs/steps and targeted run IDs.

## Core Command Patterns

### Pull requests

List open PRs (compact):

```bash
gh pr list --state open --limit 20 --json number,title,author,updatedAt,isDraft,reviewDecision,statusCheckRollup,url -q '.[] | {n: .number, title, author: .author.login, draft: .isDraft, review: .reviewDecision, checks: (.statusCheckRollup // [] | length), updated: .updatedAt, url}'
```

Get one PR summary:

```bash
gh pr view <number> --json number,title,state,isDraft,author,baseRefName,headRefName,reviewDecision,mergeable,statusCheckRollup,url -q '{n: .number, title, state, draft: .isDraft, author: .author.login, base: .baseRefName, head: .headRefName, review: .reviewDecision, mergeable: .mergeable, checks: (.statusCheckRollup // [] | length), url}'
```

Get files changed only:

```bash
gh pr view <number> --json files -q '.files[].path'
```

### Issues

List open issues (compact):

```bash
gh issue list --state open --limit 30 --json number,title,author,labels,updatedAt,url -q '.[] | {n: .number, title, author: .author.login, labels: [.labels[].name], updated: .updatedAt, url}'
```

Get one issue summary:

```bash
gh issue view <number> --json number,title,state,author,labels,assignees,createdAt,updatedAt,url -q '{n: .number, title, state, author: .author.login, labels: [.labels[].name], assignees: [.assignees[].login], created: .createdAt, updated: .updatedAt, url}'
```

### CI / Workflows

List recent runs:

```bash
gh run list --limit 20 --json databaseId,workflowName,headBranch,status,conclusion,event,createdAt,url -q '.[] | {id: .databaseId, wf: .workflowName, branch: .headBranch, status, conclusion, event, created: .createdAt, url}'
```

Show only failed runs:

```bash
gh run list --limit 30 --json databaseId,workflowName,conclusion,url -q '.[] | select(.conclusion == "failure") | {id: .databaseId, wf: .workflowName, url}'
```

Inspect one failed run jobs:

```bash
gh run view <run-id> --json jobs -q '.jobs[] | select(.conclusion == "failure") | {name, status, conclusion, startedAt, completedAt}'
```

Fetch log only when needed:

```bash
gh run view <run-id> --log-failed
```

## Safe Write Operations

Create issue:

```bash
gh issue create --title "<title>" --body "<body>" --label "<label>"
```

Comment on PR/issue:

```bash
gh pr comment <number> --body "<comment>"
# or
gh issue comment <number> --body "<comment>"
```

Create PR from branch:

```bash
gh pr create --title "<title>" --body "<body>" --base <base> --head <head>
```

Merge PR (only when requested):

```bash
gh pr merge <number> --squash --delete-branch
```

## Troubleshooting

- Auth problems: `gh auth status` then `gh auth login`
- Wrong repo context: use `--repo owner/name`
- Missing fields in query: run once without `-q` and inspect available JSON keys
- CI debugging too noisy: start from `gh run list` filtered to failures, then inspect one run

## Operating Checklist

1. Confirm auth and repo.
2. Pull compact status snapshot (PRs/issues/runs).
3. Identify anomalies (failed checks, blocked merge, stale PRs).
4. Drill down only into anomalies.
5. Return concise action items with URLs.

## Examples

### Example: "Check open PRs and blockers"

1. `gh pr list --state open --limit 20 --json number,title,reviewDecision,mergeable,statusCheckRollup,url`
2. Extract only PRs with failing checks or `mergeable != MERGEABLE`.
3. Report per-PR blockers and next action.

### Example: "Debug failing CI"

1. `gh run list --limit 30 --json databaseId,workflowName,conclusion,url`
2. Pick latest failed run ID.
3. `gh run view <run-id> --json jobs`
4. `gh run view <run-id> --log-failed` only if job-level data is insufficient.
