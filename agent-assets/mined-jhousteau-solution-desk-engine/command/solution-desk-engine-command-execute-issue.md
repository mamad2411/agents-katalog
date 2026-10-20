---
name: execute-issue
description: Complete GitHub issue implementation workflow from analysis to pull request
arguments:
  - name: issue_number
    description: GitHub issue number to implement
    required: true
---

<role>
You are the issue implementation coordinator. Your task is to fully implement GitHub issue from analysis through pull request creation, following Genesis best practices and ensuring AI-safe development.
</role>

<purpose>
This command automates the complete issue implementation workflow:
- Fetches and analyzes the GitHub issue
- Creates an appropriate sparse worktree for AI-safe development
- Guides implementation with proper planning
- Ensures quality through testing and validation
- Creates a properly linked pull request
- Prepares for post-merge cleanup

This ensures consistent, high-quality issue implementation with proper tracking.
</purpose>

<parameters>
**Required**: Issue number (e.g., `123`)

The issue must:
- Exist in the current repository
- Be in OPEN state
- Have clear requirements or description
</parameters>

<procedure>

## 1. **Issue Analysis & Validation**
```bash
# Validate issue exists and is open
ISSUE_NUMBER=${1}
ISSUE_STATE=$(gh issue view $ISSUE_NUMBER --json state -q .state 2>/dev/null)

if [ "$ISSUE_STATE" != "OPEN" ]; then
    echo "❌ Issue #$ISSUE_NUMBER is not open or doesn't exist"
    exit 1
fi

# Fetch complete issue details
gh issue view $ISSUE_NUMBER --json title,body,labels,assignees,milestone

# Extract key information
ISSUE_TITLE=$(gh issue view $ISSUE_NUMBER --json title -q .title)
ISSUE_BODY=$(gh issue view $ISSUE_NUMBER --json body -q .body)
ISSUE_LABELS=$(gh issue view $ISSUE_NUMBER --json labels -q '.labels[].name' | tr '\n' ',')

# Determine issue type from labels or title
if echo "$ISSUE_LABELS" | grep -q "bug"; then
    ISSUE_TYPE="fix"
elif echo "$ISSUE_LABELS" | grep -q "enhancement\|feature"; then
    ISSUE_TYPE="feat"
elif echo "$ISSUE_LABELS" | grep -q "documentation"; then
    ISSUE_TYPE="docs"
elif echo "$ISSUE_TITLE" | grep -iq "fix\|bug\|error"; then
    ISSUE_TYPE="fix"
elif echo "$ISSUE_TITLE" | grep -iq "add\|implement\|create"; then
    ISSUE_TYPE="feat"
else
    ISSUE_TYPE="chore"
fi

echo "📋 Issue #$ISSUE_NUMBER: $ISSUE_TITLE"
echo "🏷️  Type: $ISSUE_TYPE"
echo "🎯 Labels: $ISSUE_LABELS"
```

## 2. **Branch & Worktree Creation**
```bash
# Create branch name
SANITIZED_TITLE=$(echo "$ISSUE_TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//' | cut -c1-40)
BRANCH_NAME="${ISSUE_TYPE}-${ISSUE_NUMBER}-${SANITIZED_TITLE}"

echo "🌿 Creating branch: $BRANCH_NAME"

# Analyze issue to determine focus paths
FOCUS_PATHS=""

# Look for file references in issue body
if echo "$ISSUE_BODY" | grep -q "genesis/"; then
    FOCUS_PATHS="genesis/"
elif echo "$ISSUE_BODY" | grep -q "bootstrap"; then
    FOCUS_PATHS="bootstrap/"
elif echo "$ISSUE_BODY" | grep -q "smart-commit"; then
    FOCUS_PATHS="smart-commit/"
elif echo "$ISSUE_BODY" | grep -q "template"; then
    FOCUS_PATHS="templates/"
elif echo "$ISSUE_BODY" | grep -q "test"; then
    FOCUS_PATHS="tests/ testing/"
elif echo "$ISSUE_BODY" | grep -q "doc"; then
    FOCUS_PATHS="docs/"
fi

# Create sparse worktree with appropriate focus
if [ -n "$FOCUS_PATHS" ]; then
    genesis worktree create $BRANCH_NAME --focus $FOCUS_PATHS --max-files 30
else
    # No specific path identified, include core areas
    genesis worktree create $BRANCH_NAME --focus genesis/ --focus tests/ --max-files 30
fi

# Navigate to worktree
cd ../${BRANCH_NAME}-worktree || cd ../${BRANCH_NAME}
```

## 3. **Implementation Planning**
Use TodoWrite to create structured implementation plan:

```python
# Create implementation tasks based on issue type
tasks = []

if ISSUE_TYPE == "fix":
    tasks = [
        "Reproduce the bug",
        "Identify root cause",
        "Implement fix",
        "Add regression test",
        "Verify fix resolves issue"
    ]
elif ISSUE_TYPE == "feat":
    tasks = [
        "Design feature architecture",
        "Implement core functionality",
        "Add unit tests",
        "Update documentation",
        "Add integration tests"
    ]
elif ISSUE_TYPE == "docs":
    tasks = [
        "Identify documentation gaps",
        "Update/create documentation",
        "Add code examples",
        "Verify accuracy",
        "Check cross-references"
    ]

# Use TodoWrite tool to track these tasks
```

## 4. **Implementation Checklist**

### For Bug Fixes:
- [ ] Bug reproduced locally
- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Regression test added
- [ ] All existing tests pass
- [ ] No new issues introduced

### For Features:
- [ ] Feature requirements clear
- [ ] Implementation follows patterns
- [ ] Unit tests written
- [ ] Documentation updated
- [ ] Integration tests added
- [ ] Performance acceptable

### For Documentation:
- [ ] Content accurate
- [ ] Examples working
- [ ] Links valid
- [ ] Formatting consistent
- [ ] Grammar/spelling checked

## 5. **Quality Validation**
```bash
echo "🧪 Running quality checks..."

# Run tests
make test || {
    echo "❌ Tests failed - fix before continuing"
    exit 1
}

# Run autofix
genesis autofix

# Validate project structure
make validate || true

# Check for common issues
echo "Checking for common issues..."
grep -r "TODO\|FIXME\|XXX" --include="*.py" --include="*.js" --include="*.ts" . || true
```

## 6. **Commit & Pull Request**
```bash
# Stage all changes
git add -A

# Review changes
echo "📝 Changes to be committed:"
git diff --staged --stat

# Create commit with issue reference
COMMIT_MSG="${ISSUE_TYPE}: ${ISSUE_TITLE}

Implements the requirements from issue #${ISSUE_NUMBER}.

Resolves #${ISSUE_NUMBER}"

genesis commit -m "$COMMIT_MSG"

# Push branch
git push -u origin $BRANCH_NAME

# Create pull request
PR_BODY="## Summary
Implements #${ISSUE_NUMBER}: ${ISSUE_TITLE}

## Changes
- [Describe key changes]

## Testing
- [ ] All tests pass
- [ ] Manual testing completed
- [ ] No regressions identified

## Issue Resolution
Resolves #${ISSUE_NUMBER}"

gh pr create \
    --title "${ISSUE_TYPE}: ${ISSUE_TITLE} (#${ISSUE_NUMBER})" \
    --body "$PR_BODY" \
    --assignee @me

# Get PR number
PR_NUMBER=$(gh pr list --head $BRANCH_NAME --json number -q '.[0].number')

# Link PR to issue (if not auto-linked)
gh issue comment $ISSUE_NUMBER --body "🔗 Pull request created: #$PR_NUMBER"

echo "✅ PR #$PR_NUMBER created and linked to issue #$ISSUE_NUMBER"
```

## 7. **Post-Implementation**
```bash
echo "
=== Next Steps ===

1. 👀 Request review: gh pr view --web
2. 🔄 Address feedback if needed
3. ✅ Merge when approved
4. 🧹 Run cleanup after merge: /pr-merged $BRANCH_NAME

Current status:
- Issue: #$ISSUE_NUMBER
- Branch: $BRANCH_NAME
- PR: #$PR_NUMBER
"
```
</procedure>

<best-practices>
## Implementation Guidelines

### 1. **Issue Analysis**
- Read the ENTIRE issue including comments
- Identify acceptance criteria explicitly
- Clarify ambiguities before starting
- Check for linked issues or dependencies

### 2. **Worktree Strategy**
- Use minimal focus paths for faster operations
- Include test directories when modifying code
- Keep under 30 files for AI safety
- Add documentation paths for feature work

### 3. **Commit Standards**
- Reference issue number in commit message
- Use conventional commit format
- Include "Resolves #XXX" for auto-closing
- Keep commits focused and atomic

### 4. **Pull Request Quality**
- Link to issue with "Resolves #XXX"
- Include test plan in PR description
- Add screenshots for UI changes
- List breaking changes prominently

### 5. **Testing Requirements**
- All existing tests must pass
- New features need new tests
- Bug fixes need regression tests
- Documentation changes need validation
</best-practices>

<error-handling>
## Common Issues & Solutions

### Issue Not Found
```bash
if ! gh issue view $ISSUE_NUMBER &>/dev/null; then
    echo "Issue #$ISSUE_NUMBER not found. Verify:"
    echo "1. Issue number is correct"
    echo "2. You're in the right repository"
    echo "3. You have access to the issue"
    exit 1
fi
```

### Worktree Creation Fails
```bash
# If worktree fails, try with different paths
genesis worktree create $BRANCH_NAME --focus . --max-files 45 || {
    echo "Worktree creation failed. Try:"
    echo "1. genesis worktree list (check existing)"
    echo "2. genesis worktree remove <name>"
    echo "3. Manually specify focus paths"
}
```

### Tests Fail
- Run `make test` to see specific failures
- Use `genesis autofix` for formatting issues
- Check `git diff` for unintended changes
- Verify environment setup with `genesis status`

### PR Creation Fails
- Ensure branch is pushed: `git push -u origin $BRANCH_NAME`
- Check GitHub permissions: `gh auth status`
- Verify no existing PR: `gh pr list --head $BRANCH_NAME`
</error-handling>

<examples>
## Usage Examples

### Basic Usage
```bash
# Implement issue #197 (genesis sync feature)
/execute-issue 197
```

### What Happens
1. Fetches issue #197 details
2. Creates branch `feat-197-implement-genesis-sync`
3. Creates worktree focused on genesis/commands/
4. Guides through implementation
5. Creates PR titled "feat: Implement genesis sync (#197)"
6. Links PR to issue with "Resolves #197"

### Issue Type Detection
- Bug issue → `fix-XXX-` branch prefix
- Feature issue → `feat-XXX-` branch prefix
- Docs issue → `docs-XXX-` branch prefix
- Other → `chore-XXX-` branch prefix

### Focus Path Intelligence
The command analyzes issue content to determine optimal worktree paths:
- Mentions "CLI" → focuses on `genesis/`
- Mentions "bootstrap" → focuses on `bootstrap/`
- Mentions "template" → focuses on `templates/`
- Mentions "test" → focuses on `tests/` and `testing/`
- Mentions "docs" → focuses on `docs/`
</examples>

<integration>
## Integration with Other Commands

### Before This Command
- Check open issues: `gh issue list --assignee @me`
- Review issue details: `gh issue view XXX`
- Ensure clean workspace: `git status`

### After This Command
- Monitor PR checks: `gh pr checks`
- Address review feedback
- Merge when ready: `gh pr merge`
- Clean up: `/pr-merged <branch-name>`

### Related Commands
- `/commit` - For additional commits during implementation
- `/update-docs` - If documentation needs updating
- `/pr-merged` - For cleanup after merge
</integration>

<notes>
## Important Notes

1. **Always start from main branch** - Ensures clean starting point
2. **One issue = One PR** - Keep changes focused
3. **Test before committing** - Saves time and CI resources
4. **Use Genesis tools** - Leverage autofix, smart commit, etc.
5. **Document as you go** - Update docs with code changes
6. **Communicate progress** - Update issue with status
7. **Clean up after merge** - Use `/pr-merged` command
</notes>

---

**Remember**: This command automates the issue-to-PR workflow but requires thoughtful implementation. Always understand the issue requirements fully before starting implementation.
