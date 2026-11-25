---
name: handoff
description: Capture a focused slice of the current work — a bug, a newly-discovered piece of work, or some other context — into a handoff document a fresh agent can pick up and continue without re-deriving everything. Requires an argument naming what the handoff is about.
---

# Handoff

Distill the current work into a **focused context package** a fresh agent can run with. A handoff
is **not** a transcript summary — it's the intersection of two inputs:

> The **argument** scopes the doc and picks the template (what this is about). The **current
> conversation** is the source it distills. Extract from the conversation only what's relevant to
> the argument; verify state claims against git and disk; never dump the whole transcript.

## Require an argument

The argument names the subject. **If none was passed, stop and ask the user what the handoff should
be about** — do not fall back to summarising the whole conversation. A handoff with no subject has
no scope and is worthless.

## Pick the template

Infer the intent from the argument and conversation, **announce which template you're using**, and
let the user override:

| Intent | Meaning | Template |
|--------|---------|----------|
| **bug** | Go *fix* this known problem | `bug-handoff.md` |
| **feature-pivot** | Go *explore/build* a *new* thing we just discovered | `feature-pivot.md` |
| **general** | Anything else — continue/transfer some other context | inline spine (below) |

`feature-pivot` is forward-looking — a new idea surfaced in the current work, spun off for a fresh
agent. It is *not* parking-and-resuming existing work. When the argument fits neither bug nor
feature-pivot, use the **general** spine:

> **Objective · Context · What's been done/tried · Relevant files & locations · Where it stands ·
> Next steps · Gotchas · Suggested skill (`talk-it-through`)**

Read the chosen template file before writing, and follow its section set.

## Write the doc

- **Source it from the conversation, scoped by the argument.** Pull what we tried, the files we
  touched, the decisions reached, the dead-ends, the insight that sparked the idea — only the parts
  relevant to the subject. Drop incidental chatter.
- **Verify state against git and disk, not memory.** Any "done so far" / "files changed" claim gets
  checked before it goes in.
- **Reference, don't duplicate.** Plans, ADRs, PRDs, issues, commits, diffs — link by path or URL,
  never copy their content in.
- **Terse and complete.** No `write-well` pass — this is a precise working doc for an agent. Value
  is in `path:line` precision and "why this failed," not voice. Aim for a screen or two; longer only
  when the bug or idea genuinely demands it. No filler, no restating the obvious.
- **Suggest only the single natural next step**, not the whole downstream pipeline — bug →
  `diagnose`, feature-pivot/general → `talk-it-through`. The user invokes anything further.

## Save and hand off

- Path: **`handoffs/<branch>/<slug>.md`**, where `<branch>` is the current git branch (its slashes
  become folders) and `<slug>` derives from the argument
  (`handoffs/feature/synthetic-interview-evals/transcript-reset-bug.md`). Overwrite if it already
  exists.
- **Ensure `handoffs/` is ignored locally** — check `git check-ignore -q handoffs/`; when it is
  not ignored, append `/handoffs/` to `$(git rev-parse --git-common-dir)/info/exclude`, never to the tracked `.gitignore`. The
  handoff is ephemeral, not repo history.
- **Print the path and a ready-to-paste resume line** for the next session, e.g.:
  `Next session: read handoffs/<branch>/<slug>.md and continue.`
