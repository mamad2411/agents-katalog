---
name: update-briefs
description: >
  Updates the briefs/ shared memory directory after a sprint completes.
  Reads sprint outputs and writes structured summaries for other agents.
  Use after any sprint completes, or when the user says "update briefs",
  "sync state", "update project state", or "what changed". Also use
  automatically after /capture-lessons or after any significant project
  change, deployment, or decision.
---

# Update Briefs

You are updating the shared memory (briefs/) after a sprint. Your job is
to keep all strategic agents informed of the current project state.

## Step 1 — Determine current sprint

Find the latest sprint directory in `tasks/sprints/` (highest number).

## Step 2 — Read sprint outputs

Read ALL available sprint output files:
1. `tasks/sprints/sprint-XX/plan.md`
2. `tasks/sprints/sprint-XX/build-output.md`
3. `tasks/sprints/sprint-XX/review-output.md`
4. `tasks/sprints/sprint-XX/fix-output.md`
5. `tasks/sprints/sprint-XX/redteam-output.md` (if exists)
6. `tasks/sprints/sprint-XX/retrospective.md` (if exists)

Also read the current `briefs/project-state.md`.

## Step 3 — Update project-state.md

Overwrite `briefs/project-state.md` with:

```markdown
# Project State

Last updated: [date] — Sprint [XX]

## Current state
[What the project does right now, what's deployed, what works]

## Last sprint summary
Sprint [XX]: [theme]
- Completed: [tasks done]
- Issues found: [critical/major from review]
- Tests: [passing/failing count if known]

## Open items
- [Deferred issues from review/fix]
- [Items added to backlog]

## Next priorities
- [What should be done next based on backlog + retro]

## Blockers (manual actions needed)
- [Things that require human intervention]
```

## Step 4 — Update marketing-sync.md

Append to `briefs/marketing-sync.md` with user-facing changes only:

```markdown
### Sprint [XX] — [Date]
**User-facing changes**:
- [New feature / fix visible to users]

**Messaging angle**: [How to communicate this]

**Not for marketing** (internal only):
- [Technical changes not relevant to users]
```

If the sprint had no user-facing changes, skip this step.

## Step 5 — Update blockers.md

If any manual actions were discovered during the sprint (deploy steps,
config changes, external service setup), append to `briefs/blockers.md`.

## Step 6 — Update decisions-log.md

Append technical decisions made during the sprint to `briefs/decisions-log.md`.

## Step 7 — Weekly debrief (conditional)

If it's end of week (Friday) or the user requests it, generate
`briefs/weekly-debrief.md` with a summary of the week's sprints.

## Channel mode (remote execution)

If invoked via Channel (Telegram/Discord), adapt your output:
- Send a SHORT summary (5-10 lines max) via the Channel reply
- Full updates go in the briefs/ files as usual
- End with: "Briefs updated. Ready for next sprint or QA review."
- Keep Channel messages concise — the human is likely on a phone

## Gotchas
- project-state.md is overwritten (current state), not appended. decisions-log.md is appended (history).
- marketing-sync.md: only include changes visible to end users. Internal refactoring is not marketing content.
- If a sprint had no user-facing changes, don't add an empty entry to marketing-sync.md.
- Read the existing briefs/ content before writing — don't lose context from previous updates.

**STOP. Your deliverable is updated briefs/ files.**
Do NOT start the next sprint or invoke QA.
