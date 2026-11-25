---
name: dry-run-first
description: >-
  Before any operation that touches system files or is hard to undo, preview what
  it will do, confirm the preview is right, then run it for real. Use this
  WHENEVER you edit files outside the project (registry, /etc, hosts, shell
  profiles, env or system config), bulk-rename or bulk-delete, run a mass
  find-and-replace, a migration, a destructive git command, or any sweep that
  changes many things at once. Run it in dry-run or preview mode first (a
  --dry-run flag, PowerShell -WhatIf, printing intended changes, or operating on a
  copy), check the output matches your intent, and only then execute. Back up when
  no dry run is possible.
---

# Dry run first

Some operations cannot be casually undone: editing a system config, deleting a
batch of files, rewriting many files at once, a destructive git command. The cost
of a mistake there is not a quick fix, it is a broken machine or lost work. A dry
run turns a blind action into a reviewable one: you see exactly what would change
before anything does.

The rule: for anything that touches system files or is hard to reverse, preview
first, confirm the preview is what you meant, then run for real.

## When to insist on a dry run

- **System and global files:** the Windows registry, `/etc`, `hosts`, shell
  profiles (`.bashrc`, `$PROFILE`), env and system config, anything outside the
  project directory.
- **Bulk file changes:** mass rename, mass delete, recursive `chmod`, a sweep that
  rewrites many files.
- **Mass find-and-replace** across a codebase, especially with a broad pattern.
- **Destructive git:** `reset --hard`, `clean -fd`, force-push, branch deletes.
- **Migrations and data mutations** that change records in place.

## How to preview

Use the safest preview the tool offers, in roughly this order:

- A built-in dry-run flag: `--dry-run`, `rsync -n`, `git rm --dry-run`,
  `git clean -n`.
- PowerShell `-WhatIf` on cmdlets that support it (`Remove-Item -WhatIf`).
- Print the planned changes: list the files that would be touched, or show the
  diff, without applying it.
- Operate on a copy first, inspect the result, then apply to the real target.

Then read the preview. Does the set of affected files and the nature of the change
match exactly what you intended? Watch for too many matches, paths outside the
intended scope, or an empty result that means your filter was wrong.

## Then run, then verify

Only after the preview checks out, run the real thing. Afterward, confirm the
result is what the preview promised. If the operation has no dry-run mode and no
safe preview, make a backup first (copy the file, stash, branch, snapshot) so you
can roll back.

## When in doubt, stop

If the preview surprises you, or you are not sure the command is scoped right, do
not run it anyway. Narrow the scope, or ask the user before doing something
destructive to their system (`dont-be-afraid-to-ask`). A throwaway script that
mutates files gets the same treatment: dry run, verify, then run
(`throwaway-scripts`).

## Before you proceed

Before you execute anything that edits system files or is hard to undo, ask: have
I previewed this, and does the preview match my intent? If you cannot preview it,
have I backed up what it could break? Only run for real once both answers are yes.
