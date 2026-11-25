---
name: git-workflow
description: Follow Git best practices including commit conventions, branching strategies, and pull request practices. Use when committing code, creating branches, or when the user asks about Git, commits, branches, or version control.
---

# Git Workflow & Best Practices

Follow consistent Git practices for better collaboration and code history.

## Commit Message Conventions

### Conventional Commits

```bash
# Format: <type>(<scope>): <subject>

# Types:
# feat: New feature
# fix: Bug fix
# docs: Documentation changes
# style: Code style changes (formatting, etc.)
# refactor: Code refactoring
# perf: Performance improvements
# test: Adding or updating tests
# chore: Maintenance tasks
# ci: CI/CD changes

# Examples:
git commit -m "feat(users): add user registration endpoint"
git commit -m "fix(orders): resolve payment processing bug"
git commit -m "docs(api): update authentication documentation"
git commit -m "refactor(auth): extract JWT logic to service"
git commit -m "perf(database): optimize user query with index"
git commit -m "test(orders): add integration tests for order creation"
```

### Commit Message Structure

```bash
# Format:
<type>(<scope>): <subject>

<body>

<footer>

# Example:
feat(orders): add order cancellation endpoint

Implement order cancellation with proper validation and
notification system. Cancelled orders are marked with status
and timestamp.

Closes #123
```

### Good Commit Messages

```bash
# ✅ Good - Clear and descriptive
feat(users): implement email verification
fix(api): handle null pointer in user service
refactor(orders): extract price calculation logic

# ❌ Bad - Vague or unclear
fix: bug fix
update: changes
wip: stuff
```

## Branching Strategies

### Git Flow

```bash
# Main branches
main          # Production-ready code
develop       # Integration branch for features

# Supporting branches
feature/*     # New features
release/*     # Preparing releases
hotfix/*      # Urgent production fixes
```

### Feature Branch Workflow

```bash
# Create feature branch
git checkout -b feature/user-authentication

# Work on feature
git add .
git commit -m "feat(auth): add login endpoint"

# Keep branch updated
git checkout develop
git pull origin develop
git checkout feature/user-authentication
git merge develop

# Push and create PR
git push origin feature/user-authentication
```

### Branch Naming Conventions

```bash
# Feature branches
feature/user-authentication
feature/order-tracking

# Bug fix branches
fix/payment-processing-error
fix/login-validation-bug

# Hotfix branches
hotfix/critical-security-patch

# Release branches
release/v1.2.0
```

## Pull Request Best Practices

### PR Description Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made

- Change 1
- Change 2
- Change 3

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Screenshots (if applicable)

[Add screenshots here]

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
```

### PR Size Guidelines

- **Small PRs** (< 200 lines) - Easier to review, faster approval
- **Medium PRs** (200-500 lines) - Acceptable for features
- **Large PRs** (> 500 lines) - Consider splitting

### Code Review Checklist

**For Authors:**

- [ ] Code follows project conventions
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No console.logs or debug code
- [ ] Error handling is comprehensive
- [ ] Performance considerations addressed

**For Reviewers:**

- [ ] Code is readable and maintainable
- [ ] Logic is correct
- [ ] Tests are adequate
- [ ] Security concerns addressed
- [ ] Performance is acceptable
- [ ] Documentation is clear

## Git Commands Best Practices

### Staging Changes

```bash
# Stage specific files
git add src/services/UserService.ts

# Stage all changes in directory
git add src/services/

# Stage all changes
git add .

# Interactive staging
git add -p
```

### Committing

```bash
# Commit with message
git commit -m "feat(users): add user creation endpoint"

# Commit with detailed message
git commit

# Amend last commit
git commit --amend -m "feat(users): add user creation endpoint with validation"

# Add to last commit
git add forgotten-file.ts
git commit --amend --no-edit
```

### Branching

```bash
# Create and switch to branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# List branches
git branch

# Delete branch
git branch -d feature/old-feature
git branch -D feature/old-feature  # Force delete
```

### Merging

```bash
# Merge feature into develop
git checkout develop
git pull origin develop
git merge feature/new-feature
git push origin develop

# Squash merge (cleaner history)
git merge --squash feature/new-feature
git commit -m "feat: add new feature"
```

### Rebasing

```bash
# Rebase feature branch on develop
git checkout feature/new-feature
git rebase develop

# Interactive rebase (clean up commits)
git rebase -i HEAD~3

# Continue after resolving conflicts
git rebase --continue

# Abort rebase
git rebase --abort
```

## .gitignore Best Practices

```gitignore
# Dependencies
node_modules/
package-lock.json
yarn.lock

# Environment variables
.env
.env.local
.env.*.local

# Build outputs
dist/
build/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
coverage/
.nyc_output/

# Temporary files
*.tmp
*.temp
```

## Best Practices

1. **Write clear commit messages** - Use conventional commits
2. **Keep commits focused** - One logical change per commit
3. **Commit often** - Small, frequent commits
4. **Use meaningful branch names** - Follow naming conventions
5. **Keep branches up to date** - Regularly merge/rebase
6. **Review before pushing** - Check your changes
7. **Write good PR descriptions** - Help reviewers understand
8. **Keep PRs small** - Easier to review and merge
9. **Respond to feedback** - Address review comments
10. **Clean up branches** - Delete merged branches

## When Working with Git

1. **Create feature branch** - Never commit directly to main
2. **Write descriptive commits** - Clear what changed and why
3. **Keep commits atomic** - One logical change per commit
4. **Update branch regularly** - Merge/rebase from main
5. **Test before committing** - Ensure code works
6. **Write PR descriptions** - Explain what and why
7. **Review your own code** - Check before requesting review
8. **Respond to reviews** - Address feedback promptly
9. **Clean up after merge** - Delete merged branches
10. **Follow team conventions** - Consistency is key
