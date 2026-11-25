---
name: structured-pr-reviewer
description: >-
  Certainty-scored pull request reviews with reasoning and final ratings.
  Use when reviewing a PR, branch diff, or when the user asks for a PR review.
argument-hint: <pr-url | base-branch>
---

# Structured PR review

Follow the steps below in order. Every finding uses **Finding format**; the review ends with **Rating format**.

## Finding format

Every finding carries:

- **Certainty** (0–100%): 0–33% preference, 34–66% plausible issue, 67–100% likely real problem
- **Reasoning**: one sentence — why it matters and what to do
- **Code snippet**: when a concrete fix or example helps

## Rating format

- **Code Quality**: [1–10] — one-sentence justification
- **Testing Coverage**: [1–10] — one-sentence justification
- **Readability**: [1–10] — one-sentence justification
- **Overall**: [1–10]
- One paragraph: strengths and improvements

## Steps

### 1. Gather

- **PR URL:** run `<skill-dir>/scripts/gather-pr <pr-url>`. One call prints metadata, files, commits, existing reviews and inline comments, CI checks, and a worktree at the PR head. Read code and run tests in that worktree. Re-run it to re-review after new commits.
- **Local branch:** follow [`GATHER.md`](GATHER.md) with the base branch the user gives.

**Done when:** full diff obtained; every changed file is in review scope; commit history reviewed; existing comments read so findings don't repeat them.

### 2. Context

State the PR goal in one sentence from the description, linked issues, and diff.

When the change spans multiple components or async flows, add a mermaid sequence diagram for the primary change path.

**Done when:** goal stated; primary change path identified (diagram when the branch applies).

### 3. Analyze

Review every modified file with non-trivial logic. Check correctness, edge cases, readability (only where it affects comprehension of the change), security, performance, and UI consistency — each only when the change touches that concern.

Prioritize high-impact issues. For complex logic, briefly explain what it does before critiquing it.

Over 800 changed lines (`gather-pr` flags it): split the files by area and give each area to a subagent with the worktree path and **Finding format**. Check every finding you keep against the code yourself.

Report each issue in **Finding format**, ordered by impact.

**Done when:** every modified file with non-trivial logic is checked; each concern area that applies has been considered.

### 4. Alternatives

Only when the approach is non-obvious or you see a clearly better design:

- Describe the current approach.
- Propose one alternative with trade-offs.
- State the winner.

Report in **Finding format** with a code snippet when feasible.

**Done when:** skipped if neither condition applies; otherwise current vs alternative compared and winner stated.

### 5. Testing

Map every behaviour change to a test (existing or missing). Note whether tests pass when you can verify.

Missing tests are findings in **Finding format**.

**Done when:** every behaviour change has a test mapping; gaps listed.

### 6. Lint

Only when the user provides a lint or static-analysis tool: run it on the changes and report results in **Finding format**.

**Done when:** skipped if no tool provided; otherwise tool output reported.

### 7. Save drafts

PR reviews only. Before reporting, write every finding that has a line to the drafts file `gather-pr` printed, so the drafts survive compaction. Use the GitHub create-review body:

```json
{"commit_id": "<head sha from gather-pr>", "event": "COMMENT",
 "body": "summary",
 "comments": [{"path": "src/a.ts", "line": 42, "body": "…"},
              {"path": "src/b.ts", "start_line": 10, "line": 14, "body": "…"}]}
```

Run `<skill-dir>/scripts/post-review <pr-url> --dry-run`; fix any anchor it marks `BAD`.

**Done when:** every finding with a line is in the file; the dry run passes.

### 8. Rate

Produce **Rating format**.

**Done when:** all four scores assigned with justifications; strengths and improvements summarized.

## Posting

Only after the user confirms which comments to post and the review event. Edit the drafts file to that set, then run `<skill-dir>/scripts/post-review <pr-url>`. It refuses to post if the PR head moved past `commit_id` or an anchor falls outside the diff, then reads the posted anchors back. Finish with `gather-pr <pr-url> --cleanup`.
