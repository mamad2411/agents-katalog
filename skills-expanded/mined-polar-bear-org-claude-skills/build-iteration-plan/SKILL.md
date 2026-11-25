---
name: build-iteration-plan
description: Writes a Prototype Iteration Plan that sorts the problems from your sessions into fix now, fix after the round and leave, sets one change per problem with the reason, logs which version each participant saw, says what the following round must show and what cannot be compared, and fixes a stop rule. Use for "run build-iteration-plan", "what do I fix before the next round", "plan round two of testing", "which version did each tester see", "can I change the prototype between sessions", "when do I stop testing", "can I add the results of both rounds together", part of the Claude for Product Builders Pack by 90n.
---

# Prototype Iteration Plan

## When To Use
You want to fix everything after session two and are no longer sure which version anyone saw. This skill answers: which problems change before the following round, what must that round show, and when do you stop testing?

## When Not To Use
If the sessions have not been read task by task, run Usability Test Findings first: this plan needs its problem list. To say whether the belief held, run Prototype Learning Card. If the fixes belong to the thing engineers will build and not to the prototype, they go in the handover, not here.

## Inputs
- The problem list with severity ratings from your findings, and which participant code saw which state of the prototype.
- The pass line on your test card and the time you have left.
If you have none of this, I start from your list of what went wrong in the sessions and mark the output as a first draft.

## Approach
Fixing between sessions in small rounds, a common practitioner convention, with the argument for small repeated rounds from Nielsen Norman Group (https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/): several small rounds improve a design more than one large study, because the second round checks whether the fixes worked and looks for what the first round hid. The judgment is restraint. One change per problem, labelled and dated, so you can tell what helped. The failure this prevents: nine changes made in one evening, a better second round, and no way to say which change did it or which screens the first three people saw.

## Workflow
1. Ask at most three questions: which problems came out of the round and how were they rated; which version did each participant code see; what stop rule will you accept before the following round starts?
2. Sort the problem list into three: fix now (the cause is clear and the fix is small), fix after the round (the cause is unclear, or the fix is large enough to change the test), and leave, with the reason written down.
3. Write one change per problem with the reason. Two changes aimed at one problem get split or one is dropped, so the following round can tell what helped.
4. Keep a version log: every change gets a version label and a date, and every participant code is tied to the version that person saw. In Claude Design, save the current work before each change, since there is no version history to go back to.
5. Mark what cannot be compared: once the prototype changes, counts from before and after are different tests. They sit side by side, each with its version, and are never added into one "[n] of [N]".
6. Write what the following round must show, per fix and before the round: the behaviour you expect to see if the fix worked, and what you would see if it did not.
7. Set the stop rule in advance. You choose it: for example the pass line on the test card is met, or a round finds no new problem rated 3 or 4, or the time box ends. I do not move it once sessions have run.

## Output Format
```markdown
# Prototype Iteration Plan
**Prototype:** [name] | **Round just run:** [number], version [label] | **Planned round:** [n+1], [dates]
## Problems sorted
| Problem | Severity 0 to 4 | Sort | One change | Reason |
|---|---|---|---|---|
| [problem] | [rating] | [fix now / fix after the round / leave] | [change, or none] | [why] |
## Version log
| Version label | Date | What changed | Saved copy | Participant codes who saw it |
|---|---|---|---|---|
| [label] | [date] | [change] | [where] | [P1, P2] |
## Cannot be compared
[Round [n] on version [label] and round [n+1] on version [label] are different tests. Counts are reported per version: [n] of [N] and [n] of [N], never summed.]
## Round [n+1] must show
| Fix | If it worked we see | If it did not we see |
|---|---|---|
| [change] | [behaviour] | [behaviour] |
**Stop rule:** [set on [date] by [role]: testing stops when [condition]]
## Decision
[The builder, by role] chooses which problems are fixed before round [n+1] and confirms the stop rule by [date], before the prototype is changed.
```

## Done When
- Every problem is in one of the three sorts, and every "leave" has a reason.
- Each fix is one change with a version label and a date, and every participant code is tied to the version that person saw.
- What the following round must show is written per fix, and the stop rule is dated before that round.

## Quality Bar
- One change per problem. A redesign of the whole flow is a new test, not a fix.
- The version log ties codes to versions, never names.
- The stop rule is the builder's and is set before the round. A good afternoon does not end testing early.
- The changes are to a prototype. What ships is decided and built by engineers.
- Each round is tested on real target users, and results from different versions are never pooled.

## Next
Run build-demo-script (Prototype Demo Script) to show the tested prototype to the people who decide, with its limits said out loud.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
