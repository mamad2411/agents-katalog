---
name: isd-does-it-teach-review
description: Reviews a storyboard or draft course objective by objective, producing a grid of what is shown, tried and given feedback, an alignment table of objective, practice and check, and a list of fixes the designer accepts or rejects. Use for "run isd-does-it-teach-review", "does this course teach anything", "it looks finished but nobody practises", "which objectives are never practised", "too much telling and no asking", "review this storyboard against the objectives", "is the quiz at the level of the objective", "this reads like any course on any topic", part of the Claude for Instructional Designers Pack by 90n.
---

# Does It Teach Review

## When To Use
The course looks finished and you suspect it teaches nothing. Every screen is tidy, the narration is fluent, and you cannot point to the moment a learner does the thing the objective names. This desk review answers one question: is each objective shown, tried and given feedback at its level?

## When Not To Use
It does not check facts (AI Content Accuracy Check), access (Accessibility Check) or how the built course behaves when someone takes it start to finish (Designer Run-Through). It is a review on paper against objectives, so it cannot tell you what real learners do: that is Learner Pilot Test. With no objectives at all, write them first with Measurable Learning Objectives.

## Inputs
- The objectives, each with its level.
- The storyboard, or the text of the built course screen by screen, with practice and checks included, and the Course Design Document if you have one.
If you have none of this, I start from the course text alone, infer the objective each section seems to serve, and mark the output as a first draft.

## Approach
Merrill's First Principles of Instruction (2002, Educational Technology Research and Development) are used here as a review grid: a real problem, activation, demonstration, application, integration. Next to it sits the alignment of objective, practice and check, and cognitive load theory (Sweller, van Merriënboer and Paas, 2019) for what to take out. A university's guidance on evaluating AI output names three risks: inaccurate, generic, misaligned. This review handles the last two. The failure it prevents: screen after polished screen explaining how to handle a refund call, one "click to reveal", and a recall question at the end, signed off because nothing on any single screen is wrong.

## Workflow
1. Ask up to three questions: which objectives and levels are agreed, which version you are reviewing, and whether there is content the sponsor insists on that serves no objective.
2. Fill the grid one objective at a time. Real problem: is there a task from this job? Demonstration: is it shown with the reasoning, as a worked example? Application: does the learner make a decision or perform the task? "Click to reveal" and "drag the label" are not application. Integration: is the learner asked to use it on their own work? Mark each present, weak or absent, with the screen. For every practice, check the feedback: does it say why and show the consequence, or only "correct" and "try again"?
3. Set the levels side by side: objective, practice, check. A recall check under an apply objective is a mismatch. So is practice that is harder than anything demonstrated.
4. Count screens that tell against screens that ask. The count describes the course. It is not a score, it carries no threshold, and it is not a target.
5. List load to remove (decoration, narration that repeats the screen, history and background serving no objective) and generic passages: content that names no task, no case and no mistake from this job and could sit in any course on any topic.
6. Propose fixes, ordered by what the learner gains, most first. You accept or reject each with a reason. The review never says the course passes.

## Output Format
```markdown
# Does It Teach Review
Reviewed: [course, version, storyboard or build] | Review run by: [designer, role], [date]
## Grid by objective
| Objective (level) | Real problem | Activation | Demonstration | Application | Integration |
|---|---|---|---|---|---|
| [objective] | [present / weak / absent, screen] | [..., screen] | [..., screen] | [..., screen] | [..., screen] |
## Alignment
| Objective (level) | Practice (level, screen) | Feedback says why? | Check (level, item) | Mismatch |
|---|---|---|---|---|
| [objective] | [activity or none] | [yes / only right or wrong / none] | [item or none] | [none, or what] |
## Tell and ask
Tell screens: [n] | Show screens: [n] | Ask or practise screens: [n] | Longest run of tell screens: [screens x to y]
## Load to remove and generic passages
| Screen | What it is | Kind (decoration / repeated narration / background / generic) | Objective it serves |
|---|---|---|---|
| [screen] | [content] | [kind] | [none] |
## Fixes, most gain for the learner first
| Order | Fix | What the learner gains | Objective | Accept or reject | Designer's reason |
|---|---|---|---|---|---|
| [1] | [fix] | [gain] | [objective] | [designer fills] | [designer fills] |
## Decision
Review run by [designer, role] on [date], version [x]. [Designer name] accepts or rejects each fix by [date] and names which accepted fixes are made before the run-through.
```

## Done When
- Every objective has a full grid row, with a screen cited for each cell.
- Every objective with no application, or with a check below its level, is named.
- Every fix has an accept or reject and a reason in the designer's words, and the review states the version and date it ran on.

## Quality Bar
- "Present" needs a screen number; a cell with no screen is "absent".
- No facts are judged here, no access issues, no interface problems: they go to their own checks.
- The review is of the course. It never judges the designer or the expert who wrote it.
- Claude shows where practice and feedback are missing; you decide what the learner needs and which fixes to make.

## Next
Run isd-accessibility-check (Accessibility Check) for the next check before you take the course yourself.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
