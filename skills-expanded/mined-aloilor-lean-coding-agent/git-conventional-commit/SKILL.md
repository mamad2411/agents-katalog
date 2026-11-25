---
name: git-conventional-commit
description: Create Conventional Commits 1.0.0 when the user explicitly asks to commit, and push when they also ask to push. Do not use for requests that only ask to propose a commit message, review changes, or stage files.
---

# Git Conventional Commit

1. Read `git status --short` and `git diff HEAD`.
2. Commit the whole worktree unless the user narrows the scope, splitting unrelated changes into logical commits. Include changes that predate the session or were written manually. Ask only when boundaries are materially ambiguous.
3. Stage each commit with `git add <paths>` or `git add -A`, check it with `git diff --cached --stat`, and commit as `<type>[optional scope][!]: <description>`. Use a short lowercase scope only when it adds context, and an imperative, repository-specific description without a trailing period. Add a body or footers only for durable context, issue references, or a `BREAKING CHANGE:` explanation.
4. Repeat until `git status --short` is empty or only explicitly excluded changes remain; report those and the instruction that excluded them. Never create an empty commit; report when there is nothing to commit.

## Push

Only when the user asks to push, and only after the commits succeed: run `git push`, or `git push --set-upstream origin HEAD` when the branch has no upstream. If HEAD is detached or there is no upstream and no `origin`, stop and report what is missing. If the push is rejected, report the error; do not rebase or retry with another push mode.

## Safety

Never discard or overwrite user changes, amend, rewrite history, force-push, or run destructive commands such as `git reset --hard`, `git checkout -- <path>`, or `git clean -fd` unless the user explicitly asks.
