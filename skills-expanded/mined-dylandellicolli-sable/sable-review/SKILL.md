---
name: sable-review
description: |
  Review accumulated SABLE methodology feedback captured by `sable-note`.
  Reads ~/dev-env/SABLE/feedback/*.md, classifies each observation
  (edit-SABLE / file-as-bead / discuss / discard), proposes specific changes
  with diffs, and after user approval, applies edits to SABLE.md and archives
  processed entries to feedback/processed/.
  Use when asked to "review SABLE feedback", "/sable-review", "what have I
  noted about SABLE", "process my sable-notes", or after a stretch of
  active work where observations have accumulated.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Bash
  - AskUserQuestion
---

# /sable-review

Curate raw SABLE feedback (captured via `sable-note`) into actionable changes.

## Inputs

- `~/dev-env/SABLE/feedback/*.md` — raw observations (skip `processed/` subdir)
- `~/dev-env/SABLE/SABLE.md` — current methodology
- `~/dev-env/SABLE/QUICKSTART.md` — current quickstart
- Recent git log for the SABLE repo — what's already been changed
- (Optional) the user's project context — to ground "is this still a real issue"

## Steps

### 1. Detect feedback

```bash
ls -1 ~/dev-env/SABLE/feedback/*.md 2>/dev/null
```

If the dir doesn't exist or no `.md` files: tell the user "No feedback to review. Capture observations with `sable-note '<text>'` first." Then stop.

### 2. Read all feedback files

Read every `feedback/*.md` (NOT `feedback/processed/*.md`). Parse entries — each is delimited by `---` and starts with a timestamp line.

For each entry, capture: timestamp, cwd, git context, observation text.

### 3. Read context

- Read `SABLE.md` (full file) so you know what's already covered.
- Read `QUICKSTART.md` so you know the public-facing entry point.
- Run `cd ~/dev-env/SABLE && git log --oneline -20 -- SABLE.md QUICKSTART.md` to see recent changes — avoid proposing things already done.

### 4. Classify each entry

Bucket into one of four categories:

| Bucket | Definition | Output format |
|--------|------------|---------------|
| **EDIT** | Specific, actionable change to SABLE.md or QUICKSTART.md | Section to edit, proposed diff (old_string → new_string) |
| **BEAD** | Real issue but the fix needs design/discussion before doc change | Suggested bead title, type, description, where to file (SABLE repo or other) |
| **DISCUSS** | Interesting observation but not yet clear what to do | Restate the observation, your read, the question for the user |
| **DISCARD** | Stale (already addressed), off-topic (not about SABLE methodology), or noise | Reason for dropping |

Be honest about uncertainty — if you can't tell whether something's actionable, put it in DISCUSS. The user is the final arbiter.

### 5. Present the triage report

Output a structured report grouped by bucket. For each entry include the original timestamp/cwd so the user can trace it back. Example shape:

```
## EDIT (3 items)

### E1 — `swarm validate output is too verbose for 50+ bead epics`
Source: 2026-04-15 09:14 · cwd: ~/dev-environment/internal-analytics

Proposed change to SABLE.md §6.5:
- Add a sentence after "Run this before creating worktrees" explaining
  that --verbose can be omitted on large epics for a summary view.

Diff:
  old: Run this before creating worktrees. If max parallelism is 2,…
  new: Run this before creating worktrees. (Skip --verbose on large
       epics — the default output is a summary; --verbose dumps the
       full graph and can be overwhelming past ~30 beads.) If max
       parallelism is 2,…

## BEAD (2 items)

### B1 — `bd q output should be optionally machine-readable`
Source: 2026-04-15 11:02 · cwd: ~/dev-environment/qbrs

Proposed bead (file in SABLE repo):
  title: bd q --json output mode for scripted capture
  type: feature
  priority: 3
  description: Currently `bd q "<title>"` prints the new ID to stdout
    among other text. Scripts (e.g. failure-trigger automations) need
    a stable, parseable format. Add --json to emit {"id": "..."}.

## DISCUSS (1 item)

### D1 — `worktree merge order matters more than docs suggest`
Source: 2026-04-15 14:30
The note observes that merging worktrees in arbitrary order causes
extra conflicts. Recommendation: should §6.4 add guidance on merge
order? Or is this case-by-case? Need your call.

## DISCARD (2 items)

### X1 — `bd close failed silently`  → already addressed in commit 88a7055 (added --verbose error mode to tdd-gate)
### X2 — `claude was rude to me`     → off-topic; not a SABLE methodology issue
```

Keep diffs short — show the meaningful changed lines, not the whole surrounding section.

### 6. Get user decisions

After presenting the report, ask the user to approve, modify, or reject each item. Use AskUserQuestion if the list is long (>5 items); for shorter lists just ask in a single message.

For each approved EDIT: confirm the exact diff before applying.
For each approved BEAD: confirm the bead spec before printing the `bd create` command.
For DISCUSS items: capture the user's resolution and reclassify (EDIT, BEAD, DISCARD).

### 7. Apply approved changes

- **EDITs**: use the Edit tool against `SABLE.md` or `QUICKSTART.md`.
- **BEADs**: do NOT auto-create. Print the exact `bd create ...` command for the user to run (or, if the user asks, run it from `~/dev-env/SABLE`). Beads belong in their target rig — don't assume.
- **DISCARDs**: no action beyond archiving.

### 8. Archive processed entries

Once all decisions are made, move processed entries out of `feedback/*.md` into `feedback/processed/YYYY-MM-DD-HHMMSS-review.md` with a header listing what each became:

```
# Processed feedback — 2026-04-15 16:42

Reviewed via /sable-review. Outcomes:

- E1 → SABLE.md §6.5 edit (commit pending)
- E2 → QUICKSTART.md prerequisites edit (commit pending)
- B1 → bead command provided to user
- D1 → resolved as: add merge-order guidance to §6.4 (now an EDIT)
- X1, X2 → discarded

(then the original entries, verbatim, for archive)
```

After moving, the active `feedback/*.md` files for those days should be left empty (just the header) or removed entirely if no entries remain.

### 9. Hand off

Report back to the user:
- N entries reviewed
- N edits applied (and to which files)
- N beads to file (with the exact commands)
- Reminder to commit + push the SABLE.md / QUICKSTART.md changes when ready

## Honesty rules

- Never silently apply a change. Every EDIT requires explicit user approval.
- Never auto-create beads — print the command, let the user run it.
- If a feedback entry references a part of SABLE.md you can't locate, put it in DISCUSS — don't guess at the section.
- If two entries contradict each other, surface the contradiction in DISCUSS rather than picking a winner.
- If you've reviewed the same observation in a previous run (check `feedback/processed/`), note it and propose to discard rather than re-litigating.

## When NOT to use this skill

- **Not for capture.** That's `sable-note`. Don't review one entry at a time as it's captured; let observations accumulate, then triage in batches.
- **Not for general SABLE questions.** "What does §6 say?" is just a Read on SABLE.md.
- **Not as a session-end ritual unless feedback exists.** Check the dir first; bail if empty.
