---
name: frac-weekly-review
description: Runs a weekly review across all the clients of a fractional leader, with expected against actual per client and the evidence, days used against days agreed, strategic against reactive time, what you would change, one thing to drop or renegotiate and next week's short list. Use for "run frac-weekly-review", "run my weekly review", "Friday review across clients", "which client got more than they pay for", "where did my week go", "plan next week across my clients", "weekly reset for fractional work", part of the Claude for Fractional Leaders Pack by 90n.
---

# Weekly Review Across Clients

## When To Use
Friday arrives and you cannot say which client got more than they pay for. The loudest client took the week, the quiet one slipped, and Monday will start the same way. This answers: what did each client get against what was expected, where did the days go, and what changes next week?

## When Not To Use
If you need the update that one client's CEO reads, run Weekly CEO Update. If one client's contract is about to roll over, run Renewal Review. This review is internal and is never sent to a client.

## Inputs
- Per client, by name or code: what you expected to move this week and what actually happened, with the evidence (from each client log)
- Days or half-days per client, and your own count of strategic against reactive time
- Anything that took your evenings, or that you pushed onto someone else
If you have none of this, I start from your calendar for the week and your memory of what moved, and mark the review as a first draft.

## Approach
A Friday reset and a Monday plan, as a public playbook for fractional executives describes the weekly routine, with four plain review questions (what was expected, what happened, why, what next) and three checks from a fractional marketplace's guidance: days against days agreed, strategic against reactive time, and whether you would sign this engagement again. The failure this prevents is the review as ritual: a tidy summary that changes nothing about next week.

## Workflow
1. Ask first for your own view, in three questions: what moved this week; what mattered most; what would you change? I organise it; I do not replace it.
2. Per client, set expected against actual with the evidence. Separate finished results from activity. A week full of meetings with nothing moved is recorded as that.
3. Set days used against days agreed, and your own split of strategic against reactive time. I use your counts and apply no threshold; you say what share of reactive work means the scope is drifting.
4. Name the cause of each miss from the evidence: the estimate, a changed priority, a dependency, capacity, unclear scope. Where the cause is unknown, it stays open. Nobody's effort or character is the cause.
5. Check the cost of an apparent success: evenings, a slipped commitment to another client, work pushed onto a team member.
6. Choose one change to test next week, and one thing to drop or renegotiate. Then the short list for Monday: per client, the one or two results that matter.

## Output Format
```markdown
# Weekly Review Across Clients
Week of: [date] · Internal page, not shared with any client
## Expected against actual
| Client (name or code) | Expected | Actual | Evidence | Why (or unknown) |
|---|---|---|---|---|
| [client] | [result] | [result or activity only] | [document, decision, figure] | [estimate / priority / dependency / capacity / scope / unknown] |
## Days and kind of work
| Client | Days agreed | Days used | Strategic | Reactive | Would I sign this again? |
|---|---|---|---|---|---|
| [client] | [n] | [n] | [your count] | [your count] | [yes / no / with changes] |
## What it cost
- [evening, slipped commitment, work pushed to someone]
## Change and drop
- One change to test next week: [change] · expected benefit: [..] · possible harm: [..]
- One thing to drop or renegotiate: [what, with whom]
## Short list for Monday
| Client | Results that matter next week |
|---|---|
| [client] | [one or two] |
## Decision
[You] decide by Monday which ask to renegotiate and with which client; the conversation is yours.
```

## Done When
- Each client has expected, actual and evidence
- Days used are set against days agreed for every client
- One change and one thing to drop or renegotiate are chosen, not five
- Next week's list holds one or two results per client

## Quality Bar
- Results come first; hours and meeting counts are never the measure of the week
- Causes come from evidence; unknown stays unknown
- A week is not called good only because the visible deliverable shipped
- Routine overtime is never the plan for next week
- Clients sit side by side on days and results only; no client's content is copied into another's row, and the page never leaves you

## Next
Run frac-weekly-ceo-update (Weekly CEO Update) to turn one client's row into the update its CEO reads.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
