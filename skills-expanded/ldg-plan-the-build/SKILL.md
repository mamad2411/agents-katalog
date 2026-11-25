---
name: ldg-plan-the-build
description: Plans the build of one training programme from brief to launch, producing phases with a deliverable, an owner by role and a closing decision each, review gates, durations taken from your own past projects, a scope line for the deadline and the risks that break the date. Use for "run ldg-plan-the-build", "addie model", "instructional design project plan", "course development timeline", "training project plan", "how long to build a course", "course due Monday", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Plan the Build

## When To Use
The brief lands Thursday and the programme is due Monday. Or it is due in two months and nobody has said who delivers what, or who closes each phase. Run this when one programme is approved and needs a plan a sponsor can read. It answers: what gets built by when, by which role, and what has to move to a later release for the date to hold?

## When Not To Use
If the only trouble is review rounds that never end, Plan the Reviews is lighter and goes deeper on that point. If the question is which programmes to build at all, run Plan the L&D Year first. The design decisions themselves belong in Write the Design Document.

## Inputs
- The brief: the need, the learners by role, the deadline, the sponsor, and any format already promised.
- How long two or three of your own past builds took, phase by phase, even roughly, and who is available by role, including when the expert and the reviewers can answer.
If you have none of this, I start from the brief and the deadline and mark the output as a first draft, with every duration as a [placeholder].

## Approach
The frame is ADDIE, from the 1975 Florida State University procedures: analyse, design, develop, implement, evaluate, each phase closed by a decision. Read as a waterfall, feedback comes too late, so the plan adds review gates from iterative development: a first design proof, a full draft, a corrected version, a final version. The judgement is to size the scope to the date, and to say out loud what moved. The failure it prevents: the date is promised first, the analysis becomes one phone call, the expert opens the full draft the evening before launch, and the weekend goes on rewriting module two.

## Workflow
1. Ask at most three questions: what is the fixed date and what happens if it slips, which of your past builds is closest in size and how long each phase took, and who gives the final sign-off?
2. Lay out the five phases. For each: the deliverable (need statement, design document, built course, launch with trainers ready, evaluation plan and first read), the owner by role, the dates, and the decision that closes it. A phase with no closing decision is not finished, it has only stopped.
3. Place the review gates where reviewers can answer fast: design proof early, then full draft, corrected version and final. If reviewers cannot turn work round in the time, keep fewer gates and write why. Who reviews what, in how many rounds, is detail for the review plan.
4. Take durations ONLY from your own past projects, scaled to this build. A phase with no history is marked "[duration, no history]". I never supply a benchmark such as hours per minute of content.
5. Count back from the deadline. Where the phases do not fit, write the scope line: what the date allows in release one, and what moves to a later release (extra modules, video, translations, the harder scenarios). Analysis is never the thing cut to zero: it can be short, and then the plan names it as short and says what was not checked.
6. Name the risks that break the date (expert time, a late reviewer, missing content, tool access), each with an owner by role and the first sign to watch for.

## Output Format
```markdown
# Build Plan
Programme: [name] | Sponsor: [role] | Deadline: [date] | Final sign-off: [role]
## Phases
| Phase | Deliverable | Owner (role) | Start | End | Duration taken from | Decision that closes it |
|---|---|---|---|---|---|---|
| Analyse | [need statement] | [role] | [date] | [date] | [past project, or "no history"] | [sponsor agrees the need] |
| Design | [design document] | [role] | [date] | [date] | [past project] | [expert signs the objectives] |
| Develop | [built course] | [role] | [date] | [date] | [past project] | [final version signed] |
| Implement | [launch, trainers ready] | [role] | [date] | [date] | [past project] | [go-live] |
| Evaluate | [evaluation plan and first read] | [role] | [date] | [date] | [past project] | [sponsor reviews the first read] |
## Review gates
| Gate | What is reviewed | Reviewer (role) | Date |
|---|---|---|---|
| [design proof, full draft, corrected version, final version, or "left out because"] | [what] | [role] | [date] |
## Scope line
Release one, by [date]: [what the date allows] | Later release, by [date]: [what moves]
Analysis: [full, or short: what was not checked]
## Risks to the date
| Risk | Owner (role) | First sign to watch for | Response |
|---|---|---|---|
| [risk] | [role] | [signal] | [action] |
## Decision
[Sponsor] accepts the scope line and the dates, or moves the deadline, by [date]; [L&D lead] confirms the phase owners by [date].
```

## Done When
- Every phase has a deliverable, an owner by role, dates and a closing decision.
- Every duration comes from your own history or is marked as having none.
- The scope line says what moves if the date holds, and each risk has an owner and a first sign.

## Quality Bar
- No benchmark durations; your own projects are the only yardstick.
- The date and the scope are shown together, so nobody can approve one without seeing the other.
- Analysis is never cut to zero; a short analysis is named as short.
- Claude drafts the plan; the sponsor accepts the scope line or moves the date, and owners are roles, never a tally of anyone's hours.

## Next
Run ldg-plan-the-compliance-training (Plan the Compliance Training) when the plan includes mandatory content, so the checks and the record rules are set before the build.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
