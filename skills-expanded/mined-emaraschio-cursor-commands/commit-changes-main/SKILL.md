---
name: commit-changes-main
description: Commit directly on main/master when explicitly allowed
user-invocable: false
---
## Overview

Commit changes to the main branch of a GitHub repository with proper commit message.

## Steps

1. **Prepare branch**
   - Ensure all changes are committed to the correct branch using the conventional commit message convention
   - Push changes to remote
   - Verify changes are up to date with main

2. **Write commit message**
   - Must use the conventional commit message convention.
   - Summarize changes clearly

3. **Commit changes**
   - Use a single commit for the changes
   - Commit the changes to the main branch
   - Push the main branch to the remote repository

## Commit Message Examples

```markdown
feat: add new feature
fix: fix bug
chore: update dependencies
refactor: refactor code
test: add tests
docs: update documentation
```

## Guardrails

- Commit to main only with explicit consent; otherwise move the work to a separate branch.
- Never force-push main or any shared branch; reconcile with a normal pull or merge instead.
- Use the Conventional Commits convention for every message.
- Never print, stage, or commit secrets or credential files (.env, .env.*, keys); exclude them and warn instead.