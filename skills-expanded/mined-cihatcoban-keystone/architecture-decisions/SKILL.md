---
name: architecture-decisions
description: Makes and records a costly-to-reverse technical decision as an ADR - forces, options, trade-offs, reversibility. Triggers - should we use a queue or direct calls, X or Y, build or buy, write an ADR, which database, monolith or microservices, why is the system built this way.
---

# Architecture Decisions

Most architecture damage is not a wrong decision — it is an **unrecorded** one.
Six months later nobody knows what was considered, what constraint drove it, or
whether that constraint still holds, so the decision becomes untouchable folklore
and the system calcifies around it.

## What counts as a decision worth recording

Record it if any is true:

- Reversing it costs more than a week
- It constrains choices in other parts of the system
- It commits to an external party (vendor, protocol, public contract)
- Reasonable engineers would disagree
- Someone will ask "why?" later and the code will not answer

Do **not** write an ADR for a library swap with a one-line diff, a naming
choice, or something the framework already dictates. ADR inflation makes the
real ones invisible.

## Decide by reversibility first

Before comparing options, classify the decision:

| Type | Test | Approach |
|---|---|---|
| **Reversible** | Undoable in a day by one person | Pick the simplest thing, move. Don't hold a meeting. |
| **Costly** | Days-to-weeks to undo | Time-boxed comparison, ADR, then commit |
| **One-way door** | Practically permanent (data format, public API, vendor lock, security model) | Prototype the riskiest assumption first; require a second opinion |

Teams routinely spend one-way-door effort on reversible decisions and the
reverse. Naming the class is half the work.

## Method

1. **State the forces, not the options.** Write what is pushing on this
   decision: load, team size, latency budget, compliance, deadline, existing
   skills, operational maturity. Options mean nothing without forces — the
   correct choice differs for a three-person team and a fifty-person one.
2. **Generate at least three options**, including "do nothing / extend what
   exists". Two options is usually a decision already made looking for
   justification.
3. **Compare on the forces**, not on general merit. A table where every row is
   a force and every column an option.
4. **Name the loser's advantage.** Write what you are giving up. If you can't,
   you haven't understood the rejected option.
5. **Identify the assumption most likely to be wrong**, and how you would
   detect it. This is the trigger for revisiting.
6. **Spike the risky part** when the decision is a one-way door. A two-day
   prototype beats a two-week argument.
7. **Record it** as an ADR (`templates/adr.template.md`), status `accepted`.

## Trade-off axes worth being explicit about

| Axis | Question |
|---|---|
| Coupling vs. speed | Does this let us move fast now at the cost of a boundary we'll want later? |
| Consistency vs. availability | What happens during a partition? Is stale data acceptable, and for how long? |
| Build vs. buy | What is the total cost of the buy — integration, lock-in, exit? |
| Simplicity vs. capability | Are we buying capability we can't operate? Complexity is paid every day |
| Operational load | Who runs this at 3am? Do we have that skill? |
| Data gravity | Once data lives here, what does moving it cost? |
| Team topology | Does this boundary match how teams are actually organized? |

**Conway's law is not a metaphor.** A boundary that cuts across team lines will
erode; a system designed against the communication structure loses.

## Anti-patterns

| Pattern | Cost |
|---|---|
| Resume-driven selection | Operational burden nobody signed up for |
| Copying a hyperscaler's architecture | Their constraint is scale; yours is probably team size |
| "We might need it later" | Complexity paid today for optionality rarely exercised |
| Deciding by demo | Demos hide operational cost |
| No ADR because "it's obvious" | It is obvious only to the people in the room, this month |
| Distributed system as the first answer | Network calls turn compile-time errors into runtime incidents |

## Revisiting

An ADR is never edited after acceptance — it is **superseded** by a new one
that links back. The history is the value: it shows what was true when, which
is the only way to judge whether the reasoning still applies.

Revisit when the recorded assumption breaks, not on a schedule.

**One carve-out: pre-implementation amendment.** Implementation regularly shows
that the decision was right but its write-up was imprecise. While nothing has
shipped against the ADR, append a dated `## Amendment (pre-implementation)`
section correcting the description — do not supersede a document that is hours
old, and do not leave the imprecise version standing. Once code depends on the
decision, the carve-out closes and any change is a new ADR.

## Exit checklist

- [ ] Decision classified reversible / costly / one-way door
- [ ] Forces written down before options
- [ ] At least three options, including doing nothing
- [ ] Comparison table maps options against forces
- [ ] What the rejected options were better at is stated
- [ ] The assumption most likely to break is named, with a detection signal
- [ ] ADR stored in `docs/adr/`, numbered, status set, linked from the spec
