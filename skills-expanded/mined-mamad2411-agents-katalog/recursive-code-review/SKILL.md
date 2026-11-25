---
name: recursive-code-review
description: Review the current GitHub pull request with the code-review skill, manage the long-running loop with a Codex goal, fix reported CRITICAL and HIGH findings, run focused tests, commit and push the fixes, and repeat until no CRITICAL or HIGH findings remain. Use when asked to autonomously resolve severe PR review findings through repeated review-fix-commit-push cycles while allowing MEDIUM and LOW findings to remain.
---

# Recursive Code Review

Resolve severe findings on the current pull request through repeated review and repair cycles.

## Workflow

1. Create a Codex goal for the full recursive review task before making changes. The goal is always: `Continue reviewing, fixing, committing, and pushing the current PR until the latest docs/reviews/codereview_PR<PR number>_<yyyyMMdd>.md report has zero CRITICAL and zero HIGH findings. Verify each severe finding before editing, make the smallest coherent fix, run focused checks, commit the fix, push the branch, and re-review. Preserve unrelated user changes, never force-push, and if blocked, report the blocker, evidence gathered, remaining severe findings, and the input needed to continue`. Do not set a token budget unless the user explicitly requested one.
2. Read the repository's `AGENTS.md`, `CLAUDE.md`, and relevant local instructions.
3. Inspect `git status --short --branch` and record pre-existing changes. Never discard, overwrite, stage, or commit unrelated user changes.
4. Run `gh pr view --json number,title,url,headRefName,baseRefName` to identify the pull request for the current branch.
5. Verify that the checked-out branch is the PR head branch. Stop and explain the mismatch instead of modifying another branch.
6. Repeat the review and repair cycle until the completion condition is met.

## Goal Handling

- Keep the Codex goal active for the entire review-fix-review loop, including across continuations or context compaction.
- Before each resumed cycle, check the current goal and continue from the last known PR state instead of restarting from scratch.
- Mark the goal complete only after the latest review report has zero CRITICAL and zero HIGH findings, required verification passed, and any repair commits were pushed.
- Mark the goal blocked only when the same stop condition has repeated for at least three consecutive goal turns and no meaningful progress remains possible without user input or an external-state change.
- When marking a budgeted goal complete, include the final token usage reported by the goal tool in the completion report.

## Review And Repair Cycle

1. Invoke the `code-review` skill for the current PR.
2. Locate its report at `docs/reviews/codereview_PR<PR number>_<yyyyMMdd>.md`.
3. Confirm that the report contains all four severity sections: `CRITICAL`, `HIGH`, `MEDIUM`, and `LOW`. Treat a missing or malformed section as an invalid review, not as zero findings.
4. Count actual review comments under `CRITICAL` and `HIGH`. Ignore headings, explanatory placeholder text, and empty sections.
5. Finish when both severe sections contain zero findings. MEDIUM and LOW findings do not block completion.
6. For every CRITICAL and HIGH finding:
   - Verify the finding against the current code before editing.
   - Fix the root cause with the smallest coherent change.
   - Follow repository instructions and existing implementation patterns.
   - Add or update focused tests when behavior changes or a regression test is practical.
   - Do not fix MEDIUM or LOW findings unless required to implement a severe fix correctly.
7. Run the narrowest relevant formatter, static checks, and tests for the files changed in this cycle.
8. If verification fails, diagnose and repair the failure before committing. Never commit or push known failing code.
9. Inspect the diff and stage only files changed for the severe findings plus the generated review report. Preserve unrelated changes.
10. Create a non-amended commit that summarizes the severe fixes. Do not rewrite existing commits.
11. Push the current branch with a normal `git push`. Never force-push.
12. Re-run the cycle against the updated PR head.

## Commit Rules

- Create one commit per completed repair cycle unless repository instructions require a different structure.
- Use a concise imperative commit subject describing the fixes.
- Include tests and their corresponding production changes in the same commit.
- Do not create an empty commit when a review has no CRITICAL or HIGH findings.
- Do not stage an entire dirty worktree with `git add .` or `git add -A`.
- Do not stage any `docs/reviews/codereview_PR<PR number>_<yyyyMMdd>.md` file.

## Stop Conditions

Stop without claiming completion when:

- No pull request exists for the current branch.
- Authentication, repository permissions, or branch protection prevents required operations.
- The PR branch does not match the checked-out branch.
- A severe finding cannot be fixed without missing product or technical decisions.
- Required verification cannot be made to pass after investigation.
- The same severe finding persists because the requested behavior conflicts with repository requirements.

Keep the Codex goal active if meaningful progress can continue. If the same blocker satisfies the Goal Handling blocked criteria, mark the goal blocked and report the exact blocker, the remaining severe findings, tests run, commits created, and push status.

## Completion Report

When CRITICAL and HIGH findings are both zero, report:

- PR number and URL
- Number of completed repair cycles
- Commits pushed
- Verification commands and outcomes
- Remaining MEDIUM and LOW counts
- Final review report path
