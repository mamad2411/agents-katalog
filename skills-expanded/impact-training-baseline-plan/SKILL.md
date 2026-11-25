---
name: impact-training-baseline-plan
description: Plans the capture of before figures ahead of a training launch, producing a row per agreed measure showing where the figure lives, its period and group, a comparison table (comparison group, trend line, forecast or none), a list of gaps with the cheapest way to close each, and a list of what cannot be claimed later. Use for "run impact-training-baseline-plan", "training baseline", "baseline before training", "before and after training data", "pre-training measurement", "comparison group for training", "what do we measure before launch", "capture where things stand today", part of the Claude Guide for Training Impact Pack by 90n.
---

# Training Baseline Plan

## When To Use
The programme launches in three weeks and no one has captured where things stand today. Use this as soon as the measures are agreed, while the before figures can still be pulled. It answers: for each measure, where is the before figure, can anything be compared with it, and what will the report be unable to say if nobody acts now?

## When Not To Use
If the measures are not agreed, run Success Measures Agreement first; a baseline for the wrong measure is wasted effort. This plan decides what is needed and what is possible. The message to the data owner is Business Data Request, and reading the figures once they exist is Before-and-After Results Table. If the programme has already launched, say so in step 1: the plan then lists what historical records can still give and what is lost.

## Inputs
- Your Success Measures Agreement, or the list of measures with their sources and owners.
- The launch date, the groups that start first, and any group that will be trained later or not at all.
- What you know about the reports involved: how far back they go and how often they refresh.
If you have none of this, I start from the programme name and the launch date and mark the output "no agreement on file: first draft".

## Approach
Evaluation is designed alongside the intervention, not after it: the principle set out on the Magenta Book page by HM Treasury and the Evaluation Task Force. The comparison options are the isolation techniques named on the ROI Institute's methodology page: control group, trend line, forecast, estimates. The judgement is honesty about strength before anyone has a result to defend. The failure this prevents: the report is due, the after figure is on the dashboard, and the before figure was overwritten the last time the dashboard refreshed.

## Workflow
1. Ask at most three questions, together: the launch date, and what has already been captured; which groups start first, and whether a similar group will be trained later or not at all; and the minimum reporting group you set.
2. Write one row per agreed measure: the report or system where the before figure lives, its owner, the period, the group and the group size. "Lives" means a place someone can pull from today. "The sponsor knows roughly" is a missing figure.
3. Match the two periods and the two groups. The before period has the same length as the planned after period, and the same season where the work has one; the group is defined the same way both times. A mismatch that cannot be fixed is written on the row, not smoothed over.
4. Test for a comparison, in this order of strength: a comparison group (a similar group not yet trained, for example a later cohort); a trend line (several periods before launch; you say how many exist); a forecast; none. Then write the strongest claim the report can make later: "shown" needs a comparison and a voucher, and with none the claim is "suggested" at most. Say so now.
5. For each missing figure, name the cheapest way to get it before launch: pull one report, run a one-week count, or send a short pre-survey read at group level. Give each a person and a date. A group below the minimum is merged with another before anything is captured.
6. Build the "cannot be claimed later" list: every measure that cannot be baselined in time, with the sentence the report will not be able to write. It goes to the sponsor before launch, when they can still move the date or pay for the gap.
7. Set a capture deadline before the launch date, with who does what. I never fill a before cell: the figure comes from its owner, with the date it was pulled.

## Output Format
```markdown
# Training Baseline Plan
Programme: [name] | Launch: [date] | Capture deadline: [date before launch] | Minimum reporting group: [you set] | Basis: [agreement signed on date / no agreement on file: first draft]
## Before figures
| Agreed measure | Where the before figure lives | Owner | Before period | Matching after period | Group, defined as | Group size | Status |
|---|---|---|---|---|---|---|---|
| [measure, as worded in the agreement] | [report or system] | [name, role] | [dates] | [dates, same length and season] | [who is in, who is out] | [your figure] | [exists / missing / cannot be baselined] |
## Comparison
| Agreed measure | Comparison available | What it rests on | Strongest claim later |
|---|---|---|---|
| [measure] | [comparison group / trend line / forecast / none] | [which group, or how many periods exist] | [shown is possible / suggested at most / unknown] |
## Gaps to close before launch
| Missing figure | Cheapest way to get it | Who | By |
|---|---|---|---|
| [figure] | [pull one report / one-week count / short group pre-survey] | [name, role] | [date] |
## Cannot be claimed later
| Measure | Why it cannot be baselined | What the report will not say | Shown to the sponsor on |
|---|---|---|---|
| [measure] | [reason] | [claim ruled out] | [date] |
## Decision
[Sponsor name] accepts the "cannot be claimed later" list, or moves the launch or funds a gap, by [date]. [L&D lead name] confirms every capture is done by [capture deadline].
```

## Done When
- Every agreed measure has a row, and its status is one of three: exists, missing, cannot be baselined.
- Every "exists" row has a period that matches the after period and a group defined the same way.
- Every measure has a comparison verdict and the strongest claim it allows.
- Every gap has a person and a date before launch, and the sponsor has seen the "cannot be claimed later" list.

## Quality Bar
- Comparison groups are groups of roles or cohorts. No person is tracked before and after, and no row is about an individual.
- The plan never overstates a comparison: two points are not a trend line, and a group that differs in obvious ways is noted as such.
- "Cannot be baselined" is a result of this plan, not a failure of it. A short honest list beats a full table of guesses.
- Any rule on pre-surveys, privacy or data protection is a point to check with a qualified adviser.
- No before figure is estimated or filled in; what cannot be baselined is listed as something the report will not claim.

## Next
Run impact-kirkpatrick-data-plan (Kirkpatrick Data Collection Plan) to schedule the rest of the collection.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
