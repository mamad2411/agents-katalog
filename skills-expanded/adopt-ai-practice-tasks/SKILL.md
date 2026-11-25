---
name: adopt-ai-practice-tasks
description: Writes three to five AI practice tasks from the team's own work with sanitised material, each with learning points, a first attempt before any model answer, a common exception, a check of the work and a fallback if blocked. Use for "run adopt-ai-practice-tasks", "AI practice tasks", "AI exercises for my team", "practice between AI sessions", "homework after the AI workshop", "AI exercises on real work", "people stopped using it after the training", part of the Claude Guide for AI Adoption Pack by 90n.
---
# AI Practice Tasks
## When To Use
People left the session keen and never opened the tool again because nothing in their week called for it. You want a small set of exercises, drawn from the team's own work, that give them a reason to try again on Tuesday. It answers: what exactly should people practise between sessions, and how do they know the result is good?

## When Not To Use
If people need a prompt at the moment they do the real task, use AI Job Aid: a practice task is an exercise, the card is used during the work. If people are not practising because they have no time, access or permission, exercises will not fix that; run AI Adoption Barrier Diagnosis.

## Inputs
- The team's role, two or three recurring tasks, and when in the week each one comes up.
- Sanitised material for each task: a real document, thread or dataset with names and sensitive details removed.
- The quality criteria the team already uses for this work, the never-put-in list, and who people can ask when stuck.
If you have none of this, I start from one recurring task described in a few lines, write placeholder material, and mark the output as a first draft.

## Approach
The set follows behaviour modelling training, from the meta-analysis by Taylor, Russ-Eft and Chan (2005): learning points, a model, practice, then feedback against the same points. That research also reports that effects shrink from learning to behaviour on the job, which is why every task here is tied to a trigger in the real week. The judgement is the order: the person tries first and sees the model second. The failure this prevents: a worked example people read, agree with and forget, because nothing ever asked them to produce the first version themselves.

## Workflow
1. Ask at most three questions: which recurring tasks the team wants to get better at with AI, what sanitised material exists for each, and which quality criteria the team already uses for that work.
2. Pick three to five tasks that rise in difficulty, each with its trigger in the real week ("when the weekly report is due"). A task with no trigger is an exercise nobody will start. You set the spacing.
3. Write two to four learning points per task as short rules, for example "give it the source document, not your memory of it". Fewer, sharper points beat a full list.
4. Build each task in this order: the trigger, the sanitised material, the first attempt the person makes before any model answer is shown, then the model with each learning point marked where it shows. Mark the model as an example to check, not the right answer.
5. Add one common exception per task (the output invents a figure, the source is too long, the task turns out to be off limits) and what to do when it happens.
6. Write the check of the work: the learning points plus the team's own quality criteria, run as a self-check or with a peer. Leave out speed, confidence and anything that rates the person.
7. Add a fallback for each task: who to ask, and how to finish the work without the tool. Nothing collects who did which task.

## Output Format
```markdown
# AI Practice Tasks
Team: [role or team] | Tasks: [three to five] | Spacing: [you set] | Help route: [role or channel]
## The set
| Task | Trigger in the real week | Difficulty | Sanitised material |
|---|---|---|---|
| [task] | [when it comes up] | [first, middle, stretch] | [what it is, what was removed] |

## Task [n]: [name] (repeat this block for each task)
Learning points: 1. [short rule] 2. [short rule] 3. [short rule]
First attempt: [what the person produces with AI, before seeing any model]
Model, shown after: [example output with each learning point marked; an example to check, not the answer]

| Common exception | What to do |
|---|---|
| [the output invents a figure] | [trace it to the source or remove it] |

| Check of the work | Against | How |
|---|---|---|
| [what to look at in the output] | [learning point or the team's own criterion] | [self-check or peer check] |

Fallback if blocked: [who to ask] | [how to finish without the tool]
## What is not collected
[No completion list, no names, no timing, no rating of anyone's attempt]
## Decision
[Team lead] confirms the tasks and the sanitised material by [date]. The team agrees the spacing and the peer check by [date]. Each person decides which tasks they try.
```

## Done When
- There are three to five tasks, each with a trigger in the real week and sanitised material.
- Every task has learning points, a first attempt before the model appears, one exception, a check of the work and a fallback.
- Nothing in the set records who practised.

## Quality Bar
- The material is the team's own work, sanitised; nothing from the never-put-in list, no invented case study.
- Learning points are rules a person can apply mid-task, and the model shows the checking as well as the asking.
- The check borrows the team's existing quality criteria; it invents no scale and no pass mark. Tasks rise in difficulty.
- The check is on the work, never on the person; nobody's practice is counted or reported.

## Next
Run adopt-ai-output-check (AI Output Check) to make checking a habit before any output is used.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
