---
name: isd-measurable-objectives
description: Drafts Measurable Learning Objectives with one objective per action (condition, observable verb, criterion), the level the job needs, the kind of evidence each objective will need, and a list of items that are not course objectives. Use for "run isd-measurable-objectives", "write measurable objectives", "the objective just says understand the policy", "rewrite be aware of", "which verb for this objective", "condition behaviour criterion", "what level does this objective need", "is this an objective or a job aid", part of the Claude for Instructional Designers Pack by 90n.
---

# Measurable Learning Objectives

## When To Use
The only objective on the page is "understand the policy", and everything downstream will inherit that fog: the practice, the questions, the argument about what to cut. Use this when you have actions or tasks and need to say what a learner will be able to do, given what, how well, and what you would have to see to believe it.

## When Not To Use
If nobody has yet agreed what people must do on the job, objectives only dress up a topic list: run Action Mapping Workshop first. If you need to decide how many items each objective gets and where assessment starts, that is Assessment Blueprint; this skill names the evidence type and stops.

## Inputs
- The actions from your action map, or the job tasks the course touches
- Any draft objectives, the expert's topic list, and the goals someone has called "awareness"
- The learners by role, and what they already do today
If you have none of this, I start from the course title and one sentence on the task it supports, and mark the output as a first draft.

## Approach
The revised Bloom's taxonomy, as set out by the University of Waterloo Centre for Teaching Excellence, gives six levels: remember, understand, apply, analyse, evaluate, create. Each objective is then written in the condition, behaviour, criterion format, so it says given what, does what, how well. The judgment is yours at two points: which level the job really needs, and what evidence would convince you. The failure this prevents is the verb list used as decoration: "understand" swapped for "describe" down the whole list, every line still a topic, and a course that teaches people to describe a lockout procedure they will never be asked to describe.

## Workflow
1. Ask three questions: which actions or tasks must this course change, which goals has anyone called "awareness" or "nice to know", and who will agree the criteria (sponsor and expert, by role)?
2. Trace first. Write one row per action and draft one objective for it. Any draft objective or topic that traces to no action goes to "no action found" for the expert to link or cut. I do not find it a home.
3. Pick the level the job needs, not the highest one. Choosing which refund applies on a live call is apply; knowing where the form is kept is remember, and is probably not a course objective at all. You confirm each level, because you know the job.
4. Replace the verb. Strike "understand", "know", "be aware of" and "appreciate", and write one verb someone could watch happen. Two verbs mean two objectives: I split them and you decide whether both stay.
5. Add the condition (the tools, information and situation the learner has) and the criterion (how well). You set every criterion with the sponsor and the expert. Where none is given I write `[criterion you set]` and never supply one.
6. Rewrite each awareness goal by asking what an aware person does differently. If the honest answer is nothing, I propose cutting it or moving it to reference, and it goes on the "not a course objective" list with where it should live.
7. Name the evidence type per objective, at the same level as the verb: recall, a decision in a realistic case, a performed task, or a product. An apply objective with recall evidence is flagged for you.

## Output Format
```markdown
# Measurable Learning Objectives
## Objectives
| # | Action it traces to | Given (condition) | Learner will (one verb, object) | To (criterion) | Level | Evidence type |
|---|---|---|---|---|---|---|
| 1 | [action from the map] | [tools, information, situation] | [verb] [object] | [criterion you set] | [apply] | [decision in a realistic case] |
## Rewrites of "understand" and "be aware"
| Original wording | What a person does differently | Rewrite, or proposal to cut |
|---|---|---|
| [be aware of X] | [observable change, or "nothing"] | [objective # / cut / move to reference] |
## Not a course objective
| Item | Why not | Where it should live |
|---|---|---|
| [where the form is kept] | [looked up at the moment of work] | [job aid / reference page / cut] |
## Open items
- No action found: [topic], for [expert role] to link or cut
- Evidence below the level of the verb: [objective #], [what it needs]
- Criterion not yet set: [objective #], [who sets it]
## Decision
[Designer name] decides the level and the wording of each objective; [sponsor name] and [expert name] agree the criteria and the "not a course objective" list by [date], before design starts.
```

## Done When
- Every objective traces to a named action or task, or the item sits under "no action found"
- No objective uses "understand", "know", "be aware of" or "appreciate", and each has exactly one verb
- Every objective has a condition, a criterion (set by you or left as a placeholder) and an evidence type at the level of its verb
- Each awareness goal is rewritten, or proposed for cutting with a reason

## Quality Bar
- A higher level is not a better objective, and every remember-level objective is questioned: could a job aid carry this?
- A criterion describes how a check is designed, never a pass mark used on a person
- Objectives describe what a role does on a task, never a named person or a team's shortfall
- Claude drafts the wording; you decide what the learner needs to be able to do, and the sponsor and the expert agree the criteria

## Next
Run isd-course-design-document (Course Design Document) to set the strategy and practice for each objective.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
