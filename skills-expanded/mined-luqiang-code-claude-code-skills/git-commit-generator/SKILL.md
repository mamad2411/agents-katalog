---
name: git-commit-generator
description: |
  Generate Conventional Commits from staged git diff. Analyzes changes and produces
  commit messages following the Conventional Commits spec (feat, fix, refactor, etc.).
  Triggers on "generate commit", "write commit message", "conventional commit".
metadata:
  type: tool
  version: "1.0.0"
  author: community
  tags: [git, commit, conventional-commits]
triggers:
  - "generate commit"
  - "write commit message"
  - "conventional commit"
  - "create commit"
allowed-tools:
  - Bash
---

# Git Commit Generator

Generate [Conventional Commits](https://www.conventionalcommits.org/) from staged changes.

## When to Use
- Ready to commit and want a properly formatted message
- Team enforces Conventional Commits standard
- User mentions "commit", "conventional commit", "commit message"

## When NOT to Use
- No staged changes yet
- Interactive rebase or amend workflows (different context)

## Workflow
1. Run `git diff --cached` to get staged changes
2. Run `git diff --cached --stat` for file overview
3. Analyze: determine type (feat/fix/refactor/docs/test/chore) and scope
4. Generate commit message:
   - Type(scope): short description (under 72 chars)
   - Blank line
   - Body: WHAT changed and WHY (wrapped at 72 chars)
   - Footer: breaking changes or issue references if applicable
5. Show the message and ask user to confirm before committing

## Output Format
```
feat(auth): add JWT refresh token rotation

Introduce automatic refresh token rotation to prevent token replay
attacks. Old refresh tokens are invalidated when a new one is issued.

BREAKING CHANGE: /api/auth/refresh now returns { accessToken, refreshToken }
Closes #234
```

## Key Principles
- Type must be one of: feat, fix, refactor, docs, test, chore, perf, ci, style
- Subject line: imperative mood ("add" not "added"), no period at end
- Body explains WHY, not just WHAT
- Reference issues with "Closes #N" or "Refs #N"
- Breaking changes MUST be flagged in footer

## Notes
- If diff is large (>500 lines), suggest splitting into multiple commits
- If no Conventional Commits type clearly fits, default to "chore"
- Never commit automatically — always ask for confirmation
