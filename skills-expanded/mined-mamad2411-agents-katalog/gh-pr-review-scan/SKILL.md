---
name: gh-pr-review-scan
description: "Use when the user wants a quick dashboard of GitHub PR review work across repositories, including open/draft PRs and total, resolved, and unresolved review counts."
---

# GitHub PR Review Scan

## Overview

Use this skill to query GitHub with `gh` and produce a Markdown table of PRs authored by the current authenticated user. Default to open PRs only; draft PRs are included because GitHub draft PRs still have `state: OPEN`, and the script labels them as `DRAFT`.

Use this for PR-level scanning across repositories. For thread-level handling inside one PR, including `reviewcheck.md`, replies, and resolving review threads, use `gh-pr-review-resolve`.

## Quick Start

Run the bundled script with repository names:

```bash
python3 scripts/open_pr_review_summary.py <owner>/<repo-a> <owner>/<repo-b> <owner>/<repo-c>
```

The script outputs a Markdown table with clickable repo and PR links:

```markdown
| Repo | PR | Status | Title | Comment Total | Resolved | Unresolved |
```

## Counting Rules

- `Comment Total` is `PR conversation comments + review thread comments`.
- `Resolved` is the number of review threads where `isResolved == true`.
- `Unresolved` is the number of review threads where `isResolved == false`.
- Closed and merged PRs are excluded by default through `state:open`.
- Draft PRs are included and displayed as `DRAFT`.
- Repositories with no matching PRs are shown with a `No open/draft PR` row.

## Review Check Format

Default output for this skill is the PR summary table above. Only use the review check record format when the user explicitly asks for a local handling record, `reviewcheck.md`, or per-comment reply tracking.

Do not use this skill's table numbering to reply to or resolve review threads. When taking thread-level actions, switch to `gh-pr-review-resolve`, re-fetch live unresolved threads, and use `threadId`/`latestCommentId` checks before resolving.

When needed, use this table:

```md
PR #<number> unresolved review threads 本地处理记录。

编号按 GitHub unresolved threads 抓取顺序：

| # | Status | ID | Link | Reply | Reply_ZH |
| --- | --- | --- | --- | --- | --- |
| 1 | 已解决 | 3394352828 | [link](https://github.com/...#discussion_r3394352828) | Updated. ... | 已更新。... |
```

- `Status`: one of `待处理`, `处理中`, `已解决`, `已回复`, `已关闭`, `无需处理`, `需确认`, `暂缓`.
- `ID`: extract the numeric part from the review discussion anchor, e.g. `#discussion_r3394352828` becomes `3394352828`; do not include `r`.
- `Link`: GitHub review comment link.
- `Reply`: copy-ready English GitHub reply.
- `Reply_ZH`: Chinese translation or explanation of `Reply`; do not post this to GitHub.

## Workflow

1. Confirm `gh` is authenticated with `gh api user --jq .login`.
2. Run `python3 scripts/open_pr_review_summary.py` with the requested repositories.
3. If network access is blocked, request escalation for `gh api`.
4. Return the generated table directly to the user, preserving Markdown links.

## Options

Pass `--all-states` before repositories to include closed and merged PRs too:

```bash
python3 scripts/open_pr_review_summary.py --all-states <owner>/<repo>
```

Pass `--author <login>` to query a specific author instead of the current `gh` user:

```bash
python3 scripts/open_pr_review_summary.py --author <github-login> <owner>/<repo>
```
