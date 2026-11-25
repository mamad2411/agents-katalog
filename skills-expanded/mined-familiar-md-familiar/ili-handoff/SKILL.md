---
name: ili-handoff
description: Hand off work — park or resume in-flight work across a session boundary, or draft a brief for someone outside familiar. Routes to one branch and runs only that one.
disable-model-invocation: true
---

# familiar — Handoff

A **menu, not a procedure**. It names the two ways work leaves this session — to a later session of
the same project, or to someone who has no access to this project at all — and hands off to exactly
one of them. It reads no project state itself and writes nothing.

## Context contract

- **Required context:** this menu only
- **Conditional context:** exactly one file under `references/`, only when step 1 selects that branch. The selected branch's own context contract governs from that point; nothing else in `references/` is opened.
- **Excluded context:** `5-System/Memory/`, `4-Trackers/`, `Knowledge`, `Inputs`, other projects, and undeclared extension content — the menu itself opens no project content.
- **Updates:** `nothing`. Every write belongs to the selected branch and is declared in that branch's own contract
- **Capabilities:** file-read. Optional capabilities must degrade as the procedure states.
- **Completion:** One branch is selected, its reference file is loaded, and its procedure runs under its own contract — or the user is told no branch fits and nothing is opened.

## Step 1 — Select the branch

If the user already named one ("park this for later", "resume the handoff", "write a brief for
Sarah"), skip the question and go straight to it. Otherwise present these two and ask which:

| Branch | Reference | What it does |
|---|---|---|
| **Session handoff** | `references/session-handoff.md` | Park in-flight work for a later session of this project, or resume an open handoff. |
| **Assignment brief** | `references/assignment.md` | Draft a standalone task brief for a coworker or an AI agent to pick up work outside familiar. |

If the request matches neither, say so and stop. Do not pick the nearest branch, and do not open a
reference file to find out whether it fits — the table above is the whole basis for the match.

## Step 2 — Run the selected branch

Load that one reference file. From there its own **Context contract** governs — its Required,
Conditional, Excluded, Updates, Capabilities, and Completion declarations replace this file's, which
covered only the menu. Do not load a second branch.

## Guardrails

- **Every branch here is user-started.** This skill carries `disable-model-invocation: true`, so a
  route match never opens it and never opens anything under `references/` — `routes.md` Resolution
  rule 3 applies to the menu, which is what keeps it applying to both branches. Identify the branch
  that fits, tell the user the command, and stop.
- The menu never performs a branch's work itself, never partially applies one, and never substitutes
  a lighter action because a branch looked heavy.
- Nothing under `references/` is a skill. Each is a procedure this menu selects; none is separately
  invocable, and none may be opened without a selection in step 1.
