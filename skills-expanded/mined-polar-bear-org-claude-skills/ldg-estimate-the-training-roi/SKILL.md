---
name: ldg-estimate-the-training-roi
description: Builds a training ROI estimate from your own figures, with the chain from application to impact, the method used to isolate the programme's effect, a money conversion with a source per value, full costs, and a low and a high case with caveats. Use for "run ldg-estimate-the-training-roi", "training roi", "roi of training", "calculate training roi", "phillips roi model", "return on investment for training", "cost benefit of training", "what did the programme return", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Estimate the Training ROI

## When To Use
The budget holder asks what the programme returned. You have costs in one place, a business measure in another, and a number is expected that finance will not take apart in the first minute. Run this after the programme has had time to show in the work, to answer one question: from the figures we hold, what is a cautious range for the return, and how sure are we?

## When Not To Use
Before the build, a return is a forecast, not an estimate: run Make the Business Case. If you have no evidence that people used the training at work, there is no impact to convert: run Check Use on the Job first.

## Inputs
- The business measure before and after, for the group, with its source, and the money value of one unit if finance has one
- What lets you separate the programme's effect: a comparison group, a trend line, a forecast, or estimates from people close to the work
- Every cost line you know: design, delivery, participants' time, tools, travel, evaluation
If you have none of this, I start from the cost lines you can name and an empty benefits table, and mark the output as a first draft.

## Approach
The estimate follows the Phillips ROI Methodology, from its originators' public page: a chain of levels ending in ROI, with four core moves: isolate the programme's effect, convert it to money with a stated source, count full costs, stay conservative. The judgement is in what you refuse to claim. The failure it prevents: a headline return that credits the programme with a whole quarter's improvement, presented a week after finance approved the new system that caused most of it.

## Workflow
1. Ask three questions: which business measure moved, what else changed in the same period, and who in finance will check the working?
2. Set out the chain from the programme's own data: reaction, learning, application, impact. If application is missing, stop there and say so. No use on the job, no impact to claim.
3. Isolate the effect and name the method: comparison group, trend analysis, forecast, or estimates from people close to the work. Each estimate is discounted by the estimator's own confidence. The whole change is never credited to training.
4. Convert to money with a standard value finance already uses, historical records, expert input or external data, and write the source beside every value. No value, no calculation: the cell stays [blank]. Then count full costs: design, delivery, participants' time, tools, travel, evaluation. Participants' time is the line most often left out and the first one finance looks for.
5. Calculate from your figures only: BCR = benefits / costs; ROI (%) = net benefits / costs x 100. Give a low and a high case from the range of the isolation and conversion inputs, never a single number. The working may be a spreadsheet file, if file creation is on.
6. List intangibles apart, with no money value, then write the caveats and what the data cannot support, in plain words.

## Output Format
```markdown
# Training ROI Estimate
Programme: [name] | Period measured: [dates] | Group: [size, group figures only] | Checked with: [finance contact]
- Chain of evidence: Reaction [evidence, source] / Learning [evidence, source] / Application [evidence, source, or "missing: stop here"] / Impact [measure]
## Isolating the programme's effect
| Impact measure | Change (your figure) | What else changed | Method | Share credited, low to high | Estimator's confidence |
|---|---|---|---|---|---|
| [measure] | [figure] | [tool, process, staffing] | [comparison group / trend / forecast / estimate] | [range] | [figure] |
## Money conversion
| Measure | Value per unit | Source of the value | Benefit, low | Benefit, high |
|---|---|---|---|---|
| [measure] | [value or blank] | [finance standard / records / expert / external] | [calc] | [calc] |
## Full costs
- [design / delivery / participants' time / tools / travel / evaluation]: [amount], [source]
## Range
| Case | Benefits | Costs | BCR | ROI (%) |
|---|---|---|---|---|
| Low | [calc] | [calc] | [calc] | [calc] |
| High | [calc] | [calc] | [calc] | [calc] |
## Outside the figure
- Intangibles, not converted: [item] | Caveats: [isolation, conversion, period]
- What the data cannot support: [claim we are not making, and why]
## Decision
[Budget holder name] reviews the range with [finance contact] by [date] and decides whether to continue, change or stop funding the programme.
```

## Done When
- Every figure is yours and carries its source; the isolation method is named, and part of the change is left to other causes
- Costs include participants' time and evaluation; the result is a low and a high case, with intangibles outside it
- The "what the data cannot support" line is filled in, not left as a placeholder

## Quality Bar
- A blank beats a guess: no value, rate or benchmark is filled in for you
- Between two defensible values, take the lower benefit and the higher cost
- The working is shown so finance can rerun it; if the data cannot carry an ROI figure at all, the estimate says so first
- Every figure is yours, measured for the group, never per person; the budget holder decides with finance what the range means

## Next
Run ldg-report-what-changed (Report What Changed) to put the range and its caveats in front of executives.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
