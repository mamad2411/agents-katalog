---
name: approval-queue-saturation-model
description: >-
  Model what happens to an approval gate as volume rises — coverage staying at
  100% while actual review collapses — and find the volume at which the control
  stops working. Use when reviewing human-in-the-loop design, approval fatigue,
  or a gate that has never been measured.
allowed-tools: Read, Grep, Glob
---

# Coverage stays at 100%; reading does not

An approval gate reports the same number at every volume, because coverage
measures whether a human was *asked*. What degrades is whether they read it,
and an attacker who can choose position only has to generate enough requests to
sit behind.

## When to use this

Any control whose enforcement is a person: approvals, exception reviews, alert
triage sign-off, change advisory.

## Procedure

**1 — Measure current volume,** per reviewer per day. Not the design volume —
the observed one, at peak rather than mean.

**2 — Establish the reading budget.** How many items can one reviewer consider
properly in a shift? Ask them; the number is usually between 20 and 30 and it
is always far below the queue.

**3 — Model detection against position.** Place a malicious item at various
depths and compute the probability it is actually read. The curve falls off a
cliff at the reading budget, not gradually.

**4 — Note who controls position.** If a requester can generate the items in
front of theirs, depth is attacker-chosen and the average case is irrelevant.

**5 — Report the two numbers that change the design.** Items per reviewer per
day, and the reading budget. The gap between them is the finding, and it points
at routing by reversibility rather than at hiring.

## Example

**Input** — the fixture committed at the top of [`scripts/approval_queue_saturation_model.py`](scripts/approval_queue_saturation_model.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
 daily volume  considered  stamped  caught  missed
           10          10        0       1       0
           25          25        0       1       0
          100          25       75       0       1
          500          25      475       0       1

At every volume the audit trail shows a human approval on 100% of
actions. The control reports full coverage in all four rows.
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
  "volume": {"per_reviewer_per_day": 0, "measured_at": "peak|mean"},
  "reading_budget": 0,
  "coverage_reported": 1.0,
  "detection_by_depth": [{"depth": 0, "read_probability": 0.0}],
  "position_attacker_controlled": true,
  "gap": 0
}
```

## Failure modes

- **Reporting coverage.** It is 100% by construction and means nothing.
- **Using mean volume.** The gate fails at peak.
- **Recommending more reviewers.** The fix is fewer items, chosen by
  reversibility.
