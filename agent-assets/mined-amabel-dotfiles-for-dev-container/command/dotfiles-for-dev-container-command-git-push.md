---
description: "Safely push changes with pre-push validation"
allowed-tools: ["Bash", "Read", "Grep", "LS"]
---

Perform a safe git push with comprehensive pre-push validation:

1. **Branch Status Check**:
   - Run `git status` to ensure working directory is clean
   - Check current branch name and upstream tracking
   - Verify no uncommitted changes exist

2. **Pre-push Validation**:
   - Run `git log --oneline -5` to show recent commits
   - Check if pushing to protected branches (main/master)
   - Validate commit messages follow conventional format
   - Look for merge conflicts or unresolved issues

3. **Code Quality Checks** (if applicable):
   - Check for common linting commands (npm run lint, ruff, etc.)
   - Run tests if test script exists (npm test, pytest, go test, etc.)
   - Verify build succeeds if build script exists

4. **Security Scan**:
   - Scan for potential secrets or sensitive data in commits
   - Check for large files that shouldn't be committed
   - Validate no debug code or console.log statements

5. **Push Execution**:
   - Show what will be pushed (`git log origin/branch..HEAD`)
   - Ask for confirmation before pushing
   - Execute `git push` or `git push -u origin branch` if first time

If any validation fails, explain the issue and suggest fixes before pushing.