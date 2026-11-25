---
name: commit-same-branch
description: Commit on the current branch with conventional message
user-invocable: false
---
## Overview

Commit changes to the same branch with proper commit message.

## Steps

1. **Write commit message**
   - Must use the conventional commit message convention.
   - Summarize changes clearly

2. **Commit changes**
   - Use a single commit for the changes
   - Commit the changes to the branch
   - Push the changes to the remote repository

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

- Commit only when the user asks; do not commit unrequested work.
- Do not push unless asked; keep commits local until the user requests a push.
- Use the Conventional Commits convention for every message.
- Before staging, review `git status`, `git diff`, and recent `git log`; write the commit message with a HEREDOC and stay on the current branch (do not create a new branch).
- Never print, stage, or commit secrets or credential files (.env, .env.*, keys); exclude them and warn instead.