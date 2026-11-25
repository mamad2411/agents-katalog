---
name: tw-self-evolve
description: "a check fails, the same finding repeats, or a milestone closes and the team must decide what changes in how it works"
kind: workflow
---

# tw-self-evolve

Owner role: **ceo** (created by CEO on 2026-11-04).

Use this skill when: a check fails, the same finding repeats, or a milestone is
closing and the team has to decide what changes in **how it works** - not what
changes in the product.

## Why this exists

This project recorded lessons, knowledge and decisions, and still paid for the
same defects twice: the archive render of a branchless deliverable was lost and
restored by hand, and the always-on budget overage recorded at M18 was "found
again" by `audit` in November. The failure was not a missing record; it was a
missing classifier and a missing promotion step. This skill is that step.

The rules live in `docs/Team/Evolution.md`; this file is the routine, kept to one
screen.

## Budget

- 5 minutes per failure (classify + record).
- 15 minutes per second occurrence (promote to a skill or open the code task).
- 30 minutes per milestone close (snapshot + age the known issues).
- 60 minutes per release (promote to the core, `refresh --check`).
- Stop at the stop condition named in each step; a routine that runs past its
  budget without a record is the defect this skill exists to prevent.

## Steps

1. **Classify before recording.** T (tool defect) / P (process) / D (doc drift) /
   G (governance) / K (knowledge), by the tests in Evolution.md 3. A T-class
   finding gets a code task and a regression that fails on the old revision. It
   never gets a lesson as its fix.
2. **Record once, in the right store.**
   - P -> `teamwork lesson add` (failure, cause, rule, evidence);
   - K -> `teamwork knowledge add` (one fact, evidence, tags, importance);
   - G -> `teamwork decision add` (evidence + falsifier + rollback);
   - T -> `teamwork task add ... --bug` with the repro, then `tests repro`;
   - D -> a doc fix that binds every changed claim to a command and a cut.
3. **Promote on the second occurrence.** Run `teamwork skill candidates`. If the
   finding is a flow, `skill create` (workflow) or `--kind mistake --from-lesson`;
   if it is a tool, the task is the fix and the lesson is retired.
4. **Take the milestone snapshot, at one cut.** Run
   `teamwork evolution snapshot --json`, `teamwork throughput`,
   `teamwork coordination --strict`, `teamwork audit`,
   `teamwork harness budget`, `teamwork tests plan`, `teamwork links`,
   `teamwork skill candidates`, `teamwork ledger verify`. Write one row per book
   in Evolution.md 9; never mix cuts.
5. **Decide with a verdict.** Every change gets `helped` / `hurt` /
   `no observed effect` / `confounded`, plus the command and the cut. A
   single-run claim is `confounded` by definition.
6. **Promote or roll back.** L1 -> L2 needs two occurrences, a trigger, a budget,
   a stop condition and a proof command. L2 -> L3 needs two milestones or
   projects and a clean guardrail check, then a release and
   `teamwork refresh --check`. Roll back on a guardrail regression or two
   unmeasured cuts.
7. **Close the books.** Run `teamwork evolution check`: it exits 1 on a `KI-`
   row past `re_measure_by`, an `EV-` row without a valid verdict, a `PB-` row
   without a level, an empty metric command, or a missing/empty table. Then
   `teamwork ledger verify`.

## Guardrails

- A skill never replaces a gate and never weakens one.
- The framework may not raise a cap, skip a layer or delete a record to make a
  number look better.
- A change to this skill is normal work: branch, commit, PR, independent review,
  merge.

## Verdict on this skill

verdict: no observed effect

- Created 2026-11-04 from the v3 design. No close-out has executed this routine
  end to end yet, so nothing has been measured.
- What would make it `helped`: two milestone cuts where RFR, promotion lag and
  freshness debt move in the stated direction with no guardrail regression.
- What would make it `confounded`: the first adoption also changes the metrics
  or the classifier, as the v3 design itself did.
