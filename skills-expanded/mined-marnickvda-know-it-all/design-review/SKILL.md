---
name: design-review
description: Use after quiz-me on a pull request, or when the user wants to comment on a PR's design decisions and rollout risks one comment at a time. Design-level, not code-level: tradeoffs, failure modes, third-party defaults, docs that disagree with behavior, rollout and rollback. Triggers include "design review on PR #123", "turn the quiz into review comments", "comment on the design of this PR with me".
---

# Design Review

Walk the user through design-level review comments on a PR, **one comment per message**, then post the approved ones as **one** GitHub review. The user approves every word; nothing goes to GitHub before they pick the review type.

**Short choices** end the message as a numbered plain-text list, after the content; then stop. The user replies with a number or in their own words. Every message here carries content above its choice, so it all stays in the message text: a question-tool popup can hide the text before it.

**In scope:** design decisions, rollout and rollback risks, failure modes, third-party defaults the code relies on, docs or comments that disagree with real behavior. **Out of scope:** code-level bugs, style, tests, naming. A code-level bug is a comment only when it makes behavior contradict the docs or PR description; then frame it as a question about that mismatch, not a fix. Otherwise mention it to the user in one line and move on.

## 1. Gather

Run inside a local clone of the PR's repo. No number given: `gh pr view --json number` finds the PR of the current branch. Get the quiz results, richest first:
- **This conversation** — quiz-me on this PR just ran: use its answer key, grades, gaps, parked questions.
- **Handoff file** — `<git common dir>/quiz-me/pr-<n>.md` (`git rev-parse --path-format=absolute --git-common-dir`). Compare its `## PR` head SHA with `gh pr view <n> --json headRefOid`. **If they differ, stop:** tell the user both SHAs and ask whether to use the notes anyway, re-check them, or ignore them. Wait for the answer.
- **Neither** — build the answer key yourself (step 2), without quizzing the user.

Then read the PR: `gh pr view <n>` (description), `gh pr view <n> --comments` (existing review comments), `gh pr diff <n>`, and the **full changed files** at the head (`git fetch origin pull/<n>/head`, `git show <sha>:<path>`).

## 2. Checked claims only

Every claim a comment rests on must be checked against its source before you draft it: library defaults at the pinned version (read the source in the module cache or at that tag; options left unset *are* those defaults), chart values, API specs, the full files around the diff. Your memory is not a source. Quote the value and where you read it (e.g. "HTTP client v2.3.1 `client.go`: retries 3"). A handoff line tagged `[unchecked]` counts as unchecked. Can't check it? Drop the claim, or turn the comment into a question.

## 3. Find candidates

Sources: quiz gaps and parked questions that are real questions for the author; design or rollout risks found while checking; docs, comments or the PR description that disagree with behavior. Always ask: *how is this switched off or rolled back if it misbehaves in production?* If neither the PR nor its config answers that, it is a `PR-wide` candidate.

- **Already covered?** If the PR description or an existing comment already states the point, drop it or narrow it to what is new. Tell the user which, and quote the line that covers it.
- **Anchor** each comment on a changed line (right side of the diff); GitHub rejects others. A point about the PR as a whole (rollback, rollout plan, missing kill switch) or about unchanged code is **`PR-wide`**: it goes in the review body, never inline.

## 4. Overview, then one comment at a time

First message, all in one: one line on what you checked (sources), any dropped or narrowed points with why, then the overview table, then comment 1.

| # | Where | Topic |
|---|-------|-------|
| 1 | `queue/worker.go:52` | Docs say at-most-once; code retries |
| 2 | `PR-wide` | No way to switch the new cache off without a deploy |

After that, each comment gets **its own message**, in exactly this shape:

````
**Comment 2 of 4 · cache/cache.go:41 · rollout risk**

```diff
@@ -30,6 +38,9 @@ func New(cfg Config) *Cache {
 	c := &Cache{ttl: cfg.TTL}
+	c.client = redis.NewClient(&redis.Options{Addr: cfg.Addr})   ◀ comment here
 	return c
```

<1–2 sentences: why this matters.>

1. **Drafted:** > <the full comment>
2. **Shorter:** > <one sentence>
3. **Different angle or place:** > <e.g. a question instead, or move to the review body>
````

Then offer a short choice: **Drafted**, **Shorter**, **Different angle**, **Skip**. The user can also write their own.

Copy the hunk header and context lines from `gh pr diff`. Mark the commented line(s). For a range, mark each line. **`PR-wide` comments:** header says `PR-wide`, no diff block, and say it goes in the review body. Then stop and wait.

**Pushback** ("isn't this overengineering?", "do you agree?"): give your honest view in a few sentences and a clear recommendation. Recommend skip when the comment doesn't earn its place; hold your ground when it does. Neither cave nor insist by reflex.

## 5. Comment style

Short, plain language, one point per comment. Prefix nits with `nit:`. Mark non-blocking points `(non-blocking)`. Unsure? Ask a question, don't state an opinion as fact.

## 6. Review type, post, verify

After the last comment, list the approved comments, each review type's drafted summary body (PR-wide comments go in it), then offer a short choice: **Comment**, **Approve**, or **Request changes**. Post nothing until the user picks.

Then post **one** review. Build the payload in a file (a script or a heredoc into a `.json` file), never inline shell quoting:

```json
{"commit_id": "<head SHA>", "event": "COMMENT", "body": "<summary + PR-wide comments>",
 "comments": [{"path": "queue/worker.go", "line": 52, "side": "RIGHT", "body": "..."},
              {"path": "cache/cache.go", "start_line": 39, "start_side": "RIGHT", "line": 41, "side": "RIGHT", "body": "..."}]}
```

`gh api repos/<owner>/<repo>/pulls/<n>/reviews --method POST --input review.json`. `event` is `COMMENT`, `APPROVE` or `REQUEST_CHANGES`.

**Verify:** `gh api repos/<owner>/<repo>/pulls/<n>/comments --paginate --jq '.[] | select(.pull_request_review_id == <review id>) | "\(.path):\(.line)"'` (the per-review comments endpoint returns `line: null`; don't use it). Report a table: intended `path:line` vs posted `path:line`, ✓ or ✗, then the review URL. Fix any ✗ with the user.

**Clean up:** if a handoff file was used, offer to delete it. Delete the payload file.
