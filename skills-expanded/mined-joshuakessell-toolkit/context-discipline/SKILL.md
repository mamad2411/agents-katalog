---
name: context-discipline
description: Stage-aware context management for a build session — what to compact, when, with exact /compact instructions per phase. Use at every checkpoint transition, when context grows past roughly half, when logs or debugging transcripts pile up, or when the user asks about context, compaction, or token usage.
---

# Context Discipline

/compact is a user command and it accepts instructions. A bare /compact makes the model
guess what mattered; a targeted one states it. At each transition, hand Joshua the exact
command to type — specific preserve/drop lists, derived from what just happened.

## The phase map

**After the plan is agreed (~8%)** — intake Q&A, scoping deliberation, and pack-install
output are dead weight; the decisions live in CLAUDE.md. Suggest:
`/compact keep the agreed MVP list, cut list, checkpoint clock times, and stack choices; drop the intake discussion and installation output`

**After the skeleton ships (~17%)** — scaffold output, dependency install logs, and deploy
logs are the bulk. Suggest:
`/compact keep the project structure, route map, env var names, and production URL; drop scaffold and install logs`

**During the core-loop build (17→50%)** — do NOT compact mid-feature; active working state
is the one thing compaction can damage. Prevent pollution instead: send doc lookups,
codebase exploration, and research to subagents so raw output never enters the main
thread. If an entire approach gets abandoned, that's the exception:
`/compact preserve the current working approach and data model; drop the abandoned <X> attempt entirely`

**After the core loop is verified (~50%)** — debugging transcripts of now-fixed bugs are
the largest garbage class in any session. Suggest:
`/compact keep final implementations and a one-line summary of each fix; drop the debugging back-and-forth`

**At feature-complete (~75%)** — before polish begins:
`/compact keep component interfaces, the styling tokens from CLAUDE.md, and the list of known rough edges; drop feature implementation details`

**Never compact** in the middle of debugging an active failure, or immediately before
/ship — both need recent turns intact.

## Cadence and signals

- Check /context at each checkpoint (it's part of /timecheck's answer). Act on composition,
  not a schedule: compact when the window is fat with logs and transcripts, not because
  time passed.
- The event to preempt is auto-compaction — hitting the limit means an unchosen, untargeted
  summary at an arbitrary moment. Deliberate beats forced, every time.
- /clear is for switching to genuinely unrelated work — rare inside one build. Losing the
  session's decisions to save tokens is a bad trade; that's what targeted /compact avoids.
- State each suggestion once, plainly, with the command ready to copy. If declined, don't
  re-raise until the next transition.
