---
name: bmad-close-epic
description: >
  Per-epic closure gate. Wraps four Stage F sub-skills -- code-review,
  testarch-trace (requirements traceability), testarch-nfr (non-functional
  requirements), and the retrospective -- into a single gate. Operates on a
  docs-only branch (no production code changes), writes a consolidated
  SUMMARY plus four detail reports, feeds retrospective lessons into
  project-context.md, opens a pull request, and halts before merge. Refuses
  an epic any of whose waves landed without an adversarial review record.
when_to_use: |
  After every wave of the epic has been through /bmad-dev-wave and
  /bmad-merge-wave, and before starting the next epic -- including when
  /bmad-status-wave shows the epic as closure-pending.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
metadata:
  version: 1.4.1
  inputs:
    - >-
      epic-id (positional, required; integer matching the leading digits of a
      Wave label in the waves.md wave table -- waves.md carries one flat table
      for the whole project, ordered by execution rather than by epic, so there
      are no per-epic sections to match). No flags: closure is not tunable,
      there is no --dry-run, no --skip-subskill, no --force.
  output-locations:
    - _bmad-output/epic-closure/epic-<N>/SUMMARY.md
    - _bmad-output/epic-closure/epic-<N>/code-review.md
    - _bmad-output/epic-closure/epic-<N>/testarch-trace.md
    - _bmad-output/epic-closure/epic-<N>/testarch-nfr.md
    - _bmad-output/epic-closure/epic-<N>/retrospective.md
    - a docs-only branch pushed to origin, and a pull request against main
    - every existing story file of the epic set to Status: done
---

# bmad-close-epic

## The Six-Step Closure Workflow
1. Preflight: waves.md lists at least one wave for the epic; every wave of the
   epic is merged AND cleaned up; every story of the epic has landed; and
   every wave of the epic carries a review record. Any failure: refuse --
   partial closures produce misleading records. The fourth condition is not
   yours to judge: run the gate script below and obey its exit code. What
   counts as proof for the second and third conditions is further below.
2. Create the docs-only closure branch off main. No production code changes
   are permitted on it.
3. Run the four sub-skills in order -- code-review, testarch-trace,
   testarch-nfr, retrospective -- each returning a structured verdict
   (PASS / CONCERNS / FAIL) plus a report. A sub-skill that produces
   unparseable output is recorded as ERROR with a stub report embedding the
   raw response; the run continues.
4. Write the five Markdown files: the four detail reports plus SUMMARY.md,
   which carries the top-level status (GREEN if all PASS; YELLOW on any
   CONCERNS, FAIL, or ERROR), the four verdicts, and an epic-to-waves table
   so the closure reads standalone.
5. Feed the retrospective lessons into project-context.md so the next epic
   starts with them in context.
6. Commit the docs, push the branch, open the pull request -- ready-for-review
   when GREEN, draft when YELLOW -- and halt. Human review is the final gate;
   this skill never merges.

## What preflight accepts as proof

**A wave is merged and cleaned up** when its pull request reads merged, no pull
request against the repository is open for its branch, and no worktree in
`git worktree list` carries its branch. Live state, checked at invocation.

Not an archived checkpoint file. An archive is a proxy for those facts and a
weaker one, since it is a file on disk that says cleanup happened rather than
evidence that it did; the live checks are the facts themselves. Read the
archive when it exists, for the step record it carries, and never refuse for
its absence.

Merged is `state == "MERGED"` from
`gh pr view <branch> --json number,state,mergedAt,mergeCommit`. There is no
`merged` field; naming it makes `gh` reject the whole call.

**A story has landed** when the wave carrying it is merged by the rule above.
A story file is read when it exists and is not required: a wave scaffolds its
stories inside its own worktree, and a wave may land without one. The ruled
acceptance criteria live in the epics document, which is the source the
traceability pass reads in either case. Refuse for a story whose wave never
merged, never for a story whose file was never written.

## The review-record gate

The fourth preflight condition is decided by a script, not by you:

    python3 {skill-root}/scripts/check_review_records.py \
        --project-root {project-root} --epic <N>

Exit 0 proceeds. Exit 1, 2 or 3 is the refusal; quote its stderr, which names
the wave and the remedy. There is no flag and no override. Do not re-derive
the verdict by reading files yourself, and do not proceed on a non-zero exit
because the gap looks defensible -- arguing the exception is exactly the step
this gate exists to remove.

  0  every wave carries a record, or lacks one lawfully (pre-rule)
  1  a wave landed on or after the rule date with no record
  2  structural: no wave map, or the epic has no waves in it
  3  a wave with no record could not be dated

The same script also runs from the PreToolUse hook the moment anything is
written under `_bmad-output/epic-closure/epic-<N>/` (Phase 4 of
docs/harness-conversion-plan.md, `bmad-dev-wave/scripts/wave_gate.py`). A
closure whose gate fails cannot be written, whether or not step 1 ran the
script; the hook's stderr carries the same refusal.

**A wave carries a review record** when `docs/wave-<id>/review-party.md`
exists, or when `docs/wave-<id>/api-surface.md` carries a "Party-review
amendments" section (the wave directory is lower-cased: wave 6A is
`docs/wave-6a/`). The first is canonical and is what /bmad-dev-wave 1.1.0
writes; the second is the recognized alternative waves 2B, 5C and 5D used,
and it is a real reachable record, so it counts. A record whose findings live
only in a commit message does not count, which is the whole point.

Required by settled-decisions register row 51 (RQ, 2026-09-10). The evidence
that earned it: waves 4A, 4B, 5A and 5B produced no such file, and in both
Epic 4 and Epic 5 those are exactly the waves carrying the acceptance clauses
nothing asserts, while wave 5A's own CRITICAL finding is discoverable only by
reading a commit message.

**The requirement is prospective, from 2026-09-10.** A wave that landed before
that date and carries no record is recorded in the closure's own code-review
pass as a pre-rule gap, with its severity argued there, and never refused.
Applying the rule backwards would block closures over waves that landed before
it existed, which buys no safety. The known instances at ruling time are waves
1A, 3C, 4A, 4B, 5A, 5B and 6A; of those only **wave 6A** belongs to an epic
still open, so Epic 6's closure is the one that will meet this and should
expect to record it rather than refuse. Refuse only a wave that landed on or
after the ruling date with no record.

**Landing dates come from git, not from GitHub.** The script finds the commit
that added anything under `docs/wave-<id>/`, then the merge that brought it to
this branch, and dates the wave by the merge. Not by the commit: a wave's docs
are written on its own branch and reach the closing branch only when the wave
merges. Measured across one instance's eighteen waves that lag runs from six
minutes to forty-six hours, and one wave's commit and merge fall on opposite
sides of the rule date -- dating by the commit would pass it as pre-rule when
its merge says refuse. A repository that squashes or rebases has no merge
commit to find, and there the commit's own date already is its landing date.

The wave map's "Branch suffix" column cannot address
a pull request: real head refs carry tool prefixes and disambiguating hashes,
and some do not share a slug with the column at all, so `gh pr view
<branch suffix>` resolves nothing. A substring search over pull requests is
worse -- a wave whose merge-cleanup branch also carries the wave label matches
twice, and which one you take changes the date.

A wave the script cannot date does not get the benefit of the doubt. An
undatable wave has no `docs/wave-<id>/` on this branch, which means it has not
landed, which is a different refusal than a missing record and is named as
one.

## Story status is this skill's to set

`bmad-dev-story` ends a story at `review` and no other skill writes `done`, so
before this rule every story sat at `review` after merging and a preflight
demanding `done` could never pass. Passing this gate is the acceptance event,
so the closure owns the transition.

At step 6, with all four verdicts written, set every story file of the epic
that exists to `Status: done` and record the ruling in the file. Do this on the
docs-only branch with the reports, so the status moves in the same pull request
that justifies it. A story with no file needs nothing. Never set `done` before
the four passes have run: the gate is what the status attests to.

Ruled by RQ in chat, 2026-08-24, at the Epic 1 closure.

## Idempotency
Re-invocation against the same epic and git state reproduces the same
verdicts (modulo bounded sub-skill non-determinism) and overwrites the same
five files on the same branch.

## Refusals
- Some wave not cleaned up: name it, and name which check failed (pull request
  unmerged, pull request open, or worktree still carrying the branch); run
  /bmad-merge-wave first.
- Some wave landed on or after 2026-09-10 with no review record: the gate
  script exits 1 and names the wave and both accepted locations. Quote it.
  There is no flag; the remedy is to write the record, which means the review
  has to have happened. A wave that landed before that date is recorded as a
  pre-rule gap, not refused.
- Some wave with no review record cannot be dated: the gate script exits 3.
  The wave has not landed here, so run or merge the wave; the missing record
  is not what blocks you.
- Epic has zero waves: refuse (planning error or typo). The gate script exits
  2 for this and for a missing wave map.
- Closure branch already exists: refuse; delete or rename it explicitly.
- Main diverged since the waves merged: refuse; reconcile main first. Local
  main merely behind origin is not divergence: fast-forward and continue.

## Version history
- 1.4.1 (2026-10-01, R4 of docs/reviews/harness-engineering-review-v1.md):
  frontmatter only. `when-to-use` is `when_to_use`, the field Claude
  Code reads, so it now reaches the skill listing; `version`, `inputs` and
  `output-locations` sit under
  `metadata:`, which Claude Code leaves to the fork's own tooling. Nothing in
  the body changed.
- 1.4.0 (2026-09-11, Phase 4 of docs/harness-conversion-plan.md): the gate is
  enforced by the PreToolUse hook as well as by step 1. Writing any closure
  artifact for an epic whose gate exits non-zero is denied at the tool call.
  The rule and the script are unchanged.
- 1.3.0 (2026-09-11, Phase 1 of docs/harness-conversion-plan.md): the review-
  record condition moves from prose into
  `scripts/check_review_records.py`, which the skill calls and whose exit code
  is the verdict. The rule is unchanged; what changed is that refusing no
  longer depends on the closing agent choosing to refuse its own work. Two
  corrections fell out of writing it against the real artifact instead of the
  documented one: waves.md carries a single flat table ordered by execution,
  not `## Epic <N>` blocks (the frontmatter said otherwise and nothing had
  checked), and wave directories are lower-cased, so a gate built on the Wave
  column's own spelling would have found no records at all. Dating a wave now
  uses the first commit that added its docs directory; the wave map's "Branch
  suffix" column is an intention rather than a record and resolves no pull
  request. A wave is dated by the merge that brought its docs to the closing
  branch, not by the commit that wrote them: the lag between the two reaches
  forty-six hours in the instance this was measured against, and wave 5D's
  commit and merge straddle the rule date.
- 1.2.0 (2026-09-10, founder ruling, settled-decisions register row 51):
  preflight adds a fourth condition, that every wave of the epic carries a
  review record at `docs/wave-<id>/review-party.md` or as a "Party-review
  amendments" section in its api-surface pin. Prospective from the ruling
  date, so a wave that merged earlier is recorded as a pre-rule gap rather
  than refused; wave 6A is the one such wave in an epic still open. The
  companion half of the row lives in /bmad-dev-wave 1.1.0, whose step 1 now
  refuses to open a wave while an earlier epic is closure-pending -- the
  state this skill's own absence created when Epic 4's gate was skipped and a
  wave 4B correctness defect survived four later waves.
- 1.1.0 (2026-08-24, founder ruling at the Epic 1 closure): preflight proves
  cleanup from live pull-request and worktree state instead of an archived
  checkpoint file, which /bmad-merge-wave never wrote here; a story with no
  story file no longer blocks, since a wave may land without one; the skill
  now owns the `review` to `done` transition, which nothing previously wrote;
  the `gh --json merged` field corrected to `state`/`mergedAt`; local main
  behind origin named explicitly as not divergence.
