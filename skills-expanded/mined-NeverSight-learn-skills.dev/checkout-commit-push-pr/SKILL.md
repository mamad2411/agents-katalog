---
name: checkout-commit-push-pr
description: "Run the full git workflow end-to-end without prompting: create a dated branch off the default branch (if needed), stage and commit changes with a descriptive message, push to origin, open a PR (honoring any repo PR template), and monitor CI checks until they pass. Use when the user asks to commit and open a PR, ship a change, push and PR, or run the checkout-commit-push-pr flow."
---

## Complete Git Workflow

DO NOT ASK ME WHAT TO DO. Just follow the workflow below. The only exceptions: a questionable untracked file (per step 2) or a diverged local default branch (per step 1) — stop and flag those instead of guessing.

1. **Check current branch and changes**

   Do that via
   ```bash
   git status
   ```

   Examine ALL pending changes to inform our git commit/PR messages — plain `git diff`
   only shows unstaged edits to tracked files, so also check what's already staged:
   ```bash
   git diff
   git diff --staged
   ```

   For untracked files you intend to commit, read their contents — a new file IS the
   change, and no diff command shows it.

   Resolve the repo's default branch — do not assume it is `main`:
   ```bash
   # Fast and local (may error if origin/HEAD is unset on older clones)
   git symbolic-ref --short refs/remotes/origin/HEAD | sed 's|^origin/||'

   # Fallback if the above errors
   gh repo view --json defaultBranchRef -q .defaultBranchRef.name
   ```

   **If already on a non-default branch, stay on it.** Only create a new branch if
   currently on the default branch — NEVER commit or push directly to the default
   branch, whatever it's named (`main`, `master`, `develop`, ...).

   If on the default branch, create and checkout a new branch using this naming convention:
   ```
   [optional JIRA-KEY-][2-4 descriptive words]-[MMDD]
   ```

   - **JIRA-KEY** *(optional)*: when this work has a known Jira ticket, prefix the branch with its key (e.g. `RWS-24-`). This lets later tooling discover the ticket from the branch name and auto-link the PR back to it.
   - **2-4 words**: Lowercase, separated by dashes, describing the issue being fixed
   - **Date**: Today's date in MMDD format (e.g. July 12th → `0712`)

   **Examples:**
   - `fix-sqlfluff-errors-1214` (December 14th)
   - `update-dbt-models-0103` (January 3rd)
   - `RWS-24-improve-dagster-debug-skill-0527` (ticket-prefixed)

   Before branching, make sure the local default branch is up to date so the new
   branch isn't based on stale code (a stale base causes unrelated diffs and avoidable
   conflicts in the PR). Uncommitted local changes are fine — `git pull --ff-only`
   won't touch them; if it fails because the local branch has diverged, stop and flag
   it rather than rebasing or merging on your own.

   ```bash
   git pull --ff-only
   git checkout -b <new-branch-name-MMDD>
   ```

2. **Stage files deliberately and commit with a descriptive message:**

   Review what `git status` reported in step 1 before staging anything:

   - **Modified/deleted tracked files**: stage them all — that's the work being shipped.
   - **Untracked files**: stage only those that belong to the change. Do NOT stage
     files that look like secrets, local config, or scratch output (e.g. `.env*`,
     `credentials*`, `*.key`, `.DS_Store`, editor swap files, large data dumps,
     one-off debug scripts). If an untracked file is ambiguous, read it first.
   - If something questionable would be committed, stop and flag it to me instead
     of guessing.

   ```bash
   # Stage all tracked changes
   git add -u

   # Stage intended untracked files explicitly, by name
   git add <new-file-1> <new-file-2>

   # Confirm exactly what will be committed
   git status
   git diff --staged --stat

   # Commit with descriptive message, informed by the diff from step 1
   git commit -m "<Overview of the change>

   - <item 1 in the more specific bulleted list of changes>
   - ...
   "
   ```

3. **Check for PR template:**

   Before creating the PR, check if the repository has a PR template:
   ```bash
   # Check common PR template locations
   ls .github/pull_request_template.md .github/PULL_REQUEST_TEMPLATE.md PULL_REQUEST_TEMPLATE.md 2>/dev/null
   ```

   - If a template exists, read it and use its structure for the PR body
   - Fill in all required sections from the template
   - If no template exists, use the default format below

   **If a Jira ticket is known at this point** — either passed in by an orchestrator (e.g. `wrap-up-session`) or auto-detected from a `JIRA-KEY-…` branch prefix — include a `**Ticket:**` line near the top of the PR body so the PR is born linked back to the ticket:

   ```
   **Ticket:** [RWS-24](https://citizenteam.atlassian.net/browse/RWS-24)
   ```

   Insert it directly under the first heading (e.g. right under `## Description & motivation` when a template is in use). If no ticket key is known, leave this out — `atlassian-ticket-management`'s `Cross-link to PR` step will backfill it after the PR exists.

4. **Push branch and create PR:**
   ```bash
   # Push to remote
   git push -u origin <new-branch-name-MMDD>

   # Create pull request (use template structure if found, otherwise use default)
   gh pr create --title "<Descriptive PR Title>" --body "$(cat <<'EOF'
## Summary
- <what changed and why, in a few bullets>

## Changes
- <specific change 1>
- ...
EOF
)"
   ```

   Note the heredoc body and closing `EOF` start at column 0 — if they're indented,
   `EOF` won't terminate the heredoc.

   **Make sure you output a link to the PR** (`gh pr create` prints it).


5. **Monitor CI/CD Checks:**
   After creating the PR, monitor the CI/CD pipeline to ensure all checks pass:

   ```bash
   # Block until all checks complete — no manual polling needed
   # (add --fail-fast to return as soon as any check fails)
   gh pr checks <PR-NUMBER> --watch

   # View detailed information about a specific workflow run
   gh run view <RUN-ID>

   # View logs for a failed job
   gh run view --log-failed --job=<JOB-ID>
   ```

   **Important:** `gh pr checks` returns "no checks reported" with exit 1 in two different cases: (a) the repo has no workflows, or (b) workflows exist but haven't registered yet (typical 10-30s after push). Do NOT conclude "no CI configured" from that output alone.

   - First check `ls .github/workflows/` — if any files exist, CI is configured and you must wait.
   - Prefer `gh pr view <PR-NUMBER> --json statusCheckRollup` which distinguishes "no workflows" from "pending."
   - If workflows exist but checks haven't appeared, wait ~30s and re-check.

   **Goal: every required check green.** Whatever checks the repo runs — linters, builds, tests, docs validation — treat each failing required check as yours to fix.

   **Handling Check Failures:**
   - Read the failed job's logs (`gh run view --log-failed`) to find the actual error — don't guess from the check name.
   - Fix the issue locally, commit, and push to the same branch; checks re-run automatically. Repeat until green.
   - Prefer the repo's own tooling for mechanical fixes (e.g. run the formatter/linter the check runs, apply its auto-fix if it has one).
   - If a failure isn't caused by your diff (flaky test, infra error, missing prerequisite like state that must be created first), stop and flag it instead of churning commits.

   **Acceptable Skipped Checks:**
   - Production-only checks on non-production branches
   - Conditional checks that don't apply to your changes

   **When All Checks Pass:**
   - PR is ready for review and merge
   - All validations have succeeded and code quality is ensured

### Commit Message Format
- **First line**: Brief summary of changes
- **Body**: Bulleted list of specific changes made
- Do NOT append a `Co-Authored-By: Claude` trailer (or any other generated-by attribution)
