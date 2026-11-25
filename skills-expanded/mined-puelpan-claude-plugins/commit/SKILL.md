---
name: commit
description: >-
  Create a well-formatted git commit using conventional commit style. Generates
  three commit message suggestions, automatically uses the first, and runs
  `git commit -am` without further prompting. Use when the user explicitly asks
  to commit the current changes (e.g. "commit this", "make a commit"). Do not
  use for creating a PR — that is the create-pr skill.
---

# Fast Commit

Create a well-formatted commit using conventional commit style.

## When to Use This Skill

Use this skill only when the user explicitly asks to commit the current changes
("commit this", "commit", "make a commit"). For opening a pull request, use the
`create-pr` skill instead.

## Instructions

- Generate 3 commit message suggestions following conventional commit style
  (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, etc.).
- Automatically use the first suggestion without asking the user.
- Immediately run `git commit -am` with the first message.
- Do NOT add Claude co-authorship footer to commits.
