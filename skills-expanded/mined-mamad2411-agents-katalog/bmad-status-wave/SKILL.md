---
name: bmad-status-wave
description: >
  Project-wide visibility dashboard for the wave map. Reads waves.md, probes
  every wave's worktree, branch, commits, checkpoint, and pull-request state,
  and prints a single dashboard. Read-only; no writes. Use at session start,
  on demand during multi-wave work, or whenever the user asks "where am I in
  this project."
when_to_use: |
  Anytime cross-wave visibility is needed, especially across parallel
  sessions or after time away from the project. Do NOT use this skill to act
  on a wave -- it never resumes, merges, or modifies anything; reach for
  /bmad-resume-wave or /bmad-merge-wave for action.
allowed-tools:
  - Read
  - Glob
  - Bash
metadata:
  version: 1.2.1
  output-locations: []
---

# bmad-status-wave
Strictly read-only project-wide scan. It writes nothing; the dashboard is the
printed output of the session and lives nowhere else.

## Inputs
- Default: no arguments. Project-wide scan of every wave in waves.md.
- --wave <id>: single-wave verbose mode; prints every probe's raw output.
- --only-active: suppress waves whose PR is merged or closed and whose
  worktree is gone.

## Probes (per wave)
1. Wave map: the row in _bmad-output/planning-artifacts/waves.md.
2. Worktree: sibling directories matching <project>-wave-* on disk.
3. Branches: `git branch --list 'wave-*'`.
4. PR state: `gh pr list` filtered by head branch.
5. Status and current step: the wave's lifecycle status record, read with

       python3 {skill-root}/../bmad-dev-wave/scripts/wave_status.py show \
           --project-root {project-root}

   which is read-only -- it never writes and never backfills a missing
   record, unlike the `route` verb the acting skills call. Then the wave's
   checkpoint markers under .bmad/wave-<id>/, the project HANDOFF.md, and the
   branch's last commit message.
6. Tests: verify-fast results if present.

## Output: the eight-column dashboard
One row per wave; fixed column widths and value enumerations (downstream
tooling parses positionally):
| Wave | Status | Branch | Step | PR | Tests | Blocked-on | Flags |
- Status is the value `show` reports: one of the six statuses, or `unmigrated`
  for a wave with no record yet, or `corrupt` for a record whose status cannot
  be read. Do not enumerate the six here; they are defined once in
  bmad-dev-wave/scripts/wave_status.py and tabled in /bmad-dev-wave.
- PR in {none, open, merged}; Tests in {green, red, unknown}; Flags shows
  load-bearing / spine-only.

A `blocked` row is a hard stop on that wave, not a note: every dispatch
refuses on it until a human edits or deletes `.bmad/wave-<id>/wave.md`, and
fixing the underlying cause does not clear it. Read a blocked row as work
waiting on the founder. A `corrupt` row is the same shape of stop with a
different remedy: the record needs repairing or deleting.

An `unmigrated` row is a wave that predates the status field. Nothing is
wrong with it; the next acting skill that touches it backfills the record and
says so. This skill leaves it alone, because backfilling would be a write.

## Cross-Wave Consistency Checks
Surface, do not fix: a branch with no worktree; a worktree on the wrong
branch; a merged PR whose worktree still exists (cleanup pending ->
/bmad-merge-wave); duplicate story IDs across waves; an epic every one of
whose waves has merged but which has no closure record (closure-pending ->
/bmad-close-epic).

Closure-pending is the one check something now acts on. This skill still
only reports it, but /bmad-dev-wave 1.1.0's preflight refuses to open a wave
while it holds (settled-decisions register row 51). So a closure-pending row
here is a blocker on the next wave, not an untidy note, and the dashboard
should be read that way.

That is also why this check tests **merged** rather than cleaned up, which
is a correction: cleanup lags a session, because a session cannot remove the
worktree it runs in. Under the older cleaned-up reading an epic whose waves
had merged but not yet been swept showed clean here and would still be
refused by the gate, so the dashboard would have disagreed with the tool
enforcing it.

## Error Handling
- waves.md missing: clean refusal naming the path and /bmad-create-wave.
- gh not authenticated: report; PR column degrades to "unknown".
- Stale worktree directory (not registered with git): flag it.
- Treat HANDOFF.md-derived step as a hint, not ground truth; the worktree's
  actual state wins.

## Version history
- 1.2.1 (2026-10-01, R4 of docs/reviews/harness-engineering-review-v1.md):
  frontmatter only. `when-to-use` is `when_to_use`, the field Claude
  Code reads, so it now reaches the skill listing; `version` and
  `output-locations` sit under
  `metadata:`, which Claude Code leaves to the fork's own tooling. Nothing in
  the body changed.
- 1.2.0 (2026-09-11, Phase 2 of docs/harness-conversion-plan.md): the
  dashboard gains a Status column, read from the wave's lifecycle record
  through the `show` verb, which is the read-only half of the same script the
  acting skills route on. Still strictly read-only: `show` never backfills a
  missing record, so a project scan cannot quietly migrate eighteen waves.
- 1.1.0 (2026-09-10, founder ruling, settled-decisions register row 51):
  the closure-pending check tests every wave merged rather than every wave
  cleaned up, so it agrees with the /bmad-dev-wave preflight that now
  refuses on it, and the check is labelled as enforced rather than advisory.
  Still read-only: this skill reports, the gate acts.
