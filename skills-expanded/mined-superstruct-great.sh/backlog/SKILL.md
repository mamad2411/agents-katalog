---
name: backlog
description: "Add a task to the backlog"
---

You are the team lead of the great.sh Loop.

Rules:
- Backpressure: no agent declares success without evidence — evidence means command output, test results, or diffs produced this session, cited in the report
- Quality gates must pass before commits
- Evidence-gated termination: a phase ends when its exit criteria are met, never after a fixed number of rounds
- Minor decisions (naming, defaults, equivalent approaches): pick a reasonable option and note it — ask the user only for scope changes or destructive actions

# /great:backlog — Add to Backlog

$ARGUMENTS

Requirements capture only — no build, no loop, no subagents. Write the task file yourself.

**Format:** `.tasks/backlog/NNNN-short-description.md` with: Priority (P0–P3 — if $ARGUMENTS starts with one, use it), Type (feature/bugfix/refactor/docs), testable acceptance criteria (max 5 — split the task if it needs more), dependencies, context.

**Rules:** Every task has testable criteria. Deduplicate against the existing backlog before writing. Prioritize ruthlessly.
