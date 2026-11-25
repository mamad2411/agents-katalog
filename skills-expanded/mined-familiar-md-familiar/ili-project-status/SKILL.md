---
name: ili-project-status
description: Where the project stands — check in and reconcile state, answer "where are we?" without writing, or sort open work by effort or urgency. Routes to one branch and runs only that one.
disable-model-invocation: true
---

# familiar — Project status

A **menu, not a procedure**. It names the three ways to look at where the project stands and hands
off to exactly one of them. It reads no project state itself and writes nothing.

## Context contract

- **Required context:** this menu only
- **Conditional context:** exactly one file under `references/`, only when step 1 selects that branch. The selected branch's own context contract governs from that point; nothing else in `references/` is opened.
- **Excluded context:** `5-System/Memory/`, `4-Trackers/`, `Knowledge`, `Inputs`, other projects, and undeclared extension content — the menu itself opens no project content.
- **Updates:** `nothing`. Every write belongs to the selected branch and is declared in that branch's own contract
- **Capabilities:** file-read. Optional capabilities must degrade as the procedure states.
- **Completion:** One branch is selected, its reference file is loaded, and its procedure runs under its own contract — or the user is told no branch fits and nothing is opened.

## Step 1 — Select the branch

If the user already named one ("where are we?", "check in", "what should I run first?") — including
by argument, `/project-status check-in`, `/project-status ongoing` or `/project-status triage` — skip
the question and go straight to it. On a project with no memory yet, choose Check-in. Otherwise
present these three and ask which:

| Branch | Reference | What it does |
|---|---|---|
| **Check-in** | `references/check-in.md` | Reconcile project state, report health and drift, and set up a fresh project on its first run. Writes state. |
| **Ongoing** | `references/ongoing.md` | Answer what is open and in progress right now, from saved state. Writes nothing. |
| **Triage** | `references/triage.md` | Sort the open work you can start today by effort or urgency. Writes nothing. |

If the request matches none, say so and stop. Do not pick the nearest branch, and do not open a
reference file to find out whether it fits — the table above is the whole basis for the match.

## Step 2 — Run the selected branch

Load that one reference file. From there its own **Context contract** governs — its Required,
Conditional, Excluded, Updates, Capabilities, and Completion declarations replace this file's, which
covered only the menu. Do not load a second branch.

## Guardrails

- **Every branch here is user-started.** This skill carries `disable-model-invocation: true`, so a
  route match never opens it and never opens anything under `references/` — `routes.md` Resolution
  rule 3 applies to the menu, which is what keeps it applying to every branch. Identify the branch
  that fits, tell the user the command, and stop.
- The menu never performs a branch's work itself, never partially applies one, and never substitutes
  a lighter action because a branch looked heavy.
- Nothing under `references/` is a skill. Each is a procedure this menu selects; none is separately
  invocable, and none may be opened without a selection in step 1.
