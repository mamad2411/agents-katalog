---
name: pr-create
description: Creates a pull request from the current branch with a generated title and description
argument-hint: [base-branch]
user-invocable: true
allowed-tools: Bash(git *) Bash(gh *)
effort: low
---

## Create Pull Request

1. Gather context:
```bash
git branch --show-current
git log main..HEAD --oneline --no-merges 2>/dev/null || git log master..HEAD --oneline --no-merges
git diff main..HEAD --stat 2>/dev/null || git diff master..HEAD --stat
```

2. Generate PR title and body from the commits and diff.

Title format: `type: short description` (Conventional Commits style, max 72 chars)

Body template:
```markdown
## Summary
- 

## Changes
- 

## Testing
- [ ] Tests added/updated
- [ ] Manually tested

## Related Issues
Closes #
```

3. Show the draft to the user and ask for confirmation or edits.

4. On confirmation:
```bash
gh pr create --title "..." --body "..." --base "${1:-main}"
```

Base branch defaults to main (or $1 if provided).
