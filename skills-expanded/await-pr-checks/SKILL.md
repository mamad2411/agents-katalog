---
name: await-pr-checks
description: Monitor PR checks, wait for completion, auto-fix test failures, and report back. Use when user says "wait for checks", "monitor CI", "watch PR", "await checks", or wants to know when CI passes.
---

# Await PR Checks

Monitor a pull request's CI checks, wait for them to complete, automatically fix test failures, and report back when everything passes (or when manual intervention is needed).

## Instructions

### Step 1: Identify the PR

1. If user provides a PR number or URL, use it.
2. Otherwise, detect from current branch: get the branch name with `git branch --show-current`, then list open pull requests using the available GitHub tools (owner, repo, head branch, state: open) to find the matching PR number.

### Step 2: Poll Check Status

Run a polling loop: fetch the PR check run status using GitHub tools (owner, repo, pullNumber).

Interpret the results (evaluate in this order):
- **Checks still running**: wait 30 seconds and poll again
- **Any check fails**: go to Step 3 (diagnose and fix)
- **Bugbot check is `skipped`**: go to Step 2b (Bugbot found issues)
- **All CI checks pass**: call `get_review_comments` to check for CodeRabbit inline comments. If found, go to Step 2c (CodeRabbit found issues). Otherwise, go to Step 5 (report success)

### Step 2b: Handle Bugbot Results

Bugbot uses a non-standard status convention:
- **`success`** = Bugbot finished and found **no bugs** — treat as a normal passing check
- **`skipped`** = Bugbot finished and found **bugs** — it has posted review comments on the PR that need resolution

When Bugbot's status is `skipped`:

1. Report to the user:
   ```
   Bugbot found issues on PR #<number> (status: skipped).
   Transitioning to /resolve-pr-comments to address Bugbot's review comments.
   ```
2. **Wait for all other checks to finish first.** If other checks are still running or have failures, handle those (Steps 3-4) before moving to Bugbot comments. Bugbot comments are code review feedback, not CI failures — they're resolved differently.
3. Once all other checks are resolved (passed or reported), invoke the `/resolve-pr-comments` skill to process Bugbot's comments through the standard one-by-one approval flow.
4. After resolving Bugbot's comments and pushing fixes, return to Step 2 to monitor the new CI run (Bugbot will re-run on the new commits).

### Step 2c: Handle CodeRabbit Results

CodeRabbit posts AI code review comments on PRs. It may also set a check status (named `coderabbitai` or similar) to indicate that a review was performed.

CodeRabbit's review status alone is **not a pass/fail gate** — with `request_changes_workflow: false` in `.coderabbit.yaml`, it only posts comments without blocking the PR. The value is in the review comments themselves.

**Wait for all CI checks to pass first.** If checks are still running or have failures, handle those (Steps 3-4) before processing CodeRabbit comments. CodeRabbit comments are code review feedback, not CI failures — they're resolved differently.

Once all CI checks pass:

1. Fetch the PR review comments using the available GitHub tools (owner, repo, pullNumber). Filter for comments from the `coderabbitai` user (or users ending in `[bot]` with "coderabbit" in the name).
2. If CodeRabbit posted review comments with actionable findings:
   ```
   CodeRabbit posted review comments on PR #<number>.
   Transitioning to /resolve-pr-comments to address CodeRabbit's review comments.
   ```
3. Invoke the `/resolve-pr-comments` skill to process CodeRabbit's comments through the standard one-by-one approval flow.
4. After resolving comments and pushing fixes, return to Step 2 to monitor the new CI run.

If CodeRabbit posted only a summary comment (no inline code review comments), report it as informational and continue — no action needed.

### Step 3: Diagnose Failures

For each failed check:

1. Get the failed check's details from the `get_check_runs` output (name, status, conclusion, details URL)
2. Fetch the build/test logs. The check runs response includes check run details and URLs. For detailed CI failure logs, follow the check run URL in the GitHub UI or run the GitHub CLI command `gh run view <run-id> --log-failed` if available.
3. Parse the log output to identify:
   - **Build errors**: compilation failures, missing references
   - **Test failures**: which tests failed and why (assertion messages, exceptions)
   - **Infrastructure failures**: timeout, OOM, flaky network — these are NOT auto-fixable

### Step 4: Auto-Fix and Retry

**For build errors and test failures:**

1. Read the relevant source files identified in the error output
2. Fix the issue (compilation error, broken test assertion, missing import, etc.)
3. Build locally to verify, using the project's standard build command
4. If tests failed, run them locally using the project's standard test command
5. Do NOT commit or push automatically — leave fixes in the working tree and tell the user: "CI fix applied locally. Run `/commit` and push when ready, then I'll continue monitoring."
6. Once the user has committed and pushed, return to Step 2 to monitor the new run

**For infrastructure/flaky failures:**

Do NOT attempt to fix. Report to the user:
```
Check "<name>" failed due to infrastructure issues (not a code problem).
You may want to re-run it manually: <check URL>
```

**Retry limit:** After 3 fix cycles without all checks passing, stop and report to the user. Do not loop indefinitely.

### Step 5: Report Results

When all checks pass:

```
All CI checks passed on PR #<number>:
- <check 1>: passed
- <check 2>: passed
- ...

<If fixes were applied:>
Fixes applied:
- <commit hash>: <description>
```

When stopping due to retry limit or unfixable failures:

```
CI checks on PR #<number> need attention:
- <check 1>: passed
- <check 2>: FAILED — <reason>

<what was tried and why it couldn't be auto-fixed>
```

### Step 5b: Knowledge Capture — Rule Check

1. Check if any CI failure patterns fixed during this workflow are not covered by existing `.agents/rules/` files
2. Search existing rules by keyword and concept to avoid duplicates
3. If a reusable pattern was found, suggest `/create-rule`. Provide:
   - The pattern (rule text)
   - The anti-pattern (the bad code or violation, with example)
   - The evidence (source: CI failure auto-fix, what was discovered)
   - Suggested context tags (e.g., `ci`, `build`, `test`, `infrastructure`)

**Do NOT write rule files directly** — `/create-rule` handles dedup, ID assignment, index update, and source tracking.

Skip this step if no new patterns were discovered.

## Critical Rules

- **Max 3 fix attempts** — do not loop forever. After 3 fix cycles, report and stop.
- **Never fix infrastructure failures** — timeouts, OOM, rate limits, and flaky network issues require manual re-run, not code changes.
- **Always build/test locally before committing** — don't commit blind fixes.
- **Don't change test expectations to make tests pass** — fix the code under test, not the test assertions (unless the test itself is genuinely wrong).
- **Commit messages must describe what was fixed** — not just "fix CI".
- **Bugbot `skipped` ≠ success** — Bugbot reports `skipped` when it finds bugs. Only `success` means no issues. When Bugbot is `skipped`, transition to `/resolve-pr-comments` to address its review comments before declaring all checks green.
- **Bugbot comments go through `/resolve-pr-comments`** — do NOT attempt to auto-fix Bugbot findings like CI failures. They are code review feedback and must be processed through the standard comment resolution flow with user approval.
- **CodeRabbit comments go through `/resolve-pr-comments`** — CodeRabbit is an AI code reviewer that posts inline review comments. Its check status (if present) is informational, not a CI gate. After CI checks pass, check for CodeRabbit review comments and process them through `/resolve-pr-comments` like Bugbot comments.
- **CodeRabbit summary comments are informational** — CodeRabbit posts a high-level summary comment (walkthrough) on each PR. This is not actionable — only process its inline code review comments through `/resolve-pr-comments`.
