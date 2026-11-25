---
name: using-git
description: Use when reading status, preparing commits, writing commit messages, comparing local changes, or handling dirty worktrees in this build environment. Focuses on safe non-interactive Git usage, selective staging, and avoiding interference with unrelated user changes.
metadata:
  author: gerph@gerph.org
license: MIT
---
# Using Git

Use this skill when the task involves Git operations in the RISC OS build
environment, especially when preparing commits or reasoning about a dirty
worktree.

## Core rules

* Prefer non-interactive Git commands.
* Never use `git add .`, `git add <directory>`, or other broad staging when a
  narrower file list is possible.
* Never revert or overwrite unrelated user changes unless the user explicitly
  asks for that.
* Do not use destructive commands such as `git reset --hard` or
  `git checkout --` unless explicitly requested.
* Expect the worktree to contain many unrelated untracked files. Filter for the
  exact files relevant to the current task.
* If the `.git` in the repository is a file, which refers to a non-existant directory, we are in a snapshot
  of a git submodule. We cannot do git operations. Do not try - give up and tell the user.


## Status and inspection

Start with targeted inspection:

```bash
git status --short
git diff -- path/to/file
git diff --cached -- path/to/file
git rev-parse --short HEAD
```

When only a few files matter, ask Git about those files directly rather than
trying to interpret the whole repository state.

Be explicit about whether you want unstaged or staged changes:

* `git diff -- path/to/file` compares the working tree against the index, so it
  shows only unstaged changes.
* `git diff --cached -- path/to/file` compares the index against `HEAD`, so use
  it when changes have already been staged and plain `git diff` appears empty.

## Staging

Stage only the intended files:

```bash
git add path/to/file1 path/to/file2
```

If the worktree is noisy, prefer:

```bash
git status --short -- path/to/file1 path/to/file2
```

before committing, to confirm that only the intended paths are staged or
modified.

## Commit messages

Use a short summary line followed by a wrapped body when needed.

Rules:

* Keep the subject concise and imperative.
* Wrap commit message body lines to 74 characters.
* Do not embed literal `\n` escape sequences in `git commit -m` bodies.
* If a multiline message is needed, feed it from standard input or a file.
* A good description opens with a short sentence or paragraph about why the change is being made
  so that the context is understood. This is important for code archeology - working out why something
  went wrong and what the reason was for a mistake.
* This can then be followed by the detail about what has been done to address this, and how it has
  been tested.
* It may include how the change is deficient because of time, or just because it's progressive work, etc
* If relevant, include information about how it was tested, but don't go into excessive detail.
* You may avoid these rules and make just a simple description if the change is self-explanatory -
  adding documentation, correcting typos, etc - or where background would not help. But never commit only a title line; there must always be some body text.

Preferred pattern:

```bash
printf '%s\n' \
  'Short subject line' \
  '' \
  'First wrapped body line.' \
  'Second wrapped body line.' | git commit -F -
```

Use multiple `-m` arguments only for separate paragraphs, not to simulate line
wrapping with escaped newlines.

## Dirty worktrees

This environment often has:

* unrelated modified files,
* many untracked files,
* generated output under `.rotransform/`, `build/`, or similar paths.

Guidance:

* Ignore unrelated untracked files unless they are directly relevant.
* Read carefully before committing if a file is already modified.
* If a file has unrelated user edits, integrate with them rather than replacing
  them.
* If the change set is mixed, commit only the files that belong to the current
  task.

## Environment-specific notes

Lessons from this environment:

* The repository may contain wrapper tools on `PATH` with familiar names. Check
  which executable is being used if command behaviour looks unusual.
* If a shell one-liner needs a multiline commit message, prefer `printf` piped
  into `git commit -F -`.
* Commit messages should be wrapped properly because literal backslash escapes
  are not interpreted inside ordinary single-quoted shell strings.
* When testing or building inside the environment, generated files should remain
  uncommitted unless they are part of the requested source change.

## When to use this skill

Use this skill for tasks such as:

* preparing a clean commit from a noisy worktree,
* writing or reviewing commit messages,
* staging only selected files,
* checking whether a repository is safe to commit,
* comparing local changes before a release or integration step.
