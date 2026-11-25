---
name: s8-pr-summary
description: Summarize changes in the current branch or working directory
disable-model-invocation: true
context: fork
agent: Explore
---

# S8 — PR Summary

Summarize the current changes for a pull request description.

## Current Changes

### Changed files:
```
!`git diff --name-only 2>/dev/null; git diff --cached --name-only 2>/dev/null`
```

### Diff stats:
```
!`git diff --stat 2>/dev/null; git diff --cached --stat 2>/dev/null`
```

### Recent commits:
```
!`git log --oneline -10 2>/dev/null`
```

## Instructions

Analyze the changes above and produce a PR summary with:

### 1. Title
A concise one-line title (under 70 characters) summarizing the change.

### 2. Summary
2-4 bullet points describing what changed and why.

### 3. Change Categories
Group the changed files into categories:
- **New features**: New functionality added
- **Bug fixes**: Existing behavior corrected
- **Refactoring**: Code restructured without behavior change
- **Tests**: Test additions or modifications
- **Docs**: Documentation changes
- **Config**: Configuration or build changes

### 4. Risks
List any potential risks or areas that need careful review:
- Breaking changes
- Security implications
- Performance concerns
- Missing test coverage
