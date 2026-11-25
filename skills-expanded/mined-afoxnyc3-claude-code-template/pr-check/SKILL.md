---
name: pr-check
description: Validate PR readiness before creating a pull request
allowed-tools: Bash, Read, Glob, Grep
disable-model-invocation: true
---

# PR Readiness Check

Validate that the current branch is ready for a pull request.

## Instructions

Run the following checks in order:

### 1. Branch Status

```bash
# Current branch
git branch --show-current

# Commits ahead of main
git log main..HEAD --oneline

# Any uncommitted changes?
git status --short
```

### 2. Linting

```bash
# Python
ruff check . && ruff format --check .

# TypeScript/JavaScript (if applicable)
# eslint . && prettier --check .

# Terraform (if applicable)
# terraform fmt -check -recursive
```

### 3. Tests

```bash
# Python
pytest --tb=short

# Node.js (if applicable)
# npm test
```

### 4. Self-Review Checklist

Read `knowledge/staff-engineer-review/SKILL.md` and verify:

- [ ] No bare `except:` clauses
- [ ] All I/O operations have timeouts
- [ ] Logs have context (not just "Error occurred")
- [ ] Tests cover happy path AND error cases
- [ ] No hardcoded secrets or credentials

### 5. Output

```markdown
## PR Readiness Check

**Branch**: [branch-name]
**Commits**: [N] commits ahead of main

### Checks
- [x] Linting passed
- [x] Tests passed
- [x] Self-review complete

### Ready for PR?
YES / NO (reason: ...)
```

## If Checks Fail

1. Fix the failing check
2. Commit the fix
3. Re-run `/pr-check`
