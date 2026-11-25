---
name: git-workflow
description: Branch naming, commit message format, and PR conventions. Use when making git commits or creating PRs.
---

# Git Workflow

## Commit Messages

Use conventional commit format:
- `feat: add new feature`
- `fix: resolve bug in X`
- `refactor: restructure Y`
- `docs: update README`
- `test: add tests for Z`
- `chore: update dependencies`

Keep the first line under 72 characters. Add a blank line and detailed description if needed.

## Branch Naming

- `feat/short-description` - New features
- `fix/issue-description` - Bug fixes
- `refactor/what-changed` - Refactoring
- `docs/what-documented` - Documentation

## Workflow

1. Create a feature branch from main
2. Make small, focused commits
3. Test your changes
4. Push and create PR when ready

## Pull Requests

- Clear title describing the change
- Description with context and testing notes
- Keep PRs focused on a single concern
