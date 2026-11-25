---
name: ldg-make-the-business-case
description: Drafts a one-page business case for one learning programme in five parts (why change, options including doing nothing and the non-training fix, build, buy or partner route, cost and affordability, delivery and measurement), with an assumptions table of low and high values and owners and a note on what would change the answer. Use for "run ldg-make-the-business-case", "business case for training", "training budget request", "justify training budget", "build or buy training", "funding for a learning programme", "the numbers are guesses", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Make the Business Case
## When To Use
You have to ask for budget before anything is built and everyone knows the numbers are guesses. The approver wants one figure, and a single figure will be picked apart at the first question. This answers: why change at all, which option is the best value against doing nothing, can we afford it, and which assumption would flip the answer?

## When Not To Use
If the programme has already run and the budget holder asks what it returned, use Estimate the Training ROI; that looks back, this looks forward. If the argument is about the right fix and not about money, use Prepare the Sponsor Conversation. A programme that fits inside this year's capacity line needs a row in the year plan, not a case.

## Inputs
- The performance problem and its evidence (the gap diagnosis, the needs table, or the request as it stands), and the options already discussed, including the ones that are not training.
- The cost figures you hold (design and delivery days, supplier quotes, licences, participants' time), the horizon to cost over, and the evaluation plan if one exists.
If you have none of this, I start from the programme description, leave every figure as a [placeholder] range and mark the output as a first draft.

## Approach
This uses the Five Case Model from HM Treasury's public guidance (the Green Book): strategic, economic, commercial, financial and management cases. It was built for public spending; here it is cut to one page for one programme. It is a forecast made before the build, and the page says so. The judgement is to show ranges with an owner beside each, not one confident figure. The failure it prevents: the case promises a result nobody can trace to a source, the budget is approved on it, and a year later the same figure is read back to you as a commitment.

## Workflow
1. Ask at most three questions: who approves the funding and by when, over what horizon the costs should run, and which options have already been ruled in or out?
2. Why change (strategic): the performance problem, its evidence, the business goal it serves, and objectives with targets you set. If the evidence is one person's request, the page says that.
3. Options (economic): doing nothing as the baseline, the non-training fix (a process change, a tool, a job aid, a manager conversation), and the programme options. Compare each against the objectives, never against another option's pitch.
4. Route (commercial) and delivery (management): build in-house, buy, or partner for the preferred option, and what each route needs from suppliers or other teams. Then who delivers, by role, the pilot and the review gates, and how and when the result will be measured, pointing to the evaluation plan.
5. Cost and affordability (financial): one-off and running costs over your horizon, with participants' time away from work counted as a cost, as low and high ranges from your figures only.
6. Assumptions table: each assumption with its low and high value, its source and an owner by role. Then name the one or two assumptions whose value flips the recommendation, and what the approver should ask about them. In Claude Docs (beta), or any document, the case stays one page.

## Output Format
```markdown
# Programme Business Case
Programme: [name] | Approver: [role] | Horizon: [period] | Status: forecast before the build
## Why change
[The performance problem, its evidence, the business goal it serves.] Objectives: [objective with the target you set]
## Options
| Option | Effect on the objectives | Cost range | Main risk |
|---|---|---|---|
| Do nothing (baseline) | [effect] | [low to high] | [risk] |
| Non-training fix: [fix] | [effect] | [low to high] | [risk] |
| [Programme option] | [effect] | [low to high] | [risk] |
## Route and delivery
Preferred option: [option], because [reason against the objectives]. Route: [build, buy or partner], and what it needs from [suppliers or other teams].
Delivered by: [roles] | Pilot: [date] | Review gates: [gates] | Measured by: [measure, date, from the evaluation plan]
## Cost and affordability
| Cost item | One-off or running | Low | High | Source |
|---|---|---|---|---|
| [item, including participants' time] | [type] | [figure] | [figure] | [your source] |
## Assumptions
| Assumption | Low | High | Source | Owner (role) |
|---|---|---|---|---|
| [assumption] | [value] | [value] | [source] | [role] |

What would change the answer: [assumption, and the value at which the recommendation flips]
## Decision
[Named approver] decides whether to fund [option] by [date]; [L&D lead] reports back on [the flipping assumption] by [date].
```

## Done When
- Doing nothing and the non-training fix both appear as options.
- Every figure is a range with a source, participants' time is in the costs, and every assumption has an owner by role.
- The assumptions that flip the recommendation are named.

## Quality Bar
- No invented costs, benefit figures, adoption rates or returns; a gap stays a [placeholder], and costs are for work and roles, never a named person's pay.
- The page says it is a forecast adapted from a public-spending method and is not a finance sign-off. Tax, accounting and contract points: check with a qualified adviser.
- Benefits that cannot be turned into money stay in words; they are not given a figure to make the case add up.
- Every figure is yours and stays a range; Claude drafts the case, and a named approver decides whether to fund it.

## Next
Run ldg-brief-the-vendor (Brief the Vendor) when the route is to buy or to partner, before any demo is booked.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
