---
name: isd-course-design-document
description: Drafts a Course Design Document with the need in one line, the strategy and practice per objective, a format choice table with reasons, what was left out and why, a living decisions log and a sign-off block. Use for "run isd-course-design-document", "write the design document", "design doc for the sponsor", "show the decisions behind the course", "why this format and not a video", "get the design signed before we build", "record what we left out", "the sponsor only sees finished screens", part of the Claude for Instructional Designers Pack by 90n.
---

# Course Design Document

## When To Use
The sponsor sees finished screens and none of the decisions that made them, so every choice looks like taste and every review reopens one. Use this once the objectives are agreed and before anything is built, to answer: what are we making, why this way and not another, what did we leave out, and who signed that?

## When Not To Use
If the objectives still say "understand", run Measurable Learning Objectives first; a design on vague objectives records vague decisions. The order of lessons belongs in Course Curriculum Map, and the decision to release the finished course belongs in Release Sign-Off Record. This sign-off is on the design only.

## Inputs
- The agreed objectives with their evidence types, and the learner analysis (roles, tasks, device and place, the time people really have)
- The fixed limits (date, tools, budget, mandatory or not) and the decisions already taken, even informally
If you have none of this, I start from the brief and a one-line description of the problem, and mark the output as a first draft.

## Approach
This is the design phase of ADDIE, from the 1975 Interservice Procedures for Instructional Systems Development (Florida State University, ERIC record ED122022), in the order backward design sets as described by the Yale Poorvu Center: identify desired results, determine acceptable evidence, then plan learning experiences and instruction. The decisions are yours; the document makes them visible and holds them still. The failure it prevents: three weeks into the build someone asks why there is no video, nobody can remember, and a choice you made for learners on a shared, noisy floor gets reversed in a meeting. In Claude Docs (beta) the draft is a document in the conversation you can export for the sponsor to sign.

## Workflow
1. Ask three questions: what will the sponsor look at to know this worked, what limits are fixed and by whom, and which decisions have already been made without being written down?
2. Results first. Write the need line as `[role] are [actual] and need to be [desired], shown by [measure]`, and list the objectives unchanged. If the measure is missing, the line says "no measure agreed". Evidence second. For each objective, name the check that would show it, at the same level as its verb. A decision objective gets a decision, never a recall question. You confirm each one.
3. Experiences last. For each objective, propose the strategy (worked example, scenario, guided task, job aid) and the practice the learner does. Content is only what that practice needs. You pick the strategy; I draft the options.
4. Fill the format choice table. Each format considered is chosen or rejected, with a reason tied to the practice the objective needs and to a line in the learner analysis. A format with no reason is flagged, and so is a format chosen before step 3.
5. Write the "left out, and why" rows, each with who agreed. Then start the decisions log: one dated row per decision, with the options, the reason and the role that agreed. It stays open through the build, and a signed decision reopens only through the change rule in your review plan. Close with one line on how the course's effect will be looked at after release, and the sign-off block. Limits you did not give stay as placeholders.

## Output Format
```markdown
# Course Design Document
## Need and audience
- Need: [role] are [actual] and need to be [desired], shown by [measure]
- Audience (by role and task): [role, what they do today, device and place, time available]
- How the effect will be looked at after release: [the measure, who looks, when]
## Design per objective
| Objective | Check (same level) | Strategy | Practice the learner does | Minimum content it needs |
|---|---|---|---|---|
| [objective 1] | [decision in a realistic case] | [scenario] | [decide on [case]] | [rule, example] |
## Format choices
| Format considered | Chosen or rejected | Reason from the practice | Reason from the learner analysis |
|---|---|---|---|
| [format] | [rejected] | [practice needs a decision, not a viewing] | [shared floor, no audio] |
## Left out, and why
| Item | Why it is out | Where it lives instead | Agreed by (role) |
|---|---|---|---|
| [topic] | [no objective needs it] | [reference / job aid / nowhere] | [expert] |
## Decisions log (kept through the build)
| Date | Decision | Options considered | Reason | Agreed by (role) | Reopened? |
|---|---|---|---|---|---|
| [date] | [decision] | [options] | [reason] | [role] | [no / yes, via change rule on [date]] |
## Sign-off
Version [v] · Sponsor: [name], [date] · Expert: [name], [date] · Designer: [name], [date]
## Decision
[Sponsor name] and [expert name] sign version [v] by [date]; [designer name] starts the build only after both signatures.
```

## Done When
- Every objective has a check, a strategy and a practice in one row, with check and objective at the same level
- Every format considered has a verdict and a reason, and none was picked before the practice
- Every "left out" row names who agreed, the decisions log has dated rows, and the sign-off block carries a version

## Quality Bar
- The order is results, evidence, experiences, and it shows in the document
- A reason cites the need, an objective, a learner constraint or a limit, never taste
- The log records decisions and reasons, not who argued for what; audience is by role and task, and limits you did not give stay as placeholders
- Claude drafts the document; the decisions in it are yours, and the sponsor and the expert sign before anything is built

## Next
Run isd-course-curriculum-map (Course Curriculum Map) to lay the lessons out in order.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
