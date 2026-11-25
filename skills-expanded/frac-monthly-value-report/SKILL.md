---
name: frac-monthly-value-report
description: Builds the monthly report of a fractional engagement, setting what was agreed against what was delivered, with a short scoreboard (baseline, last month, now, and the source of each figure), days used against days agreed, scope changes and how each was handled, and what stays open. Use for "run frac-monthly-value-report", "write my monthly report for the client", "monthly report template for a fractional executive", "show what the seat changed", "prove value before the renewal", "agreed against delivered", "monthly scoreboard for my client", part of the Claude for Fractional Leaders Pack by 90n.
---

# Monthly Value Report

## When To Use
The renewal is two months away and you have no page that shows what the seat changed. Weekly updates went out; nobody could reassemble them into "here is what you bought and here is what you got". Use it every month from the first, so the renewal is a reading of pages that already exist.

## When Not To Use
If the board needs its one page, run Board Update. If the contract is about to roll over and a decision is due, run Renewal Review, which uses these reports.

## Inputs
- The statement of work and the 90-day plan: deliverables, objectives, measures, baselines
- This month's figures from the client's systems, each with its source, and this client's log for days used and scope asks
- Last month's report, if there is one
If you have none of this, I start from what was agreed and what you delivered, leave the scoreboard blank and mark the report as a first draft.

## Approach
A monthly log of what was delivered against what was agreed, as a fractional marketplace's guidance on boundaries describes it, with a short scoreboard of five measures at most, as a public playbook for fractional executives recommends: baselines set early, the same definitions each month. The judgment is to show the page even when it is thin. The failure this prevents is value that cannot be seen at renewal, and its opposite, a scoreboard that claims credit for results the seat did not cause.

## Workflow
1. Ask at most three questions: which month; have any measure definitions changed; which results this month do you believe the seat influenced, and which merely happened?
2. Set agreed against delivered, line by line from the statement of work and the plan: delivered, partly, not yet, with the evidence. A line not delivered is shown with its reason and new date.
3. Fill the scoreboard, five measures at most: baseline, last month, now, source. If a definition changed, show both versions for this month and say why.
4. For each movement, say what you can show about its cause. Where the seat's part cannot be separated from other causes, write "contributed, not attributable" and leave the claim out of any summary.
5. Set days used against days agreed, and list scope changes: accepted and priced, swapped, deferred, declined, or absorbed. Absorbed asks are shown too; they are what the next review needs to see.
6. Write a short commentary: what moved, what blocked, what stays open. Draft it in Claude Docs or as text; you send it or walk the CEO through it.

## Output Format
```markdown
# Monthly Value Report
Client: [name] · Month: [month] · Days used: [n] of [n] agreed
## Agreed against delivered
| Agreed (statement of work or plan line) | Delivered | Evidence | If not yet: reason and new date |
|---|---|---|---|
| [line] | [yes / partly / not yet] | [document, decision, figure] | [reason, date] |
## Scoreboard
| Measure and definition | Baseline | Last month | Now | Source | Cause I can show |
|---|---|---|---|---|---|
| [measure] | [value] | [value] | [value] | [system] | [shown / contributed, not attributable] |
## Scope changes this month
| Ask | Handled as | Days or fee effect |
|---|---|---|
| [ask] | [priced / swapped / deferred / declined / absorbed] | [effect] |
## What moved, what blocked, what stays open
[Short commentary in your words]
## Decision
[CEO] and [you] review this page on [date] and agree what changes next month.
```

## Done When
- Every agreed line shows delivered, partly or not yet, with evidence
- The scoreboard has five measures or fewer, each with a source
- Days used and every scope ask of the month appear, absorbed ones included
- No result is claimed that you cannot show

## Quality Bar
- The same measures and definitions every month; a change is shown side by side
- A thin month is reported as thin
- Team members are credited for their work by name where you say so, never rated
- No benchmark or comparison with other companies is added
- Every figure comes from this client's systems as you give it; none is invented, and no result from another client is used for comparison

## Next
Run frac-board-update (Board Update) to put the same numbers on the one page the board reads.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
