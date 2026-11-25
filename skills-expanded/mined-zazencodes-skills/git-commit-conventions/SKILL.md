---
name: git-commit-conventions
description: Make focused commits with short messages and the user's git authorship. Use before every commit or push, including /commit.
---

# Git Commit Conventions

Follow these conventions on every commit.

- Commit authorship should follow the user's system git config only; no co-author trailers.
- Commit messages should be very simple: one short line per distinct batch of changes.

## Working conventions

- Read `git diff` and check for untracked files before deciding on commits.
- One commit per distinct batch of changes. Only group files together when they
  are closely related; otherwise commit them separately.
- Match the message style of the recent commits in this repo.
- Never add AI attribution — no `Co-Authored-By`, no "Generated with" footer.
- Attempt simple fixes yourself; ask for guidance on merge conflicts or anything
  that risks losing work.

## Splitting a mixed working tree

Batches are defined by *intent*, not by file. Two batches routinely touch the same
file — a feature and a follow-up fix to it, a refactor and a behaviour change. That
they interleave inside a file is the normal case, not a reason to give up and make
one commit.

Default to splitting. Do it without being asked, and do not ask permission first:
splitting is expected, and the work below is mechanical and reversible.

- Separate work the user asked for in separate turns into separate commits. If they
  said "build X", then later "now fix Y", that is two batches even if Y edits the
  files X created.
- Do not merge batches because the split "would be a rebase, not staging" or because
  a file was rewritten wholesale. Neither is a reason to combine them.
- `git add -p` needs a TTY and is unavailable. Use the reconstruct method instead:
  1. Copy the final version of every file containing more than one batch somewhere
     outside the repo.
  2. `git reset --soft HEAD~1` if already committed, otherwise just start here.
  3. Edit those files back to the state of the *first* batch alone, then commit it.
  4. Restore the saved final versions, then commit the second batch.
  Repeat step 3–4 for a third batch and beyond.
- Order commits so each one stands alone: the earlier commit must build and pass
  tests without the later one. Verify it — `git stash -u`, check out the earlier
  commit, run the test suite, then return. An earlier commit that only works once
  the next lands is a broken split, not a split.
- Stage explicit paths. `git add -A` silently sweeps in unrelated untracked files;
  check `git show --stat` after committing and amend if something snuck in.
- When done, confirm the split preserved the work: `git diff <original-sha> HEAD`
  should be empty, or show only changes you can name and justify.

If a split genuinely cannot be made to work, say so and explain what blocks it,
rather than committing everything together and mentioning it afterwards.
