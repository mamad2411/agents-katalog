---
name: stakeholder-seam-map
description: >-
  Map which control function operates which controls and what question each is
  asking, then find the seams where two individually reasonable assumptions
  leave a use case ungoverned. Use when everyone reports full coverage and
  something was still missed.
allowed-tools: Read, Grep, Glob
---

# Every function is covered and the use case is not

Governance failures cluster in the seams. Legal assumes security assessed the
tool; security assumes procurement assessed the vendor; procurement assumes it
was an internal build. Each assumption is reasonable, each function reports full
coverage, and the use case is governed by nobody.

## When to use this

Standing up an AI governance programme, and after any incident where several
functions were involved and none of them owned it.

## Procedure

**1 — List the functions and the question each asks.** Legal, compliance,
security, privacy, model risk, internal audit. The question is what makes their
coverage claim meaningful — "is it lawful" is a different sweep from "is it
contained".

**2 — Count the controls each function operates.** Operates, not opines on. The
total is usually smaller than the sum of what everyone believes they cover.

**3 — Take each function's self-report at face value** and record it. This is
the state everybody is in before the exercise.

**4 — Walk real use cases through the map.** For each, which function actually
governed it. The ones nobody claims are the seams, and there are always some.

**5 — Write the seam as a pair of assumptions, with an owner.** "Legal assumed
security reviewed the connector; security assumed it was procurement" — then
name who closes it. A seam with no owner is a seam next quarter.

## Example

**Input** — the fixture committed at the top of [`scripts/stakeholder_seam_map.py`](scripts/stakeholder_seam_map.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
   compliance  4 controls  green
   cyber       6 controls  green
   legal       4 controls  green
   model_risk  4 controls  green
   privacy     4 controls  green

functions reporting green : 5/5
open seams                : 4
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
  "functions": [{"name": "str", "question": "str", "controls_operated": 0}],
  "self_reports": [{"function": "str", "claims_coverage": true}],
  "use_cases": [{"name": "str", "governed_by": ["str"], "ungoverned": false}],
  "seams": [{"assumption_a": "str", "assumption_b": "str", "owner": "str|null"}]
}
```

## Failure modes

- **Counting controls a function has an opinion about.** Count what it
  operates.
- **Auditing functions rather than use cases.** The seam is only visible from
  the use case.
- **A seam with no owner.** It is a description, not a fix.
