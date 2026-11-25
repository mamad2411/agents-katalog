---
name: git-discipline
description: |
  Enforce conventional commits, clean branch strategy, small focused diffs, and PR-ready history.
  Use before any commit or when preparing work for review.
  Triggers: "commit this cleanly", "prepare for PR", "fix the git history", "use git-discipline".
version: 1.0.0
author: Cobus Greyling
---

# Git Discipline

Never let agentic speed destroy repository hygiene.

## Mandatory Steps

1. **Stage intentionally** — only the files that belong in this logical change.
2. **Write a Conventional Commit message**:
   - `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `perf:`
   - Scope when useful: `feat(api): ...`
   - Body that explains *why*, not just what.
3. **Create or update branch** following `feature/`, `fix/`, etc.
4. **Never commit directly to main.**
5. **Rebase or merge cleanly** before opening PR.
6. **PR description** should reference the plan or relevant skills used.

## Agent Behavior

- After edits, offer to run `git diff --staged` and propose a commit.
- If history is messy, propose a rebase plan (never force-push without confirmation).
- When multiple logical changes are staged together, split them.

## Verification
- `git log --oneline -10` should tell a clear story.
- Each commit should be buildable/testable in isolation where practical.
