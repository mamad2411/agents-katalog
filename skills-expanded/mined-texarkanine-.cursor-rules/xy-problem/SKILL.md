---
name: xy-problem
description: Checkpoint for "I'll use X to achieve Y" moments — before investing work in a chosen means, verify it actually achieves the goal and is the right choice among the things that do. Use when selecting a new dependency, library, tool, or approach; when a plan step names a means whose fitness rests on reputation or assumption rather than inspection; or when repeated attempts to make a chosen means work keep failing.
---
# XY Problem Check

The [XY problem](https://xyproblem.info/) is working on your attempted solution rather than your actual problem. The classic form is a human asking for help with a dead-end workaround while hiding the real goal. The agent form is quieter and more expensive: the agent decides "this library / tool / approach will achieve the goal," locks the choice in without inspecting it, and re-anchors all further work on the choice — so the question being worked becomes "how do I make this thing do what I need" even when the honest answer is that it can't.

Two words carry this whole document: the **goal** is the outcome actually required; the **means** is the thing chosen to get there. A means-decision is sound only if it survives two questions:

1. Does the means actually achieve the goal?
2. Of the things that achieve the goal, is this means the right one for this situation?

This skill is a checkpoint workflow: a set of trigger signals, then a four-step check to run when one fires.

## When to Run the Check

Run the check when any of these holds:

- You are about to add a dependency — a library, framework, tool, or service — to accomplish a task.
- A plan or design step has the shape "use `<means>` to do `<goal>`," and its fitness rests on its name, its README, its popularity, or your memory of it rather than on inspection.
- You inherited the means from a ticket, plan document, or earlier conversation, and there is no recorded evidence it was vetted.
- You have tried more than once to make an already-chosen means do something and it keeps not working. This is the retroactive trigger: "how do I make this thing do Z" loops are the signature of a means that was never verified, and the check may reveal that no configuration of it will ever work.

## Depth Calibration

Scale the check to the decision's weight. A reversible one-line choice — which of two equivalent stdlib calls to use — deserves a moment's thought, not a survey. A choice that other work will be built on top of — a test framework, an HTTP layer, a data model — deserves the full check, because unwinding it later costs everything built above it. Weigh blast radius, reversibility, and how load-bearing the assumed capability is.

Bezos's one-way/two-way door test is a second key for the same judgment. Plot the decision on two axes, reversible↔irreversible and consequential↔inconsequential: a reversible, low-consequence choice is a two-way door, decided on the spot with the information at hand; an irreversible or consequential one is a one-way door, made slowly and deliberately — which here means the full check. The test cuts both ways: it demands rigor at one-way doors and forbids ceremony at two-way ones, so a means-decision you can undo with one commit and a line or two should not be buried under a survey.

## The Check

1. **State the goal without naming the means.** Write it as an observable outcome: "integration tests must observe and stub the HTTP requests our client actually makes," not "use library L to intercept HTTP." If you cannot state the goal without naming the means, you have lost the goal — recover it from the original request or requirements before doing anything else.
2. **Verify the means achieves the goal — by inspection, not reputation.** Locate the specific load-bearing capability in primary sources: the current documentation, the source, the library's own tests. Then prove it in this project's context — a minimal spike — whenever the capability is one the rest of the work will stand on. Evidence is a doc section, a source line, or a passing spike; a package name, a README tagline, a star count, or your recollection of the library is not evidence. For dependency choices, `references/dependency-vetting.md` holds the concrete checklist.
3. **Survey what else achieves the goal.** Enumerate the alternatives, and always include the do-less candidates: an existing dependency, the standard library, a small amount of bespoke code, or reshaping the task so the capability isn't needed. Compare against this situation's constraints — the project's runtime and conventions, maintenance burden, what is already installed — not against generic popularity.
4. **Decide and record.** Keep the means, swap it, or surface the tradeoff to the user if the survey exposed a genuine judgment call. Record the decision in two or three sentences wherever the work is being tracked: the goal, the evidence the means achieves it, and why it beat the alternatives. The record is what lets the next reader — or the next run of this check — audit the decision instead of re-deriving it.

Gate: do not build on the means until step 2's evidence exists. Work stacked on an unverified capability is the sunk cost that makes the XY problem expensive to escape.

## Failure Signature

What the unchecked path looks like, so it can be recognized mid-flight: a team needs integration tests that assert on outgoing HTTP calls. An agent picks an interception library because its README says "intercept HTTP," and starts building the test suite on it. The library patches Node's `http` module; the client under test issues requests through a different stack the library never touches. Every subsequent work session asks "how do I configure the library to catch these calls" — a question with no answer, because the wrong question was locked in at the moment of choosing.

Mid-flight tells: the questions you're researching are shaped "how do I make <means> do <goal>"; adapter and workaround code is accumulating around the means; you are re-reading the same documentation hunting for a capability you have not yet seen demonstrated. When you notice any of these, run the check now and treat the work already spent as spent — it is not a reason to keep forcing the means.
