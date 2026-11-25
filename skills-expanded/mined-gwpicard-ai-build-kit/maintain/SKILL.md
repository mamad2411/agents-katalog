---
name: maintain
description: Keep project records accurate and the live copy healthy. Every visit checks records and the live copy. Monthly and quarterly work runs only when due. Use after outside work, before a handover, after time away, or when retiring a tool. A session that died part-way goes to what-now first. Do not use for building, repairing or planning.
---

# Maintain

Maintenance never offers queued, parallel, looped building or automatic merging.

Make the records true, compare the live copy with `main`, and finish a kit
update. Report findings before applying anything beyond routine
updates.

In Codex, if a push, fetch or remote check fails with `unable to get password
from user`, run the installed `setup-ai-build-kit` skill's
`templates/foundation/codex-github-check.py` with python3 and `--message`. Give
its sentence and stop.

## Every visit

1. Follow `references/truing.md`. Keep the person's work out of records commits.
   For uncommitted work, follow the `records` skill's `references/unsaved-work.md`
   and explain it now. Say clean-checkpoint steps wait; continue
   read-only checks.
   Read the recipe with `scripts/recipe-freshness.py`. If stale or superseded,
   report its finding and offer to open a
   piece to move to a current recommendation. On a no, change no project files.
2. Compare the live copy with `main` using the `live-copy` skill. Do not change
   the live service or changelog. Offer `/setup-hosting` for backups, restores,
   previews or recipe checks, and name any gap.
3. From the project root run
   `merge/scripts/protect-branch.py --check <origin's owner/repository> main`.
   Exit 0 means required; 3 records the private Free limit, with one notice and
   no offer; 4 means available, so offer to run without `--check` with approval.
   Report other exits. Do not change protection without that approval.
4. Run the installed `setup-ai-build-kit` skill's
   `templates/foundation/scan-secrets.sh` from the project root with `--all`.
   Exit 0 means no secret was found, 1 means one was found, and 2 means the scan
   could not run. On a find, say to rotate it. Never show its value.
5. Read `.ai-build-kit-maintenance`. Monthly work is due 30 days after
   `last-light-pass`, or founding if absent. Quarterly work is due 90 days
   after `last-full-pass`, at founding if absent, and when a handover is asked
   for. Either runs when requested. Say when skipped work falls due.
6. Run `scripts/upgrade-check.py --latest --route` using `references/latest-release.md`.
7. Finish a kit update using `references/kit-update.md` on every visit. The
   monthly routine's first step does it instead. In Codex, offer its
   session-start GitHub check.

Run `scripts/docker-resources.py sweep`.

## Due routines

When monthly work is due, load `references/monthly.md` and follow it in order.
For quarterly work, also load `references/quarterly.md`.

## Handover and retirement

For handover or retirement, load `references/handover-retirement.md`.

## Done when

Records match events; the protection check and live-copy gap are reported; due
work and approved changes are saved; and the person knows when the next visit
is due.
