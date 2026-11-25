---
name: impact-performance-problem-diagnosis
description: Diagnoses one performance problem before anything is built, producing the gap by task in one unit, a cause table that separates the work environment from skill and knowledge at role level, a cheap check for every assumed cause and a verdict on how much of the gap training could close. Use for "run impact-performance-problem-diagnosis", "is it a training problem", "performance consulting", "why are people not doing it", "cause analysis", "performance problem diagnosis", "can't do or won't do", "is it a skill gap", part of the Claude Guide for Training Impact Pack by 90n.
---

# Performance Problem Diagnosis

## When To Use
The conversation with the sponsor left you unsure whether people cannot do it or are not set up to do it. Use this when you have notes, perhaps a report or two, and a build date approaching. It answers: what is causing this gap, which causes are shown and which are only assumed, and how much of it could training close?

## When Not To Use
If you already know the causes and need something to offer the sponsor, use Non-Training Options: this skill names causes and stops. For needs across several roles, use Training Needs Assessment Update. If a request asks what is wrong with one person, this is not the tool. Restate it to the role and the task first.

## Inputs
- Your notes from the sponsor conversation, or the request restated as a performance line.
- Any evidence of the gap: error counts, cycle times, tickets, complaints. Upload the export as a CSV file, or paste it. Group figures only: aggregate the file before you share it, with no row per person.
- What people in the role work with: the process, the tools, the guidance, how good work gets noticed.
If you have none of this, I start from the performance line alone, mark every cause "assumed" and mark the output as a first draft.

## Approach
Performance analysis and cause analysis, the first two processes of the Human Performance Technology model attributed to ISPI, as described on the University at Buffalo's page on the model. The cause table has two sides, the work environment and the role, and each cause carries its evidence or the word "assumed". The judgement is that an honest "assumed" with a way to check it is worth more than a confident guess. The failure it prevents: a second, longer course for people who already know how, while the target that rewards speed over accuracy goes untouched.

## Workflow
1. Ask at most three questions, all at once: which tasks the gap shows up in, what number or report shows it, and how big a gap you consider worth acting on.
2. Per task, write desired and actual performance in the same unit, and the gap. Gaps below the size the user set are marked "watch, not act". A task with no actual figure reads "not measured", never an estimate.
3. Build the cause table in two sides. Work environment: information and feedback, tools and resources, incentives and consequences, process. Role level: skill and knowledge, capacity, motivation, read as what the work rewards and never as someone's attitude. Start with the environment side, since it is the side a training request skips.
4. Give every cause its evidence (the source and what it shows) or the word "assumed". What the sponsor believes is recorded as the sponsor's view, not as evidence.
5. Ask the skill question for each task: could people in the role do it correctly if conditions were right, or have they done it right before? If yes, it is not a skill gap, however loud the request.
6. Write a cheap check for every assumed cause: who to ask or what to look at, what would confirm it and what would kill it, and how long it takes by the user's own estimate. A person runs the checks. Checks look at the work and at group figures, never at one person's record.
7. Give the verdict: how much of the gap training could close, in words (most, some, little, none), with the reasoning and what training alone would leave untouched. No percentage unless the user's own data gives one. With assumed causes still open, the verdict is "provisional".

## Output Format
```markdown
# Performance Problem Diagnosis
Problem: [role] are [actual] and need to be [desired], shown by [measure] | Gap worth acting on: [you set] | Status: [provisional / checked]
## Gap by task
| Task | Desired | Actual | Unit | Gap | Source | Act or watch |
|---|---|---|---|---|---|---|
| [task] | [your figure] | [your figure or "not measured"] | [unit] | [difference] | [report, role that holds it] | [act / watch] |
## Causes
| Task | Side | Category | Cause | Evidence or "assumed" |
|---|---|---|---|---|
| [task] | [work environment / role level] | [information and feedback, tools and resources, incentives and consequences, process, skill and knowledge, capacity, motivation] | [cause, stated about the work] | [source and what it shows, or "assumed"] |
## Skill question
| Task | Could people in the role do it if conditions were right? | Done right before? | Skill gap? |
|---|---|---|---|
| [task] | [yes / no / not known] | [yes / no / not known] | [yes / no / not known] |
## Checks for assumed causes
| Assumed cause | Who to ask or what to look at | Confirms it | Kills it | Time needed (your estimate) | Run by (role) |
|---|---|---|---|---|---|
| [cause] | [role, report or place] | [what you would find] | [what you would find] | [your estimate] | [role] |
## Verdict
Training could close [most / some / little / none] of this gap, because [reasoning]. Training alone would not change: [causes].
## Decision
[L&D lead, by name] runs the checks by [date]. [Sponsor, by name] decides by [date] whether to look at options for the causes that are not skill gaps before anything is built.
```

## Done When
- Every task has desired and actual in the same unit, or reads "not measured".
- Every cause has a source or says "assumed", and every assumed cause has a check with something that would kill it.
- Each task has an answer to the skill question, even if it is "not known", and the verdict is one of four words with its reasoning.

## Quality Bar
- One performance problem per diagnosis, and no options, recommendation or course outline: it names causes and stops.
- Gap sizes and thresholds are the user's. Claude supplies no norm and fills no empty cell.
- No "low performer" list, and no comparison of individuals or of teams' managers. Causes are written about the role and the work.
- A cause with no evidence stays "assumed"; nothing is written about a named person's ability or motives, and a named person decides what happens next.

## Next
Run impact-non-training-options (Non-Training Options) to offer something for each cause that is not a skill gap.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
