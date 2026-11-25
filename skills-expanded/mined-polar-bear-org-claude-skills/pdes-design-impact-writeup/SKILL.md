---
name: pdes-design-impact-writeup
description: Writes a Design Impact Write-Up with three lines up front, what design changed with ship dates, before and after per metric from your data only, what else moved in the same window, a confidence level with its reason, results that got worse kept in and lessons, with missing numbers left as not measured. Use for "run pdes-design-impact-writeup", "design impact write-up", "what did the redesign deliver", "show the impact of my design", "before and after metrics for a redesign", "prove the value of design work", "design results report", "post-launch design review", part of the Claude for Product Designers Pack by 90n.
---

# Design Impact Write-Up

## When To Use
Someone asks what the redesign delivered and you have screens, not outcomes. Run it once the work has shipped and the period you agreed to wait has passed. It answers: what changed for users, how sure are we, and what else could explain it?

## When Not To Use
If the work has not shipped and nobody agreed what success would look like, run HEART Metrics Plan first; this write-up reads those metrics back and cannot invent them afterwards. If the story is for readers outside the team and about your own decisions and role, use Portfolio Case Study.

## Inputs
- The metrics agreed before the work, or the outcome you were aiming for, and what design changed: each screen, flow or copy change with its ship date
- Before and after values per metric, with the source and the date range of each; real research findings, anonymised
- What else changed in the same window: launches, pricing, campaigns, fixes, season
If you have none of this, I start from the list of shipped changes, write every number as `[not measured]` and mark the output as a first draft.

## Approach
Goals, Signals, Metrics from the HEART framework (Rodden, Hutchinson and Fu, CHI 2010), read back after shipping in the order they were set. One standard is held throughout, and it is a deliberate choice of this skill: contribution, not attribution. Design rarely moves a number alone. The failure it prevents: you tell the room the new checkout raised conversion, and the first question is about the campaign that ran the same month. A write-up that names the campaign first is the one people believe.

## Workflow
1. Ask three questions: who will read this, which metrics were agreed before the work, and what else changed in the same window?
2. Read back goal, signal, metric in that order, in two or three lines. If no metric was agreed beforehand, say so in the write-up; a metric chosen afterwards is labelled as chosen afterwards.
3. List what design changed: each screen, flow or copy change with its ship date. "Improved the experience" is not a change.
4. Before and after per metric, from your data only, each with its date ranges and source. A missing value is `[not measured]`. A metric that got worse is reported with the same care as one that got better.
5. Contribution: list every other change in the window and how it could move the same metric. Write "design contributed to", never "design caused".
6. Give each result a confidence of high, medium or low, with the reason: sample, instrumentation gaps, other changes. Qualitative evidence comes only from research you pasted.
7. Write the lessons, then the three-line summary last and place it first. Before it is shared, the person who owns the data checks every figure against its source. Draft in any chat, in Claude Docs as a document or in Claude Slides as a short deck.

## Output Format
```markdown
# Design Impact Write-Up
**Work:** [feature or flow] | **Shipped:** [date] | **Period read:** [dates] | **Author:** [role] | **Reader:** [role]
## Three lines up front
[What changed for users. The clearest result, as a contribution. The confidence and its reason.]
**Goal, signal, metric:** [goal] > [signal] > [metric] | **Agreed before the work?** [yes, where / no, chosen afterwards]
## What design changed
| Change | Screen or flow | Shipped |
|---|---|---|
| [specific change] | [where] | [date] |
## Before and after
| Metric | Before (dates) | After (dates) | Source | Direction | Confidence and reason |
|---|---|---|---|---|---|
| [metric] | [value] or [not measured] | [value] or [not measured] | [source] | [better / worse / flat] | [high / medium / low, reason] |
## What else moved
| Other change in the window | Could it move the same metric? |
|---|---|
| [launch, price, campaign, fix, season] | [yes / no / unknown, how] |
## Lessons
[What the evidence suggests, what stays unknown, what you would measure next time.]
## Decision
[Product manager or design lead, by role] decides by [date] whether the result is kept, iterated or rolled back, after [data owner, by role] confirms the figures by [date].
```

## Done When
- Every number has a source and a date range, or reads `[not measured]`
- Every result carries a confidence level with its reason, and the "what else moved" table is filled or marked `[none known, to verify]`
- No sentence says design caused a result

## Quality Bar
- Results that got worse stay in, in the same table and the same tone
- Credit goes to the work as a whole, never a ranking of who contributed most
- User quotes appear only if pasted from real research, and are anonymised
- Claude writes only numbers you gave it; impact is a contribution, and every missing figure stays "not measured".

## Next
Run pdes-portfolio-case-study (Portfolio Case Study) to tell the story outside the team.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
