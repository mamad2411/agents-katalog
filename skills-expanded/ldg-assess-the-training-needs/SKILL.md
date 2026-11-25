---
name: ldg-assess-the-training-needs
description: Finds what a role or team lacks, producing needs by role and task with the evidence for each, a priority table on criteria the team sets and a "training cannot fix" list. Use for "run ldg-assess-the-training-needs", "training needs assessment", "training needs analysis", "learning needs analysis", "TNA", "what training does my team need", "skills gap by role", "stop the training wish list", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Assess the Training Needs

## When To Use
You need to know what a team actually lacks, not collect a yearly wish list of course titles. Use this when a role changes, when requests from one team keep piling up, or before the year is planned. It answers: which needs, in which roles and tasks, matter most to the business, and which of them can training fix?

## When Not To Use
For one problem with one measure, Diagnose the Performance Gap is faster and sharper. This skill also stops at ranked needs: deciding what runs this year within your days and budget is Plan the L&D Year.

## Inputs
- The business goals or changes the team faces, and the roles in scope with their main tasks.
- The data that exists: quality or error reports, tickets, process documents, onboarding and exit feedback, past requests.
- Interview, observation or survey notes, already aggregated. No appraisal scores, performance ratings or named individuals.
If you have none of this, I start from the roles and the business goals and mark the output as a first draft.

## Approach
Learning needs analysis as the CIPD factsheet describes it: organisation, team and individual levels looked at together. This guide replaces the individual level with role and task, so it rates needs, never people. The judgement is that a need exists only where a task, a piece of evidence and a consequence meet. The failure it prevents: a survey asks every manager which courses their team wants, the most familiar titles win, and the calendar fills with sessions that no business goal asked for.

## Workflow
1. Ask at most three questions: which business goals or changes must this serve, which roles are in scope, and below what group size should survey results be suppressed?
2. Read three levels together. Organisation: the strategy and the capability it will need. Team: where work stalls or quality drops. Role and task: what people in each role must do. A need that appears at one level only is worth a second look.
3. Mix the sources: existing data, interviews, observation, surveys, business documents. You run the interviews and the observation; I prepare the questions and sort what comes back. One source alone is a hint, flagged "single source".
4. Write each need the same way: role, task, evidence source, how many in the role it affects (from your data, never an estimate), and the consequence if it stays unmet.
5. Split every need. Training can fix it when the cause is skill or knowledge. It cannot when the cause is information, tools, incentives or process; those go to the second list and on to Diagnose the Performance Gap, not onto a course list.
6. Build the priority table for the trainable needs on criteria and weights you set. Scores sit in the open so anyone can challenge them. Needs are scored, never people. The tables can come as a spreadsheet file, if file creation is on.

## Output Format
```markdown
# Training Needs by Role and Task
Scope: [roles, team] | Goals served: [business goals] | Suppression size: [set by you]
## Needs
| Role | Task | Need | Evidence sources | Single source? | People in role affected | Consequence if unmet |
|---|---|---|---|---|---|---|
| [role] | [task] | [need] | [data, interview, observation, survey, document] | [yes / no] | [count from your data] | [business effect] |
## Priority of the trainable needs
Criteria and weights (set by you): [criterion 1, weight] | [criterion 2, weight] | [criterion 3, weight]
| Need | [Criterion 1] | [Criterion 2] | [Criterion 3] | Weighted total | Rank |
|---|---|---|---|---|---|
| [need] | [score] | [score] | [score] | [total] | [n] |
## Training cannot fix
| Need | Likely cause | Who could fix it (role) | Send to |
|---|---|---|---|
| [need] | [information, tools, incentives, process] | [role] | Diagnose the Performance Gap |
## Still to find out
[Single-source needs and the second source that would confirm each one.]
## Decision
[L&D lead] agrees the top needs and the criteria with [sponsor] by [date].
```

## Done When
- Every need names a role and a task, never a person.
- Every need has at least one evidence source, and single-source needs are flagged with the source that would confirm them.
- The criteria and weights are yours and are printed above the priority table.
- Environment causes sit in "training cannot fix", not in the ranking.

## Quality Bar
- A course title is not a need until it ties to a task and a consequence.
- Survey results appear in aggregate only; groups below the suppression size you set are dropped.
- Counts come from your data; Claude never estimates how many people lack something.
- No appraisal scores, performance ratings or named individuals are used, even if offered.
- Needs are analysed by role and task; no named person is rated, and the L&D lead agrees the priorities with the sponsor.

## Next
Run ldg-map-the-actions (Map the Actions) to turn the top need into on-the-job actions and practice.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
