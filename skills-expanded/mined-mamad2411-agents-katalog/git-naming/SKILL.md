---
name: git-naming
description: Naming conventions for git branches and commit messages, designed for cloud agents and local development. Ensures consistent, parseable git history.
---
# Git Naming Conventions

Naming conventions for git branches and commit messages to ensure consistent, parseable git history. These conventions are optimized for cloud agents but apply to all development work.

## Branch Naming

Use kebab-case (lowercase with hyphens) for all branch names. Branch names should be descriptive and indicate the type of work.

### Pattern

`{type}/{scope}-{description}`

### Types

- `feature/` - New functionality or enhancements
- `fix/` - Bug fixes
- `refactor/` - Code refactoring without changing behavior
- `docs/` - Documentation changes
- `test/` - Adding or updating tests
- `chore/` - Maintenance tasks, dependency updates
- `perf/` - Performance improvements
- `style/` - Code style changes (formatting, whitespace)
- `ci/` - CI/CD pipeline changes

### Scope (Optional)

Component, module, or area affected:
- `frontend/`, `backend/`, `api/`, `ui/`, `terminal/`, `window/`

## Commit Messages

Follow the Conventional Commits specification for consistency and automated parsing.
