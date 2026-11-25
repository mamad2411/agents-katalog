---
name: frac-decision-record
description: Writes a decision record for a client engagement, with the status (proposed, conditional, final), the owner, the choice and the reasons, the options rejected, what was known at the time, dissent, conditions, actions with owners, the review date and what would reopen it. Use for "run frac-decision-record", "write the decision record", "decision log entry", "the decision got reopened when I was away", "record what we decided and why", "document this decision", "who decided this and when", part of the Claude for Fractional Leaders Pack by 90n.
---

# Decision Record

## When To Use
A decision made on your day gets reopened on a day you are not there. Someone who missed the meeting asks why, nobody can quote the reasons, and by your next visit the team has half reversed it. This answers: what was decided, by whom, on what information, and what would justify looking at it again?

## When Not To Use
If the choice has not been made and the options are still being argued, run Decision Brief. If you only need the one-line entry among the week's notes, the Client Log holds it and links here.

## Inputs
- The decision in the owner's words, and whether it is proposed, conditional or final
- The options that were considered and why each was set aside
- What was known when it was made, who disagreed, and the first actions
If you have none of this, I start from your notes of the meeting, mark the status "proposed, to confirm with [owner]" and mark the record as a first draft.

## Approach
A decision record written at the time of the decision, a practitioner convention; a fractional marketplace's guidance on knowledge transfer asks for the same fields in a decision log (what, why over the alternatives, expected outcome, measure and timeframe). The judgment is to write down what was known then and to leave it alone afterwards. The failure this prevents is the decision that lives in the head of someone who is there two days a week.

## Workflow
1. Ask at most three questions: what was decided, in the owner's words; is it proposed, conditional or final; who was in the room and who disagreed?
2. Set the status honestly. Silence is never recorded as approval, and a decision whose owner has not confirmed it stays "proposed".
3. Record the owner, the date, the scope, the choice and the reasons, then each option rejected with one line on why.
4. Capture what was known at the time: the facts, the assumptions, the expected result and by when. Keep the dissent, attributed by role, as it was said.
5. List the conditions that must hold before action, then the actions with owners and dates, including who tells the people affected. The owner communicates it; I draft nothing in their name unless asked.
6. Set the review date and write what would reopen the decision and who may raise it, so that an ordinary adjustment is not mistaken for a reversal. Keep the record in this client's Project (beta) or folder; it is not rewritten once the outcome is known.

## Output Format
```markdown
# Decision Record
Client: [name] · Decision: [short title] · Status: [proposed / conditional / final] · Date: [date]
## The choice
Owner: [role, name] · Scope: [what it covers] · Decided: [the choice, in the owner's words]
Reasons: [why this over the others]
## Options rejected
| Option | Why it was set aside |
|---|---|
| [option] | [reason] |
## What was known at the time
Facts: [..] · Assumptions: [..] · Expected result: [what, by when, measured how]
Dissent: [view, by role] · Conditions before action: [..]
## Actions
| Action | Owner | By |
|---|---|---|
| [action, including who tells whom] | [owner] | [date] |
## Review
Review date: [date] · Reopen if: [evidence that would justify it] · May be raised by: [roles]
## Decision
[Owner] confirms the status and the wording by [date]; until then this record reads "proposed".
```

## Done When
- The status is one of the three and matches what the owner confirmed
- Rejected options and dissent are recorded, not tidied away
- Every action has an owner and a date
- The record states what would reopen the decision

## Quality Bar
- Written the day of the decision, from what was known that day
- Dissent is recorded by role and without comment
- The record is never edited to fit the outcome; a later change is a new entry
- A proposal is never worded as a decision
- Only what you give me is recorded, nothing is inferred or invented, and the record stays in this client's workspace and no other

## Next
Run frac-sponsor-change-plan (Sponsor Change Plan) so the reasons behind your seat are known to more than one person.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
