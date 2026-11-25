---
name: strat-quarterly-strategy-review
description: Read the strategy's bets against what happened this quarter, with expected against happened per bet, each bet marked holding, weakening or broken against its kill criterion, the cause, and a keep, adjust or stop proposal for the owner. Use for "run strat-quarterly-strategy-review", "quarterly strategy review", "is the strategy working", "review our bets", "strategy retro", "check the kill criteria", "keep, adjust or stop", "end of quarter strategy check", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Quarterly Strategy Review

## When To Use
Nobody can say whether the strategy is working, so direction changes with the loudest result of the month. Use this at the end of each quarter, once the numbers are in. It answers: against what we wrote down in advance, which bets still hold, which are weakening, which are broken, and what should the owner do about each?

## When Not To Use
Not for grading one quarter's key results on their own: Quarterly OKRs does that. Not for reporting on roadmap items to a room: run Roadmap Review Deck. If no bets or kill criteria were ever written, run Strategic Bets first, because a review with nothing written in advance is an argument about memory.

## Inputs
- The bets with their kill criteria and dates, as written before the quarter
- The KPI sheet with its thresholds, and this quarter's key results with the data
- Which customers the team talked to this quarter (how many conversations, which segments), or "none"
If you have none of this, I start from the strategy document and your account of the quarter, list what was never written in advance and mark the output as a first draft.

## Approach
The spine is the four after-action review questions as set out in USAID, "After-Action Review Technical Guidance" (2006), which says it builds on US Army practice: what was intended, what actually happened, what went well and why, what can be improved and how. The guidance is explicit that the review is not a critique and does not grade success or failure. Key results are graded the way Google re:Work describes (rework.withgoogle.com/intl/en/guides/set-goals-with-okrs), and the kill criteria act as the signposts of change named in the US Government "Tradecraft Primer" (2009, cia.gov/resources/csi/static/Tradecraft-Primer-apr09.pdf). The failure this prevents: a bet declared dead because one number dipped, when the action behind it was never carried out. It runs in any chat; a Claude Project is optional if you want each quarter's files kept in one place.

## Workflow
1. I ask up to three questions: which quarter and which bets are in scope, who owns the strategy and decides after this review, and where the pre-written kill criteria and thresholds are. Nothing is reconstructed from memory.
2. Per bet I set what was expected beside what happened, each with its source. A result with no source is listed as unknown, not estimated.
3. I read each bet as holding, weakening or broken, strictly against the kill criterion written in advance. Where no criterion is on file I say so, do not read the bet as broken, and draft one for the owner to set for next quarter.
4. I name the cause in two cuts. First market, product or measurement, never a person. Then strategy or execution: was the bet wrong, or was the action not carried out? A bet whose action never ran has not been tested.
5. I grade each key result from 0.0 to 1.0 from the data; on an aspirational key result, 0.6 to 0.7 is reported as expected, not as a miss. Then I report the customers the team talked to this quarter in aggregate: how many conversations, which segments, or "none" said plainly. A reading built on no customer contact carries that note.
6. I propose keep, adjust or stop per bet, with the evidence behind it and what an adjustment would change. The owner decides.

## Output Format
```markdown
# Quarterly Strategy Review
**Quarter:** [quarter] | **Strategy owner:** [role] | **Written in advance on:** [date of bets and KPI sheet]
## Expected against happened
| Bet | Expected | Happened | Source |
|---|---|---|---|
| [bet] | [signal or threshold written in advance] | [result or unknown] | [source, date range] |
## Bet readings
| Bet | Kill criterion (written on [date]) | Reading | Cause | Strategy or execution |
|---|---|---|---|---|
| [bet] | [criterion or none on file] | [holding / weakening / broken / not readable] | [market / product / measurement] | [strategy / execution / action not run] |
## Key result grades
| Key result | Committed or aspirational | Grade (0.0 to 1.0) | What moved it |
|---|---|---|---|
| [key result] | [label] | [grade] | [market / product change / measurement] |
## Customers and proposals
Customers we talked to: [number] conversations across [segments], or "none this quarter". What they did that bears on a bet: [observation, interview code].
| Bet | Keep, adjust or stop | Evidence | If adjusted, what changes |
|---|---|---|---|
| [bet] | [proposal] | [evidence and source] | [change, new criterion or date] |
## Decision
[Strategy owner, by role] decides keep, adjust or stop for each bet by [date], and sets any missing kill criterion before the new quarter starts.
```

## Done When
- Every bet has a reading tied to a criterion written before the results, or says "none on file"
- Every expected and happened line carries a source or is marked unknown
- Each cause is market, product or measurement, tagged strategy or execution, and the customer line is filled even when the answer is "none"
- Each bet has one proposal, and the decision line names a role and a date

## Quality Bar
- No criterion is invented or loosened after the result is known, and the review grades no person or team.
- One bad number is a weakening signal, not a broken bet, unless the criterion says so.
- "Unknown" is a valid result. No figure is filled in to complete a row, and a tracking change is stated beside the number it affects.
- Bets are read against criteria written before the results. Claude proposes keep, adjust or stop, and the owner decides.

## Next
Run strat-strategy-change-note (Strategy Change Note) to tell the teams what changed and what did not, if the owner decides to adjust or stop a bet.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
