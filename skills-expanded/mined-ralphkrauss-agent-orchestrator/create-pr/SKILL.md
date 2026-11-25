---
name: create-pr
description: Create a GitHub pull request with the issue number in the title. Use when user says "create PR", "open PR", "make pull request", or after completing a plan implementation.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Create PR

Create a GitHub pull request with consistent title formatting that includes the issue number.

## Instructions

### Step 0: Verify Self-Review Has Been Run

Before creating a PR, check that `/review-pr` has been run on this branch:

1. Check if `/review-pr` was run in the current session (the user ran it earlier in this conversation)
2. If not, warn: *"Self-review has not been run. Run `/review-pr` first to catch issues before PR creation?"*
3. If the user confirms to skip, proceed — but note "Self-review skipped" in the PR description
4. If the user ran `/review-pr` and there are unresolved Critical findings, warn: *"/review-pr found N unresolved critical findings. Resolve them before creating a PR, or proceed anyway?"*

This is advisory, not blocking — the user can always override.

### Step 1: Determine Issue Number and Branch

1. Get the current branch: `git branch --show-current`
2. If the branch name starts with a number (e.g., `50-archive-dynamodb-event-store`), extract it as the issue number.
3. If no issue number is detected, ask the user for it.

### Step 2: Build PR Title

**Format: `#{issue-number} {Short description}`** — the issue number MUST be the very first thing in the title. No exceptions.

Rules:
- Issue number comes first, prefixed with `#`
- Single space after the number — no colon, no dash
- Description starts with a capital letter
- No conventional-commit prefixes (`feat:`, `fix:`, `chore:`, etc.)

**Correct examples:**
- `#50 Archive DynamoDB event store`
- `#14 Localization infrastructure`
- `#148 Allow custom page size in the DataTable`

**Do NOT use these formats:**
- `#50: Title` — no colon after the issue number
- `feat: Title (#50)` — no conventional-commit prefix, no issue number at end
- `fix: resolve something` — missing issue number entirely
- `#50 implement thing` — must capitalize first word of description

Derive the short description from:
- The plan file at `plans/{branch-name}/plan.md` (use the feature title)
- The GitHub issue title: fetch the issue details using the available GitHub tools (owner, repo, issue_number) and extract the title from the result
- Or ask the user

### Step 3: Build PR Body

Use the plan file to construct the body:

```markdown
## Summary

- Bullet point summary of what was implemented (2-5 bullets)

## Issue

Closes #{issue-number}

## Test Plan

- [ ] Verification steps or test commands run
```

If a plan exists, derive the summary from the completed tasks in the Implementation Tasks table.

### Step 4: Push and Create

1. Push the branch:

```bash
git push -u origin HEAD
```

2. Create the pull request using the available GitHub tools with:
   - `owner`: repository owner
   - `repo`: repository name
   - `title`: `"#{issue-number} {description}"`
   - `head`: current branch name
   - `base`: `"main"`
   - `body`: the PR body from Step 3

### Step 5: Return the PR URL

Display the PR URL to the user when done.

## Critical Rules

- **Title format is `#{number} {Description}`** -- issue number first, no colon, no prefix, capitalized description. This is non-negotiable.
- **Comment prefix** -- if adding PR comments, prefix with `**[Claude Code]:**`
- **Don't force-push** -- use regular `git push`
