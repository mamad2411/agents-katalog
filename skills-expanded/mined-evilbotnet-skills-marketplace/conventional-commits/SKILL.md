---
name: conventional-commits
description: Generate a Conventional Commits message from the staged diff. Use when the user asks to write a commit message or commit changes with a well-formed message.
---

# Conventional Commits

Produce a commit message that follows Conventional Commits 1.0.0.

## Procedure

1. Run `git diff --staged --stat` and `git diff --staged` to understand
   the change. If nothing is staged, tell the user and stop.
2. Infer the type: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`,
   `perf`, or `build`. Infer a scope from the dominant directory or
   subsystem touched; omit the scope if the change is cross-cutting.
3. Compose the message:
   - Subject: `type(scope): imperative summary` — max 72 characters,
     no trailing period.
   - Body: explain WHY the change was made, not what (the diff shows what).
     Wrap at 72 columns.
   - Footer: `BREAKING CHANGE:` when applicable; reference issues the
     user mentioned.
4. Show the proposed message and ask before running `git commit` unless
   the user already told you to commit.
