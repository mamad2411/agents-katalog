---
name: gh-issue-view
description: Read GitHub issues and PRs using the gh CLI. Use this skill whenever the user asks to read, view, check, or look at a GitHub issue or pull request — even if they just say "look at issue 18" or "what does #42 say". Always use this skill instead of bare `gh issue view` or `gh pr view` commands to avoid the GitHub Projects (classic) deprecation error that causes exit code 1.
---

# GitHub Issue / PR Viewer

## The Problem

Running `gh issue view <number>` or `gh pr view <number>` without `--json` triggers a GraphQL error about the deprecated `projectCards` field (classic Projects sunset), causing **exit code 1** even when the issue data is perfectly accessible. This breaks silently and wastes retries.

## Always Use This Pattern

When reading an issue:
```bash
gh issue view <number> --json title,body,state,labels,assignees,comments,number,url,author,createdAt,updatedAt
```

When reading a PR:
```bash
gh pr view <number> --json title,body,state,labels,assignees,comments,number,url,author,createdAt,updatedAt,mergeable,mergeStateStatus,headRefName,baseRefName,reviews
```

**Never** use bare `gh issue view <number>` or `gh pr view <number>` without `--json` — they will fail.

## Repo Detection

If not already in a git repo with a GitHub remote, or if the user specifies a repo:
```bash
gh issue view <number> --repo owner/repo --json title,body,state,...
```

To auto-detect the current repo:
```bash
gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null
```

If auto-detect fails (not a GitHub repo), ask the user for `owner/repo`.

## Presenting the Output

After fetching, present:
- **Title** and **#number** (with URL as a link)
- **State** (open/closed) and **Labels**
- **Author** and **Created** date
- **Body** — render as markdown
- **Comments** — show each with author + timestamp + body; collapse threads longer than 5 comments and offer to expand

Don't dump raw JSON at the user — parse and display it clearly.

## Listing Issues / PRs

For listing, same rule applies — avoid fields that touch projectCards:
```bash
gh issue list --json number,title,state,labels,assignees,author,createdAt,url
gh pr list --json number,title,state,labels,assignees,author,createdAt,url,headRefName,baseRefName
```
