---
name: isd-assessment-blueprint
description: Drafts an Assessment Blueprint with a grid of objectives by level, evidence type and number of items, the line where practice ends and assessment begins, and a use-of-results statement naming who decided it. Use for "run isd-assessment-blueprint", "plan the assessment", "table of specifications", "how many questions per objective", "the quiz is written last from the slides", "does this quiz prove anything", "practice or assessment", "what will the results be used for", part of the Claude for Instructional Designers Pack by 90n.
---

# Assessment Blueprint

## When To Use
The quiz is written last, from whatever is on the slides, so the topic with the most slides gets the most questions and the one decision that matters on the job gets none. Use this before the content is written, to answer: what evidence does each objective need, how much of it, where is it practice and where is it assessment, and what will anyone do with a result?

## When Not To Use
This plans and counts; it writes no items. For the questions themselves, run Knowledge Check Questions. If the objectives have no level or evidence type yet, run Measurable Learning Objectives first. Reading results after release is Course Data Review.

## Inputs
- The agreed objectives with their level and evidence type
- The weight the sponsor and the expert give each objective on the job (their words are enough: critical, frequent, rare)
- Whether anyone has asked for a result, who, and what they intend to do with it
If you have none of this, I start from the objectives alone, leave every item count empty, and mark the output as a first draft.

## Approach
The grid is a table of specifications: objectives down the side, cognitive level across, and the number of items in each cell, so the assessment follows the objectives and not the slide count. The tiers of LTEM, from Work-Learning Research, set what counts as evidence: attendance, activity and learner perceptions cannot validate learning; knowledge recall, decision-making competence and task competence can, and more so when remembered after some days. Your judgment decides the weights and where the line sits. The failure this prevents: a recall quiz at the end of a course on handling a refund call, reported upward as proof that people can now handle the call.

## Workflow
1. Ask three questions: how do the sponsor and the expert weight each objective on the job, has anyone asked for a result and what for, and who in the organisation decides how results are used?
2. Build the grid, one row per objective: level, evidence type (recall, decision in a realistic case, performed task), number of items, and where it sits (practice or assessment). You set the number of items from the objective's weight. With no weight I leave `[items you set]`; I propose no count.
3. Run the balance check. The share of items per objective should follow the importance given to it, not the number of slides on the topic. I list every objective with no item and every planned item with no objective; you move the counts.
4. Run the level check. An apply objective needs a decision or a task, never a recall item. Each mismatch is flagged with what it needs, and anything resting only on attendance, clicks or a satisfaction rating is marked as no evidence of learning.
5. Draw the practice and assessment line. Practice is unscored, repeatable and gives full feedback. Assessment starts only where a named person has decided a result is needed. If nobody has, everything is practice, and the blueprint says so plainly.
6. Write the use-of-results statement: what a result will be used for, what it will never be used for, who sees it, how long it is kept, who decided. Reporting is by item and in aggregate by default, leaving out groups under `[group size you set]`. If a result has consequences for a person's job, that is for the organisation and its advisers: check with a qualified adviser.
7. Write any pass mark as `[pass mark, set by whom]`. I never propose one, and I do not draft rankings or reports on individuals; if asked, I say why and offer the by-item view.

## Output Format
```markdown
# Assessment Blueprint
## Grid
| Objective | Level | Weight on the job (given by) | Evidence type | Number of items | Sits in |
|---|---|---|---|---|---|
| [objective 1] | [apply] | [critical, per expert] | [decision in a realistic case] | [items you set] | [practice / assessment] |
## Balance and level check
| Finding | Where | Proposal | Your call |
|---|---|---|---|
| [objective with no item / item with no objective / recall under an apply objective] | [objective # or item] | [add a decision item / drop / raise the level] | [accept / reject] |
## Practice and assessment
| Part of the course | Practice or assessment | Scored? | Repeatable? | Feedback | Who decided a result is needed |
|---|---|---|---|---|---|
| [lesson or module] | [practice] | [no] | [yes] | [full, per option] | [n/a / role] |
## Use of results
- Used for: [improving the course, by item]
- Never used for: [ranking, comparing or grading a learner]
- Who sees it: [role], as [by item, in aggregate; groups under [group size you set] left out]
- Kept for: [period, set by whom] · Pass mark: [pass mark, set by whom / none]
- Consequences for a person's job: [none / yes: decided by the organisation, check with a qualified adviser]
## Decision
[Name, role] decides what a result is used for and signs the use-of-results statement by [date]; [designer name] sets the item counts, and no item is written before both are done.
```

## Done When
- Every objective has a row with an evidence type at the level of its verb
- Every item count was set by you, or is still a placeholder
- Each part of the course is marked practice or assessment, and the use-of-results statement is complete, both naming who decided

## Quality Bar
- Item counts follow the weight on the job, never the slide count
- Recall is planned only where the job needs recall; no pass mark, threshold or count appears that you did not give
- The blueprint counts and places items; item quality is checked when they are written
- Reporting is by item and in aggregate; nothing here ranks or reports on an individual
- Claude drafts the grid; a named person decides what a result is used for, and no learner's result is used to grade them

## Next
Run isd-branching-scenario (Branching Scenario Script) to write the decision practice the blueprint calls for.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
