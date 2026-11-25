---
name: pdes-design-decision-log
description: Keeps a Design Decision Log with one short numbered record per significant design decision (title, context, decision, status, consequences), the decider by role, a link to the rationale, a revisit trigger and an index. Use for "run pdes-design-decision-log", "why did we decide this", "nobody remembers why", "log this design decision", "design decision record", "this was settled months ago", "mark that decision as superseded", "decision history for my product area", part of the Claude for Product Designers Pack by 90n.
---

# Design Decision Log

## When To Use
A decision made months ago is reopened and nobody remembers why it was made, so it gets argued from scratch with half the facts. Run it each time a significant design decision in your product area is proposed, made or replaced, and keep the file running. It answers: what did we decide, when, in what context, and is it still in force?

## When Not To Use
If you need the full argument for one decision, use Design Rationale Doc and link it from the entry. If the decision is a change to the design system, the system owner decides it: use Design System Change Record. Do not log every small choice; a log of trivia is a log nobody opens.

## Inputs
- The decision in your words, its date and who decided, by role
- The rationale or the context behind it, with a link if one exists
- The existing log, if there is one, so numbers and links stay intact
If you have none of this, I start from the decision as you remember it and the date, and mark the output as a first draft.

## Approach
The Architecture Decision Record (Nygard, 2011, cognitect.com/blog/2011/11/15/documenting-architecture-decisions), applied here to design decisions: five parts in order, which are title, context, decision, status and consequences. Records are short, numbered in sequence and never edited after the fact; a changed decision gets a new record that supersedes the old one. Four things in this log are additions to that format: the decider, the link to the rationale, the revisit trigger and the index. The failure it prevents is the "we agreed" that nobody agreed to. A Project is an optional place to keep the log, since it holds the file across weeks; otherwise paste the file back into any chat.

## Workflow
1. Ask three questions: what was decided or proposed, which role decides it, and is it new or does it replace an earlier entry?
2. Check significance: someone will question it later, or it is costly to reverse. If neither is true, say so and do not log it.
3. Write the Title as a short noun phrase with the next number in sequence; a number is never used twice. Write the Context as the forces at play, in neutral facts: constraints, what was known then, what was not.
4. Write the Decision in active voice ("We will ..."). Set the Status: proposed, accepted, deprecated or superseded. Only the named decider moves an entry to accepted; without their word it stays proposed, however long the thread went quiet.
5. Write the Consequences: positive, negative and neutral, all listed. The negative ones are the point; a record with none reads as a sales note.
6. Add the decider's role and the date, the link to the rationale, and the revisit trigger: the observable event that reopens it.
7. File it and update the index. For a reversal, add a new entry and mark the old one superseded with a link to its replacement. Never edit history; an entry that needs a correction gets a dated note.

## Output Format
```markdown
# Design Decision Log
**Product area:** [name] | **Kept by:** [role] | **Last updated:** [date]
## Index
| # | Title | Status | Date | Decider (role) | Superseded by |
|---|---|---|---|---|---|
| [n] | [short noun phrase] | [proposed / accepted / deprecated / superseded] | [date] | [role] | [# or blank] |
## [n]. [Title]
- **Date:** [date] | **Status:** [status] | **Decider:** [role]
- **Context:** [the forces at play, neutral, facts only]
- **Decision:** We will [decision].
- **Consequences:** positive [what gets easier]; negative [what gets harder]; neutral [what changes without being better or worse]
- **Rationale:** [link, or "none written"]
- **Revisit trigger:** [observable event, and who watches for it]
- **Dated note:** [only if a correction is needed]
## Open questions
- [what the record could not state, and who can answer]
## Decision
[Decider, by role] confirms the status of entry [n] by [date]; [designer] files the update the same day.
```

## Done When
- Each entry has all five parts in order, plus a decider, a date and a revisit trigger
- No entry is marked accepted without the decider's word
- Superseded entries are kept and linked to the entry that replaces them
- The index matches the entries, and each record fits on one or two pages

## Quality Bar
- One decision per entry; a bundle is split into separate numbered records
- Context is neutral, with no commentary on who opposed the decision
- A decision that rests on untested design says so in the consequences
- The revisit trigger is an event someone could observe, not "when we have time"
- Claude records what was decided; silence is never logged as acceptance, and only the decider sets a status.

## Next
Run pdes-design-system-rules-file (Design System Rules File) to give Claude the system before screens are drafted.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
