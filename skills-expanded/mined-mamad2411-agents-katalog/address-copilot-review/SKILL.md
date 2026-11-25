---
name: address-copilot-review
description: Handle GitHub Copilot PR review comments end-to-end. Use when the user asks to read Copilot's review on a pull request, decide which comments to act on, implement appropriate fixes, push follow-up commits, reply on each review thread with either the fix or the rationale for not changing code, and resolve threads that are fully addressed.
---

# Address Copilot Review

Use this skill when a user wants Copilot PR review comments handled all the way through, not just summarized.

This workflow is specifically for GitHub PR review comments from Copilot or other bot reviewers, where the expected outcome is:
- understand every review comment
- decide whether to change code
- implement and verify worthwhile fixes
- push the branch
- reply on every thread
- resolve threads that are actually addressed

## Preconditions

- `gh` must be authenticated for the repo
- the current branch should already correspond to the PR under review, or you should otherwise know the PR number
- if you make code changes, verify them before pushing

## Workflow

1. Inspect the local branch state first.

Use quick local checks like:

```bash
git status --short
git branch --show-current
git remote -v
```

2. Fetch the PR review context from GitHub.

Useful commands:

```bash
gh pr view --json number,title,url,headRefName,baseRefName,reviewDecision,reviews,comments,latestReviews
gh api repos/<owner>/<repo>/pulls/<pr-number>/comments
```

Notes:
- `gh pr view --comments` can help for a human-readable pass
- `gh api repos/.../pulls/<pr>/comments` is the reliable way to get line-level review comments
- bot overview reviews often summarize the PR but do not replace the actual review threads

3. Build a concrete action list from the review comments.

For each comment, classify it as one of:
- fix now
- no code change, but respond with rationale
- defer as follow-up work, and say so clearly

Bias toward fixing:
- correctness issues
- data safety issues
- risky behavior changes
- cleanup suggestions that are small and obviously correct

Bias toward deferring:
- large architectural refactors that materially expand the PR scope
- speculative performance work without evidence
- suggestions that are technically valid but too risky for the current fix

4. Read the actual code before deciding.

Do not trust the review comment blindly. Open the affected file, understand the current behavior, then decide.

5. Make the code changes that are worth taking.

Guidance:
- keep fixes minimal and targeted
- avoid mixing unrelated cleanup into the review-follow-up commit
- if a comment suggests a broader rewrite, prefer the smallest safe improvement that addresses the real issue

6. Add or adjust tests when the change affects behavior.

If you add new runtime or parsing logic, add focused tests when practical. Prefer targeted coverage over broad churn.

7. Verify before pushing.

Use the narrowest useful verification for the change:
- focused `xcodebuild build-for-testing` for touched tests
- targeted compile checks for app code
- broader verification only when necessary

Be explicit if environment issues block verification.

8. Commit and push the follow-up.

Typical flow:

```bash
git add <files>
git commit -m "Address Copilot PR review feedback"
git push origin <branch>
```

9. Reply to every review thread.

For each comment, post one of:
- fixed in `<commit>`
- not taking this in this PR, with concise rationale

Good reply patterns:
- "Fixed in `<sha>`. <one-sentence summary of what changed and why>"
- "I'm not taking this refactor in this PR. <brief scope/risk rationale>. <optional note about follow-up conditions>"

Useful command pattern:

```bash
gh api repos/<owner>/<repo>/pulls/<pr-number>/comments/<comment-id>/replies -f body='...'
```

10. Resolve review threads that are actually addressed.

After replying, inspect thread state and resolve threads that are done.

Useful query:

```bash
gh api graphql -f query='query { repository(owner:"<owner>", name:"<repo>") { pullRequest(number:<pr-number>) { reviewThreads(first:50) { nodes { id isResolved isOutdated comments(first:10) { nodes { id url body author { login } } } } } } } }'
```

Resolve with GraphQL:

```bash
gh api graphql -f query='mutation { resolveReviewThread(input:{threadId:"<thread-id>"}) { thread { id isResolved } } }'
```

Resolution rule:
- resolve when the code change landed or when you made an explicit final decision and replied with rationale
- do not leave addressed threads open just because no code changed
- do not resolve threads that still need follow-up in the current PR

## Decision Standards

When deciding whether to act on a Copilot comment:

- Prefer evidence over authority. Copilot can be right, partially right, or wrong.
- Preserve the intent of the PR. Avoid ballooning scope.
- Protect user data and migration safety first.
- If a comment reveals a smaller safe improvement than the one suggested, take the smaller improvement and explain that choice.

## Final Response To The User

Report back with:
- what comments were fixed
- what comments were declined and why
- what verification ran
- confirmation that replies were posted
- confirmation that addressed threads were resolved

Keep it concise, but make sure the user does not have to guess whether replies/resolutions actually happened.
