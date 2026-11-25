---
name: model-risk-validation-scope
description: >-
  Check whether a model validated under one autonomy level and tool set is still
  covered by that validation as deployed, and find the monitoring that stops at
  the model's output. Use when applying model risk management to an agentic
  system.
allowed-tools: Read, Grep, Glob
---

# The validation was of a system that had no tools

Model risk management carries three pillars — validation, monitoring,
governance — and each makes an assumption that agentic deployment breaks.
Validation assumes the thing validated is the thing deployed; a model validated
with no tools at L1 and deployed with three tools at L3 is the same model and a
different system, and the validation does not cover it.

## When to use this

Applying an existing model risk framework to agents, and at every autonomy or
tool-manifest change afterwards.

## Procedure

**1 — Write down what was validated.** Model, version, tool set, autonomy level,
data scope. Validation scope is usually recorded as the model alone, which is
the defect.

**2 — Write down what is deployed,** in the same fields. Then diff. Any
difference in tools or autonomy means the validation does not cover the
deployment, and that sentence is the finding.

**3 — Check what monitoring observes.** Most monitors the model's output
distribution. List what it does not observe — rows written to production, actions
taken, resources reached — because that is where agentic risk lives.

**4 — Name the re-validation triggers.** Tool added, autonomy raised, model
version changed, data scope widened. Without triggers, re-validation happens on
the audit calendar, which is the assumption that failed in the first place.

**5 — Report per pillar.** Validation coverage, monitoring blind spots,
governance triggers. Three findings with three owners rather than one finding
about the framework.

## Example

**Input** — the fixture committed at the top of [`scripts/model_risk_validation_scope.py`](scripts/model_risk_validation_scope.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
pillar                  what it asks                                  what it quietly assumes
conceptual_soundness    is the method appropriate for the purpose     assumes the purpose is stable and stated
independent_validation  did someone other than the builder check      assumes the thing checked is the thing deployed
ongoing_monitoring      is it still performing as validated           assumes performance is what changes

All three survive contact with AI. The assumptions are what break.
validation still covers what is deployed: False
   tool surface changed: ['db_update', 'read_ticket', 'write_ticket']
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "validated": {"model": "str", "version": "str", "tools": ["str"], "autonomy": "str", "data": ["str"]},
  "deployed": {"model": "str", "version": "str", "tools": ["str"], "autonomy": "str", "data": ["str"]},
  "covers": false,
  "differences": ["str"],
  "monitoring": {"observes": ["str"], "does_not_observe": ["str"]},
  "revalidation_triggers": ["str"]
}
```

## Failure modes

- **Recording validation scope as the model.** It is the system.
- **Monitoring output distribution only.** The actions are the risk.
- **Calendar re-validation.** The triggers are events, not dates.
