---
name: impact-kirkpatrick-data-plan
description: Builds the collection schedule for a training evaluation across the four Kirkpatrick levels, producing a schedule of measure, instrument, source, owner, date and reporting group size per level, a required drivers table with owners, and a written choice of how deep to evaluate this programme. Use for "run impact-kirkpatrick-data-plan", "kirkpatrick model", "kirkpatrick model of evaluation", "evaluation plan", "who collects what", "data collection plan for training", "kirkpatrick four levels", "how deep should we evaluate this programme", part of the Claude Guide for Training Impact Pack by 90n.
---

# Kirkpatrick Data Collection Plan

## When To Use
The measures are agreed and you need to know who collects what, and when, without evaluating everything to the same depth. Use this once the agreement and the baseline plan exist and before the programme starts. It answers: for each level, which instrument, from which source, owned by whom, on what date, and which levels this programme does not need?

## When Not To Use
If the measures and verdicts are not agreed, run Success Measures Agreement first; this plan never defines or changes a measure. The before figures belong to Training Baseline Plan. To write an instrument itself, go to the skill the plan names, starting with Post-Training Survey.

## Inputs
- Your Success Measures Agreement, with the measures as worded and the reporting dates.
- The programme dates, the groups and their sizes, and the critical behaviours.
- Who could run the drivers back at work, as roles, and anything else changing in the work over the period.
If you have none of this, I start from the programme title and its dates and mark the output "no agreement on file: first draft". Ask for the plan as a spreadsheet file if file creation is turned on; the markdown table is the default.

## Approach
The Kirkpatrick Model, as set out by Kirkpatrick Partners: four levels (reaction, learning, behaviour, results), planned from Level 4 down, with leading indicators and required drivers. The four elements of a data collection plan come from the ROI Institute's methodology page: objectives and measures, methods, sources, timing. The judgement is that depth is a choice, made once and written down. The failure this prevents: every programme gets the same end-of-course form, the flagship gets nothing more, and when the sponsor asks about results there is no row saying who was meant to pull the figure.

## Workflow
1. Ask at most three questions, together: where this programme sits on your own cost and visibility bands; how many weeks people need before they have had a real chance to apply it; and the minimum reporting group you set.
2. Make the depth choice first. From your bands I propose which levels to collect, and you confirm. Not every programme goes to Level 4. Each skipped level is written down with its reason, so nobody later reads silence as a result.
3. Lay out the rows from Level 4 down. Level 4: the result and its leading indicators. Level 3: the critical behaviours. Level 2: knowledge and skill, plus confidence and commitment. Level 1: relevance first, then engagement. Each measure is copied from the agreement word for word; one that looks wrong is flagged for the people who signed, never reworded here.
4. Fill each row: instrument, source, owner, date and reporting group size. The instrument is named by its skill. Level 4 figures come through Business Data Request. Level 3 comes from Training Follow-Up Survey, Behaviour Observation Checklist and Learner Interview Guide. Level 1, and confidence and commitment, come from Post-Training Survey. Knowledge and skill use the course's own check, as a group result.
5. Set the timing. Level 1 at the end of the programme. Level 2 during or at the end. Level 3 after the weeks you gave in step 1. Level 4 on the reporting date in the agreement. A row with no owner or no date is marked "open" and counted at the top.
6. List the required drivers for each behaviour in four kinds: reinforce, monitor, encourage, reward, each with an owner, usually the manager. No drivers, no behaviour change: the plan says so plainly. "Monitor" means a group-level check, never tracking a person.
7. Note the performance environment (tools, workload, process changes) with a date and someone who can confirm it, so a flat result is not blamed on the training or on the people.

## Output Format
```markdown
# Kirkpatrick Data Collection Plan
Programme: [name] | Plan owner: [name, role] | Minimum reporting group: [you set] | Open rows: [count] | Basis: [agreement signed on date / no agreement on file: first draft]
## Depth for this programme
Cost band (yours): [band] | Visibility band (yours): [band] | Levels collected: [levels] | Levels skipped, and why: [level and reason]
## Collection schedule
| Level | Agreed measure, as worded | Instrument | Source | Owner | Date | Reporting group size |
|---|---|---|---|---|---|---|
| 4 Result | [measure] | Business Data Request | [report or system] | [name, role] | [reporting date in the agreement] | [your figure] |
| 4 Leading indicator | [measure] | Business Data Request | [report or system] | [name, role] | [date] | [your figure] |
| 3 Behaviour | [behaviour] | [Training Follow-Up Survey / Behaviour Observation Checklist / Learner Interview Guide] | [learners / observer] | [name, role] | [end date plus the weeks you set] | [your figure] |
| 2 Learning | [knowledge and skill / confidence and commitment] | [the course's own check, group result / Post-Training Survey] | [source] | [name, role] | [date] | [your figure] |
| 1 Reaction | [relevance, then engagement] | Post-Training Survey | [learners] | [name, role] | [last day] | [your figure] |
## Required drivers
| Critical behaviour | Kind (reinforce / monitor / encourage / reward) | What happens | Owner | From |
|---|---|---|---|---|
| [behaviour] | [kind] | [job aid, group-level check, manager conversation, recognition] | [role] | [date] |
## Performance environment
- [Factor: tool, workload or process change] | When: [dates] | Who can confirm it: [role]
## Decision
[Plan owner name] confirms the depth and every row owner by [date, before the programme starts]. [Sponsor name] names the driver owners, or accepts in writing that Level 3 will go unsupported, by [date].
```

## Done When
- The depth choice is written, with a reason for every level skipped.
- Every row collected has an instrument, a source, an owner, a date and a reporting group size, or is counted as open.
- Every critical behaviour has at least one required driver with an owner, or the plan says it has none.
- Every measure reads exactly as it does in the agreement.

## Quality Bar
- Rows run from Level 4 down. A plan that starts from the survey is a Level 1 plan with extra rows.
- The plan names instruments and writes none of their questions. A group below the minimum is merged or its row is not reported. No per-learner score leaves the course.
- No typical response rate, timing norm or depth rule is supplied: the weeks, the bands and the sizes are yours.
- Learning and behaviour data are collected and reported for groups, never used about a person; a named owner stands behind each row.

## Next
Run impact-post-training-survey (Post-Training Survey) to build the first instrument on the plan.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
