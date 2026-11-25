---
name: review-comment-resolution
description: "Works through reviewer comments on a pull request: applies the fixes that are right, pushes back on the ones that are not and drafts a reply to every thread."
---

# Review comment resolution

Every open thread gets exactly one outcome: fixed, answered, or questioned.

## Steps

1. Fetch the open threads. With the GitHub CLI: `gh pr view --comments` and `gh api repos/{owner}/{repo}/pulls/{n}/comments`. Include file, line, author and whether the thread is resolved. Ignore resolved threads.
2. Read the diff the comments refer to (`gh pr diff`) and the code around each line. A comment may be about a line that has since moved.
3. Sort each thread:
   - **Fix**: correct and in scope. Make the smallest change that satisfies it.
   - **Discuss**: wrong, risky or out of scope. Prepare a short reason with evidence (a test, a caller, a line of the spec).
   - **Ask**: ambiguous. Prepare one specific question.
   - **Defer**: valid but separate. Suggest a follow-up issue.
4. Apply the fixes. Group them into one commit per theme with a message such as "Address review: validate input in importer". Do not rewrite history on a shared branch.
5. Run the tests and linter for what you touched.
6. Draft the replies. Fix replies say what changed and cite the commit. Keep every reply under three sentences and polite; never defensive.

## Rules

- Do not mark threads resolved or post replies yourself. Give the drafts to the user.
- If two reviewers conflict, say so and propose one option; do not pick silently.

## Report

A table: thread (file:line), author, outcome, change or reply text. List the tests you ran.
