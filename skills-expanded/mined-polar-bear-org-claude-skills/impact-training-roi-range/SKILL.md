---
name: impact-training-roi-range
description: Builds a Training ROI Range from your own figures, producing a stop check on the chain of evidence up to application, a working sheet finance can rerun with a source beside every value, and a low and a high case with intangibles left unconverted. Use for "run impact-training-roi-range", "training roi", "phillips roi model", "return on investment for training", "benefit cost ratio", "what did the programme return", "training ROI calculation", "justify the training budget", part of the Claude Guide for Training Impact Pack by 90n.
---

# Training ROI Range

## When To Use
The budget holder asks what the programme returned, and finance will check the working. The programme has run, the results table exists, and you need an answer that survives someone rerunning every line. It answers one question: from the figures we hold, what is the lowest and the highest return we can defend, or can the data carry no return at all?

## When Not To Use
If you are asking for budget for a programme that has not run, use Training Business Case: this skill only looks back. If the sponsor wants to know how the training was used and what got in the way, use Success Case Method Write-Up; cases do not add up to a return.

## Inputs
- The change in the business measure from your Before-and-After Results Table, at group level, with its source and voucher
- How the programme's effect can be separated from everything else: a control group, a trend line, a forecast, or estimates from people close to the work
- The money value of one unit of the measure, with where it comes from, and every cost line you know, including participants' time
If you have none of this, I start from the cost lines you can name and a blank working sheet, and mark the output as a first draft. Ask for the working as a spreadsheet file if file creation is turned on; the markdown sheet is the default.

## Approach
The Phillips ROI Methodology, as set out on the ROI Institute's methodology page, runs a chain of five levels: reaction and planned action, learning, application and implementation, business impact, and ROI. Its moves are to isolate the programme's effect, convert it to money, count fully loaded costs, report intangibles unconverted and stay conservative. This skill puts a stop rule in front of all of them, because a return with no evidence of use on the job is arithmetic on someone else's result. The failure it prevents: a headline return built on a whole quarter's improvement when a new tool, a seasonal peak and a staffing change landed in the same weeks, and finance finds it in the first question.

## Workflow
1. Ask three questions at once: which measure moved, and what else changed in the same period? Which isolation method can you actually support? Who in finance will check the working, and which standard values do they already use?
2. Run the stop check first. Set out the chain: reaction, learning, application, impact. If there is no evidence of application on the job, stop: no ROI is calculated, and the output says what is missing and who could collect it.
3. Isolate, and name the method: control group, trend line, forecast, or estimates. With estimates, each estimator's own confidence is applied as a discount, and the estimates are pooled for the group. The share credited is a range, low to high, from your inputs. The whole change is never credited.
4. Convert to money from one of four sources: a standard value finance already uses, historical records, an internal expert, or an external source you supply. The source sits beside every value. No value, no conversion: the cell stays blank and the result is not calculated.
5. Count fully loaded costs: needs assessment, design and development, delivery, participants' time away from work, evaluation. Leaving out participants' time is the fastest way to lose finance.
6. Run the two formulas on your figures only: BCR = programme benefits / programme costs; ROI (%) = net programme benefits / programme costs x 100. The low case takes the lower share, the lower value and the higher cost; the high case the reverse. Every line carries a reference so finance can rerun it.
7. List intangibles with no money value, state the limits in plain words, and hand the sheet to you to check against the sources before finance sees it.

## Output Format
```markdown
# Training ROI Range
Programme: [name] | Period: [dates] | Group: [definition and size, never individuals] | Finance reviewer: [name]
## Stop check
- Reaction: [evidence, source] | Learning: [evidence, source] | Business impact: [evidence, source]
- Application on the job: [evidence, source, or MISSING]
- Verdict: [carry on / STOP, no ROI calculated: missing evidence, who could collect it]
## Working sheet
| Ref | Line | Low case | High case | Source | Voucher |
|---|---|---|---|---|---|
| A | Change in [measure] over [period you set] | [your figure] | [your figure] | [results table row] | [name] |
| B | Share credited to the programme, by [isolation method] | [lower share] | [higher share] | [source] | [name] |
| C | Confidence discount, estimates only | [your figure] | [your figure] | [estimators, by role] | [name] |
| D | Money value of one unit | [lower value] | [higher value] | [finance standard / records / internal expert / your external source] | [name] |
| E | Fully loaded costs: needs assessment + design and development + delivery + participants' time + evaluation | [higher cost] | [lower cost] | [source per line] | [name] |
| F | Programme benefits = A x B x D, and x C only where estimates were used | [calc] | [calc] | from A to D | |
| G | BCR = F / E | [calc] | [calc] | | |
| H | ROI (%) = (F - E) / E x 100 | [calc] | [calc] | | |
## Intangibles and limits
- [Intangible, not converted] | [limit on the isolation, the conversion or the period]
## Decision
[Budget holder name] reviews the range with [finance reviewer] by [date] and decides whether to continue, change, stop or scale the programme.
```

## Done When
- The stop check is filled in, and if application is missing there is no ROI line at all
- Every value in lines A to E is yours, with its source and voucher beside it
- The isolation method is named and the share credited is below the whole change
- Costs include participants' time and evaluation, and the result is a low and a high case, with the lower benefit and the higher cost taken wherever two values were in doubt

## Quality Bar
- A blank beats a guess: with no money value, the sheet says so and stops at benefits in the measure's own unit
- Say plainly when the data cannot carry an ROI at all; that sentence is a result
- Benefits and time costs are stated for the group, never per person
- No value, rate or benchmark is supplied by Claude; the whole change is never credited to the programme, and finance and a named owner stand behind every figure

## Next
Run impact-sponsor-impact-one-pager (Sponsor Impact One-Pager) to put the result in front of the sponsor on one page.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
