---
name: gh-review-comment-evaluator
description: Evaluate GitHub pull request review comments and decide whether they should be fixed. Use when the user provides a GitHub pull request URL and asks to inspect review comments, summarize actionable feedback, judge whether each comment is must-fix or optional, check whether feedback is already resolved, or decide what to implement next. If the user wants to apply fixes, create an implementation plan before making code changes and follow the target repository instructions.
---

# gh-review-comment-evaluator

Accept a GitHub pull request URL. Inspect the review discussion with GitHub CLI first, then use GitHub MCP only when CLI output is unavailable or incomplete.

Do not change code while evaluating comments. First, decide which comments matter and explain why.

## Workflow

### 1. Parse the pull request URL

Extract:

- owner
- repo
- pull request number

If the URL is not a GitHub pull request URL, stop and ask for the correct URL.

### 2. Gather pull request context

Prefer GitHub CLI. Use the smallest set of reads that gives enough context.

Recommended GitHub CLI reads:

- `gh pr view <url> --json number,title,state,isDraft,reviewDecision,files,reviews`
- `gh api repos/<owner>/<repo>/pulls/<number>/comments`
- `gh api repos/<owner>/<repo>/pulls/<number>/reviews`
- `gh api repos/<owner>/<repo>/issues/<number>/comments`
- `gh api graphql` when review thread IDs, resolution state, or thread operations are needed

Use GitHub MCP only when GitHub CLI is unavailable or when CLI output is missing the needed thread detail.

Recommended GitHub MCP fallback reads:

- `pull_request_read(method="get")`
- `pull_request_read(method="get_review_comments")`
- `pull_request_read(method="get_reviews")`
- `pull_request_read(method="get_files")`
- `pull_request_read(method="get_comments")`

When needed, inspect the current diff or local branch so the comment is judged against the latest code rather than only the original review snapshot.

### 3. Evaluate each comment

Classify each review comment into one of these buckets:

- `must-fix`: likely blocks approval, correctness, broken behavior, missing tests for required behavior, security, compatibility, or clear repository-rule violation
- `optional`: reasonable improvement, naming preference, cleanup, or style suggestion that does not appear blocking
- `already-resolved`: the latest code or discussion already addresses the concern, or the thread is resolved and no longer applies
- `clarification-needed`: the request is ambiguous, conflicts with other guidance, or needs more product or architectural context

Use these heuristics:

- Treat comments from unresolved review threads as higher priority than resolved threads.
- Give more weight to correctness, regression risk, API contract, accessibility, security, and test coverage than to taste.
- Check whether the reviewer explicitly requested changes or only suggested an alternative.
- Check whether later commits, later comments, or force-pushes already addressed the point.
- Avoid calling something `already-resolved` unless the current diff or discussion clearly supports that conclusion.
- If the comment depends on repository conventions, inspect the local repository instructions before deciding.

### 4. Handle already-resolved threads

When a thread is classified as `already-resolved`, do not stop at the label. Check whether the thread already contains a clear note that the issue was resolved.

Treat these as already documented:

- a maintainer or author reply that explicitly says the issue was fixed or resolved
- a later comment that points to the fixing commit or updated implementation
- a thread that is already resolved and whose final reply already explains that the issue was addressed

If a clear resolution note already exists, leave the thread as-is.

If the issue is resolved in code but the thread does not yet say so:

1. Reply in the thread with a short note that the issue is already resolved.
2. Mention the current evidence, such as the updated file, latest diff, or commit.
3. Resolve the review thread after replying.

Prefer GitHub CLI for both actions.

CLI patterns:

- Reply to a review comment with `gh api repos/<owner>/<repo>/pulls/<number>/comments -f body='<reply>' -F in_reply_to=<comment_id>`
- Fetch review thread IDs and resolution state with `gh api graphql`
- Resolve a thread with `gh api graphql` and the `resolveReviewThread` mutation using the thread ID

Use GitHub MCP only if CLI access is blocked and the MCP tool can provide the missing operation.

Format the reply like this:

- Write the main resolution sentence as normal text, not as a quote.
- Write the main sentence in Japanese and English on one line as `日本語 / English`.
- Add a separate Markdown quote line underneath that explicitly says the note is AI-generated.

Example:

```md
最新の変更でこの指摘は解消されています。このスレッドを resolve します。 / This issue has already been resolved in the latest changes, so I’m resolving this thread.

> AIによるコメントです。 / This comment was generated by AI.
```

Do not post the reply if the same conclusion is already written in the thread.

### 5. Summarize the evaluation

Return a concise summary with:

- overall recommendation for the pull request
- grouped comments by bucket
- per-comment rationale with file path or thread context when available
- a short list of the changes worth making now
- open questions that block confident action

Use direct language. Distinguish facts from inference.

Suggested structure:

```text
PR summary
- ...

Must-fix
- <comment summary> — <reason>

Optional
- <comment summary> — <reason>

Already resolved
- <comment summary> — <reason>

Clarification needed
- <comment summary> — <reason>
```

### 6. Decide whether to implement

After summarizing the evaluation, ask whether the user wants to apply the must-fix items and any selected optional items.

Do not begin implementation just because a fix seems obvious.

### 7. If the user wants fixes, plan before editing

Before changing code:

1. Inspect repository instructions such as `AGENTS.md`, contribution docs, or local workflow rules.
2. Create an implementation plan.
3. If the repository uses a planning location such as `.cursor/plans/`, write the plan there.
4. Share the plan with the user.
5. Wait for approval when repository rules require approval before code changes.
6. Only then implement the selected fixes.

After implementation, run the repository-required validation commands and report the result.

## Evaluation standards

Prefer fixing comments that are:

- tied to incorrect behavior
- likely to fail tests or review gates
- repeated by multiple reviewers
- aligned with existing patterns in the repository
- cheap to fix with low regression risk

Usually leave as optional comments that are:

- purely stylistic with no established project rule
- subjective refactors outside the pull request scope
- superseded by a stronger reviewer decision
- better handled in a follow-up pull request

## Guardrails

- Do not invent missing review context.
- Do not assume an unresolved thread is valid without checking the latest code.
- Do not implement fixes in the same step as evaluation unless the user explicitly asks and planning requirements are satisfied.
- Do not ignore repository-specific instructions when moving from evaluation to implementation.
