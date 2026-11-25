---
name: git-conflict-resolution
description: Resolves merge and rebase conflicts by working out what each side intended, combining them on purpose and proving the result with tests.
---

# Git conflict resolution

A conflict is two intentions colliding. Find both before you edit a line.

## Steps

1. Run `git status` and list the conflicted files. Note whether this is a merge, rebase or cherry-pick: during a rebase, "ours" is the branch being rebased onto and "theirs" is your own commit, which is the reverse of what people expect.
2. For each file, read the intent of both sides: `git log --merge -p -- <file>` shows the commits from each side that touch it. Read their messages and diffs. Read the whole file around the markers, not just the marked block.
3. Choose one of three outcomes and be able to say why: keep one side, keep both combined, or write something new that satisfies both. Never keep both blocks pasted together without checking they still make sense.
4. Remove every `<<<<<<<`, `=======` and `>>>>>>>` line. Search for them: `git diff --check` must be clean.
5. Generated files and lockfiles: do not hand-edit. Take one side, then regenerate (`npm install`, `cargo update -p <crate>`, the project's codegen command).
6. After each file, `git add <file>`. When all are staged, run the build and the tests before `git merge --continue` or `git rebase --continue`.
7. If a conflict is a real design disagreement (both sides changed behavior incompatibly), stop and ask the user. Do not guess.

## Rules

- Never run `git checkout --theirs .` or `--ours .` on everything.
- Never abort or force-push without being asked.

## Report

Per file: what each side did, what you kept and why. Then the test result and anything you want a human to double-check.
