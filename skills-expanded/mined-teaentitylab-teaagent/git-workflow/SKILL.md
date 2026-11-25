---
name: git-workflow
description: Use when performing git operations, managing branches, commits, and collaborative workflows.
tags: git, version-control, workflow, branching
---

# Git Workflow Skill

Use this skill when performing git operations, branch management, or collaborative workflows.

## Workflow

1. Check current state: `git status`, `git branch`, `git log`
2. Stage changes: use `git add` with appropriate scope
3. Create commits: write clear, conventional commit messages
4. Push changes: handle remote operations safely
5. Handle conflicts: use proper merge/rebase strategies

## Key Tools

- `git_status` - Check repository state
- `git_diff` - View unstaged/staged changes
- `git_commit` - Create commits
- `git_branch` - Manage branches
- `git_push` / `git_pull` - Remote operations
- `git_merge` / `git_rebase` - Integrate changes

## Rules

- Always verify `git status` before destructive operations
- Use `--dry-run` for risky operations (push, force push, reset)
- Prefer interactive rebase for commit history cleanup
- Write commit messages following conventional commits format
- Never commit secrets, keys, or credentials
- Create feature branches for non-trivial changes

## Branch Naming

- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation
- `test/` - Test additions

## References

- See the workflow and rules sections above for advanced workflows and common scenarios.