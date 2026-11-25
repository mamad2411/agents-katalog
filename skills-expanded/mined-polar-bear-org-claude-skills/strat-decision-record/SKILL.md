---
name: strat-decision-record
description: Write the record of a strategy choice once the owner has made it, with the status, the choice in the owner's words, the options rejected, what was known at the time and the triggers that would reopen it. Use for "run strat-decision-record", "strategy decision record", "write the decision record", "record why we chose this option", "log this strategy decision", "why did this option win", "decision log entry", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Strategy Decision Record

## When To Use
Three months on, nobody remembers why this option won, and the decision is argued again from the start. Use this right after the owner has made a strategy choice, or to pin down one that is half made. It answers: what was decided, by whom, on what evidence, and what would justify reopening it?

## When Not To Use
Not before the decision. If the call still has to be argued for and asked for, run Recommendation Memo. If the options still need comparing, run Decision Matrix. To tell the teams about a change, run Strategy Change Note: the record keeps the reasoning, it does not announce anything.

## Inputs
- The decision as the owner said it, word for word if you have it (a message, meeting notes, the memo that was approved)
- Who decided (name and role), on what date, and what the choice covers
- The options that lost, the evidence and assumptions on the table at the time, and any disagreement that stayed open
If you have none of this, I start from your one-sentence account of the choice, set the status to proposed and mark the output as a first draft.

## Approach
This is the decision record with context, decision, status and consequences described by Michael Nygard in "Documenting architecture decisions" (2011, cognitect.com/blog/2011/11/15/documenting-architecture-decisions). It was written for software architecture; here it is applied to a strategy choice. The record argues nothing and is written once. The failure it prevents is the record that gets tidied after the results come in, so that a reasonable bet made on thin evidence reads as either genius or foolishness. It works in a plain chat; a Claude Project can hold the cycle's records so the next one starts from them.

## Workflow
1. I ask up to three questions: how do you state the decision in your own words, is it proposed, conditional or final, and who has the authority to make it? Silence is never approval. If authority is unclear, the status stays proposed.
2. I write the context: the forces at play, the evidence and the assumptions known on the decision date, each with its source or the word assumption. Anything learned later is left out, because the point is to judge the reasoning without knowing the outcome.
3. I write the choice in the owner's words, then the owner (name and role), the date and the scope: what it covers and what it leaves open.
4. I list each rejected option, do nothing included, with the one reason it lost. Dissent is kept as a position with its reasoning, attributed only if the person agrees. Nobody is marked right or wrong.
5. I list the conditions that must be met before anyone acts. For a condition that touches a contract, a regulated matter or a board duty, check with a qualified adviser.
6. I write the consequences the owner accepts, then the review date, the evidence triggers that would reopen the choice and the role that can raise each one. Ordinary execution adjustments are kept apart from reopening the whole choice.
7. If this replaces an earlier decision, it gets a new record. The old one is marked superseded with a link and is never edited.

## Output Format
```markdown
# Strategy Decision Record
**Status:** [proposed / conditional / final] | **Date:** [date] | **Supersedes:** [record link or none]
## Context at the time
| What we knew or assumed | Fact or assumption | Source |
|---|---|---|
| [statement] | [fact / assumption] | [source and date] |
## The choice
[The choice in the owner's words.] Owner: [name, role]. Scope: [what it covers, what it leaves open].
## Options rejected
| Option | The one reason it lost |
|---|---|
| [option, do nothing included] | [reason] |
## Dissent and conditions
Dissent: [position and its reasoning, attributed only with consent]. Condition before action: [condition], checked by [role] by [date].
## Consequences and review
| Consequence accepted | Trigger that would reopen the choice | Who can raise it |
|---|---|---|
| [consequence] | [observable evidence] | [role] |
## Decision
[Owner, by role] confirms the status and the wording by [date]. The choice is reviewed on [review date] and reopened earlier only if a listed trigger is met.
```

## Done When
- The owner has confirmed the status, and a reader who was not in the room can say what was chosen, what lost and why
- Every context line is a fact with a source or is marked as an assumption
- The review date and at least one reopening trigger are written, each with a role

## Quality Bar
- The record states what was known on the date. No hindsight, no later results.
- It argues nothing, and dissent is a view with its reasoning, never a verdict on a person.
- A trigger is observable evidence, not "if priorities change". A changed decision gets a new record.
- The choice is recorded in the owner's words. Claude never turns silence into approval or rewrites the record after the outcome.

## Next
Run strat-quarterly-strategy-review (Quarterly Strategy Review) to read the bets against what happened when the review date comes.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
