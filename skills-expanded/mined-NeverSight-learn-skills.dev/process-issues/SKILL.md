---
name: process-issues
description: Autonomous loop that picks up ai-ready GitHub issues, handles PR feedback, and asks clarifying questions when blocked. Use when user says "work issues", "start working", "process backlog", or wants AI to autonomously implement GitHub issues.
---

# Process Issues

Autonomous loop that picks up `ai-ready` issues, implements them via the `code-implementation` skill, and handles feedback on open PRs.

## Comment Authorship

All comments posted by this workflow run under the same GitHub account as the user. To distinguish AI comments from human comments, **every comment posted by AI MUST start with `**[AI]**`**. When reading comments, use this rule:
- Starts with `**[AI]**` → posted by AI (previous runs)
- Does NOT start with `**[AI]**` → posted by a human

## Worktree Isolation

This skill MUST run in its own git worktree to avoid conflicts with other parallel Claude instances.

Before starting, check if already in a worktree:

```
git rev-parse --show-toplevel
```

If NOT already in a worktree for this skill, create one and switch to it using the `EnterWorktree` tool (if available). If `EnterWorktree` is not available, create one manually and prefix ALL subsequent commands with `cd <worktree-path> &&`:

```
WORKTREE=$(git rev-parse --show-toplevel)/../$(basename "$(git rev-parse --show-toplevel)")-issues
git worktree add "$WORKTREE" main 2>/dev/null || true
```

Then for every command in this skill, prefix with:
```
cd $WORKTREE && <command>
```

This is necessary because `cd` does not persist between Bash calls.

## Loop Cycle

Each cycle runs through three phases in order:

0. **Pre-flight checks** — verify the environment is ready
1. **Handle feedback** on existing PRs
2. **Implement** the next available issue

---

## Phase 0: Pre-flight Checks

Run these before every cycle. If any fail, stop and report the problem.

```
# Clean up stale worktrees (from previous crashed runs)
git worktree prune

# Check gh is authenticated
gh auth status

# Check working tree is clean (no uncommitted changes)
git status --porcelain
```

If `git status --porcelain` produces output, stop: "Working tree is dirty. Commit or stash changes before running."

If `gh auth status` fails, stop: "GitHub CLI is not authenticated. Run `gh auth login`."

Ensure required labels exist (run once per cycle — `gh label create` is a no-op if the label already exists):

```
for label in ai-ready ai-in-progress ai-done ai-blocked ai-needs-input needs-ai-review ai-changes-requested ai-approved prd; do
  gh label create "$label" 2>/dev/null || true
done
```

Check for the `ai-pause` label — this is the graceful stop signal. The mechanism: **create** the `ai-pause` label to pause, **delete** it (`gh label delete ai-pause -y`) to resume.

```
gh label list --search "ai-pause" --json name
```

If the `ai-pause` label exists, stop: "ai-pause label detected. Stopping gracefully. Delete the label (`gh label delete ai-pause -y`) to resume."

---

## Phase A: Handle PR Feedback

### A1. Find PRs needing attention

Process up to 3 PRs per cycle to avoid spending the entire session on feedback. If more remain, they'll be handled in the next cycle.

First, check for PRs labeled `ai-changes-requested` — this is the primary signal:

```
gh pr list --author "@me" --state open --label "ai-changes-requested" --json number,title,url
```

Also check for unlabeled PRs that may have feedback:

```
gh pr list --author "@me" --state open --json number,title,url,isDraft,labels
```

For each PR without an `ai-changes-requested`, `needs-ai-review`, or `ai-approved` label, read the comments:

```
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
gh pr view <number> --comments
gh api repos/$REPO/pulls/<number>/comments
```

Read the actual comment contents and determine if there is unaddressed human feedback. Human comments are those that do NOT start with `**[AI]**` — look for review comments requesting changes, questions from reviewers, or suggestions that haven't been acted on yet.

Also check for recently rejected PRs (closed without merging) and reset their linked issues. Limit to 10 most recent to avoid scanning the entire history:

```
gh pr list --author "@me" --state closed --limit 10 --json number,title,mergedAt,body,closedAt
```

For each closed PR where `mergedAt` is empty (not merged), extract the issue number from the body (`Closes #<number>`). Before resetting, verify the issue still has the `ai-done` label and hasn't been manually reassigned or relabeled by a human:

```
gh issue view <number> --json labels,assignees --jq '.labels[].name' | grep -q "ai-done"
```

Only if the issue is still labeled `ai-done` and has no human assignee:

```
gh issue edit <number> --remove-label "ai-done" --add-label "ai-ready"
gh issue comment <number> --body "**[AI]** PR #<pr-number> was closed without merging. Resetting to ai-ready for a fresh attempt."
```

Skip if the issue was already relabeled (e.g., a human moved it to `ai-blocked` or removed `ai-done`) — that means someone handled it manually.

If no PRs need attention, skip to Phase B.

### A2. Address feedback

For each PR needing attention:

```
gh pr checkout <number>
```

Read the review comments (reuse `$REPO` from A1):

```
gh pr view <number> --comments
gh api repos/$REPO/pulls/<number>/comments
```

Categorize each new comment:
- **Fix**: concrete change requested — use the `code-implementation` skill to make the changes
- **Question**: reviewer wants clarification — reply with an answer; if it reveals a needed change, make it
- **Nit**: style/preference — apply if reasonable, group into one commit

Commit fixes:

```
git commit -m "fix(#<issue>): address review - <brief description>"
git push
```

Post a summary and update labels:

```
gh pr comment <number> --body "$(cat <<'EOF'
**[AI]** Addressed review feedback:
- <what was fixed>

Ready for another look.
EOF
)"
```

Update the PR label to request a new review (this also ensures previously unlabeled PRs enter the label workflow):

```
gh pr edit <number> --remove-label "ai-changes-requested" --add-label "needs-ai-review"
```

Clean up before continuing — return to main and ensure a clean state:

```
git checkout main
git pull origin main
git status --porcelain
```

If the working tree is dirty after checkout, stash or resolve before proceeding.

---

## Phase B: Implement Next Issue

### B0. Recover stale issues

Check for issues stuck in `ai-in-progress` from a previous crashed run:

```
gh issue list --label "ai-in-progress" --state open --limit 100 --json number,title
```

For each one, check if there's an active branch (local or remote) or open PR:

```
LOCAL_BRANCH=$(git branch --list "issue-<number>-*" | head -1 | xargs)
REMOTE_BRANCH=$(git ls-remote --heads origin "issue-<number>-*" 2>/dev/null | head -1 | awk '{print $2}' | sed 's|refs/heads/||')
OPEN_PR=$(gh pr list --author "@me" --state open --json number,headRefName --jq ".[] | select(.headRefName | startswith(\"issue-<number>-\")) | .number")
```

- If an open PR exists, the work was partially done — skip it (it will be handled when someone reviews it or closes it)
- If a branch exists (local or remote) but no PR, the work started but wasn't finished — skip it (leave for manual inspection)
- If no branch and no PR exist, the issue was claimed but never worked on — reset it:

```
gh issue edit <number> --remove-label "ai-in-progress" --add-label "ai-ready"
gh issue comment <number> --body "**[AI]** Resetting to ai-ready — previous work session was interrupted before any progress was made."
```

### B1. Find the next issue

```
gh issue list --label "ai-ready" --state open --limit 100 --json number,title,body,labels
```

Also check for previously blocked issues that now have answers:

```
gh issue list --label "ai-blocked" --state open --limit 100 --json number,title,body,labels
```

For each `ai-blocked` issue, determine why it's blocked and whether it's been unblocked:

**Dependency-blocked** (has a `## Blocked by` section with issue references):
Check if all referenced blocking issues are now closed:

```
gh issue view <blocking-number> --json state --jq '.state'
```

If all blockers are closed, the issue is unblocked — relabel it to `ai-ready`:

```
gh issue edit <number> --remove-label "ai-blocked" --add-label "ai-ready"
gh issue comment <number> --body "**[AI]** All blocking issues are now closed. Moving to ai-ready."
```

Then treat it as eligible in the current cycle.

**Question-blocked** (AI posted a question via `**[AI]** I have a question`):
Read the comments to see if a human has replied. Human comments are those that do NOT start with `**[AI]**`. If a human comment exists after the last AI question, treat the issue as eligible again.

**Failure-blocked** (AI posted a failure message like "Implementation failed", "too large", "Merge conflict"):
Only treat as eligible if a human has commented since the failure (indicating they've addressed the underlying problem). Otherwise leave it blocked.

Selection order:
1. Unblocked `ai-blocked` issues with answered questions (priority first, then oldest)
2. `ai-ready` issues not labeled `ai-in-progress` (priority first, then oldest)
3. Skip issues whose "Blocked by" references are still open

Priority: if an issue has a `priority:high` or `priority:critical` label, pick it before lower-priority or unlabeled issues.

**Persistent failure guard:** Before selecting an `ai-ready` issue, scan its comments for previous `**[AI]**` failure messages (e.g., "Implementation failed", "too large", "Merge conflict"). If the same issue has been attempted and failed 2+ times without new human input in between, skip it — it likely needs human intervention even though it's labeled `ai-ready`. Leave it for the next cycle or until a human comments.

If no issues are eligible, report "No issues to work on" and stop.

### B2. Claim the issue

Sync main before branching to avoid working on stale code:

```
git checkout main
git pull origin main
```

Then claim and create the branch. Check for an existing branch first (the slug may differ from what you'd generate):

```
gh issue edit <number> --remove-label "ai-ready" --add-label "ai-in-progress"
gh issue comment <number> --body "**[AI]** Starting work on this issue."
EXISTING=$(git branch --list "issue-<number>-*" | head -1 | xargs)
if [ -n "$EXISTING" ]; then
  git checkout "$EXISTING"
else
  git checkout -b issue-<number>-<short-slug>
fi
```

For previously `ai-blocked` issues:

```
gh issue edit <number> --remove-label "ai-blocked" --add-label "ai-in-progress"
gh issue comment <number> --body "**[AI]** Question answered. Resuming work."
EXISTING=$(git branch --list "issue-<number>-*" | head -1 | xargs)
if [ -n "$EXISTING" ]; then
  git checkout "$EXISTING"
else
  git checkout -b issue-<number>-<short-slug>
fi
```

### B3. Understand the issue

Read the issue body. If it references a parent PRD, read that too. Explore relevant parts of the codebase.

**If the issue is unclear or missing critical information:**

- Comment on the issue with a specific question:

```
gh issue comment <number> --body "$(cat <<'EOF'
**[AI]** I have a question before I can proceed:

<specific question about what's unclear>

Labeling as `ai-blocked` — I'll pick this up again once answered.
EOF
)"
```

- Label it `ai-blocked`, remove `ai-in-progress`:

```
gh issue edit <number> --remove-label "ai-in-progress" --add-label "ai-blocked"
```

- Return to main before moving on:

```
git checkout main
```

- **Move to the next issue** (go back to B1)

### B4. Implement

Use the `code-implementation` skill to implement the issue. Pass it the issue body as the task description and `#<number>` as the commit reference.

If `code-implementation` fails for any reason, clean up and move on. The common failure modes and their responses:

**Too large (>500 lines):**
```
gh issue comment <number> --body "**[AI]** This issue looks too large for autonomous implementation. Consider breaking it into smaller issues."
gh issue edit <number> --remove-label "ai-in-progress" --add-label "ai-blocked"
git checkout main
```

**Merge conflict:**
```
gh issue comment <number> --body "**[AI]** Merge conflict with main. Leaving for manual resolution."
gh issue edit <number> --remove-label "ai-in-progress" --add-label "ai-blocked"
git checkout main
```

**Existing tests failing (before any changes were made):**
```
gh issue comment <number> --body "**[AI]** Existing test suite is failing before any changes. Skipping until the test suite is green."
gh issue edit <number> --remove-label "ai-in-progress" --add-label "ai-blocked"
git checkout main
```

**Any other failure** (push rejected, ambiguous requirements the skill couldn't resolve, unexpected errors):
```
gh issue comment <number> --body "**[AI]** Implementation failed: <brief description of what went wrong>. Leaving for manual investigation."
gh issue edit <number> --remove-label "ai-in-progress" --add-label "ai-blocked"
git checkout main
```

The key invariant: **never leave an issue labeled `ai-in-progress` after a failure**. Always move it to `ai-blocked` with a comment explaining what happened, then return to main.

Move to the next issue.

### B5. Open a draft PR

First check if a PR already exists for this branch (e.g., from a previous crashed run):

```
EXISTING_PR=$(gh pr list --author "@me" --state open --head "$(git branch --show-current)" --json number --jq '.[0].number')
```

If a PR already exists, skip creation and use that PR number. Otherwise create one:

```
gh pr create --draft --title "<issue title>" --body "$(cat <<'EOF'
Closes #<number>

## What was done

<brief summary of changes>

## Decisions made

<any non-obvious choices and why>

## Testing

<what tests were added and what they verify>
EOF
)"
```

If `gh pr create` fails (e.g., no commits ahead of main, permission error), treat it as an implementation failure — clean up labels and move on:

```
gh issue comment <number> --body "**[AI]** Implementation completed but PR creation failed: <error>. Branch `<branch-name>` has the changes."
gh issue edit <number> --remove-label "ai-in-progress" --add-label "ai-blocked"
git checkout main
```

### B6. Update the issue

```
gh issue edit <number> --remove-label "ai-in-progress" --add-label "ai-done"
gh issue comment <number> --body "**[AI]** PR opened: <pr-url>"
```

### B7. Wait for CI (non-blocking)

Check if the repo has CI checks configured:

```
gh pr checks <pr-number> --json name,state,bucket
```

If no checks are configured, skip straight to marking the PR ready for review.

If checks are running, check once after a short wait (10-15 seconds), then check once more. Don't poll in a tight loop — if checks aren't done after 2 checks, move on. The PR stays as a draft and CI status will be picked up in a later cycle.

```
gh pr checks <pr-number> --json name,state,bucket
```

If checks pass, proceed to B8.

If checks fail, attempt to fix (up to 2 attempts per cycle):
1. Read the failure logs: `gh run view <run-id> --log-failed`
2. Fix the issue, commit, and push
3. Check once more after a brief wait

If checks still fail after 2 attempts, leave the PR as draft and comment:

```
gh pr comment <pr-number> --body "**[AI]** CI is failing after fix attempts. Leaving as draft for investigation."
```

Move to the next issue.

### B8. Mark PR ready for review

Only mark ready after CI passes (or if the repo has no CI checks):

```
gh pr ready <pr-number>
gh pr edit <pr-number> --add-label "needs-ai-review"
```

### B9. Next issue

Return to main so the branch is free for other worktrees (e.g., `process-reviews`):

```
git checkout main
```

Report: "Finished #<number>. Moving to next cycle."

Go back to the top of the loop (Phase A).

---

## Usage with /loop

```
/loop 10m /process-issues
```

## Safety Rails

- Open PRs as drafts first, then mark ready for review — never merge
- If an issue seems too large (>500 lines of changes), stop and tell the user
- If tests in the repo are failing before you start, stop and tell the user
- If you encounter a conflict with another branch, stop and tell the user
- Never force push
- When blocked, always ask a specific question — never guess
- If a `gh` command fails with HTTP 403 or "rate limit exceeded", stop the current cycle and report: "GitHub API rate limit hit. Wait before retrying." Do not retry immediately.
