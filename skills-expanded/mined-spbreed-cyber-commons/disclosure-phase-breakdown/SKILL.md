---
name: disclosure-phase-breakdown
description: >-
  Break a disclosure deadline into its phases and find the one that consumes
  most of it — usually establishing who acted rather than containment. Use when
  a reporting obligation is being planned for, or was missed.
allowed-tools: Read, Grep, Glob
---

# Two-thirds of the clock is establishing who acted

Disclosure planning concentrates on containment because that is the exciting
part. The phase breakdown says otherwise: containment in an hour, and
establishing the acting identity in forty-eight, on a seventy-two hour clock.
The delay is attribution, and attribution is fixed months earlier by what the
logs record.

## When to use this

Planning for a reporting obligation, and at post-incident review when a deadline
was met late or narrowly.

## Procedure

**1 — Enumerate the phases.** Detection, triage, containment, establishing who
acted, scoping affected subjects, drafting, approval, submission. All of them,
including the approval step everyone forgets.

**2 — Attribute hours to each from a real incident** or a tabletop. Estimates
here are systematically optimistic; use measured values where you have them and
mark the rest as estimates.

**3 — Find the dominant phase.** It is usually attribution or scoping. Report it
as a proportion of the whole clock, which is what makes it actionable.

**4 — Re-run with delegation chains recorded.** Model what attribution costs
when the acting identity and the chain are on every record. The difference is
the business case for B2.7-style attribution, in hours against a regulatory
deadline.

**5 — Pre-draft what can be pre-drafted.** The regime, the template, the
distribution list, the approver. Drafting under time pressure is where the
avoidable hours are.

## Example

**Input** — the fixture committed at the top of [`scripts/disclosure_phase_breakdown.py`](scripts/disclosure_phase_breakdown.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
scenario                          contain   report   met   margin
------------------------------------------------------------------
attribution sound                     2.0     20.0  True     52.0
attribution broken, 3d scope          6.0     92.0 False    -20.0
fast containment, slow scope          1.0     80.0 False     -8.0

The third row contained in ONE HOUR and missed by 8 hours.
phase                                   hours  cumulative  note
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
  "obligation": {"regime": "str", "hours": 0},
  "phases": [{"phase": "str", "hours": 0, "measured": false}],
  "total_hours": 0,
  "dominant": {"phase": "str", "share": 0.0},
  "with_attribution": {"phase_hours": 0, "total_hours": 0, "meets_deadline": true},
  "pre_drafted": ["str"]
}
```

## Failure modes

- **Optimising containment.** It is already the fast phase.
- **Estimating attribution.** Measure it once; it is worse than you think.
- **Omitting approval.** It is a real phase with a real queue.
