---
name: impact-quarterly-ld-report
description: Drafts the L&D function's quarter on one page, producing outcome measures against plan, a programmes table with the evidence reached and its strength, what stopped, what is at risk, capacity used and the decisions asked for next quarter. Use for "run impact-quarterly-ld-report", "quarterly L&D report", "L&D report to leadership", "learning and development quarterly review", "training report for the business", "L&D results against plan", "one page L&D report", part of the Claude Guide for Training Impact Pack by 90n.
---

# Quarterly L&D Report

## When To Use
The quarter closes and you want a report that reads like the other functions' reports: plan, actual, gap, what you need. Use it when you have a metrics set and this quarter's figures, and the question is how the function did against its own plan and what it asks for next.

## When Not To Use
Not for one programme: Sponsor Impact One-Pager reports a programme to the sponsor who signed its agreement, and Executive Impact Briefing argues one flagship programme in depth. If you have not yet fixed what the function measures, run L&D Metrics Set first; a report with new measures every quarter cannot be compared with the last one.

## Inputs
- Your metrics set, your plan figures for the year, and this quarter's actuals, each with its source and the person who vouches for it. Upload the export as a CSV file, or paste it; group figures only.
- For each programme, the evidence reached and its claim strength, from its own report; and last quarter's page, so the layout and the definitions stay the same.
If you have none of this, I start from the figures you can paste today and mark the output as a first draft, with "no plan set" wherever the plan is missing.

## Approach
A summary report against plan, the form every other function already uses: plan, actual to date, forecast. Two principles shape it: the type of report follows the reader's reason for measuring (from the catalogue abstract of ISO/TS 30437:2023, the abstract only), and you define the audience and the action you want from it before you write (the CDC guide "Evaluation Reporting: A Guide to Help Ensure Use of Evaluation Findings"). The failure this prevents is the quarterly that lists everything delivered and nothing missed, so the first gap a reader finds alone costs you the whole page. Claude Docs (beta) suits the page; in Projects (beta, on select plans) the quarters and their sources stay together.

## Workflow
1. I ask three questions at once: which quarter, who reads the page and what you want them to do after reading it; where the plan figures and the actuals come from, and who vouches for them; and the minimum reporting group, with who signs the page.
2. Fix the layout before any figure goes in: the same sections in the same order as last quarter. If a measure's definition changed since then, the row says so and the two quarters are not set side by side.
3. Outcome measures against plan, one row each from the metrics set: plan to date, actual to date, gap (actual minus plan, in the measure's unit), and the forecast for the year, which is the owner's forecast and never a line I extend from two quarters. Where no plan figure exists the cell says "no plan set".
4. The programmes table: programme, the level of evidence reached (reaction, learning, behaviour, results), claim strength (shown, suggested, unknown) and status. Copy these from each programme's own report. A programme nobody evaluated appears as "unknown"; leaving it off the page is the overclaim.
5. What stopped this quarter and why, in the same type size as what ran. What is at risk, each with the warning already sent or the date it is due. Capacity used: days and budget, plan beside used, your figures. Then the decisions asked for next quarter, each with an owner and a date; a report that asks for nothing is read once.
6. Write the top two lines last: how the quarter went against plan, and what is asked. The caveat that would change the reader's view goes there, then cut to one page; the rest is an annex.

## Output Format
```markdown
# Quarterly L&D Report
Quarter: [quarter, year] · For: [reader, role] · Signed by: [name, role] · Minimum reporting group: [you set] · Status: [first draft / signed]
**The quarter in two lines:** [how the quarter went against plan, with the caveat that matters] [what is asked]
## Outcome measures against plan
| Measure | Plan to date | Actual to date | Gap | Forecast for the year | Source | Voucher |
|---|---|---|---|---|---|---|
| [measure] | [your figure / no plan set] | [your figure] | [actual minus plan] | [owner's forecast / none given] | [source] | [name / no voucher yet] |
## Programmes and their evidence
| Programme | Level of evidence reached | Claim strength | Status |
|---|---|---|---|
| [programme] | [reaction / learning / behaviour / results / none] | [shown / suggested / unknown] | [running / finished / stopped] |
## Stopped and at risk
| What | Stopped or at risk | Why, from the evidence | What it frees, or the warning sent or due | Owner |
|---|---|---|---|---|
| [programme or activity] | [stopped] | [reason] | [days or budget, your figure] | [name, role] |
| [programme] | [at risk] | [indicator that is off] | [date sent / date due] | [name, role] |
## Capacity used
| | Plan | Used | Source |
|---|---|---|---|
| [Days / Budget] | [your figure] | [your figure] | [source] |
## Decision
| Decision asked | Who decides | By when |
|---|---|---|
| [what a named person is asked to decide for next quarter] | [name, role] | [date] |
```

## Done When
- The page fits on one side, keeps last quarter's layout and definitions, and every figure has a source and a voucher and matches the programme's own report to the digit.
- Every plan cell holds your plan figure or "no plan set"; no cell was filled to look complete.
- What stopped and what is at risk are on the page, and each decision asked has an owner and a date.

## Quality Bar
- The top two lines can be read alone and still tell the truth about the quarter; a gap is stated as a gap, with no softening adjective.
- Claim strength travels with every programme: "suggested" is never promoted to "shown" on the way to this page.
- No table by named manager, trainer or learner; groups below the minimum are merged or left out.
- Every figure is the user's, set against the user's own plan; no trend, comparison or industry figure is added, and a named person signs the page.

## Next
Run impact-executive-impact-briefing (Executive Impact Briefing) to take the strongest programme to the executive team.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
