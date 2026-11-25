---
name: git-history-cleanup
description: Turns a noisy branch of wip and fixup commits into a short, logical series with interactive rebase, with a backup and a tree-equality check.
---

# Git history cleanup

Rewrite only unpublished history, and prove the end result is identical.

## Steps

1. Check what you are about to rewrite: `git status` must be clean, and `git log origin/<branch>..HEAD` shows the unpushed commits. If the branch is already pushed and others may have it, stop and ask first.
2. Make a backup: `git branch backup/<branch>-before-cleanup`. Record the tree: `git rev-parse HEAD^{tree}`.
3. Read the whole range with `git log --stat --reverse <base>..HEAD` and design the target series on paper: usually 3 to 7 commits, ordered so each one builds (refactor, then behavior, then tests, then docs).
4. Rebase without an editor prompt. Write the rebase plan yourself and pass it with `GIT_SEQUENCE_EDITOR` (for example a small script, or `git commit --fixup` followed by `git rebase -i --autosquash <base>`). Use `reword` for messages, `fixup` to fold, `edit` to split a commit with `git reset HEAD^` and staged hunks.
5. Messages: imperative subject under 72 characters, a blank line, then why the change was made. No "wip", no ticket-only subjects.
6. After every `edit` stop, run the build and the fast tests so each commit stands.
7. Verify: `git rev-parse HEAD^{tree}` must equal the recorded tree. If it differs, the rewrite changed code: reset to the backup and retry.

## Rules

- Never rewrite `main` or any shared branch. Never force-push; tell the user to use `git push --force-with-lease` themselves.
- If the rebase conflicts, resolve carefully or abort with `git rebase --abort`.

## Report

Old and new commit lists, and confirmation that the trees match.
