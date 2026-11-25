---
name: isd-microlearning-series
description: Drafts a spaced series of short units, one job action each, with a retrieval prompt and a decision in every unit, the order and the gaps between them, and a table of what the series replaces in the long course. Use for "run isd-microlearning-series", "turn this long module into microlearning", "nobody finishes the long course", "plan a spaced series", "short units with retrieval practice", "do not just chop the module into pieces", "what should each micro unit contain", "design a drip course", part of the Claude for Instructional Designers Pack by 90n.
---

# Microlearning Series
## When To Use
Nobody will finish the long module, and the answer is not to chop it into pieces. You have a map of the actions people must take on the job and a long course that buries them. It answers: which few units earn their place, what each one makes the learner recall and decide, and what the long course loses as a result.

## When Not To Use
Not for ordering the lessons of a course taken in one sitting: use Course Curriculum Map. If people need the answer in the middle of the task and do not need it in their heads, the series is the wrong format and Job Aid Template fits. With no agreed actions yet, run Action Mapping Workshop first.

## Inputs
- The actions from your map, or the objectives, for the task the series covers, and the long course or its outline, so the replacement table has something to replace
- How long people must remember this before they use it, in your words
- How units can reach people (the channel, described plainly) and how much time they really have
If you have none of this, I start from one task and the actions you can name, and mark the output as a first draft with the replacement table empty.

## Approach
Two findings carry this skill. Spacing (Cepeda and colleagues, 2006, Psychological Bulletin): practice spread over time is remembered better than practice in one block, and the gap that works best grows with how long people must remember. Retrieval practice (Roediger and Karpicke, 2006, Psychological Science): recalling something from memory helps later retention more than studying it again. Microlearning itself is a format, and an open-access systematic review finds the evidence for it mixed beyond those two effects, so the series is built on the effects and not on shortness. The failure this prevents: the long module cut into equal slices, each still a lecture, now with a longer menu.

## Workflow
1. Ask at most three questions: which actions the series covers; how long people must remember before they use it; how units reach people and how much time they have. Nothing else is asked later.
2. One unit, one action. List each action as a candidate unit; a unit that covers a topic and no action is cut and sent to the replacement table. You decide how many units the audience will tolerate, and I say which actions fall out.
3. Draft each unit in three parts: a retrieval prompt on an earlier unit, answered from memory before anything is shown; one new point with a worked case, marked fictional; a decision the learner makes, with feedback that says why. The first unit retrieves what people already do on the task.
4. Order by whole task, simple to hard: the routine case, then the one with a complication, then the exception. Order by topic is the long course again. Then the gaps: they are yours, longer where people must remember for longer; I leave `[gap you set]` and give no number of days. Fill the retrieval table so each earlier point comes back at least once in a later unit.
5. Fill the replacement table: what in the long course each unit replaces, what moves to a job aid, what is dropped, and who agrees to each drop. A series that only slices the course fails here, and the output says so.
6. Describe delivery in plain terms and list the facts for the expert. Reminders go to everyone on the same schedule, never to people chosen by how they answered.

## Output Format
```markdown
# Microlearning Series Plan
Task: [task] | Audience: [role] | Must be remembered for: [period, in your words] | Date: [date]
## Units
| Unit | Action it serves | Retrieval prompt (from memory, on which earlier unit) | New point and worked case (fictional) | Decision and feedback | Whole task level | Gap before this unit, and why |
|---|---|---|---|---|---|---|
| [n] | [action] | [prompt] / [unit] | [point] / [case] | [decision] / [why] | [routine / complication / exception] | [gap you set] / [how long this must be remembered] |
## Retrieval table
| Earlier point | Taught in unit | Brought back in unit | How |
|---|---|---|---|
| [point] | [n] | [n] | [prompt / decision] |
## What the series replaces
| Part of the long course | Becomes | Reason | Agreed by |
|---|---|---|---|
| [section] | [unit n / job aid / dropped] | [reason] | [role] |
## Delivery
How units reach people: [channel, in plain words]. Reminder schedule, the same for everyone: [schedule you set]. Units can be left and resumed: [yes / no].
## Facts for the expert
| Fact | Unit | Source | Status |
|---|---|---|---|
| [fact] | [n] | [source and place] | [confirmed / to confirm with the expert] |
## Decision
[Name, designer] decides by [date] which units are built and what the series replaces. [Name, sponsor] accepts the dropped content by [date]. [Name, expert] confirms the facts by [date].
```

## Done When
- Every unit serves one action and has all three parts
- Every earlier point is retrieved in at least one later unit, and every gap is set by you or reads `[gap you set]`
- The replacement table accounts for every section of the long course, and each dropped section has a role that agreed to it

## Quality Bar
- A unit is defined by its action, not its length. No unit length, gap or retention figure is invented.
- Retrieval comes before the content it recalls is shown again.
- Worked cases are marked fictional; facts are flagged for the expert and never corrected.
- No record of who opened what or who answered what at individual level, and no reminder aimed at one person's answers.
- Claude drafts the units; you decide what the series replaces, and retrieval prompts are practice, never a score kept on a learner.

## Next
Run isd-live-to-elearning (Live Session to E-Learning Conversion) to plan the move when the source is a live session.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
