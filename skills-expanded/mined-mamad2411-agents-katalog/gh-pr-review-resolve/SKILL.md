---
name: gh-pr-review-resolve
description: "Use when the user wants to work through one GitHub PR's review comments: find unresolved threads, decide what is fixed, draft replies, save review notes, or resolve threads."
---

# GH PR Review Resolve

## Overview

Use this skill to summarize unresolved GitHub PR review threads, identify recent reviewer comments, identify which are addressed by the current commit/diff, draft replies for those, and list remaining unresolved issues with high/medium/low priority labels.

Use GitHub CLI GraphQL for thread-aware state. Do not rely only on flat PR comments because flat comments lose `isResolved`, `isOutdated`, and thread grouping.

Use this for thread-level handling inside one PR. For repository-wide PR review counts and open/draft PR scanning, use `gh-pr-review-scan`.

## Workflow

1. Resolve the PR:
   - If the user provides a PR URL, parse `owner/repo` and PR number from it.
   - If the user provides `owner/repo#123` or `#123`, use that.
   - If no PR is provided, infer it from the current branch with `gh pr view --json number,url,headRefName,baseRefName`.
2. Fetch unresolved review threads with `scripts/fetch_unresolved_threads.py`.
3. Inspect local context:
   - `git status --short`
   - `git log -1 --oneline --stat`
   - relevant `git show HEAD -- <paths>` or `git diff -- <paths>` when judging whether the latest commit/current diff fixed a thread.
4. Classify unresolved threads:
   - **Fixed by current commit/diff**: the reviewed issue is now addressed locally, even if GitHub still shows the thread unresolved or outdated.
   - **Still unresolved**: the issue still exists, or the current code has not clearly addressed it.
   - **Needs decision**: architectural/product judgment is needed before changing code.
   - Assign every unresolved or needs-decision thread a priority label: `High`, `Medium`, or `Low`.
5. Output:
   - If the user asks for recent comments, start with **Recent Unresolved Comments** sorted by `latestCommentAt` descending.
   - First list PR/comment links and suggested replies for fixed threads.
   - Then list still-unresolved issues sorted by priority.
   - Use numbered lists for review items so the user can reference them easily.
   - Keep numbering stable within the current response and state that numbers correspond to unresolved threads sorted by `latestCommentAt` descending.
   - Include each unresolved item as: `Priority`, `status`, `file:line`, `reviewer`, `latest comment date`, `comment link`, `summary`, and `recommended next action`.
   - When a suggested reply is useful, place only the reply text in a fenced `md` code block so it can be copied directly.

## Review Check Format

When the user asks for a local handling record, `reviewcheck.md`, or a table of fixed review comments and replies, use this format:

```md
PR #<number> unresolved review threads 本地处理记录。

编号按 GitHub unresolved threads 抓取顺序：

| # | Status | ID | Link | Reply | Reply_ZH |
| --- | --- | --- | --- | --- | --- |
| 1 | 已解决 | 3394352828 | [link](https://github.com/...#discussion_r3394352828) | Updated. ... | 已更新。... |
```

Column rules:

- `#`: current table number, using the unresolved thread fetch order.
- `Status`: use only the status values listed in **Status Values**.
- `ID`: extract the numeric part from the review discussion anchor, e.g. `#discussion_r3394352828` becomes `3394352828`; do not include `r`.
- `Link`: GitHub review comment link.
- `Reply`: copy-ready English GitHub reply.
- `Reply_ZH`: Chinese translation or explanation of `Reply`; do not post this to GitHub.

## Review Record Save Prompt

After generating a review check table, proactively ask whether to save it as Markdown unless the user already gave an explicit save/display instruction.

Ask with these options:

| Option | Behavior |
| --- | --- |
| `保存并展示` | Default. Save the Markdown file and show the table in the response. |
| `仅展示` | Do not write a file; show the table in the response. |
| `仅保存` | Save the Markdown file; respond with the file path and a short summary only. |
| `不保存` | Do not write the file; do not show the full table unless the user explicitly asked to display it. |

Default save path:

```text
reviews/<owner>-<repo>-<pr-number>.md
```

Examples:

```text
reviews/<owner>-<repo>-35.md
reviews/<owner>-<repo>-42.md
```

Save rules:

- Save relative to the current project checkout by default.
- Create the `reviews/` directory if it does not exist.
- If the user provides an explicit path, use that path instead.
- If `owner` is unknown, use `<repo>-<pr-number>.md`.
- If both `owner` and `repo` are unknown, use `pr-<pr-number>.md`.
- Never overwrite an existing review record silently; ask before replacing it, or append a timestamp suffix if the user wants a separate record.
- The saved file must include the heading, ordering note, and the full `| # | Status | ID | Link | Reply | Reply_ZH |` table.

## Status Values

Use these exact `Status` values in `reviewcheck.md` and other local review handling records:

| Status | Meaning |
| --- | --- |
| `待处理` | Not started yet, or just fetched from GitHub. |
| `处理中` | Code changes are in progress, but not confirmed complete. |
| `已解决` | Fixed locally and ready to reply to the reviewer. |
| `已回复` | Replied on GitHub, but the review thread may not be resolved yet. |
| `已关闭` | Replied and resolved the review thread. |
| `无需处理` | No code change is needed, such as a false positive, outdated concern, or non-blocking note. |
| `需确认` | Product, architecture, or tradeoff confirmation is needed before acting. |
| `暂缓` | Valid work, but deferred outside the current PR or current handling batch. |

Default flow: `待处理` -> `处理中` -> `已解决` -> `已回复` -> `已关闭`.

Special flows:

- `待处理` -> `无需处理`
- `待处理` -> `需确认`
- `需确认` -> `处理中` / `暂缓` / `无需处理`
- `已解决` -> `暂缓` if the fix should move out of the current PR.

## Script

Resolve `<skill_dir>` to the directory containing this `SKILL.md`, then run from the target git checkout:

```bash
python3 <skill_dir>/scripts/fetch_unresolved_threads.py [PR]
```

Examples:

```bash
python3 .../fetch_unresolved_threads.py https://github.com/<owner>/<repo>/pull/35
python3 .../fetch_unresolved_threads.py <owner>/<repo>#35
python3 .../fetch_unresolved_threads.py 35
python3 .../fetch_unresolved_threads.py
```

The script prints JSON with PR metadata and unresolved threads sorted newest-first by `latestCommentAt`. Each unresolved thread includes `commentCount`, `latestCommentAt`, and `latestComment` for recent-comment summaries. It uses `gh api graphql`; `gh` must be authenticated.

To reply to a numbered unresolved thread and mark it resolved:

```bash
python3 <skill_dir>/scripts/reply_and_resolve_thread.py [PR] --index <number> --body '<markdown reply>'
```

Prefer exact thread ids when processing more than one thread or after pushing
new commits, because unresolved-thread indexes can change when GitHub marks
threads outdated or resolved:

```bash
python3 <skill_dir>/scripts/reply_and_resolve_thread.py [PR] \
  --thread-id PRRT_xxx \
  --expect-comment-id 3394352828 \
  --body '<markdown reply>'
```

Prefer stdin for multi-line Markdown replies:

```bash
printf '%s\n' 'Updated. <implementation note>' | python3 <skill_dir>/scripts/reply_and_resolve_thread.py [PR] --index <number>
```

The script replies with the GitHub REST review-comment replies endpoint, equivalent to:

```bash
gh api repos/<owner>/<repo>/pulls/<pr-number>/comments/<comment-database-id>/replies -f body='<markdown reply>'
```

Then it resolves the review thread with GraphQL `resolveReviewThread`, because the REST reply endpoint does not mark a thread resolved. Use `--dry-run` first when using `--index`, especially after commits, pushes, or resolving another thread. The script refetches unresolved threads before selecting, so `--index` always means the current newest-first unresolved order, not an older summary.

## Recent Comment Summary

When asked to summarize recent unresolved comments, produce a compact grouped summary:

```md
## Recent Unresolved Comments

1. **High** | `path:line` | @reviewer | updated YYYY-MM-DD
  - Comment: <one-sentence summary of the latest unresolved reviewer concern>
  - Status: Still unresolved / Fixed locally / Needs decision
  - Action: <specific next step>
  - Link: <comment URL>
  - Reply:
    ```md
    Updated. <copy-ready reply text>
    ```
```

Use the latest comment in each thread to define recency, but summarize the whole thread when earlier comments clarify the issue. If several comments share a theme, group them under one priority heading while preserving individual links.

## Reply And Resolve By Number

When the user asks to reply to or resolve a numbered item:

1. Re-fetch unresolved threads immediately before acting.
2. Map the requested number to the newest-first unresolved thread order used in the latest summary.
3. Run `reply_and_resolve_thread.py --dry-run` and verify the selected thread's `threadId`, `latestCommentId`, path, line, URL, and reply body before sending.
4. Prefer `--thread-id` plus `--expect-comment-id` for the live call after a dry run.
5. Refuse to resolve if the item is still clearly unresolved or needs a product decision, unless the user explicitly confirms they want to resolve anyway.
6. Confirm the exact reply body before sending if the user did not provide one.
7. Send the reply and resolve the thread with `reply_and_resolve_thread.py`.
8. Report the created reply URL and resolved status.

If the user provides several numbers, process them one at a time. After each successful reply/resolve, re-fetch unresolved threads before using another `--index`, because indexes may shift. For batch handling, first create a local table with `threadId`, `latestCommentId`, link, and reply for each item, then use `--thread-id` and `--expect-comment-id` so replies cannot drift onto the wrong thread.

## Reply Style

Draft replies as concise implementation notes:

```md
Updated. <specific code-level change and why it addresses the review concern>.
```

Always wrap copy-ready replies in fenced `md` code blocks. Do not put bullets, labels, or surrounding explanation inside the code block; include only the exact text to paste into GitHub.

Keep replies on one line by default. Avoid repetitive prefixes such as `Removed. Removed ...`, `Updated. Updated ...`, or `Fixed. Fixed ...`. If the implementation note already starts with the matching action verb, omit the standalone status word and write the natural sentence instead.

Wrap code identifiers in backticks in summaries, actions, and replies. This includes function names, interface/type names, file names, variable names, config keys, question ids, API endpoints, CLI commands, and literal values.

Use one of these status words:

- `Resolved.`
- `Updated.`
- `Fixed.`
- `Noted.`
- `Removed.`
- `Improved.`

Prefer the obvious matching word. Do not add a separate status word if the sentence already says the same thing naturally.

For outdated threads that are fixed, mention the new mechanism instead of saying only "outdated".

For unresolved threads, do not draft a fake fix. State the remaining issue, `High`/`Medium`/`Low` priority, and recommended next action.

## Priority Guidance

- **High**: correctness bugs, data loss/overwrite, runtime errors, broken user flow, security/privacy exposure, invalid persisted state.
- **Medium**: architectural bloat that affects maintainability or future correctness, confusing state ownership, brittle API/payload shape, missing defensive handling.
- **Low**: nitpicks, comments/docstrings, naming, small simplifications, formatting, local readability issues.

When in doubt, prefer a higher priority for profile writes, backend payload changes, and resume/localStorage behavior.
