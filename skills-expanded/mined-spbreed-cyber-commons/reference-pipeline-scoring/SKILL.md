---
name: reference-pipeline-scoring
description: >-
  Map a published or vendor pipeline onto the stage model, check its output
  against the schema it claims, and score its findings against a held-out key.
  Use when evaluating a reference implementation, a security product's agent, or
  any pipeline you are asked to adopt.
allowed-tools: Read, Grep, Glob
---

# A reference implementation is something you evaluate

Somebody else's pipeline is a set of claims: these stages, this output shape,
this accuracy. All three are checkable, and checking them is cheaper than
adopting and discovering. The interesting result is usually not the score — it
is the phase the pipeline does not cover at all.

## When to use this

Before adopting a published pipeline, when comparing two, and when a vendor
claims a number you are expected to plan around.

## Procedure

**1 — Map it onto the stage model.** For each stage, does the pipeline cover it
strongly, weakly, or not at all? Coverage claims are usually accurate about the
stages the pipeline is proud of and silent about a whole phase.

**2 — Take its output and check conformance to its own schema.** Required
fields present, enumerated values in range, nothing that is prose where an
object was promised. Conformance failures in a published sample are the cheapest
finding available.

**3 — Score against a held-out key.** Not the examples the pipeline ships. Match
findings to truth by location and defect class, then compute precision and
recall, and report both — a pipeline can look excellent on either alone.

**4 — Separate the model's errors from the harness's.** A null CWE is a schema
problem; a finding at the wrong location is an analysis problem. They have
different fixes and different owners.

**5 — Report the uncovered phase as the headline.** A pipeline that scores well
on the stages it implements is still a partial answer, and the gap is what you
would have to build.

## Example

**Input** — the fixture committed at the top of [`scripts/reference_pipeline_scoring.py`](scripts/reference_pipeline_scoring.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
stage  name                              mantis    note
------------------------------------------------------------------------------------------------
  1  historical parsing                yes       historical_learnings.jsonl is read on subsequent runs
  2  structural indexing               partial   operates over the agent's code-reading tools
  3  component summarisation           partial   context assembled per review target
  4  architecture synthesis            no        assumes you supply the architecture context
  5  threat modelling                  partial   review skills encode threat patterns rather than deriving them
  6  strategic planning                no        you decide what to point it at
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
  "stages": [{"stage": 0, "coverage": "strong|weak|none"}],
  "uncovered_phases": ["str"],
  "conformance": {"samples": 0, "conforming": 0, "failures": [{"sample": 0, "reason": "str"}]},
  "score": {"matched": 0, "precision": 0.0, "recall": 0.0, "key": "held-out"},
  "errors": {"schema": 0, "analysis": 0}
}
```

## Failure modes

- **Scoring on the shipped examples.** They were chosen.
- **Reporting one of precision and recall.** Either alone flatters.
- **Treating uncovered stages as out of scope.** They are the work you inherit.
