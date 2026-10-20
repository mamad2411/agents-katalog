---
name: plan-drift-gate
description: "Hold a build to its plan before inspection. The builder's brief is derived step by step from maker's plan (files, change, proof per step), one commit per step. After the build, maker runs in check mode first: DIVERGED without a recorded return to architect blocks, and inspector is not called until the diff is ON PLAN, so inspection judges correctness and not shape. Use when a maker plan is about to be built, a finished diff needs checking against its plan, or a builder has wandered from the steps it was given. Not for writing the plan (maker), reviewing a diff for defects (code-review), or briefing one agent on a task (agent-delegation)."
allowed-tools: Agent(maker), Agent(inspector), Read, Write, Edit, Grep, Glob, Bash(git:*)
---

# Plan-drift gate

A build passes this gate when each step of maker's plan maps to exactly one commit that changes the files the plan named, proves what the plan said it would prove, and was checked by maker before the inspector saw it.

The plan is the contract between builder and inspector. Without a check against it, drift is invisible until review, where the inspector either spends its strongest model arguing about shape (why was this file touched, why is this step missing) or approves what was built and ratifies the drift. Checking shape first is cheap, mechanical work for a mid tier, and it leaves the top tier to judge whether the change is correct.

## Scope

Use for: the stretch between `PLAN READY` and the call to `inspector`.

Do not use for: writing the plan (`maker`), reviewing a diff for defects (`code-review`), or the general shape of a brief for one agent (`agent-delegation`). Where the verdicts go next is `family-relay`.

## Workflow

### 1. Derive the builder's brief from the plan, step by step

Copy each step's files, change and proof into the brief unchanged, in plan order. Do not rewrite them in your own words: a reworded step is a plan the builder can honestly misread. Add two lines the plan does not carry: one commit per step, with the step number in the subject; and a stop condition, which is that a step needing a file or a change the plan does not list stops the build and asks. Read `references/builder-brief.md` for the shape.

### 2. Build on the tier the work needs

The builder runs on a mid tier at high effort, whether it is the main agent or one writing agent. Following a precise plan is mid-tier work, and the effort is spent on care at each step, not on a stronger model second-guessing the plan.

### 3. Run maker in check mode before anything else

Give maker the diff, one commit per step, and the plan. It runs on a mid tier at medium effort. It returns `ON PLAN` or `DIVERGED`, and a divergence names the step it belongs to. A fresh maker delegation each time: a resumed one is checking its own earlier reading.

### 4. Treat DIVERGED as blocking

On `DIVERGED`, do not call inspector. Either revert the divergent step to the plan, or return to architect with the frame, the plan and the divergence, and record that return: what diverged, why, and what architect ruled. A `DIVERGED` with neither is blocking. Do not ask maker to amend the plan to fit the diff. Read `references/divergence.md` for what counts as divergence and what does not.

### 5. Send only an ON PLAN diff to inspector

Inspector runs on the top tier, with the frame's success criterion, the diff and the commands to run. Because shape is settled, a `FIX` from it is about correctness. A revised plan after an architect ruling is checked again from step 3, against the revised plan, never the old one.

### 6. Count the strikes

A second `DIVERGED` on the same step means the approach, not the builder, is wrong; `family-relay`'s two-strike rule sends it past architect to framer.

## Anti-patterns

**The paraphrased brief.** It looks faithful and carries the writer's reading of the plan, which is exactly what the check should be free of.

**One commit for the whole plan.** Maker can say a divergence exists but not where, and reverting a step becomes surgery.

**Inspector first.** It finds the drift, but at the top tier's price and mixed in with its findings on correctness, where the drift is easy to wave through.

**Maker as the repair.** Asking maker to update the plan after `DIVERGED` turns the check into a rubber stamp.

## References

- `references/builder-brief.md`: read at step 1 for the brief's shape, the commit convention and the stop condition.
- `references/divergence.md`: read at step 4 for what counts as divergence, what is tolerated, and the record of a return to architect.
