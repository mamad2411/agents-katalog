---
name: impact-programme-decision-record
description: Writes the full record of one decision about a programme, producing the decision in the owner's words with its status, the options rejected, the evidence known at the time with its strength, and the review date with what would reopen it. Use for "run impact-programme-decision-record", "programme decision record", "write down the decision", "record why we kept the programme", "the sponsor said keep going", "stop or scale decision", "decision log for training", "why did we continue this course", part of the Claude Guide for Training Impact Pack by 90n.
---

# Programme Decision Record
## When To Use
The sponsor said "let's keep going" in a corridor, and in six months nobody will remember why, or whether it was a decision at all. Use this the same week a programme is continued, changed, stopped or scaled. It answers: what exactly was decided, by whom, on which evidence, and what would make us look at it again?

## When Not To Use
For several programmes in one sitting, Evidence Review Meeting gives you the table of decisions; come here for the ones that need their reasons kept. If nothing is chosen yet and you are still comparing fixes, use Non-Training Options. To explain why a programme missed its measure, use Programme Shortfall Note: the record states what was decided because of it.

## Inputs
- The decision as the owner put it, word for word if you have it, and how it reached you (a meeting, a message, a remark).
- The evidence on the table at the time (the one-pager, the results table with claim strengths, any shortfall note), the options considered, and anyone who disagreed. Claude Docs (beta) suits a record the owner will confirm in writing; a plain chat works too.
If you have none of this, I start from the decision as you remember it, set the status to "proposed", and mark the output as a first draft.

## Approach
A decision record in its plain form: the choice, the rationale, the evidence then known, and the triggers for review. It is common practice wherever a choice has to be explained later. The judgement is to freeze what was known on the day, so the decision can be assessed later on its reasoning and not on how things turned out. The failure it prevents: a programme runs a second year on a remark nobody confirmed, the figures come in flat, and the record that would have shown "conditional on the manager briefings" was never written.

## Workflow
1. Ask at most three questions: what the owner said and where, who has the authority to decide on this programme, and what evidence was in front of them at the time.
2. Write the decision in the owner's own words, as one of four: continue, change, stop or scale. Set the status: proposed, conditional or final. Silence, a nod or a corridor remark is "proposed" until the owner confirms it. If the authority is unclear, the status stays "proposed" and the record says who must confirm. Then fix the frame: the owner by role and name, the date, and the scope (which programme, which groups, which period, what is left out).
3. List the options rejected, each with the reason given at the time. An option nobody raised is not added afterwards to make the choice look considered.
4. Record the evidence known at the time, each item with its claim strength (shown, suggested, unknown) and its source, then the assumptions made. I copy from the reports you give me and add no finding of my own.
5. Record dissent as it was given, by role unless the person asks to be named. Then the conditions that must hold before action, and the actions with owner and date.
6. Set the review date and the evidence that would reopen the decision, with who can raise it. The record is never rewritten: later changes are appended below it with a date.

## Output Format
```markdown
# Programme Decision Record
Programme: [programme] | Recorded: [date] | Recorded by: [role]
## The choice
In the owner's words: "[as stated]" | Type: [continue, change, stop, scale] | Status: [proposed, conditional, final]
Owner with authority: [name, role] | Scope: [groups, period, what is left out]
## Options rejected, and dissent
| Option | Reason given at the time |
|---|---|
| [option] | [reason] |

Dissent, as given: [view] ([role])
## Evidence known at the time
| Evidence | Source | Voucher | Claim strength |
|---|---|---|---|
| [finding, copied from the report] | [report] | [name or "no voucher yet"] | [shown, suggested, unknown] |
| [assumption made, and by whom] | [none] | [none] | [an assumption, not evidence] |
## Conditions and actions
| Condition or action | Owner | Date |
|---|---|---|
| [what must hold, or what gets done] | [named owner] | [date] |
## Review and later changes
Review date: [date] | Reopened if: [evidence that would reopen it] | Who can raise it: [roles]
Appended [date]: [what changed, and who confirmed it]
## Decision
[Owner] confirms the wording and the status by [date]; until then this record stays "proposed".
```

## Done When
- The decision is one of the four types, in the owner's words, with a status.
- Every evidence row has a source and a claim strength, and nothing in it postdates the decision.
- Rejected options and dissent are present or "none raised", and a review date and a reopening trigger exist, with who can raise it.

## Quality Bar
- Evidence is frozen as it stood: later results are appended with a date, never written into the original rows, and dissent is not softened into agreement.
- The record is about a programme. No trainer, manager or learner is named as a reason for the choice.
- A stop that touches a supplier contract or anyone's role: check with a qualified adviser.
- The record holds the evidence as it was known, with its strength; Claude never turns silence into approval, and a named owner decides.

## Next
Run impact-programme-shortfall-note (Programme Shortfall Note) when the decision followed a programme that missed its measure.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
