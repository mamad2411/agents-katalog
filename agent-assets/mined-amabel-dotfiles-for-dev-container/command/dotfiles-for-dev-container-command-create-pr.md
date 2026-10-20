---
description: "Create a pull request with auto-generated title and description"
allowed-tools: ["Bash", "Read", "Grep", "WebFetch"]
---

Create a comprehensive pull request with auto-generated content:

1. **Pre-Check: Ensure Commits are Pushed**:
   - Check if current branch has unpushed commits using `git status` and `git log origin/HEAD..HEAD`
   - If unpushed commits exist, push them first using `git push` or `git push -u origin <branch>`
   - Verify push was successful before proceeding

2. **Branch Analysis**:
   - Get current branch name and base branch (usually main/master)
   - Run `git log origin/main..HEAD --oneline` to see commits being included
   - Run `git diff origin/main...HEAD --stat` to see file changes summary

3. **PR Title Generation**:
   - Analyze commit messages to determine overall change type
   - Generate a concise PR title following conventional format
   - Examples: "feat: add user authentication", "fix: resolve memory leak in parser"

4. **PR Description Generation**:
   - **Summary**: Brief description of what this PR accomplishes
   - **Changes**: List of key changes made
   - **Testing**: Describe testing approach or tests added
   - **Breaking Changes**: Note any breaking changes
   - **Related Issues**: Check for issue references in commits

5. **PR Creation**:
   - Use `gh pr create` to create the pull request
   - Include generated title and description
   - Set appropriate labels based on change type
   - Request reviewers if configured in settings

6. **Post-Creation**:
   - Display the PR URL
   - Suggest next steps (e.g., run CI, notify team)

Example PR template:
```
## Summary
Brief description of changes

## Changes Made
- Feature/fix 1
- Feature/fix 2

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] No breaking changes

## Related Issues
Closes #123
```