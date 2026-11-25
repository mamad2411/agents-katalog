---
name: pr-create
description: Create a PR and request initial review
uses:
  - development/git
requires:
  tools: [git, gh]
---

# PR Create

## When to Use

After code is committed and pushed, create a pull request and request review.

## Prerequisites

- Code committed to feature branch
- Branch pushed to remote
- Tests passing locally

## Steps

### 1. Verify Ready State

```bash
# Confirm on feature branch
git branch --show-current
# Should NOT be main/master

# Confirm clean working directory
git status
# Should show nothing to commit

# Confirm pushed
git log origin/<branch>..HEAD
# Should be empty (all commits pushed)
```

### 2. Check What Will Be in PR

```bash
# See commits
git log main..HEAD --oneline

# See diff
git diff main...HEAD --stat
```

### 3. Create PR

```bash
gh pr create --title "<type>(scope): description" --body "$(cat <<'EOF'
## Summary
- What this PR does
- Why it's needed

## Changes
- List of changes

## Test Plan
- How to test

## Linked Issues
Closes #<issue_number>

---
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

Title format: `type(scope): short description`
- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation
- `refactor`: code refactor
- `test`: tests
- `style`: formatting

### 4. Request Review

```bash
# For Gemini
gh pr comment <PR_NUMBER> --body "@gemini-code-assist review"

# For Copilot (structured prompt for thorough review)
gh pr comment <PR_NUMBER> --body '@copilot Please review this PR with **inline comments only**...'
```

### 5. Record PR Number

Note the PR number for:
- Tracking in coordinator
- Referencing in commits
- Linking in issues

## Completion Checklist

- [ ] PR created with descriptive title and body
- [ ] Linked to issue(s)
- [ ] Review requested
- [ ] PR number noted
