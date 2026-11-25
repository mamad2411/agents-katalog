---
name: agri-commit
description: Stage files with git add and create a Git commit following Conventional Commits 1.0.0. Use this skill whenever the user asks to commit, make a commit, git commit, save changes to git, or commit their work — even if they don't mention "conventional commits" explicitly.
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*)
metadata:
  author: Lucas Yang
  version: "2026.04.19"
---

# Git Commit (Conventional Commits 1.0.0)

## Workflow

1. Run `git status` to assess the state (staged, unstaged, untracked).
2. **If both staged and unstaged content coexist**, commit only what's already staged — leave unstaged modifications untouched. Mention this choice briefly so the user knows the unstaged files were skipped.
3. If nothing is staged yet, run `git add -A` automatically.
4. Read `git diff --cached` to understand the changes, then compose a Conventional Commits 1.0.0 message.
5. Commit using a heredoc to preserve multi-line formatting, then confirm with the resulting hash.

## Notes

- If there's nothing to commit, say so and stop.
- When changes span unrelated concerns, suggest splitting; if the user prefers one commit, pick the type matching the primary intent.
- **Language**: Write `type` and optional `scope` in lowercase English (feat, fix, chore, refactor, docs, etc.); write the subject and body in Traditional Chinese with Taiwanese phrasing. Example: `feat(auth): 加入 Google 登入支援`
- **Omit the body unless it is truly necessary.** A one-line subject is preferred; only add a body when the _why_ or context cannot be inferred from the diff and the subject alone.
