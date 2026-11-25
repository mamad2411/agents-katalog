---
name: commit
description: Commit on a new branch with conventional message
user-invocable: false
---
## Overview

Commit changes to the repository in a new branch with proper commit message.

## Steps

1. **Prepare branch**
   - Create a new branch
   - Verify branch is up to date with main or master

2. **Write commit message**
   - Must use the conventional commit message convention.
   - Summarize changes clearly

3. **Commit changes**
   - Use a single commit for the changes
   - Commit the changes to the branch
   - Push the branch to the remote repository

## Commit Message Examples

```markdown
feat(scope): add new feature
fix(script): resolve script error
chore(script): update script dependencies
refactor(script): standardize script error handling
test(script): add comprehensive script tests
docs(script): update script documentation
```

## Guardrails

- Use the Conventional Commits convention for every message.
- Commit only when the user asks; do not push or amend without an explicit request.
- Never skip hooks; if a hook fails, fix the issue and make a new commit.
- Never print, stage, or commit secrets or credential files (.env, .env.*, keys); exclude them and warn instead.