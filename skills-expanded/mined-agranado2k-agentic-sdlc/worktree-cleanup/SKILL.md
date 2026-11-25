---
name: worktree-cleanup
description: Prune merged feature worktrees, fast-forward the root checkout's base branch, run the project's post-sync command, and refresh the "Active worktrees" row in docs/diary.md. Invoke as `/worktree-cleanup` (or `/worktree-cleanup --dry-run` to preview). Conservative — never removes dirty or unmerged worktrees.
allowed-tools: Read, Grep, Glob, Bash, Edit
metadata:
  phase: mechanical
---

# /worktree-cleanup — prune merged worktrees + sync the root checkout

## What this does

Closes the lifecycle the root `AGENTS.md`'s first hard rule opens. Agents create
`worktree/<slug>` per feature, but after the pull request merges the worktree,
its local branch, and the diary's "Active worktrees" row are all left behind —
and the root checkout's base branch goes stale, so the next worktree branches
from an old base and pays a merge-reconciliation tax later.

The git mechanics live in `scripts/worktree-cleanup.sh`; this skill runs it and
then does the one thing a script should not do on a human's behalf — edit the
project's own memory.

## Hard rules

1. **Never force-remove.** The script already skips dirty or unmerged worktrees;
   do not override it by removing a worktree or deleting a kept branch by hand.
2. **Never touch uncommitted work in the root checkout.** If the script reports
   the root as dirty, surface that to the operator; don't stash or commit on
   their behalf.
3. **Diary edits follow the diary's own update protocol** (it is stated in
   `docs/diary.md`'s header): refresh the **"Active worktrees"** row in the
   Current state block, which is edited in place; never rewrite or delete the
   dated entries below it.

## Procedure

1. **Dry-run first** and show the operator what would happen:

   ```bash
   sh scripts/worktree-cleanup.sh --dry-run
   ```

2. **Run for real** (skip step 1's pause if the operator invoked the skill with
   a clear "clean up" intent — the script is conservative by design):

   ```bash
   sh scripts/worktree-cleanup.sh
   ```

3. **Update `docs/diary.md`**: set the "Active worktrees" row in the Current
   state table to the worktrees that remain (or "None." if empty). If the row
   was already stale before this run, say so in the next dated entry rather than
   silently fixing history.

4. **Report** the script's summary block plus the diary edit: base branch before
   → after, worktrees removed, worktrees kept and why. Record each worktree's
   fate from that summary, one event per worktree the script named:
   `sh scripts/trace.sh emit kind=worktree.prune subject=worktree:<slug> outcome=removed|kept reason='<merged, and how the script knew; or why it was kept — dirty, unmerged, fresh, live>' || :`.
   The trace is written here and never read (the kit's ADR-0008); unconfigured, the
   call is a silent no-op.

## What "merged" means here

A branch is pruned when it is an ancestor of the base ref (the normal case for
merge commits and rebases) **or** its pull request is recorded as merged by the
forge CLI. The second test exists because squash merges rewrite the commits, so
ancestry can never succeed for them. Anything that satisfies neither test is
kept. A **fresh** branch — one that has not moved since it was created, so it
has no commits of its own — is kept and reported as fresh before either test
runs, because ancestry would otherwise read a session that is just starting as
merged and remove its worktree. A **live** worktree — merged and clean, but
still held by a session, which the script reads from an open run on its run
stack or a process working in it — is kept too, and the summary names the run
or the process; a session that is finishing up after its pull request landed
looks exactly like a finished one otherwise.

## Configuration

Both are environment variables read by the script, both optional:

- `WORKTREE_CLEANUP_BASE` — the merge target. Defaults to origin's HEAD branch.
- `WORKTREE_CLEANUP_POST_SYNC` — a command to run when the base branch moved,
  typically a dependency install. Empty by default: the kit does not know your
  toolchain, so it prints a reminder instead of guessing. Set it in
  `constitution/local-workflow.md`'s "Before you push" section once you know
  what it should be, so the next person does not have to rediscover it.

## Cross-references

- The root `AGENTS.md`, hard rule 1 — why the worktrees exist at all.
- `/merge-train` — runs this skill as its final step, once a batch has landed.
- `docs/diary.md` — the update protocol step 3 obeys.
