---
name: process-reviews
description: Autonomous loop that finds PRs needing AI review and delegates to the code-review skill. Use when user says "review PRs", "start reviewing", "check for PRs to review", "process reviews", or wants AI to continuously monitor and review PRs.
---

# Process Reviews

Autonomous loop that finds PRs ready for review, delegates each to the `code-review` skill, and updates labels based on the result. A human always makes the final merge decision.

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
WORKTREE=$(git rev-parse --show-toplevel)/../$(basename "$(git rev-parse --show-toplevel)")-reviews
git worktree add "$WORKTREE" main 2>/dev/null || true
```

Then for every command in this skill, prefix with:
```
cd $WORKTREE && <command>
```

This is necessary because `cd` does not persist between Bash calls.

## Loop Cycle

Each cycle:

0. **Pre-flight checks** — verify the environment is ready
1. **Find PRs** needing review
2. **Review** each PR (delegate to `code-review`)
3. **Update labels** based on the verdict
4. **Report** what was reviewed

---

## Phase 0: Pre-flight Checks

Run these before every cycle. If any fail, stop and report the problem.

```
# Clean up stale worktrees
git worktree prune

# Check gh is authenticated
gh auth status

# Check working tree is clean
git status --porcelain
```

If `git status --porcelain` produces output, stop: "Working tree is dirty. Commit or stash changes before running."

If `gh auth status` fails, stop: "GitHub CLI is not authenticated. Run `gh auth login`."

Ensure required labels exist:

```
for label in ai-ready ai-in-progress ai-done ai-blocked ai-needs-input needs-ai-review ai-changes-requested ai-approved prd; do
  gh label create "$label" --force 2>/dev/null || true
done
```

Check for the `ai-pause` label — **create** it to pause, **delete** it (`gh label delete ai-pause -y`) to resume:

```
gh label list --search "ai-pause" --json name
```

If the `ai-pause` label exists, stop: "ai-pause label detected. Stopping gracefully. Delete the label (`gh label delete ai-pause -y`) to resume."

Set up the repo variable for API calls used later:

```
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
```

---

## Phase 1: Find PRs needing review

Process up to 5 PRs per cycle. If more remain, they'll be handled in the next cycle. Collect candidates from all sources below, deduplicate by PR number, then take the first 5.

### Labeled PRs (primary signal)

```
gh pr list --state open --label "needs-ai-review" --json number,title,url,isDraft,author --limit 100
```

Skip any draft PRs. Re-check draft status at review time as well — a PR could be converted to draft between detection and review.

### Stale `ai-approved` PRs (new commits since approval)

PRs labeled `ai-approved` need re-review if new commits were pushed after the approval. Check for these to avoid a blind spot where post-approval changes go unreviewed:

```
gh pr list --state open --label "ai-approved" --json number,title,url,isDraft,author,updatedAt --limit 50
```

For each non-draft `ai-approved` PR, compare the latest commit date against the last `**[AI]**` review comment date:

```
# Get last commit date
gh pr view <number> --json commits --jq '.commits[-1].committedDate'

# Get last AI review comment date
gh api repos/$REPO/pulls/<number>/comments --jq '[.[] | select(.body | startswith("**[AI]**")) | .created_at] | sort | last'
```

If the last commit is newer than the last AI review, the PR needs re-review. Remove the stale label:

```
gh pr edit <number> --remove-label "ai-approved" --add-label "needs-ai-review"
```

### Unlabeled PRs (fallback detection)

Only check up to 15 unlabeled PRs per cycle to avoid excessive API calls:

```
gh pr list --state open --json number,title,url,isDraft,author,labels --limit 50
```

Filter to non-draft PRs without an `ai-changes-requested`, `needs-ai-review`, or `ai-approved` label. Take the first 15 after filtering, then for each, read comments:

```
gh pr view <number> --json comments
```

A PR needs review if:
- It has no `**[AI]**` review comments at all (needs first review)
- It has previous AI review feedback AND new commits were pushed after the last AI review (needs re-review)

To determine if new commits exist since the last AI review, compare dates:

```
# Last AI review comment timestamp
gh pr view <number> --json comments --jq '[.comments[] | select(.body | startswith("**[AI]**")) | .createdAt] | sort | last'

# Last commit timestamp
gh pr view <number> --json commits --jq '.commits[-1].committedDate'
```

Skip PRs where the last AI review found no issues and no new commits exist since.

### Determine review type

For each PR needing review, determine if this is:
- **First review** — no previous `**[AI]**` review comments exist
- **Re-review** — previous AI feedback exists, but feedback was addressed (new commits pushed, or human replied)

---

## Phase 2: Review each PR

For each PR needing review:

### Checkout the PR branch

The `code-review` skill needs to read source files (not just diffs) to understand the full context of changes. Checkout the PR branch so file reads reflect the PR's state, including newly added files:

```
gh pr checkout <number> --detach
```

Re-check that the PR is not a draft (it could have been converted since Phase 1):

```
gh pr view <number> --json isDraft --jq '.isDraft'
```

If it's now a draft, skip it — checkout main and move to the next PR.

### Delegate to code-review

Pass to the `code-review` skill:
- The PR number
- Whether this is a first review or re-review

The `code-review` skill will:
- Read the diff and surrounding context
- Check the linked issue
- Analyze for bugs, security, performance, style, tests, issue alignment
- Post inline review comments
- Return a verdict: **approve** or **request-changes**

If `code-review` fails or returns no verdict (e.g., it encounters an error), log the issue and skip to the next PR — don't update labels. The PR will be picked up again in the next cycle.

### Return to main

After each review (success or failure), return to main before processing the next PR:

```
git checkout main
```

---

## Phase 3: Update labels

Based on the verdict from `code-review`:

### If verdict is `request-changes`:

```
gh pr edit <number> --remove-label "needs-ai-review" --add-label "ai-changes-requested"
```

### If verdict is `approve`:

```
gh pr edit <number> --remove-label "needs-ai-review" --remove-label "ai-changes-requested" --add-label "ai-approved"
```

The `ai-approved` label signals that the AI review found no issues. A human reviewer should still verify and make the final merge decision — the AI never merges or formally approves PRs.

---

## Phase 4: Report

After reviewing all PRs in this cycle, report a summary:

```
Reviewed N PRs:
- #123 "Add user auth" → ai-changes-requested (1 bug, 2 suggestions)
- #456 "Fix pagination" → ai-approved (no issues)
```

Then loop back to Phase 0 for the next cycle.

---

## Usage with /loop

```
/loop 10m /process-reviews
```

## Safety Rails

- Never merge PRs — only post review comments and update labels
- Never use `APPROVE` or `REQUEST_CHANGES` GitHub review events — only `COMMENT`
- Skip draft PRs (check at detection AND before review — status can change between phases)
- Human always makes the final merge decision
- The `ai-approved` label means "AI found no issues" — not "approved to merge"
- If a `gh` command fails with HTTP 403 or "rate limit exceeded", stop the current cycle and report: "GitHub API rate limit hit. Wait before retrying." Do not retry immediately.
