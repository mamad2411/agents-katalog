---
name: implementation-notes
description: >-
  Keep a running implementation-notes.md logging decisions, plan
  deviations, and surprises during implementation. Use PROACTIVELY the
  moment you start implementing an agreed plan, spec, or decision — the
  trigger is you beginning the work, not the user's wording: terse
  approvals ("开搞", "go ahead", "LGTM"), incremental starts
  ("先做第一步"), resuming across sessions, or starting from a
  reference-hunt taking list. If you notice mid-implementation it is
  missing, create it and backfill. Also use when the user says
  "keep implementation notes", "记录实现笔记". Not for post-hoc
  summaries of already-finished work.
---

# Implementation Notes

No plan survives contact with the codebase. Log what changed and why, without
stopping the work.

## Workflow

1. **At the start of implementation**, create `implementation-notes.md` in
   the project root. If the file already exists, do not overwrite it — when
   its latest section is this same task, keep appending there; otherwise
   append a new `# Implementation Notes — <task name> (<YYYY-MM-DD>)`
   section at the end, opening with the same AGENT comment as the template
   below. Do not commit the file unless the user asks (once committed,
   the exclude stops applying — keep later edits out of unrelated commits).
   If this is a git repo, exclude it locally (not `.gitignore` — that would
   show up in the diff):
   `n=implementation-notes.md; p="$(git rev-parse --git-path info/exclude 2>/dev/null)" && { mkdir -p "$(dirname "$p")" && { grep -qxF "$n" "$p" || echo "$n" >> "$p"; }; } 2>/dev/null || echo "note: could not exclude $n — leaving it untracked, never staging it"`
   (worktree-safe; if the write is blocked, leave the file untracked and
   never stage it). Structure:

```markdown
# Implementation Notes — <task name> (<YYYY-MM-DD>)
<!-- AGENT (re-read this even after context compaction): running log for this
task. (1) Log every decision and deviation immediately, 1-3 lines each;
deviations as: plan said / found / did instead / why. (2) Re-read this file
before every commit and after each completed todo; log anything the plan
didn't say before moving on. (3) Never commit or stage this file. (4) Before
the session ends: re-read it, give the user a digest of THIS task's
Deviations and Open Questions, and remind them to feed this file into the
next planning round (or pitch-explainer / change-quiz). Full workflow: read
the implementation-notes skill. -->

## Context
Links to the plan/spec/prototype/taking list this run is based on (e.g.
implementation-plan.md, ./design-directions/). If the plan lives only in
chat, restate its one-line goal and key decisions here.

## Decisions
Choices made where the plan was silent. One line each: what + why.

## Deviations
Where reality forced a change from the plan.
Each entry: what the plan said / what was found / what was done instead / why.

## Surprises & Open Questions
Edge cases, dead code, wrong assumptions in the plan — anything the next
planning session should know.
```

2. **During implementation**, when an edge case forces a choice the plan
   didn't anticipate: pick the conservative option (smallest blast radius,
   easiest to reverse), log it under Deviations, and keep going. Only stop to
   ask the user when the deviation would invalidate the plan's goal.
3. **Update the file as you go**, not retroactively at the end. Entries are
   one to three lines; this is a log, not documentation. To keep the log
   alive across long sessions: re-read `implementation-notes.md` before
   every commit and after completing each todo item — if you did something
   the plan didn't say and it's not in the file, log it before moving on.
   If you notice only after a commit that an entry is missing — or that no
   notes file exists at all — log it or create it now and backfill; a late
   entry beats a lost one. If you keep a todo list, make "update
   implementation-notes.md and give the digest" the final item.
4. **At the end of the session**, re-read the file and give the user a brief
   digest of this task's Deviations and Open Questions — the discovered
   unknowns the next planning round needs. If this task answered an older
   section's Open Question, mark it resolved in place. The digest is the
   immediate confirmation; the file is the cross-session handoff. Close by
   reminding the user to feed `implementation-notes.md` into the next
   planning round (or pitch-explainer / change-quiz if this work heads to
   review).

## Rules

- If the change is a single commit's worth of work with no written plan to
  deviate from, skip the file — say so in one line and just do the work.
  Deviations cannot exist without a plan.
- An explicit user opt-out ("别整笔记", "no notes file") overrides
  PROACTIVELY: skip the file and keep deviations visible in chat instead.
- Never silently deviate from the agreed plan; every deviation gets an entry.
- Cosmetic differences (naming, equivalent APIs) are not deviations unless
  they change behavior or interfaces.
- Do not duplicate what git already records (diffs, file lists); record the
  reasoning that a diff cannot show.
- If another agent may share this checkout, treat the file as append-only:
  re-read it right before writing, and if it changed since you last read it,
  merge your entries after the new content instead of overwriting.
- When implementing in parallel worktrees (e.g. best-of-n runners), keep one
  notes file per worktree; info/exclude is shared, so one exclude run covers
  all worktrees. `git worktree remove` silently deletes the excluded notes
  file — before removing any worktree, append its sections to the main
  checkout's implementation-notes.md (a runner that cannot write there must
  carry its digest in its final report). At integration time, run
  `git worktree list`, collect every remaining notes file into the main one
  as dated sections, then give one combined digest.
