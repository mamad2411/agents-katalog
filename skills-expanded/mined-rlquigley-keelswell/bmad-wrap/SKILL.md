---
name: bmad-wrap
description: >
  Session-end triage. Triages session learnings into auto-memory (CLAUDE.md
  edits are rare and hard-capped), checks active plans, reconciles TODO.md
  and HANDOFF.md, confirms the wrap, proposes next-session options
  with one tagged recommended, generating a copy-pasteable kickoff
  prompt, suggested run mode (auto, accept edits, plan, manual),
  model, and effort level (low, medium, high, extra, ultracode) from
  the user's selection, names the session (32 characters max)
  from a session summary, and ends with the PR closeout: the
  reconciled TODO.md and HANDOFF.md are committed to ride the working
  branch's PR, opened on confirmation if missing, or held on until an
  existing open PR is merged and validated. Run at the end of every
  working session, whether or not a wave was active.
when_to_use: |
  At the end of every working session. A finished wave needs its learnings
  captured; an unfinished wave needs a handoff the next session can resume
  from; the same discipline covers both.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash          # read-only allow-list: git status, git log, git diff,
                  # git branch, date, gh pr list / view. Sole exception,
                  # gated on the user's step-5 confirmation: step 6's
                  # git add/commit of TODO.md + HANDOFF.md, git push of
                  # the working branch, and gh pr create. No other
                  # mutating git commands, ever.
  - Write         # writable surface: _bmad-output/session-wrap/**,
                  # TODO.md, HANDOFF.md; CLAUDE.md is readable but NOT
                  # on any writable path
metadata:
  version: 1.10.0
  inputs:
    - --scope=session|day|since=<git-ref>   # contradiction-scan window;
                                            # default session
  output-locations:
    - _bmad-output/session-wrap/<UTC-timestamp>/triage.md
  exit-codes:
    - 0: wrap complete (findings or no findings -- findings are the product)
    - 1: the triage report itself could not be written (disk full, permission)
---

# bmad-wrap

## Preflight: confirm the working tree

Before step 3 touches TODO.md or HANDOFF.md, and again before step 6 commits,
run `git rev-parse --show-toplevel` and `git branch --show-current`. Compare
the toplevel against the directory this session has actually been reading
and writing project files in. A worktree recycled or removed mid-session
(the session's original worktree gone, a new one created, or the invocation
silently landed back in the main checkout) is the single most common way a
wrap goes wrong: it reads or writes the right file at the wrong checkout, and
the resulting edit or commit lands on the wrong branch entirely. If the
toplevel or branch does not match what the session expects, stop and
reconcile before writing anything -- copy in-memory edits to the correct
worktree, or re-derive them there, rather than committing from the wrong
one. Never assume the shell's cwd carried over correctly; re-verify it right
before each write, not once at the start.

## The Six-Step Workflow
1. Triage session learnings. Default destination is auto-memory
   (~/.claude/projects/<project-slug>/memory/). CLAUDE.md additions are
   hard-capped at ZERO per session by default; a candidate edit must pass all
   four checks to even be proposed: durable (applies indefinitely),
   project-wide (not one module or feature), not already covered, and not
   contradicting any existing CLAUDE.md rule. Edits failing any check route
   to auto-memory.
2. Check active plans and in-flight waves (via /bmad-status-wave's probe
   set); surface closure-pending epics.
3. Reconcile TODO.md: re-run the Preflight check first. Remove items whose
   PRs merged AND items the working branch's PR completes (their closure
   rides the PR that completes them, per step 6), so TODO.md holds open
   items only; list each removal in the triage report under a Closed
   heading; refresh the Last updated line. Closure history lives in the
   triage reports and TODO.md's git history, never as a growing section of
   TODO.md itself.
4. Reconcile HANDOFF.md: rewrite the Current State table (Stage, Wave, Step,
   Status traffic light), Key Design Decisions Since Last Handoff,
   Blocked-On, and the forward-looking Next Session Proposal -- an
   options list with one recommended, the user's selection, and the
   kickoff prompt and run-mode, model, and effort suggestions
   generated from it (see The Next Session Proposal).
5. Confirm the wrap; write the triage report; restate the selected
   option with its kickoff prompt block and run-mode, model, and
   effort lines; name the session (see The Session Name). This
   confirmation is also the gate for step 6's commit, push, and PR
   creation.
6. PR closeout, always last. Re-run the Preflight check first -- committing
   from the wrong worktree here silently lands the reconciled files on the
   wrong branch. Check unpushed commits (`git log
   @{u}..` per branch) and the working branch's PR state (`gh pr
   list --head <branch> --state all`), then:
   - No PR: commit the reconciled TODO.md and HANDOFF.md on the
     working branch, push, and open the PR (gated on step 5's
     confirmation) -- the PR carries the session's work and the
     bookkeeping together.
   - PR open, not merged: commit TODO.md and HANDOFF.md on the
     branch and push (same gate) so the PR picks them up; halt and
     ask the user to merge. When the user reports it merged,
     validate with gh (state MERGED); on a failed validation, say so
     and ask again -- never proceed on an unvalidated claim.
   - PR already merged before the wrap: nothing to open; the
     TODO/HANDOFF updates have no open PR to ride -- report them
     uncommitted and leave the decision to the user.

## The Contradiction Scan (step 1 support)
Before proposing any CLAUDE.md edit, scan existing CLAUDE.md for any rule the
edit would supersede or undermine, over the --scope window; on any hit,
resolve the contradiction first or route the learning to auto-memory. Cap
the surfaced list at the top 20 contradictions.

## The Next Session Proposal (step 4 support)
The proposal is a selection dialogue, not a single suggestion:
1. Draft two to four candidate options for the next session's work,
   drawn from step 2's findings (in-flight waves, closure-pending
   epics, blocked items) and open TODO.md entries. Each option is one
   or two lines: the work, and why it is a candidate now.
2. Tag exactly one option "(recommended)", with a one-line reason.
3. Present the list and wait for the user to select an option.
4. Generate the kickoff prompt from the selected option: exactly one
   fenced code block, a copy-pasteable first message for the next
   session. It must be self-contained -- name the skill or command to
   invoke, the target (wave, story, epic, or standalone task), and the
   key file paths -- and must not depend on the wrapped session's
   context to make sense. The prompt always instructs the session to
   create a new branch (named for the work) and work in it, never
   directly on main.
5. With the prompt, suggest the mode to run it in -- auto, accept
   edits, plan, or manual -- matched to the selected work: plan for
   unscoped or design-heavy work, accept edits for well-specified
   implementation, auto for mechanical low-risk work, manual when the
   work is risky or destructive. Suggest the model the same way --
   e.g. fable or opus for design-heavy, ambiguous, or high-risk work,
   sonnet for well-specified implementation, haiku for mechanical
   low-risk work; name whatever tiers are current. Suggest the effort
   level too -- low, medium, high, extra, or ultracode -- scaled to
   how much the work has to be reasoned through rather than typed:
   low for mechanical edits, medium for routine implementation, high
   for design or debugging, extra for the hardest single-session
   problems, ultracode only when the work genuinely wants multi-agent
   orchestration (it is opt-in and costly; never suggest it by
   default). Three lines directly below the prompt block: the mode,
   and why; the model, and why; the effort level, and why.
Step 4 then writes the full options list, the selection, the kickoff
prompt block, and the run-mode, model, and effort lines into
HANDOFF.md's Next Session Proposal; step 5 repeats the block and all
three lines verbatim in the triage report and in the wrap
confirmation, so the prompt is at hand both at wrap time and when the
next session opens HANDOFF.md.

## The Session Name (step 5 support)
Step 5 ends by naming the session. Write a one-or-two-sentence
summary of what the session actually did, then derive the session name
from that summary: at most 32 characters, ASCII. The cap is hard --
count before emitting. The summary and name close the triage report,
and the name is the last line of the wrap confirmation, ready to use
as the session title.

## Report
Exactly one file per invocation: _bmad-output/session-wrap/<ts>/triage.md,
where <ts> is the invocation's UTC minute (colons replaced by hyphens, e.g.
2026-07-01T22-30-00Z). A second run in the same minute overwrites; a later
run creates a new directory. No locking; a lost report is regenerated from
fresh inputs.

## Error Handling
- CLAUDE.md does not exist: warn; steps 3-6 still run; step 1 routes
  everything to auto-memory.
- No active waves: steps 2's wave portion is a clean no-op.
- /bmad-status-wave output malformed: degrade to direct probes; note it.
- User does not select an option: the recommended option is treated as
  selected; the report notes the default was taken.
- No remote or gh unavailable at step 6: report the PR gap and print
  the would-be commands; never fail the wrap over it.
- User declines to merge at step 6: proceed; record the open PR in
  the report and under HANDOFF.md's Blocked-On (a follow-up commit
  riding the same open PR, same gate).
- Session ran directly on main (no working branch): skip step 6's
  commit and PR entirely; report the reconciled files as uncommitted
  and note the kickoff prompt's new-branch rule exists to prevent
  this.
- Preflight toplevel/branch mismatch at step 3 or step 6: stop before
  writing; reconcile the edits into the correct worktree first. Do not
  write or commit from a checkout other than the one the session has
  been working in.
- Wave gate denies a write after this session's step-8 NEEDS_WORK
  (`DENIED (in-place)`): the session built the wave and may not edit its
  worktree, and a session rooted in that worktree is usually refused the
  main checkout too. The gate exempts one path, to the Write tool only:
  `_bmad-output/session-wrap/` inside the wave's worktree. Write the
  triage report there with the Write tool, never through Bash. TODO.md,
  HANDOFF.md and step 6's commit stay denied: put their reconciled text
  in the report under "Owed by the next session", leave the report
  uncommitted, and say so in the confirmation. /bmad-resume-wave's
  session commits it on the wave branch. Do not route around the gate
  through another tool or another checkout.
- Disk full or output directory unwritable: exit 1 (the only error exit).
