---
name: firm-outside-view-check
description: Tests the forecast behind a recommendation against comparable completed cases, with the forecast stated precisely, the cases you can actually name and the rule for including them, their range of outcomes, why this case might differ and the evidence for it, your revised estimate and the one missing fact most likely to change it. Use for "run firm-outside-view-check", "is my timeline realistic", "check the outside view", "reference class for this estimate", "how long did similar work really take", "am I being optimistic about this client", "sanity check my forecast", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Outside View Check

## When To Use
You are about to tell the client it will take a quarter and the team will adopt it by summer. Ask yourself where that came from. Usually from picturing this client, this sponsor, this plan going well. Run this before the estimate enters a recommendation or a proposal, to hold it against what happened in work that has actually finished.

## When Not To Use
With no forecast in the recommendation, skip this. To find which assumption would flip the choice between options, use Sensitivity Analysis; this checks one estimate against history.

## Inputs
- The forecast (what, by when, measured how) and your first estimate with its reasoning
- Completed work you know well enough to compare (yours, or the client's own past projects)
- What you believe is different this time
If you have none of this, I start from the forecast alone and will most likely return "no defensible reference class", which is a valid result.

## Approach
Reference class forecasting is the method Bent Flyvbjerg sets out in "From Nobel Prize to Project Management: Getting Risks Right" (Project Management Journal, 2006; arxiv.org/abs/1302.3642): place the case among similar completed ones, look at how those turned out, then adjust. An independent consultant often has only a handful of comparable cases, so this skill must be free to say the class is too thin. The failure it prevents is a base rate invented to look rigorous.

## Workflow
1. Ask, in one go: what exactly are you forecasting, by what date, and what counts as achieved? What is your estimate today and why? Which finished cases could it be compared with?
2. State the forecast so a stranger could score it later: the event, the date, the measure.
3. List the comparable completed cases and write the rule for including them before looking at their results. Include the ones that went badly and the ones abandoned; remembered successes alone are not a class.
4. Check the class: how many cases, how old, how similar, who selected them. If it is too small or too different, say "no defensible reference class" and stop the arithmetic there.
5. Where the class holds, show the range of what happened (shortest, longest, the middle) and keep it visibly separate from your forecast. A few cases never justify a narrow range.
6. List why this case might differ, each with its evidence, then record your revised estimate as your judgment, with a range, and the one missing fact most likely to move it.

## Output Format
```markdown
# Outside View Note
Forecast: [event] by [date], measured as [measure] · For: [recommendation or proposal]
## First estimate
[Your estimate and the reasoning behind it]
## Reference class
Rule for inclusion: [rule, written before the results]
| Completed case (anonymised) | Planned | Actual | Included because |
|---|---|---|---|
| [case] | [plan] | [what happened] | [rule met] |
Class check: [n cases, age, similarity] · Verdict: [usable / no defensible reference class]
## What the cases show
[Range of actual outcomes, or "not shown: class too thin"]
## Why this case might differ
| Difference claimed | Evidence | Direction |
|---|---|---|
| [difference] | [evidence or none] | [better / worse / unclear] |
## Revised estimate (your judgment)
[Estimate with range] · Missing fact most likely to change it: [fact, and who holds it]
## Decision
[You] decide by [date] which estimate goes into the recommendation, and whether [missing fact] must be obtained from [client role] first.
```

## Done When
- The forecast names an event, a date and a measure
- The inclusion rule was written before the results were listed
- The class is declared usable or not defensible, with the reason
- The revised estimate is labelled as your judgment, with a range

## Quality Bar
- Cases come from you or the client; I supply none and no sector base rate
- Failed and abandoned cases stay in the class
- A subjective range is never called a confidence interval
- Past clients appear anonymised, by role and problem only
- Every case and figure is yours or the client's; I invent no comparable and no base rate, and the estimate you sign is your own.

## Next
Run firm-recommendation-premortem (Recommendation Pre-Mortem) to try to break the option you now favour.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
