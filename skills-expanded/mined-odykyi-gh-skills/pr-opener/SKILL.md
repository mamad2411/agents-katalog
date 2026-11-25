---
name: pr-opener
description: |
  Creates Pull Requests with proper formatting, descriptions, and mandatory issue 
  linking. Use when the user wants to open a PR, create a pull request, push and PR, 
  or submit completed work. **REQUIRED PRE-CONDITION**: Every PR MUST have a linked 
  GitHub issue - this is enforced, never open a PR without an issue. Coordinates with 
  pr-labeler for automatic label application.
---

# PR Opener

Creates PRs with proper formatting, descriptions, and mandatory issue linking.

## Overview

**Purpose**: Open PRs that tell a complete story - what changed, why it changed, and how to verify.

**Core Principle**: Issue-first workflow. You cannot create a PR without first having a linked issue.

## When to Use

Use this skill when:
- User wants to open a PR
- Creating a pull request from a branch
- Pushing and creating PR
- Submitting completed work
- Converting work to a PR with proper formatting

## Definition of Done (DoD)

| Check | Required | Verification |
|-------|----------|--------------|
| Issue exists | ✅ Yes | Search for existing or create new |
| PR references issue | ✅ Yes | `Closes #<issue>` as a plain line in the PR body |
| Issue references PR | ✅ Yes | Comment on issue with PR link |
| Labels applied | ✅ Yes | Dispatch pr-labeler |
| Branch pushed | ✅ Yes | `git push -u origin <branch>` |

## Workflow

### Step 1: Check for Linked Issue (MANDATORY)

**Search strategies**:
```bash
# Extract task ID from branch name (supports both TASK-15 and issue-432 forms)
git branch --show-current
grep -oE "[A-Za-z]+-[0-9]+" <<< "$(git branch --show-current)" | head -1

# Search GitHub issues
gh issue list --search "$(git branch --show-current)" --state all
gh issue list --search "<TASK-ID>" --state all
```

**Decision**:
- ✅ Issue exists → Proceed to Step 2
- ❌ No issue → Create issue first (Step 1B)

### Step 2: Create Issue (If Missing)

```bash
branch=$(git branch --show-current)
task_id=$(echo "$branch" | grep -oE "[A-Za-z]+-[0-9]+" | head -1 || echo "")

if [ -n "$task_id" ]; then
  title="$task_id: ${branch//-/ }"
else
  default_branch=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||' || echo main)
  title=$(git log --oneline "origin/${default_branch}..HEAD" --reverse | head -1 | cut -d' ' -f2-)
fi

# Only apply a label that exists in this repository
label="enhancement"
if gh label list --limit 200 --json name --jq '.[].name' | grep -qx "$label"; then
  gh issue create --title "$title" --body "Created automatically for branch \`${branch}\` by pr-opener." --label "$label"
else
  gh issue create --title "$title" --body "Created automatically for branch \`${branch}\` by pr-opener."
fi
```

### Step 2.5: Push Branch (MANDATORY)

```bash
git push -u origin <branch>
```

### Step 3: Create PR with Issue Link

**PR Title Format**:
```
<type>: <Description> (Closes #<issue-number>)
```

**Examples**:
- `feat: Add Stripe payment (Closes #42)`
- `fix: Resolve 404 on settings page (Closes #73)`
- `refactor: Extract service logic (Closes #55)`

**Create PR**:
```bash
# Run from the worktree containing the branch
cd <worktree-path>
git rev-parse --abbrev-ref HEAD   # must equal <branch>

gh pr create --title "<type>: <Description> (Closes #${issue_number})" --body "
Closes #${issue_number}

## Summary
Brief description of what changed

## Implementation
- Key change 1
- Key change 2

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Definition of Done
- ✅ Issue exists and is linked
- ✅ PR references issue with 'Closes #${issue_number}'

## Related
- Issue: #${issue_number}
- Branch: ${branch}
"
```

### Step 4: Link PR to Issue

```bash
# Add PR link to issue
pr_url=$(gh pr view "$branch" --json url --jq '.url')
gh issue comment "$issue_number" --body "PR created: ${pr_url}"
```

### Step 5: Apply Labels

```bash
pr_number=$(gh pr view "$branch" --json number --jq '.number')
```

Then invoke the pr-labeler skill:

```
@pr-labeler auto-label <pr_number>
```

## Commands

### 1. Open PR

```
@pr-opener Open PR for <branch-name>
```

**Workflow**:
1. Verify/create issue
2. Push branch
3. Create PR with `Closes #N`
4. Link PR to issue
5. Apply labels via pr-labeler

### 2. Open PR with Issue

```
@pr-opener Open PR for <branch-name> with issue #<number>
```

### 3. Verify DoD

```
@pr-opener Verify DoD for PR #<number>
```

## Error Handling

### PR Already Exists

```
⚠️ PR already exists: https://github.com/.../pull/123

Checking for issue link...
❌ Missing issue link in existing PR

Action: Creating issue and updating PR...
✅ Updated PR #123 with issue link #45
```

### No Issue Found

```
❌ CANNOT PROCEED

No issue exists for this work.

Required Actions:
1. Manually create issue on GitHub
2. Re-run pr-opener with issue number
3. Or provide the issue number: @pr-opener Open PR for <branch-name> with issue #<number>
```

## Integration

**Called by**:
- The orchestrating agent (after work completion)
- pr-manager (batch operations)
- User (manual PR creation)

**Calls to**:
- issue-reporter (if issue needs tracking)
- pr-labeler (to apply labels)

**Pre-requisites**:
- Code committed
- Tests passing
- Issue exists (or will be created)

## References

This skill is self-contained. The DoD requirements are in the table above; the issue-search and label commands are in Step 1 and Step 5.
