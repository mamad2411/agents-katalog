---
spec_hash: 800156060bd5
name: model-fitness
description: Decides whether a language model is fit for a named role, using measurements taken on the deciding machine rather than published benchmarks. Use when a candidate model needs evidence before adoption, when an incumbent is suspected of regressing after a runtime or quantisation change, or when writing eval cases for model selection. Does not apply to choosing judge models, which is a separate calibration question.
---

# Model fitness

## Purpose

Decide whether a model is fit for a **named role**, and produce a verdict backed
by numbers the deciding machine measured itself.

Model selection is unusually easy to do badly while feeling rigorous. A release
lands with a benchmark table; the numbers are real and they answer a question
nobody here asked — on other hardware, at another quantisation, for a task the
role does not perform. The result is a confident choice nobody can defend six
months later, because no one recorded what "better" meant.

This skill owns the judgement. It does not own the harness producing raw
timings, nor the decision to adopt, which stays a human commit.

## When to Use

Use when:

- A candidate model has passed triage and needs evidence before adoption.
- An incumbent may have regressed after a runtime or quantisation change.
- Eval cases for model selection are being written or reviewed.

Do not use for:

- **Choosing a judge model.** That is a calibration question with its own
  harness, and importing its scores is the specific error this skill prevents.
- **Ranking models in the abstract.** A ranking without a role is not a finding.

## How to Apply

### Measure per role, never across

Evaluate only for roles the model is a candidate for, and report per role. Never
combine per-role results into an overall score, and never use a result from one
role as evidence for another. A strong chat result is not code evidence — say
the code role is unmeasured, or run its cases.

### State the measurement beside every claim

Attach to every quality claim: the case that produced it, the date, and the
conditions that affect it — model tag, quantisation, context, and whether
anything else was resident. A claim without those is a recollection.

Not "faster and better at following instructions". Name the cases, the date,
both exact tags, and the conditions.

### Report unmeasured dimensions as unmeasured

Name what was not measured rather than omitting it. Mark a recommendation
provisional when any dimension material to the role is unmeasured, and say
which one. Speed and size results are not a fitness verdict.

### Invalidate runs whose conditions differ

Record harness conditions. Treat a run as non-comparable when they differ from
what it is compared against — different context, quantisation, runtime version,
or another model resident. Re-run rather than reconcile: under contention a slow
result cannot be distinguished from a slow model.

### Prefer mechanical checks to judged ones

Use a mechanically decidable check wherever one exists — schema conformance,
exact-match recall, well-formed tool calls. Reserve model-judged scoring for
properties with no mechanical form, and report it as judged when used.

Ask for a shape a script can validate, then validate it. Do not ask a model
whether the shape looks right.

### Grow coverage from blocked decisions

Add a property or role when a decision could not be made without it. Do not fill
the matrix for completeness. Start at the smallest useful set; record uncovered
roles as known gaps.

### Source cases by provenance

Eval cases are **synthesised** — written from general understanding of a problem
class. Never build a case by transforming real work material, including by
replacing names or identifiers: scrubbing changes what is recognisable, not
where the case came from.

When real usage reveals an uncovered problem class, prompt for a synthesised
case describing that class. Do not copy the material that prompted it.

## Constraints

- **Published benchmarks are not evidence.** Model cards, announcements,
  leaderboards, and recall may motivate a candidate; they may not support a
  verdict.
- **No cross-task score transfer**, including judge-calibration scores used as
  generation evidence.
- **No unmeasured superlatives.** Never describe a model as better, best, or
  improved on a dimension not measured on the deciding machine.
