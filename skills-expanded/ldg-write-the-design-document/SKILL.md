---
name: ldg-write-the-design-document
description: Drafts the design document for one course or programme, with the audience by role and need, a strategy, practice and check per objective, every design decision with its options and rationale, what was left out and why, and a sign-off block. Use for "run ldg-write-the-design-document", "instructional design document", "instructional design", "design document for this course", "ADDIE design phase", "backward design", "get sign-off before we build", "show the design decisions", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Write the Design Document

## When To Use
Leaders think AI can do the job and nobody sees the design decisions behind a course. Write this when the sponsor only ever sees finished screens, so that what you chose, what you turned down and why are on one page that people sign before the build.

## When Not To Use
If the objectives still say "understand the topic", run Write the Objectives first; a design on vague objectives records vague decisions. If you are laying several modules out in order across a programme, that belongs in Map the Curriculum.

## Inputs
- The agreed objectives, and the action map or gap diagnosis behind them
- The audience by role (what they do today, where they work, the time they can give) and the expert's notes
- The agreed result and behaviours from your evaluation plan, and the fixed limits (deadline, budget, tools)
If you have none of this, I start from the brief and the sponsor's one-line business problem, and mark the output as a first draft.

## Approach
The method is the design phase of ADDIE (from the 1975 Florida State University procedures, where each step records its rationale and a management decision) with backward design as a university teaching-centre guide describes it: desired results, then acceptable evidence, then learning experiences. A draft is quick to produce; the choices in it are yours, and this document is where they become visible. I can draft it in Claude Docs (beta), or any document. The failure this prevents: two weeks before launch a director asks why the product history is missing, nobody can find where that was decided, and it goes back in as six screens.

## Workflow
1. Ask three questions: what result will the sponsor look at, what must people do differently to get it, and which limits are fixed (deadline, budget, tools, time off the job)?
2. Results first. Write the need in one line ("[role] are [actual] and need to be [desired], shown by [measure]") and list the objectives exactly as agreed. If one needs rewording, that goes back to the people who agreed it.
3. Evidence second. For each objective, name the check that would show it, at the same level: a decision objective gets a decision to make, never a recall question.
4. Experiences last. For each objective choose the strategy (worked example, scenario, role-play, job aid, on-the-job task) and the practice, before any content. Content is only what the practice needs.
5. Keep the decision log as you go: what was decided, the options you weighed, the rationale and who agreed. A rationale cites the need, an objective or a limit. "It looks better" is taste, and taste loses the first argument with a senior reviewer. "Left out and why" is its own section, one row per item, with where the material lives instead; these rows are what stop late additions.
6. Add one evaluation line pointing to the agreed result and behaviours, without rebuilding the measures, then the sign-off block. Nothing is built before it is signed; later changes go through your review plan's change rule.

## Output Format
```markdown
# Design Document
## Audience and need
- Audience (by role): [role, what they do today, where they work, time available]
- Need: [role] are [actual] and need to be [desired], shown by [measure]. Fixed limits: [deadline], [budget], [tools], [time off the job]
## Design per objective
| Objective (as agreed) | Check at the same level | Strategy | Practice | Content the practice needs |
|---|---|---|---|---|
| [objective 1] | [decision on a case] | [scenario] | [decide what to do in [situation]] | [the minimum] |
## Decision log
| Decision | Options considered | Rationale (need, objective or limit) | Agreed by (role) |
|---|---|---|---|
| [decision] | [option A / option B / option C] | [rationale] | [role] |
## Left out and why
| Item | Why it is out | Where it lives instead | Agreed by (role) |
|---|---|---|---|
| [topic or module] | [no objective needs it] | [reference page / job aid / nowhere] | [expert] |
## Evaluation and sign-off
- Agreed result: [result]. Critical behaviours: [behaviours]. Measures and dates are in the evaluation plan.
| Version | Sponsor | Expert | L&D lead |
|---|---|---|---|
| [v1] | [name, date signed] | [name, date signed] | [name, date signed] |
## Decision
[Sponsor name] and [expert name] sign version [v1] by [date]; [L&D lead name] starts the build only after both signatures.
```

## Done When
- Every objective has a check at the same level, a strategy and a practice in one row
- Every decision shows the options considered and a rationale that is not taste, and "Left out and why" has a row for each item the expert or the sponsor asked for and did not get
- The evaluation line adds no new measure, and the sign-off block names three roles and a version

## Quality Bar
- The order is results, evidence, experiences; a format is never picked first and justified later
- The audience is described by role and task, never by named people or a personal profile
- Objectives appear unchanged, and limits you did not give (budget, seat time) stay as [placeholders]
- Claude drafts the document; the design decisions are yours, and the sponsor and an expert sign before anything is built

## Next
Run ldg-map-the-curriculum (Map the Curriculum) to lay the modules out in order.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
