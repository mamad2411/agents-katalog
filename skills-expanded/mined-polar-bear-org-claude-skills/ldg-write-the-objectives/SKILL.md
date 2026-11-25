---
name: ldg-write-the-objectives
description: Writes learning objectives with an observable verb at the Bloom's level the job needs, a condition and a criterion for each, rewrites of "awareness only" goals, and a flag wherever the check sits below its objective. Use for "run ldg-write-the-objectives", "learning objectives", "write learning objectives", "bloom's taxonomy verbs", "make objectives measurable", "awareness only training", "the objective just says understand the topic", "rewrite these objectives", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Write the Objectives

## When To Use
The only objective on the brief is "understand the topic", and the expert calls half the content "awareness only". You need to say, in words a reviewer can sign, what people will do at the end, in which situation, and how well.

## When Not To Use
If nobody has agreed what people must do on the job, objectives only dress up a topic list: run Map the Actions first. If the objectives are agreed and you need the strategy, practice and check around them, run Write the Design Document.

## Inputs
- The on-the-job actions or tasks the course is for (from your action map or task breakdown)
- Any draft objectives, the brief, or the expert's topic list
- The learners by role, what they already do today, and any check that exists or is planned
If you have none of this, I start from the course title and one sentence on the job it supports, and mark the output as a first draft.

## Approach
The method is the revised Bloom's taxonomy, as a university teaching-centre page sets it out: remember, understand, apply, analyse, evaluate, create, each stated as a verb. Each objective also gets a condition and a criterion. The judgement is in the level: the right one is the level the job asks for, which is often lower or higher than the verb list tempts you to write. The failure this prevents: a course on handling complaints whose objective says "know the escalation policy", whose quiz asks which team owns escalations, and whose learners still freeze when an angry caller asks for a manager.

## Workflow
1. Ask three questions: which on-the-job actions must this course change, what does doing them well look like to the sponsor, and which topics has the expert called "awareness only"?
2. Trace first. List every action or task, then tie each draft objective and topic to one. Whatever ties to nothing goes on a "no action found" list for the expert to link or drop; it does not get an objective to keep the peace.
3. Pick the level the job needs, not the highest. Choosing between two responses is apply or analyse; judging a colleague's draft against a standard is evaluate. Question every remember-level item: could a job aid carry this instead of a person's memory?
4. Replace the verb. Strike "understand", "know", "be aware of" and "appreciate" and write one observable verb at the chosen level (classify, choose, draft, diagnose, justify). Two verbs usually hide two objectives: split them. If you cannot picture someone watching it happen, rewrite it.
5. Add the condition (given what: the tools, the information, the situation) and the criterion (how well: accuracy, time, standard). You set every criterion; I leave it as a [placeholder] and never invent one.
6. Rewrite each awareness-only goal by asking what someone who is aware does differently on a working day. If the honest answer is nothing, I propose cutting it or moving it to a reference page, with a reason the expert can accept.
7. Compare each objective with its existing or planned check, and flag any check that sits at a lower level (a recall question under an analyse objective) so it is rewritten before the build.

## Output Format
```markdown
# Learning Objectives
Course: [name] | Learners (role): [role] | Draft date: [date]
## Objectives
| # | On-the-job action | Objective (given, verb, criterion) | Level | Could a job aid carry this? | Check, and its level |
|---|---|---|---|---|---|
| 1 | [action or task] | Given [condition], [role] will [one verb] [object] to [criterion you set] | [apply] | [no / yes, move to look-up] | [planned check] at [level] |
## Awareness-only goals
| Goal as written | What an aware person does differently | Proposal |
|---|---|---|
| [be aware of X] | [observable change, or "nothing"] | [rewritten objective / cut / move to reference], because [reason] |
## For the expert
- No action found: [topic], link it to an action or agree to drop it
- Check below its objective: [objective #], [current check], [level it needs]
## Decision
[Sponsor name] and [expert name] agree the objectives and their criteria by [date], before the evaluation is planned and the design is written.
```

## Done When
- Every objective traces to a named on-the-job action or task
- No objective uses "understand", "know", "be aware of" or "appreciate" as its verb, and each has one verb only
- Every objective has a condition and a criterion, with criteria left as placeholders you set
- Each awareness-only goal is rewritten or proposed for cutting, with its reason
- Every check below its objective's level is flagged

## Quality Bar
- The level matches the job task; a higher level is not a better objective
- The verb names something a person could be seen doing in the condition given
- A remember-level objective stays only if the job needs it in the head mid-task
- Objectives describe what the role does, never one named person's shortfall
- Claude drafts the objectives; the sponsor and the expert agree them, and a criterion describes the check, never a pass mark held against a person

## Next
Run ldg-plan-the-evaluation (Plan the Evaluation) to agree what should change before the design is written.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
