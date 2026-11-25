---
name: work-issues
description: Automatically pick up ai-ready GitHub issues, implement them using TDD, and open draft PRs. Use when user says "work issues", "start working", "process backlog", or wants AI to autonomously implement GitHub issues.
---

# Work Issues

Pick up `ai-ready` GitHub issues and implement them autonomously, one at a time.

## Worktree Isolation

This skill MUST run in its own git worktree to avoid conflicts with other parallel Claude instances (e.g. handle-pr-feedback, review-prs).

Before starting, set up a worktree if not already in one:

```
# From the main repo clone
git worktree add ../$(basename "$PWD")-issues main
cd ../$(basename "$PWD")-issues
```

If already running inside a worktree, skip this step.

## Process

### 1. Find the next issue

```
gh issue list --label "ai-ready" --state open --json number,title,body,labels
```

Select the next issue by:
1. Skip issues labeled `ai-in-progress` or `ai-blocked`
2. Skip issues whose "Blocked by" references are still open
3. Pick the lowest-numbered eligible issue (oldest first)

If no issues are eligible, tell the user and stop.

### 2. Claim the issue

- Remove label `ai-ready`, add label `ai-in-progress`
- Comment on the issue: "Starting work on this issue."
- Create a branch: `git checkout -b issue-<number>-<short-slug>`

```
gh issue edit <number> --remove-label "ai-ready" --add-label "ai-in-progress"
gh issue comment <number> --body "Starting work on this issue."
git checkout -b issue-<number>-<short-slug>
```

### 3. Understand the issue

Read the issue body. If it references a parent PRD, read that too. Explore relevant parts of the codebase to understand current state.

If the issue is ambiguous or missing critical information:
- Label it `ai-blocked`
- Comment on the issue explaining what's unclear
- Move to the next issue

### 4. Plan

Write a brief plan as a comment on the issue:
- What you'll change
- Which behaviors you'll test
- Your TDD cycle order (RED-GREEN pairs)

Do NOT ask the user to approve - just post the plan and start.

### 5. Implement with TDD

For each behavior in your plan:

```
RED:   Write one test that captures expected behavior -> verify it fails
GREEN: Write minimal code to pass -> verify it passes
```

Rules:
- One test at a time, vertical slices
- Tests verify behavior through public interfaces, not implementation details
- Only enough code to pass the current test
- Run tests after each step to confirm RED/GREEN state
- Never refactor while RED

After all tests pass, refactor if needed. Run tests again.

### 6. Commit and push

Make clean, atomic commits as you go. Each RED-GREEN cycle can be one commit, or group logically.

```
git add -A
git commit -m "feat(#<number>): <description>"
git push -u origin issue-<number>-<short-slug>
```

### 7. Open a draft PR

```
gh pr create --draft --title "<issue title>" --body "Closes #<number>

## What was done

<brief summary of changes>

## Decisions made

<any non-obvious choices and why>

## Testing

<what tests were added and what they verify>
"
```

### 8. Update the issue

- Remove `ai-in-progress`, add `ai-done`
- Comment with a link to the PR

```
gh issue edit <number> --remove-label "ai-in-progress" --add-label "ai-done"
gh issue comment <number> --body "PR opened: <pr-url>"
```

### 9. Mark PR ready for review

Convert the draft PR to ready for review:

```
gh pr ready <number>
```

### 10. Next issue

Report: "Finished #<number>. Moving to the next issue."

Go back to step 1. If no eligible issues remain, stop.

## Safety Rails

- Open PRs as drafts first, then mark ready for review when done - never merge
- If an issue seems too large (>500 lines of changes), stop and tell the user
- If tests in the repo are failing before you start, stop and tell the user
- If you encounter a conflict with another branch, stop and tell the user
- Never force push
