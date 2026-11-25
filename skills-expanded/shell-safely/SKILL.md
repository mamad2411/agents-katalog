---
name: shell-safely
description: "Running terminal commands without destroying anything: look before you write, prefer reversible steps, and pause before the commands that delete or overwrite. Read before any command that deletes, overwrites, or changes system state."
---

# Running commands safely

## Look before you write

Before deleting or overwriting, print what will be affected. `ls` the glob,
`cat` the file, `git status` the tree. A destructive command run against the
wrong path is not recoverable by apologising afterwards.

## Prefer reversible steps

- Move to a temporary directory rather than `rm`.
- `cp file file.bak` before editing in place.
- On a git repository, commit or stash first, then any mistake is one `git
  checkout` away from undone.

## Commands that deserve a pause

`rm -rf`, `git reset --hard`, `git clean`, `git push --force`, `DROP`,
`TRUNCATE`, `DELETE` without a `WHERE`, a migration against a real database,
`chmod -R`, `kill -9` on something you did not start, and anything with `sudo`.
Read the whole command before you run it; a path pasted from somewhere else may
not be the one you mean.

## During a security engagement

The same care, with teeth: never a destructive payload against a target, never
an automated tool's "get me a shell" mode, never a command that alters or
destroys the data you were authorized to test, not exploit.
