---
name: gh-clean
description: Remove the dev-workflow pipeline's own worktrees, stale branches, and temp artifacts — safely. Use after a merge (gh-merge invokes this at its Step 8) or standalone when pipeline debris needs clearing. Refuses to touch the operator's main worktree or any other session's worktree, never runs `git clean` where a `.env` lives, and requires the project's artifacts gate green before finishing. Conservative: anything not provably pipeline-owned is reported and left in place, never force-removed.
---

# GH Clean

**Session shape:** inline within gh-merge (its Step 8) — it must match
`gh-merge-<session>` worktrees against the invoking session, so it inherits the
merger's context rather than spawning; fully runnable standalone.
**Conventions scope:** none — this skill cites no CONVENTIONS.md sections; do not
load that file.
**Routine trigger (optional):** this stage may also run as an event-triggered
cloud routine (Pull request: Closed) in a fresh clone. There, the local-worktree
teardown steps below DO NOT APPLY — never attempt to manage worktrees or files
on the operator's machine; scope narrows to the triggering PR's remote head
branch (delete only if merged and unused by any open PR) plus the artifacts
gate, with the same conservative report-don't-guess posture.

## Overview

You are the pipeline's cleanup stage. Pipeline runs create their own worktrees,
branches, and temp artifacts; over a sprint these accumulate as debris. Your job
is to remove **only what the pipeline itself created and no longer needs** —
conservatively, with the two memorialized traps encoded so cleanup cannot repeat
past damage:

- A prior `git clean` **wiped an operator `.env`** (memory:
  `long-worker-session-failure-modes`).
- A prior cleanup pass **switched branches / mutated refs in the main
  worktree**, corrupting it (memory: `worktree-review-isolation`,
  `lead-operate-from-own-worktree`).

**Taxonomy, statuses, and the state machine are owned by
[`agents/gh-workflow/CONVENTIONS.md`](../../agents/gh-workflow/CONVENTIONS.md).**
This skill references those sections and never restates their tables.

Invoked by `gh-merge` after each merge (its Step 8), but fully runnable
standalone whenever pipeline debris needs clearing.

## Scope (single-purpose)

Remove exactly three categories of pipeline-owned debris, nothing else:

1. **Worktrees the pipeline created** for a ticket/PR whose work has landed or
   whose branch is gone — i.e. its PR is merged or closed. A pipeline worktree
   is one this skill (or gh-resolve / gh-merge / a worker) created for a
   specific issue/PR, identifiable by its branch name (the profile's
   `<work-branch-convention>` / `<merge-worktree-convention>`) or by being listed
   as a known pipeline worktree path.
2. **Stale local + remote branches** belonging to those same merged/closed
   PRs — delete both sides once the PR is confirmed merged or closed.
3. **The pipeline's own temp artifacts** — scratch files/directories the
   pipeline wrote during its run (e.g. under a `tmp/`/`.tmp-*` path), the same
   categories the profile's `<artifacts-gate>` forbids from being tracked.

**Anything ambiguous is left in place and reported, not deleted.** An
over-eager cleaner is worse than a lazy one (Design Guidance, #677). If you
cannot cheaply prove a worktree/branch is pipeline-owned and safe to drop, skip
it and say so in the report.

## Non-negotiables (read first)

### 1. Never touch the operator's main worktree

**Refuse outright** to remove, `git clean`, checkout-switch, or otherwise
mutate:

- The operator's main worktree — the profile's `<operator-main-checkout>` (PROFILE.md).
- Any **other session's** worktree — a worktree you did not create for *this*
  cleanup pass, even if it looks stale (it may hold another agent's in-flight
  or interrupted-but-recoverable work; memory: `recover-interrupted-bg-worker`
  — a surviving worktree can hold unmerged work worth finishing, not deleting).

Before removing any worktree, confirm via `git worktree list` that its path is
one **this pipeline run is authorized to own** (either a worktree tied to a
ticket whose PR is verified merged/closed — Workflow step 3 — or the current
session's own `gh-merge-<session>` scratch worktree — Workflow step 2) and that
it is **not** the main worktree path. If a target is ambiguous, **report it and
stop** — do not guess.

### 2. Never `git clean` where a `.env` lives

A gitignored `.env` holds operator credentials (`key_id`, API secrets) that
`Settings()` requires; a prior `git clean` deleted one, cascading into a wall
of unrelated-looking `key_id`/`Settings` test failures across the whole suite
(memory: `long-worker-session-failure-modes`, mode 2).

Before running `git clean` in **any** directory, check for `.env`:

```sh
git -C <target-worktree> status --porcelain --ignored | grep -F ".env"
# or simply:
test -f <target-worktree>/.env && echo "DOT-ENV PRESENT — do not git clean"
```

- If `.env` is present, **do not run `git clean` in that worktree.** Remove the
  worktree itself via `git worktree remove` (below) instead — that deletes the
  whole directory tree in one step without ever invoking `clean`, so the
  presence check is a belt-and-suspenders guard against a bare/leftover
  directory that `worktree remove` didn't fully clear.
- If a worktree cannot be removed via `git worktree remove` (e.g. it is already
  gone from `git worktree list` but a directory remains) and manual deletion is
  needed, re-run the `.env` check on that directory first; if `.env` is
  present, remove the directory with a targeted `rm`/`Remove-Item` of the known
  debris paths — never a bare `git clean -fdx` there.
- This check runs **every time**, even for worktrees you believe are pipeline
  worktrees — belief is not verification.

### 3. The artifacts gate green before finishing

Run the profile's `<artifacts-gate>` (from a repo checkout with the
current tree — the operator's main worktree is fine to **read** for this,
since the check only runs `git ls-files`, a read-only op, never a mutation) as
the last step. It must exit clean. If it reports a tracked artifact, that is a
**different** problem (a tracked file that should have been gitignored) — report
it; do not attempt to fix it by force-deleting anything outside this skill's
three categories.

## Workflow

### 1. Inventory

```sh
git worktree list
git branch -a
```

Classify each worktree/branch:

- **Main worktree** (the profile's `<operator-main-checkout>`) — never a
  candidate. Exclude immediately.
- **Pipeline worktrees** — path matches the profile's worktree convention (e.g.
  `<worktree-root>/<repo-name>-<issue>`, `<merge-worktree>` per gh-merge's *Prepare*
  step) and/or its checked-out branch matches the pipeline branch conventions
  (`<work-branch-convention>`, `<merge-worktree-convention>` — PROFILE.md).
- **Everything else** — an operator worktree you don't recognize, a
  differently-named worktree, anything you can't confidently attribute. Not a
  candidate; report and skip.

### 2. The merger's own `gh-merge-<session>` worktree (explicit SAFE path)

Handle this case **first, before the PR-state lookup below** — otherwise it is
missed. gh-merge's *Prepare* step creates a dedicated `gh-merge-<session>`
worktree on a throwaway `gh-merge-<session>` branch that has **no PR** (it is a
scratch tree for materializing and gating the merge, per gh-merge's Step 5), and
gh-merge's Step 8 invokes gh-clean **specifically to tear that worktree down**.
Because it has no PR, the step-3 lookup would return "PR not found" and the
conservative default would wrongly leave it behind. So:

- When invoked by (or as) the merger, the current session's **own**
  `gh-merge-<session>` worktree — identified by the `gh-merge-<session>`
  branch-name pattern **matching the invoking session** — is **provably
  pipeline-owned scratch** and is **SAFE to remove directly** (step 4), skipping
  the PR-state lookup. Its branch is a scratch branch with no PR; delete it
  locally too (it never has a remote to clean).
- This exception is **narrow**: it covers only the merge worktree for *this*
  cleanup pass's own session. A `gh-merge-<other-session>` worktree belonging to
  a **different** merger session is another session's worktree — **never
  removed** (non-negotiable #1); report it and leave it.
- The operator's main worktree is still **never** a target here, even though
  gh-merge also runs from a dedicated worktree — the two are distinct: the merge
  worktree lives at gh-merge's `<merge-worktree>` path on a `gh-merge-<session>`
  branch, never at the profile's `<operator-main-checkout>`.

### 3. Verify each remaining pipeline worktree/branch is safe to drop

For every pipeline candidate **other than** the current session's own merge
worktree (handled in step 2), confirm its PR state before removing anything:

```sh
gh pr list --repo <repo> --state all --head <branch-name> --json number,state,mergedAt
```

- **Merged or closed** → safe to remove the worktree and delete the branch
  (local + remote).
- **Open** → still in flight. Skip it, even if it looks idle — an open PR's
  worktree may be a `recover-interrupted-bg-worker` case (a background worker
  died but its worktree holds unfinished, unmerged, still-valuable work).
  Report it as "open, left in place," not removed.
- **Unknown / PR not found** (e.g. a throwaway/manual branch with no PR that is
  **not** this session's own `gh-merge-<session>` scratch tree) → ambiguous.
  Leave it and report it; do not delete on a guess.

### 4. Remove verified-safe worktrees

Use `git worktree remove`, never a raw `rm -rf` / `Remove-Item -Recurse` on a
live worktree path — `worktree remove` keeps git's own bookkeeping (the
`.git/worktrees/<name>` admin dir) consistent, and refuses if the worktree has
uncommitted changes (a useful safety stop: an uncommitted-changes refusal means
the worktree is not actually done, so surface it rather than forcing past it).

```sh
git worktree remove <path>            # refuses on uncommitted changes — do not --force past this blindly
git worktree prune                    # clears any stale worktree admin entries left behind
```

If `git worktree remove` refuses due to uncommitted changes, **do not**
`--force` it automatically — inspect what's uncommitted first (it may be
recoverable work, per `recover-interrupted-bg-worker`); only force past it if
you've confirmed the changes are disposable (e.g. leftover scratch files, not
real edits).

### 5. Delete stale branches (local + remote)

Only for branches whose PR is confirmed merged/closed (step 3), or the current
session's own scratch `gh-merge-<session>` branch (step 2), and whose worktree
(if any) is already removed (step 4):

```sh
git branch -d <branch-name>                        # local; -d refuses unmerged branches (safety net)
git push origin --delete <branch-name>              # remote, only if it still exists
```

`gh pr merge --delete-branch` (used by gh-merge) already deletes the remote
branch at merge time for most PRs — check `git branch -a` / the remote first so
this step is a no-op rather than an error for those. Use `-d`, not `-D`: a
refusal on an unmerged branch is a correctness signal, not friction to force
past.

### 6. Clear the pipeline's own temp artifacts

Remove only scratch paths the pipeline itself wrote during its run (the same
categories the `<artifacts-gate>` forbids from being *tracked*: `tmp/`,
`.tmp-*`, `evidence-outputs/`, `archive`/`archived`/`_archive` dirs) **and**
that are confirmed untracked/gitignored debris in a pipeline-owned worktree —
never a path inside the operator's main worktree, and never via `git clean`
(non-negotiable #2). Confirm each path is gitignored/untracked
(`git check-ignore <path>` or `git status --porcelain`) before deleting it
directly.

### 7. Gate: the artifacts check

```sh
<artifacts-gate>            # the profile's command (PROFILE.md)
```

Must exit 0 / print "No tracked artifacts or archive directories found." If it
fails, report the violation — do not silently work around it by deleting
something outside this skill's scope.

### 8. Report

Summarize what happened, explicitly:

- **Removed:** worktrees (path + issue/PR#, or the session's own
  `gh-merge-<session>` scratch worktree), branches (local/remote), temp
  artifacts (path).
- **Refused / left in place:** the main worktree (if a caller asked for it —
  state the refusal), any **other**-session worktree encountered (including a
  `gh-merge-<other-session>` tree), any ambiguous or still-open candidate — each
  with why.
- **Artifacts-gate** result (must be green to consider the run
  complete).

## Boundaries

- **Conservative by default.** When a worktree/branch/artifact's pipeline
  ownership or merge state can't be cheaply confirmed, leave it and report it —
  never force-remove to make the run look complete.
- **Never the main worktree.** Not a target, not a fallback, not even to read a
  file for the artifacts gate above and beyond what `git ls-files` needs —
  reading is fine; removing, cleaning, or branch-switching there is not.
- **Never another session's worktree**, even one that looks idle or stale — an
  open PR or an unverified branch means someone else's work may still be live
  there.
- **Never `git clean`** in any directory without first confirming no `.env`
  lives there; prefer `git worktree remove` over `git clean` categorically —
  it never needs the distinction because it never invokes `clean`.
- **No scope creep.** This skill removes worktrees, branches, and temp
  artifacts. It does not touch the board Status, close issues, or edit PRs —
  those are `gh-merge`'s job; gh-clean runs after, purely for hygiene.

## Tool guidance

- `git worktree list`, `git branch -a`, `gh pr list --head <branch>` for
  inventory and PR-state verification.
- `git worktree remove` / `git worktree prune` for worktree teardown — not
  `rm -rf` / `Remove-Item -Recurse -Force`.
- `git branch -d` (local) / `git push origin --delete` (remote) for branch
  teardown — not `-D`, which bypasses the unmerged-branch safety check.
- The profile's `<artifacts-gate>` as the closing gate.
