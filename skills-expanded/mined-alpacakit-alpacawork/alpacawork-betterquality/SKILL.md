---
name: alpacawork-betterquality
description: An alpacawork add-on. Owners and coordinators working in alpacawork use it when planning a result, while building it, when showing it to other AIs and handling what they find, and when fixes stop converging; an agent asked to review a result uses it to review. Use it for any result, including ones that must work for people with no one there to explain (error text, a guide, a screen, a promo, a name). It is not a skill about writing tests.
---

# alpacawork-betterquality (frame first, build rough, show a fresh AI, fix until the gate)

These rules are added on top of the alpacawork skill. They cover two blind spots of whoever builds a result:

- If you start thinking about what is good and bad only after you begin building, the heaviest decisions get made without being compared, and later checks only fix the details of a shape that is already decided.
- A builder cannot set aside what they know about their own work. They already know what each part is meant to do, so they cannot see where someone without that knowledge stops, and they read their own interpretation of the request as the request.

So: write down before building what the result is for and how it will be judged; build rough and compare skeletons while changing them is cheap; and have the result checked by a fresh AI that is given only what the real judge has — never the builder's explanation.

The process is the same for every kind of result. What differs by use is which checks the frame sets, and what follows from them: which kind of fresh AI looks, how options are compared, the round cap, and whether a final check is run.

This skill does not change the alpacawork skill's guardrails or its delivery mechanism, and the scope of approval follows "Approval defaults" there. Requests, the choice of conversation, verification, records and reports follow the alpacawork skill; how to place and ask other agents is in [references/alpacawork.md](references/alpacawork.md). The sections are in the order of what to think about; they do not fix the shape of the process. Write records and messages to the user in the user's language.

## Terms

- **Frame**: what is written before building — who the result is for, its purpose, the checks and the gate ([references/frame.md](references/frame.md)), and per decision its weight, the options, who will look and the round cap ("Weight of a decision" below).
- **Check**: one thing the result is judged on. **Gate**: the required pass conditions over the checks.
- **Skeleton**: what comes first, the form, the idea the result rests on, the data shape, the unit and the information source. The **direction** is the skeleton you would otherwise start from: the existing version, the approach written in the request, or your own first idea.
- **Reviewer**: a fresh AI that is given the user's words and judges whether the result is as asked and correct ([references/reviewer.md](references/reviewer.md)).
- **Audience stand-in**: a fresh AI that plays the audience, is not told the intent, and shows where the result does not land ([references/showing.md](references/showing.md)). It does not read this skill.
- **Round**: one showing to fresh AIs together with handling what it found.

## Who uses which part

- Framing, building, showing and handling findings: the agent responsible for the result. How much of this the coordinator takes on is governed by [alpacawork's "Principles of the role"](../alpacawork/references/coordinator.md#principles-of-the-role).
- Reviewing: the agent asked for a review follows [references/reviewer.md](references/reviewer.md).

## What to read

Work with only light decisions that you check yourself needs nothing but this file. For any other work, read each file below when its moment comes:

| When | Read |
|---|---|
| Before building anything that is not light work, and again when the requester asks to add to or change an existing result | [references/frame.md](references/frame.md): who the result is for, its purpose, the checks and the gate |
| Before building, when a decision is heavy, the user judges the direction themselves, or the operation cannot be undone | [references/direction.md](references/direction.md): questioning and comparing the direction, what the user sees first, trying on a copy |
| Before the first showing to a fresh AI, and each time findings come back | [references/rounds.md](references/rounds.md): showing, judging, fixing, counting, stopping |
| The frame has checks of whether the result lands with its audience | [references/showing.md](references/showing.md) |
| Placing or asking another agent | [references/alpacawork.md](references/alpacawork.md) |
| You were asked to review | [references/reviewer.md](references/reviewer.md) only; when asked to review a frame before building, also [references/frame.md](references/frame.md) |

## 1. Weight of a decision

- Judge weight per decision, not per task: within one task, the skeleton can be heavy while the wording is light. Measure it as "cost of undoing × breadth of impact".
- Rule of thumb (not fixed). If the user's instructions, the project policy or the request text state numbers, follow them.

| Weight | How to tell | Number of options | Review |
|---|---|---|---|
| Light | A detail that is quickly undone | 1 | After building, by yourself or by one reviewer |
| Medium | Takes effort to undo | 1 to 2 | After building, by one reviewer other than the builder |
| Heavy | Costly to undo and broad in impact (the skeleton, for example) | 2 to 3 genuinely different ones, compared before committing | The options and the frame before building, and the result after building, by two or more reviewers with different models or different viewpoints |

- **Light work.** Work with only light decisions needs no written frame and no reviewer: check the real thing yourself, and say in the report that it was self-checked and why. Do not skip independent review when the user's instructions, the project policy (the policy chain) or the request text require it. With no written frame, the conditions of use the gate names are the paths, sizes, layouts and states the result's audience meets.
- **Audience stand-ins** are not reviewers and are not counted in the Review column. Use them whenever the result must work for people with no one there to explain — at least one per segment per round — except for a one-line fix that a single self-check settles and for audiences an AI cannot stand in for. For such a result, the skeleton counts as heavy for questioning the direction ([references/direction.md](references/direction.md)) whenever it can meaningfully differ; the number of reviewers still follows the table.
- Difference matters more than number. Options count only when they are genuinely different skeletons; a rewording of the same one is one option. Reviewers count only when they differ in model or in viewpoint. Do not hard-code a model name; choose from what can be selected at the time so that they differ.
- **Round cap.** One cap covers every round of the same result. The default is 3 including the first, and 5 when the frame has checks of whether it lands, unless an instruction you follow sets another.
- Write in the frame before starting, one line per decision, the weight you gave, the number of options, who will look, the cap, and why.

## 2. Build rough, then finish

- **While it is rough, compare only the direction.** A rough version exists to be compared or shown; polish before that is mostly spent on parts that turn out wrong. Details and correctness are checked once the version is finished, beyond what a rough version shown to the user needs ([references/direction.md](references/direction.md)).
- **Before building, read [references/direction.md](references/direction.md) when one of these holds.** A decision is heavy: its direction is questioned once with a rough alternative and the skeletons are compared in round 1, and the builder does not choose alone. The user judges the direction themselves (they asked for a trial, a sample or options to judge from, or the project policy reserves the choice): they see a rough version, checked by you, first, and the rounds wait for the direction they settle. The operation cannot be undone: it is tried on a copy or test data first.
- **Investigation.** Limit it to the affected area, in proportion to the weight and uncertainty, and stop once you know the grounds and the impact needed for the decision. Check the existing mechanism against primary sources and against how it is actually used.
- **Finish, then check it yourself before asking for a review**, in the way that fits its medium, under every condition of use the gate names: operate a screen at its actual width, read a document in the form the recipient gets, run a CLI or API with the user's input, together with the automated checks that cover what changed. Asking for review of something you already know is unfinished wastes a round.

## 3. Show, fix and report

Every round goes to an AI in a conversation separate from the building, and what it finds is judged against the gate, fixed at its cause and shown again until the gate is met, the cap is reached or the fixes stop converging. Before the first showing, read [references/rounds.md](references/rounds.md).

## 4. Records and report

- Record the cap and the rounds used in the task's values. A reviewer's reply stays in its Run, and what was adopted or rejected stays in the request for the fix or the re-review; do not copy either into a file. Audience rounds keep a log as [references/showing.md](references/showing.md) says.
- In the report, write which version was looked at and by whom (or that it was self-checked), the purpose and whether the requester confirmed it, the direction decision and why, what later rounds changed in what the user had seen when they judged the direction, the rounds used, what each version removed and added, what changed the most, the required findings rejected and why, the stumbles left on purpose, what is unresolved or unverified, and why the rounds ended. Say that audience stand-ins were AIs. Do not write a skipped check as carried out.
- When the user's own acceptance is required, do not replace it with independent review.
