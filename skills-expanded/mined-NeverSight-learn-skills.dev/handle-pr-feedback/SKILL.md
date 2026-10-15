---
name: handle-pr-feedback
description: Read PR review comments and push fixes in response. Use when user says "handle feedback", "fix PR comments", "address review", or wants AI to respond to pull request review feedback.
---

# Handle PR Feedback

Read review comments on a draft PR and push fixes.

## Worktree Isolation

This skill MUST run in its own git worktree to avoid conflicts with other parallel Claude instances (e.g. work-issues, review-prs).

Before starting, set up a worktree if not already in one:

```
# From the main repo clone
git worktree add ../$(basename "$PWD")-feedback main
cd ../$(basename "$PWD")-feedback
```

If already running inside a worktree, skip this step.

## Process

### 1. Get the PR

Ask for the PR number, or if the user doesn't provide one:

```
gh pr list --author "@me" --state open --draft --json number,title,url
```

Show the list and ask which one to work on, or pick the one with unresolved reviews.

### 2. Read the feedback

```
gh pr view <number> --comments
gh api repos/{owner}/{repo}/pulls/<number>/reviews
gh api repos/{owner}/{repo}/pulls/<number>/comments
```

Categorize each comment:
- **Fix**: concrete change requested
- **Question**: reviewer wants clarification
- **Nit**: style/preference suggestion
- **Approval**: positive feedback, no action needed

### 3. Check out the branch

```
gh pr checkout <number>
```

### 4. Address feedback

For each **Fix** comment:
- Make the requested change
- Run tests to verify nothing breaks
- Commit with message: `fix(#<issue>): address review - <brief description>`

For each **Question** comment:
- Reply on the PR with an answer
- If the answer reveals a needed code change, make it

For each **Nit** comment:
- Apply if reasonable, skip if it conflicts with project conventions
- Group nit fixes into a single commit

### 5. Push and update

```
git push
```

Reply on the PR summarizing what was addressed:

```
gh pr comment <number> --body "$(cat <<'EOF'
<!-- feedback-addressed -->
Addressed review feedback:
- <fix 1>
- <fix 2>
- Replied to questions about <topic>
- Applied nits: <list>

Ready for another look.
EOF
)"
```

### 6. Report

Tell the user what was done and link to the PR.
