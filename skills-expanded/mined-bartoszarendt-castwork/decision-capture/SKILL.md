---
name: decision-capture
description: Use when a choice is made that future work should not silently reverse — an architecture, a dependency, a convention, a deliberate tradeoff. Covers what is worth recording and where it goes.
metadata:
  area: records
  side_effects: writes-files
  credentials: none
  runs_scripts: none
---

# Decision capture

The reason for a choice evaporates faster than the choice. Record the reason.

## What is worth recording

A decision is durable when reversing it later would be expensive or when someone
would otherwise reasonably do the opposite:

- an architecture or a boundary between components;
- a dependency added, or deliberately not added;
- a convention the codebase will be held to;
- a tradeoff taken knowingly — the slower approach for the clearer one, the
  duplicated code over the wrong abstraction;
- a requirement deliberately not met.

Not worth recording: anything the code already says plainly, and anything that
only mattered for one task.

## Where it goes

**Inside the task, under `## Blockers and decisions`**, when it explains this
task and stops mattering afterwards.

**In `.castwork/decisions/`**, when it outlives the task. A decision the
owner makes in conversation belongs here too when it outlives the task: a
session ends, and the choice goes with it unless it is written down. An
owner's choice that settles only this task's next step, such as whether to try
again, goes in the task, quoted and dated. Cite the decision's id in each task
record it governs, so a later reader of the task finds it. Where it changes
what a task may do or does next, that task's `## Current state` says so once
the decision is recorded.

Where a decision contradicts a document or record still in use, such as a
plan, a report's conclusion or the instructions for the next phase, update it
in the same change, within your authorization, or name it under
`## Consequences` with who updates it. Earlier measurements and assessments
stay as they were, as history: a reviewer otherwise finds the decision in one
place and the opposite still instructed in another.

Before writing one, run `npx --no castwork decision list` and read any
decision that covers the same ground: the new one may supersede it (see
[Changing a decision](#changing-a-decision)). Then
`npx --no castwork decision new "<title>"` writes the template, numbering the
record for you:

```markdown
---
schema: 1
id: D-001
title: Store money as integer minor units
date: 2026-03-04
status: accepted
---

## Decision
## Context
## Alternatives considered
## Consequences
## Revisit if
```

## Writing one well

**Whose decision it is.** Quote the owner's words and date them. A reason,
condition, or alternative you add is yours: say so. A condition that returns
the work to the owner is a stop you schedule; add one only where what follows
is the owner's call, and let any other stop return the work to the agent doing
it, or to the thinker when a coordinator runs the roles.
Record what the owner committed to, such as an outcome, a guarantee, a risk
they accepted, or a scope, apart from the method, check, or proof chosen to
meet it, and say whose choice the method was. Record a risk they accepted or
refused with the conditions it was put to them under, and whether it was seen
in use or only made to happen in a test: their answer covers that risk as
described. Their decision binds the
commitment, and a method only where they chose it themselves or a declared
requirement or the working policy demands it; approving a decision that names
the agents' method does not make it theirs. A method the agents chose, which
no declared requirement or working policy demands, may change when the
replacement keeps or tightens the commitment within existing authorization:
an engineering call, recorded citing theirs, in the task when it settles only
that task and otherwise in a decision record. One that weakens the commitment
goes back to them.
When the owner approves several recommendations in one answer, such as
"approved as recommended", record as theirs the parts that were their calls and
every limit they approved, such as a cap, a coverage requirement or a stop on
failure, each with what it commits them to, and the methods that came with them
as the agents' choices, citing the approval, so that a later step can change
those as above. This applies to what you record from now on: a restriction an
existing decision records as approved stays binding until the owner changes it.
Record a grant by what it bounds, such as its caps, its limits and stops, the
risk accepted, and its scope, including any attempt limit the owner approved or
supplied. A stopped assignment does not by itself revoke it.
When the owner authorizes work to proceed, such as a phase to implement,
record what they authorized, where they said it, and its scope and limits.
Agreeing a plan is a decision about what the work is, not that authority,
unless they say so; for a plan, record which of its consequential rules are
their words and which are proposals they confirmed.
An owner's instruction on how they want to be consulted belongs in the working
policy in `.castwork/project.md`, in their words, rather than in one record:
propose the line, and it lasts beyond the session once they approve it. An
instruction they scope to the session, such as one that begins "in this
session", stays in the session: propose no line for it, nor again one they
declined.
When the owner answers by choosing an option the agents drafted, such as "1A",
quote their answer and the option's text as it was put to them, and say the
wording is the agents': the choice binds what the option delivers and the
limits it names, and its method stays the agents' as above. Only words the
owner wrote themselves are recorded as their own.
If their answer could select more than one option, ask
before you record it. An answer that names no option while one of their calls
is open, such as "proceed" or "continue", selects none: ask which, in one line,
rather than recording the option you think they meant.

**Context** is what made the decision necessary. Someone reading in a year needs
to know what the pressure was, or the decision looks arbitrary.

**Alternatives considered** is the part that earns the file. Name what you did
not choose and why. A decision record with no alternatives is a note.

**Consequences** says what this commits the project to and what it rules out.

**Revisit if** names the observation that would reopen it. This is what stops a
decision record from becoming a rule nobody may question — every decision is
allowed an expiry condition.

## Changing a decision

Do not quietly contradict one. Write a new record that supersedes it, or change
the old one's status and say what replaced it. A replaced decision keeps its
file: set its `status` to `superseded` and name the record that replaced it
under `## Decision`, so `decision list` shows it plainly. A project whose
decisions drift without record is a project that will make the same mistake
twice.
