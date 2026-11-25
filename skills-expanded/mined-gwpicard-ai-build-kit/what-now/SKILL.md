---
name: what-now
description: Orient returners. Read state and name steps.
---

# What now

Read `masterplan.md` (risk record first), changelog, Git status, commits, pull
requests and `AGENTS.md`. Refresh with `sh .agents/tools/plan-refresh.sh`;
`records/references/pieces.md`
covers the fallback. Offline, use the dated plan.

Check live status, unfinished work, merged changes awaiting records, failures,
reviews, setup, conflicts, upkeep due by `.ai-build-kit-maintenance`, and
promised rechecks. Run these
checks from the project root; keep only exit codes:

- `python3` with `maintain/scripts/upgrade-check.py`; exit 1 means the kit
  update is unfinished.
- `sh` with `records/scripts/trued-mark.sh`; anything but 0 means the mark
  cannot be used.

## Tell them where things stand

Start with build state, next command and reason. Put broken work first,
then failed checks, reviews and unfinished setup. Count ready,
waiting, blocked and half-done pieces; before launch, say how many entries are
still notes rather than pieces. Say what
waiting pieces need and whether the person must act. If more pieces wait on
them than are ready, recommend planning.

Name pieces, never issue numbers: at most three, or give the total and
nearest. State dependencies in sentences. `/implement` shows ready pieces.
Before launch, suggest `/implement`, `/shape` or `/setup-hosting`; once live,
`/shape` or `/maintain`.

If the update check exits 1, `/maintain` finishes the update. If the mark
check fails, `/maintain` checks the masterplan. Close with a short recap of where the tool has got to,
unless already named or nothing happened lately.

## Recovery

- **Circling piece:** tell them: save the work
  (`records/references/unsaved-work.md`), then open a fresh chat asking it
  to read the piece, check and notes. Apply
  `repair/references/escalation.md`.

- **Uncommitted work:** follow the `records` skill's
  `references/unsaved-work.md` and give its explanation now.
- **Conflict or live break:** follow `merge` or `live-copy`.
- **Missing capability:** name the limit, fallback and setup action.
- **Person's step:** say where, what to do and what to bring back. Never ask
  for a secret in chat.
### Failing check

Say what it catches. A pull request failure goes to
  `/implement`; a failure on `main` is a fault for `/shape`.

### Unfinished setup step

Name what remains and the action that finishes it.
- **Review finding:** name its piece; `/implement` settles it before merge.
- **Accepted risk:** say what was given up, when and by whom, and that asking
  reopens the skipped check. Do not ask again.

## Done when

The next step and its reason are clear. No unfinished or waiting work is
unacknowledged, and no recovery decision has been made for the person.
