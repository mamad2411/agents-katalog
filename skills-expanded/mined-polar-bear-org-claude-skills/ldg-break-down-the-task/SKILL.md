---
name: ldg-break-down-the-task
description: Builds a task breakdown for one role, with the task list, the steps, decisions and standard per task, a blank difficulty, importance and frequency table for people who do the work to fill, and a train, job aid, practise often or leave out call per task. Use for "run ldg-break-down-the-task", "task analysis", "job task analysis", "task list for a role", "what should be in the course", "difficulty importance frequency", "DIF analysis", "the outline follows the manual", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Break Down the Task

## When To Use
The course outline follows the manual's chapters and nobody has listed what people in the role actually do. Use this before the outline is fixed, when you can reach a few people who do the work. It answers: which tasks make up this role, and which of them deserve training time, a job aid, repeated practice, or nothing at all?

## When Not To Use
If you start from one business goal and need the few actions that move it, run Map the Actions; this skill covers the whole role, which is more than one goal needs. If you are comparing needs across several roles, use Assess the Training Needs. For the judgement hidden inside one hard task, run Interview the Expert.

## Inputs
- The role, and what you have on it: procedures, the manual's contents page, a job description, your expert interview notes
- Who can fill the ratings (people who do the work and their team leads, by role), and your team's rating scale if one exists
If you have none of this, I start from the role's name and the tasks you can list from memory, and mark the output as a first draft.

## Approach
Job and task analysis with task selection by difficulty, importance and frequency, from the US Department of Energy training handbook (DOE-HDBK-1078-94), which sorts rated tasks into train, no train and overtrain lists and has experts validate them. It was written for high-hazard facilities, so use it lightly. "Overtrain" is called "practise often" here, and the job aid call is this guide's addition. The failure this prevents: a full morning on the thing everyone does many times a day, and a single slide on the rare task where an error is expensive, because that is how the manual was weighted.

## Workflow
1. Ask up to three questions: which one role, who will fill the ratings, and which sources I can read.
2. Draft the task list for that role only. Each task is an action verb plus an object, something you could watch, with a clear start and end. "Understand the returns policy" is a topic and gets rewritten or dropped; "process a return without a receipt" is a task. Each line carries its source.
3. For each task, write the steps, the decisions inside it and the standard: what "done right" means to someone checking the result. Where the sources are silent, the cell says "ask the expert".
4. Prepare the blank rating table: difficulty, importance, frequency, on a scale your team sets and defines in words. People who do the work and their team leads fill it. I never fill a rating, and the ratings describe the task, not how well anyone performs it.
5. Write the sorting rule down before anyone looks at the ratings, then apply it. A common reading for you to confirm: difficult, important and rarely done means practise often; easy and done daily means leave out; rare or detailed steps that can be looked up mid-task mean job aid; the rest of what is hard and matters means train.
6. Show the result against the manual: tasks with no chapter, chapters with no task. That gap is the argument for a new outline.
7. Send the calls back to the experts for validation before the outline is built, and record what they changed and why.

## Output Format
```markdown
# Task Breakdown
## Role and sources
Role: [role] | Sources: [procedures, interview notes, people asked] | Ratings filled by: [roles] | Scale: [scale and what each point means]
## Tasks
| No. | Task (verb + object) | Steps | Decisions inside it | Standard | Source |
|---|---|---|---|---|---|
| [1] | [Task] | [Steps] | [Decisions] | [What done right means] | [Source or "ask the expert"] |
## Ratings (filled by people who do the work)
| No. | Difficulty | Importance | Frequency | Notes from raters |
|---|---|---|---|---|
| [1] | [to fill] | [to fill] | [to fill] | [to fill] |
## Call per task
Sorting rule, written before the ratings were read: [the rule the team agreed]
| No. | Call (train / job aid / practise often / leave out) | Reason from the rule | Expert validation |
|---|---|---|---|
| [1] | [Call] | [Reason] | [Agreed / changed to ..., why] |
## Against the manual
Tasks with no chapter: [list] | Chapters with no task: [list]
## Decision
[Expert name] and [L&D lead name] sign the call per task by [date], before the outline is built.
```

## Done When
- The list covers one role, and every task is a verb plus an object you could observe
- Every rating was entered by a person who does the work or leads it
- The sorting rule is written above the calls, and each call cites it
- The experts have seen the calls, and their changes are recorded

## Quality Bar
- Topics and knowledge areas are not tasks; they attach to the task that needs them or go
- A "leave out" call names where the task is learned instead, even if that is "on day one, by doing it"
- Safety and regulated tasks keep their mandatory treatment whatever the ratings say: check with a qualified adviser
- The ratings describe tasks, never people; people who do the work fill them in, and the expert and the L&D lead sign the calls

## Next
Run ldg-plan-the-reviews (Plan the Reviews) to agree who signs what before the build starts.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
