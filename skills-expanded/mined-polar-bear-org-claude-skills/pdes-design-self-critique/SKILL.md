---
name: pdes-design-self-critique
description: Runs a Design Self-Critique on one task before a review, with your own pass against the ten usability heuristics, a separate second-opinion pass from Claude, the two merged into one issue list, and your call on each issue (fix before the review, deliberate trade-off, needs a real user). Use for "run pdes-design-self-critique", "critique my design before the review", "heuristic evaluation of my flow", "find the obvious problems first", "second opinion on my screens", "what will the room pick apart", "check my flow against the heuristics", part of the Claude for Product Designers Pack by 90n.
---

# Design Self-Critique

## When To Use
The review is tomorrow and you want to find the obvious problems before the room does. You have looked at the flow so long that you no longer see it. It answers: what would a careful inspector flag on this one task, which of those are choices I made on purpose, and what do I fix tonight?

## When Not To Use
If people have already tried the design in sessions, write Usability Test Findings: what they did outranks anything an inspection says. If you need the standing checklist for every stage, use Design Quality Bar. Contrast, focus and labels belong in Accessibility Review.

## Inputs
- One task and the user it belongs to, with the screens in order (a written walkthrough, a frame list or exported text)
- Your own notes from walking the task, however rough, pasted before you see mine
- Optional: the Figma connector, which reads frames, variables and components; screenshots come back to Claude as text descriptions
If you have none of this, I start from a written description of the task and mark the output as a first draft.

## Approach
Heuristic evaluation as Nielsen Norman Group describes it (How to Conduct a Heuristic Evaluation, 2023): prepare, evaluate alone, then consolidate, with three to five evaluators who do not see each other's notes first. Here your pass comes first and mine second, so neither anchors the other, and mine counts as one more evaluator at most. The failure it prevents: you ask "what do you think?", get twelve confident points, and walk into the review defending a list you never checked against your own reasons.

## Workflow
1. Ask three questions: which one task and which user, what stage is the work at and when is the review, and have you already walked it yourself (if yes, paste your notes now)?
2. Prepare: write the task as numbered steps, and list the ten heuristics under the names NN/g gives them. One task only; a second task is a second run.
3. Your pass first. Walk the steps alone and note each issue with the step where it happens. If you ask for my pass before pasting yours, I ask for yours again: it is the order that keeps the two independent.
4. My pass, labelled "second opinion from a file". I walk the same steps against the same ten heuristics and list what I could not see. From text descriptions of screenshots I cannot judge spacing, colour or visual weight, and I say so in the table.
5. Consolidate: one issue per row, with where it happens, the heuristic it touches, and found by (you, Claude, both). Duplicates merge; an issue only one of us saw stays in.
6. You make one of three calls on every row: fix before the review, deliberate trade-off (with your reason), or needs a real user. I do not make the call and I do not rank the rows.
7. State the limits the NN/g page gives: a heuristic violation is not always a problem, and this method cannot replace research with users. No severity numbers here; severity belongs to what people did in observed sessions. If a colleague can spare a short slot, their solo pass is worth more than a second one of mine.

## Output Format
```markdown
# Design Self-Critique
**Work:** [flow or screen] | **Task:** [one task, as numbered steps] | **User:** [who] | **Stage:** [explore, refine or ready to build] | **Review:** [date]
## Issues, merged
| # | Where it happens | Issue | Heuristic (NN/g name) | Found by | My call |
|---|---|---|---|---|---|
| [n] | [step or screen] | [what goes wrong] | [heuristic] | [you, Claude or both] | [fix, trade-off with reason, or needs a real user] |
## What the second opinion could not see
- [e.g. visual detail on a screen that came through as a text description]
## Fix before the review
- [issue number and the change]
## Deliberate trade-offs to say out loud
- [issue number, what it gives up, why]
## For real users to settle
- [issue number and the question a session would answer]
## Decision
[Designer] makes the fixes by [review date] and decides with [product manager] by [date] which open items go into the next round of sessions.
```

## Done When
- Your pass was pasted before mine was shown, and each row says who found it
- Every issue names a step and one heuristic by its exact name
- Every row has your call, and no row carries a severity number
- The limits of my pass are written in the output

## Quality Bar
- Issues describe the work and where it breaks, with no remark on the designer's skill
- A trade-off needs a reason you can say to the room; "I like it" goes to the fix or the user column
- Nothing here is called a finding: findings come from sessions with people
- Claude's pass is a second opinion on a file, never a user and never a test

## Next
Run pdes-accessibility-review (Accessibility Review) to run the check heuristics do not cover.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
