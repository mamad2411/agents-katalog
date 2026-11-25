---
name: review-pr
description: Process and resolve PR review comments systematically
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
disable-model-invocation: true
argument-hint: "[PR_NUMBER]"
---

# Review PR Comments

Systematically process and resolve PR review comments.

## Instructions

### 1. Fetch PR Comments

```bash
# Get PR number from argument or prompt
PR_NUMBER={{PR_NUMBER}}

# Fetch review comments
gh pr view $PR_NUMBER --json reviews,comments

# Fetch inline code comments
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/comments
```

### 2. Categorize Comments

Group comments by priority:

| Category | Action | Examples |
|----------|--------|----------|
| **Bug/Security** | Must fix | Security vulnerability, logic error |
| **Performance** | Should fix | Inefficient algorithm, N+1 query |
| **Best Practice** | Should fix | Error handling, logging |
| **Nitpick** | Optional | Style, naming preference |
| **Question** | Respond | Clarification needed |

### 3. Process Each Comment

For each comment:

1. **Read the comment** - Understand what's being requested
2. **Locate the code** - Find the file and line mentioned
3. **Evaluate the suggestion** - Is it valid? Does it improve the code?
4. **Implement fix** - If valid, make the change
5. **Add test** - If a bug was found, add a test
6. **Respond** - Reply to the comment explaining the fix

### 4. Resolution Template

For each comment, document:

```markdown
### Comment: [summary]
**File**: `path/to/file.py:line`
**Reviewer**: [name]
**Category**: Bug/Security/Performance/Best Practice/Nitpick/Question

**Requested Change**: [what was asked]

**Resolution**:
- [ ] Implemented fix
- [ ] Added test
- [ ] Responded to comment

**Commit**: [commit hash if applicable]
```

### 5. Validate Fixes

After addressing comments:

```bash
# Run linting
ruff check . && ruff format --check .

# Run tests
pytest

# Verify PR still builds
```

### 6. Push and Respond

```bash
# Commit fixes
git add -A
git commit -m "fix: address PR review comments"

# Push
git push

# Post summary comment on PR
gh pr comment $PR_NUMBER --body "Addressed review comments:
- [x] Fixed [issue 1]
- [x] Fixed [issue 2]
- [x] Responded to questions"
```

## Output

Produce a resolution summary:

```markdown
## PR Review Resolution Summary

**PR**: #[number]
**Total Comments**: [N]
**Resolved**: [M]
**Deferred**: [K] (with reasons)

### Changes Made
- [Change 1]
- [Change 2]

### Commits
- [hash] [message]

### Outstanding Items
- [Item needing follow-up]
```
