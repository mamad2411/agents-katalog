---
name: bmad-resume-wave
description: |
  Resume an interrupted /bmad-dev-wave session from the correct re-entry
  step. Inspects worktree, branch, commits, and checkpoint files to decide
  where the previous session stopped, then re-dispatches /bmad-dev-wave with
  --from-step set to the chosen step. Refuses to act on dirty worktrees,
  already-completed waves, or contradictory state. Re-runs the open-questions
  gate against current memory.
allowed-tools: Read Glob Grep Bash Skill(bmad-dev-wave *)
when_to_use: |
  When the user invokes /bmad-resume-wave with a wave ID; when a previous
  /bmad-dev-wave session was interrupted (crash, timeout, accidental /clear,
  machine reboot) and the wave has uncommitted or partially-committed state;
  or when /bmad-wrap surfaced an in-progress wave at session end and the next
  session needs to pick it up.
metadata:
  version: 1.4.0
  when-not-to-use:
    - Wave has not yet been started (use /bmad-dev-wave from step 1)
    - Wave is already complete and merged (no recovery needed)
    - Wave ID does not appear in waves.md (refuse with not-found error)
  outputs:
    - .bmad/wave-<id>/resume-from-step-<N>.json
    - the re-dispatch's opening prompt, from any open evaluator findings
---

# bmad-resume-wave
Resume an interrupted /bmad-dev-wave session from the correct re-entry step.

## Inputs
### Required
- **wave-id**: The wave label as it appears in waves.md (e.g. "1A", "2B").
  Used to locate the wave's worktree at ../<project>-wave-<id>/ and the
  checkpoint directory at .bmad/wave-<id>/. Must match a row in waves.md
  exactly.
### Optional
- **--from-step <N>**: Override the auto-detected re-entry step. Valid range:
  1 through 12. Warn-and-confirm semantics.
- **--dry-run**: Run all five state probes and write the resume-decision
  artifact, but do not re-dispatch /bmad-dev-wave.

## Outputs
### Resume-decision artifact
Path: .bmad/wave-<id>/resume-from-step-<N>.json
### Re-dispatch side effect
On successful auto-detection (or confirmed override), the skill invokes
/bmad-dev-wave with --wave-id <id> --from-step <N> and exits.

## The Status Router
The re-entry stage comes from the wave's lifecycle status record, not from
this skill's reading of the filesystem and not from the conversation:

    python3 {skill-root}/../bmad-dev-wave/scripts/wave_status.py route \
        --project-root {project-root} --wave <id>

Exit 0 proceeds and its JSON carries `status`, `stage` and `reentry_step`;
`reentry_step` is the `--from-step` value. Exit 1, 2 or 3 is the refusal;
quote its stderr. There is no flag and no override.

  0  proceed
  1  the wave is blocked -- see below
  2  structural: no wave map, or the wave is not in it
  3  the record exists and its status is missing or unrecognized

The vocabulary lives in that one script and the table is in /bmad-dev-wave,
which owns it. Do not restate the status names here and do not re-derive the
stage by reading files: a second reading that disagrees with the record is the
inference this phase exists to remove.

A wave with no record yet predates the field. `route` backfills it once from
the same evidence the probes below gather, prints an `UNMIGRATED` notice
naming the inferred status, and proceeds. Read that notice before confirming
the re-dispatch; it is the one dispatch whose stage was guessed rather than
recorded.

## Blocked is sticky
Exit 1 means the wave is blocked, and a blocked wave stays blocked on every
later dispatch **even after its cause is fixed**. This skill cannot clear it,
--from-step cannot skip past it, and no flag exists to force it. Quote the
refusal, which names when the wave was blocked and why. Clearing it is a human
act: edit `status:` in `.bmad/wave-<id>/wave.md` to another valid status, or
delete that file. Deleting only the `status:` line exits 3 instead.

## The Opening Prompt
Before re-dispatching, ask whether this wave owes the next session an answer
to a fresh-context evaluation:

    python3 {skill-root}/../bmad-dev-wave/scripts/evaluate_wave.py \
        opening-prompt --project-root {project-root} --wave <id>

  0  nothing owed -- no evaluation on disk, or the latest one is PASS
  1  open findings -- stdout's `prompt` is the opening prompt, verbatim
  2  structural: no wave map, or the wave is not in it
  3  an evaluation record carries no readable verdict; repair or delete it

On exit 1, that text opens the re-dispatched session. Use it as written. Do
not paraphrase it, do not trim the findings to the ones you think matter, and
do not lead with your own reading of what went wrong -- the evaluator saw a
context you do not have, and this skill runs precisely when the session that
could have argued with it is gone.

Phase 3 of docs/harness-conversion-plan.md. The findings reach the next
session because a script read them off disk, not because a session remembered
to carry them.

## State-Inspection Probes
The probes no longer decide the stage; they fix the step inside the stage the
record named, and they still refuse the states below. Five probes run in
order: wave-map, worktree, branch, commits, checkpoint.
- Wave-map: the ID resolves to a row in waves.md; refuse otherwise.
- Worktree: exists at the sibling path? on the expected branch? clean or
  dirty? Refuse to resume a dirty worktree.
- Branch: wave-<id>-* exists locally? tip SHA captured.
- Commits: which stories have per-story commits already (foundation commit
  plus per-story pattern for parallel waves; per-story only for serial).
- Checkpoint: read .bmad/wave-<id>/checkpoint.json and the step-N.done
  markers. The router already reads both conventions to pick the step within
  the stage; this probe is what the commit probe is reconciled against, and a
  disagreement between markers and commits is reported, not resolved silently.

## Open-Questions Re-Check
Always re-run, regardless of checkpoint state, in case questions were
resolved (or new ones recorded) since the original dispatch. A wave the
SessionEnd hook blocked because `.bmad/wave-<id>/step-4.5.pending` was still
present when its session ended is cleared the way every block is: a human
records the answer, deletes the marker, and edits the record. This skill does
neither.

## --from-step Override
Warn-and-confirm semantics: print the routed step and the override, require
explicit confirmation before honoring the override. The override moves the
step, never the status: it cannot re-enter a blocked wave, and it cannot turn
a `done` wave's follow-up review pass back into a resumption.

## Error Handling
- Wave blocked: refuse; quote the router's stderr. Not clearable here.
- Wave record present with an unreadable status: refuse (exit 3). Repair the
  record or delete it; do not guess the status.
- Worktree deleted: cannot resume; re-run /bmad-dev-wave fresh (the wave map
  still stands).
- PR force-pushed by another session: report divergence; ask before
  continuing.
- Wave already merged and cleaned: nothing to resume; exit 0 with a note.
- HANDOFF.md Status red: refuse to resume without an explicit override.
- Evaluation record with no readable verdict (exit 3): refuse; repair or
  delete the record. Do not resume against a guess at what it said.

## Version history
- 1.4.0 (2026-10-01, R4 of docs/reviews/harness-engineering-review-v1.md):
  frontmatter only. `tools:` is a subagent field and did nothing in a skill;
  it is now `allowed-tools: Read Glob Grep Bash Skill(bmad-dev-wave *)`, which
  pre-approves those tools for the turn that invokes this skill and restricts
  nothing. `SlashCommand`, not a current tool, is gone: the Skill tool runs
  /bmad-dev-wave. `when-to-use` is `when_to_use`, the field Claude Code reads,
  as one string; `version`, `when-not-to-use` and `outputs` sit under
  `metadata:`.
- 1.3.0 (2026-09-11, Phase 4 of docs/harness-conversion-plan.md): names the
  step-4.5 pending marker and the SessionEnd block it produces, so a resumed
  wave blocked for an unanswered question is read as that and not as drift.
- 1.2.0 (2026-09-11, Phase 3 of docs/harness-conversion-plan.md): a wave with
  an open NEEDS_WORK evaluation re-dispatches with the evaluator's findings as
  its opening prompt, generated from the record on disk by
  bmad-dev-wave/scripts/evaluate_wave.py rather than recalled by whoever was
  in the room. That is the half of the generator-evaluator split this skill
  owns: findings that survive the death of the session that received them.
- 1.1.0 (2026-09-11, Phase 2 of docs/harness-conversion-plan.md): the
  re-entry stage comes from the wave's lifecycle status record rather than
  from this skill's own inference, and a blocked wave refuses here as it does
  everywhere else. The five probes stay, demoted from deciding the stage to
  fixing the step within it. The vocabulary is read from
  bmad-dev-wave/scripts/wave_status.py, which defines it once.

## See Also
- /bmad-create-wave: produces the wave map this skill reads.
- /bmad-dev-wave: the executor this skill re-dispatches.
- /bmad-status-wave: shares the state-inspection probe set; reports state
  without re-dispatching.
- /bmad-merge-wave: refuses to merge waves whose state this skill would
  refuse to resume.
- /bmad-wrap: surfaces in-progress waves at session-end and recommends this
  skill for the next session.
