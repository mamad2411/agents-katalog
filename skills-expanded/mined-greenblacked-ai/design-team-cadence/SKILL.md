---
name: design-team-cadence
description: "Design or repair the recurring operating cadence of an engineering team, platform group, or organisation: one-to-ones, staff meetings, planning and operational reviews, architecture forums, skip-levels, retrospectives, and escalation paths. Produces a minimal meeting and decision system with explicit purpose, inputs, ownership, decision rights, outputs, frequency, cancellation rules, and health signals. Use this skill whenever a manager or lead asks how to run the team, reduce meetings, establish management routines, create an operating rhythm, route recurring decisions, improve one-to-ones, structure leadership meetings, coordinate teams, or scale to manager-of-managers — including phrases like \"our meetings achieve nothing\", \"what cadence should I run\", or \"everyone is surprised by decisions\". Do not use it to document or review one decision, diagnose delivery metrics, write a status update, review individual performance, or facilitate an active incident."
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Design a Team Cadence

A good cadence moves information once, makes decisions in named places, surfaces risk
before escalation is expensive, and leaves enough uninterrupted time to do the work.

Meeting systems usually grow by accumulation. Each meeting once solved a real problem,
then the problem changed and the meeting stayed. Repair the system from decisions and
feedback loops outward, not from a fashionable calendar template inward.

## Scope

Use for: team and leadership operating rhythms, one-to-one systems, decision forums,
planning and review loops, cross-team coordination, skip-levels, and meeting reduction.

Do not use for: documenting or reviewing one decision, evaluating an individual's
performance, diagnosing delivery health from metrics, writing stakeholder updates, or
commanding a live incident. Use `decision-record` for a single ADR, RFC, or proposal.

## Principles

1. Every recurring forum must produce a decision, commitment, shared model, or protected
   relationship. Information-only meetings become written updates.
2. One decision has one home. Duplicated forums create pre-meetings, shadow decisions,
   and stakeholders who learn outcomes too late.
3. Cadence follows the decision's half-life. Daily for volatile operations, weekly for
   delivery trade-offs, monthly or quarterly for strategy and organisation.
4. Protect dissent before commitment and clarity after it. “Consensus” is not a decision
   rule unless everyone genuinely holds a veto.
5. Every recurring meeting has a cancellation rule. A meeting that can never be cancelled
   has become ceremony rather than control.

## Workflow

### 1. Diagnose from failures, not the current calendar

Ask for recent examples:

- Which decision surprised people after it was made?
- Which risk was known but reached the owner too late?
- Which topic appears in three meetings without resolution?
- Which meeting would nobody miss if it vanished for a month?
- Where does a manager learn about team health, delivery, operations, and people risk?
- Which work loses focus time because attendance is broader than decision rights?

Capture the decision and feedback needs before listing existing meetings.

### 2. Map the loops

Use five loops; omit any the team genuinely does not need:

| Loop | Question | Typical horizon |
| --- | --- | --- |
| People | What support, feedback, growth, or load needs attention? | Weekly to monthly |
| Delivery | What changed, what is blocked, and what trade-off needs a decision? | Weekly |
| Operations | What is degrading, repeating, or consuming interruption budget? | Weekly to monthly |
| Technical direction | Which consequential design choice needs challenge or recording? | As needed or fortnightly |
| Strategy and organisation | Are priorities, ownership, interfaces, and capacity still right? | Monthly to quarterly |

Read `references/cadence-patterns.md` when choosing a concrete rhythm for a single team,
platform group, or manager-of-managers organisation.

### 3. Write a contract for every forum

No recurring meeting enters the design without:

- purpose stated as a decision or relationship outcome;
- owner and decision maker;
- required inputs and their deadline;
- minimum participants, with optional observers separated;
- agenda ordered by decisions, not departments;
- output location and owner for actions;
- frequency and duration justified by the decision half-life;
- cancellation rule when there is no decision-ready input;
- one signal showing whether the forum works.

Use the templates in `references/forum-contracts.md`; copy only the forums selected.

### 4. Separate written flow from synchronous work

Send facts asynchronously: status, metrics, changelogs, dashboards, and proposals that
can be read without debate. Use synchronous time for disagreement, judgment, coaching,
and decisions whose trade-offs change as people respond.

Set a reading deadline. “Pre-read” without protected reading time becomes a presentation,
and the meeting expands to include both reading and deciding.

### 5. Design the minimum viable cadence

Start with the fewest loops that close the diagnosed gaps. A common single-team baseline:

- weekly one-to-ones, adjusted by need rather than rank;
- weekly decision-focused team meeting;
- weekly or fortnightly delivery and operational review, combined when ownership matches;
- architecture review only when a decision is ready;
- monthly retrospective and capacity reset;
- quarterly strategy and ownership review.

This is a starting hypothesis, not a universal calendar. Merge forums when the same
people, evidence, and decision rights apply. Split them when confidentiality or authority
differs.

### 6. Define escalation and decision rights

For each recurring decision class, name who proposes, who decides, who must be consulted,
and who is informed. Prefer a lightweight table over a large responsibility framework.

Escalation must state the trigger, destination, response expectation, and what the team
may do while waiting. “Escalate when blocked” creates argument about both words during the
moment clarity matters most.

### 7. Pilot and remove

Run the cadence for four weeks. During the pilot, record decisions made, decisions
reopened, late surprises, attendance hours, cancelled sessions, and actions completed.

At the end, remove or change at least one forum. A cadence review that only adds meetings
is evidence that the system cannot retire obsolete control.

## Output format

```markdown
## Operating diagnosis
[The three failures the cadence must correct, with examples.]

## Decision and feedback map
| Loop | Decision or feedback | Owner | Required evidence | Half-life |

## Proposed cadence
| Forum | Purpose/output | Participants | Frequency | Health signal | Kill/change criterion |

## Decision and escalation rights
| Decision class | Proposes | Decides | Consulted | Escalation trigger |

## Stop or replace
[Existing meetings, reports, and duplicate routes removed.]

## Four-week pilot
[Start date, forum health signals, review date, and kill/change criteria.]
```

## Anti-patterns

**Calendar-first design.** Copying another company's weekly rhythm imports its interfaces,
decision rights, and failure modes without importing its organisation.

**Status theatre.** Reading updates aloud consumes focus time and hides the one decision
that needs the room.

**Every stakeholder in every meeting.** Attendance becomes a substitute for a reliable
written record and clear consultation rules.

**Architecture review as permission queue.** A central forum that approves every small
choice slows teams and teaches them to hide decisions. Set a consequence threshold.

**One-to-ones as project status.** The employee loses the only protected space for
feedback, growth, load, conflict, and context the group setting cannot surface.

**Retrospective without removal authority.** The team names systemic waste every month
and learns that nothing in the operating system can actually change.

## Reference files

- `references/cadence-patterns.md` — read when selecting a rhythm: patterns for one team, a platform group, and a manager-of-managers organisation, plus scaling and overload signals.
- `references/forum-contracts.md` — read when writing the chosen forums: copyable contracts for one-to-ones, team decisions, delivery/operations, architecture, strategy, skip-levels, and retrospectives.
