---
name: audit-light
description: This skill should be used when the user asks to "run a mnemonica light audit", "check docs since last commit", "quick doc sync", "sync knowledge docs with recent commits", or wants a fast, incremental check that recent commits are reflected in the project's knowledge/ documentation without rescanning the whole codebase.
---

# Mnemonica: audit-light

Reconcile `knowledge/` with only what changed since the last checkpoint — a cheap, targeted
pass, not a full rescan. Read
`${CLAUDE_PLUGIN_ROOT}/references/knowledge-conventions.md` first; it defines the checkpoint
file format, the module index format, and the update/cross-cutting rules this skill applies.
This skill requires git (it has no concept of "since the last checkpoint" without commit
history) and is always invoked directly by the user — never by a hook, and never
automatically on commit or push.

If the user's invocation includes extra wording beyond the trigger phrase, treat it as
scoping or preference for this run — for example, pointing out a companion tool to also
consult, or which module they especially care about. It cannot skip the escalation in Step 3
when the diff is too broad, and it cannot make the checkpoint advance when this skill would
otherwise not advance it.

## Step 1: Get the change range

Run `${CLAUDE_PLUGIN_ROOT}/skills/audit-light/scripts/diff-since-checkpoint.sh <project-root>`.

- Exit 5 (`NO_GIT_REPO`): this project has no git repository. Tell the user `audit-light`
  needs git and cannot run here; suggest `git init` (no remote required) if they want
  incremental audits, and stop.
- Exit 2 (`NO_CHECKPOINT`): there is no baseline to diff from yet. Tell the user to run
  `mnemonica:audit-full` first — it creates the checkpoint as part of its own run — and stop.
- Exit 3 (`STALE_CHECKPOINT`): the recorded commit is not an ancestor of `HEAD` anymore
  (rebase, squash, or history rewrite — note that the old commit can still physically exist
  in the repository for a long time after this happens, so this is a real ancestry check, not
  a mere existence check). Tell the user the checkpoint is stale and recommend
  `mnemonica:audit-full` to re-baseline, and stop.
- Exit 4 (`CORRUPT_CHECKPOINT`): the state file exists but couldn't be parsed. This should not
  happen through normal use (the checkpoint is always written by
  `scripts/write-checkpoint.sh`), so treat it as a sign the file was hand-edited. Recommend
  `mnemonica:audit-full` to re-baseline, and stop.
- Success: the script prints the commit range, the new HEAD SHA, and the list of files
  changed across that range.

## Step 2: Check index integrity

Run `${CLAUDE_PLUGIN_ROOT}/scripts/check-index-integrity.sh <project-root>`.

- Exit 1: one or more module files listed in the CLAUDE.md index are missing from disk
  (`knowledge/` was edited or deleted outside of Mnemonica). Recreating a module from scratch
  is a bootstrap-style operation, not a targeted one — out of scope for a light audit. Note
  the missing files in the final report and recommend `mnemonica:audit-full`, but continue
  with Steps 3-5 for whatever modules do still exist; a few missing files elsewhere shouldn't
  block reconciling the ones that are present.
- Exit 0 or 2: nothing to flag here — continue normally. (Exit 2, no MNEMONICA block at all,
  should not happen if `setup` ran, but isn't this skill's problem to fix.)

## Step 3: Map changed files to modules

Read the module index in `.claude/CLAUDE.md` (the block inside `MNEMONICA:BEGIN`/`END`).
Match each changed file path (from Step 1) against each module's owned-path glob(s). A file
may match zero, one, or multiple modules.

- Files matching no module: track them for the report (Step 6) rather than dropping them
  silently — they belong to no documented system yet, or to a system too new to have a
  module. Whether that's fine or worth flagging is the user's call, not this skill's; make
  sure they can see it happened.
- If the matched modules span most or all of the project's modules at once (a broad, sweeping
  change), do not attempt to patch every module piecemeal — tell the user this looks broad
  enough that `mnemonica:audit-full` would be more reliable, and stop. **Do not proceed to
  Step 5 (checkpoint update) in this case** — the checkpoint must stay where it is so the
  range that was too broad for a light audit is still there for `audit-full` (or a future
  `audit-light` run) to actually reconcile. Advancing it here would make that range silently
  vanish from consideration.

## Step 4: Reconcile the matched modules

For each matched module (this should normally be a small number):

1. Read the actual current code at the paths that changed.
2. Read the module file's current content.
3. Correct anything the module says that the code no longer does, and add coverage for
   anything genuinely new — per the update rule in `knowledge-conventions.md`, this is not
   append-only.
4. If more than one module was matched, apply the cross-cutting rule: pick the module where
   the core logic actually lives as primary, give it the full update, and give the other
   matched modules only a one-line `See also:` note pointing at the primary.

None of this requires asking the user — creating or editing module content is always a
low-risk edit per `knowledge-conventions.md`.

## Step 5: Update the checkpoint

Run `${CLAUDE_PLUGIN_ROOT}/scripts/write-checkpoint.sh <project-root> light`. Only reach this
step if Step 3 did not escalate to `audit-full`. It is fine to reach this step even if zero
modules were matched (Step 3 legitimately found nothing relevant in range) — that is a
completed review of the range, not a skipped one, and the checkpoint should advance. The one
case that must never advance the checkpoint is the broad-diff escalation in Step 3.

## Step 6: Report

Tell the user which modules were updated and why, in one or two sentences per module. If any
module files were missing (Step 2), list them. If any changed files matched no module (Step
3), list them too, so nothing that happened is invisible. If nothing needed changing, say so
plainly rather than fabricating an update.
