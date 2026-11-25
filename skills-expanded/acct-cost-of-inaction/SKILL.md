---
name: acct-cost-of-inaction
description: Builds a cost of inaction worksheet in the customer's own figures, with each consequence, who gave the figure and when, the arithmetic shown step by step, the timing pressure they stated and what changes if they wait a quarter. Use for "run acct-cost-of-inaction", "cost of inaction", "cost of doing nothing", "why should they act now", "no urgency in this deal", "business case from the customer's numbers", "what does waiting cost them", part of the Claude for Account Executives Pack by 90n.
---

# Cost of Inaction

## When To Use
The customer likes you and nothing makes this urgent. The meeting was warm, the problem is real, and the deal will sit behind ten other priorities unless someone can see what staying as they are costs. Run this after discovery. It answers: what does waiting cost them, in their own figures, and do they think it matters?

## When Not To Use
Before the call, when you have no figures yet, run Discovery Call Questions to prepare the implication questions that produce them. To connect your offer to their needs, run FAB Statements.

## Inputs
- Your call notes, with the customer's figures and who gave each one.
- Their answers to your implication questions, even partial ones.
- Any deadline, event or decision the customer mentioned.
If you have none of this, I build the empty worksheet with the questions to ask, and mark it as a first draft. The table pastes into any spreadsheet.

## Approach
The cost of doing nothing is common practice, described here generically: lay out what the problem costs if nobody acts, so the customer compares acting with waiting and not your price with zero. It only works with the customer's own numbers. A borrowed benchmark is the fastest way to lose the room: the customer corrects it, then doubts every other line. So blanks stay blank, and "nothing changes if we wait" is a valid answer and a useful one.

## Workflow
1. I ask at most three questions: which figures did the customer give and who said each, was a deadline or event mentioned, and did anyone say what happens if this waits.
2. One row per consequence, in the customer's words: what it affects.
3. Per row: their figure and unit, who gave it (by job role) and when, and the period it covers. A figure stays exactly as stated; "a few hours a week" is written "a few hours a week", not converted into money.
4. Where there is no figure the cell stays blank, with the question to ask beside it. I never estimate, benchmark, borrow a typical figure or extrapolate.
5. Arithmetic on their figures only, step by step (their weekly figure times the weeks they named), each result naming the rows it used. No total that mixes units.
6. Timing: the deadlines, events or decisions that make "later" costly, as they stated them, with who said each.
7. "If they wait a quarter": what changes, in their words. If the answer is "not much", I write that and tell you plainly: the timing may be wrong, which is worth knowing before you write a proposal or put the deal in a forecast.

## Output Format
```markdown
# Cost of Inaction Worksheet
Account: [name] · From: [call of date, your notes]
## Consequences in their figures
| Consequence (their words) | Figure and unit | Who said it, when | Period | Question if blank |
|---|---|---|---|---|
| [consequence] | [figure as stated, or blank] | [job role, date] | [period] | [question] |
## Working
| Result | Calculation | Rows used |
|---|---|---|
| [label] | [their figure] x [their period] = [result] | [rows] |
## Timing they stated
- [Deadline, event or decision] (said by [job role], [date])
## If they wait a quarter
[What changes, in their words, or "nothing changes", stated plainly]
## Decision
[You] decide by [date] whether the cost is strong enough to propose now; [customer role] confirms the figures before any of them appears in a proposal.
```

## Done When
- Every figure has a speaker by job role and a date; every blank has its question.
- Every calculation shows its inputs and uses only the customer's figures.
- The wait-a-quarter answer is recorded, even when it is "nothing".

## Quality Bar
- Units stay as stated; nothing is converted into money or time the customer did not give.
- No benchmark, industry figure or typical cost anywhere on the sheet.
- A weak cost is reported as weak, never inflated to create urgency.
- The worksheet is for understanding, not for pressure lines.
- Every figure is the customer's own, with who said it; blanks stay blank and no number is invented.

## Next
Run acct-fab-statements (FAB Statements) to tie your offer to the needs behind these costs, with proof.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
