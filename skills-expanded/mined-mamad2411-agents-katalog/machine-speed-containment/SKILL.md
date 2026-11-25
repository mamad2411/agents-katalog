---
name: machine-speed-containment
description: >-
  Race an agent's action rate against the approval delay in front of
  containment, time the whole containment path end to end, and decide which
  signals may auto-revoke. Use when containment requires a human and the subject
  acts hundreds of times a minute.
allowed-tools: Read, Grep, Glob
---

# Eight minutes of approval is 2,400 actions

Containment that waits for a person is measured against a subject that does not
wait. The arithmetic is not close, and it is the argument for pre-authorising
revocation for a named set of signals — with the false-revocation cost stated,
because that is the objection.

## When to use this

Designing containment for agent workloads, and after any incident where the
containment step was correct and late.

## Procedure

**1 — Measure the subject's rate.** Actions per minute, observed rather than
designed. Multiply by the approval delay to get the actions taken while
somebody decides.

**2 — Time the whole path, not the revocation.** Detection, triage, decision,
approval, execution, propagation. The revocation itself is usually seconds and
the path is usually minutes; reporting only the last step makes the problem
invisible.

**3 — Find the dominant term.** It is almost always human approval or
propagation delay, and it is almost never the API call. Optimise the dominant
term or nothing changes.

**4 — Classify signals for auto-revocation.** For each, its precision and what a
false revocation costs. High-precision signals against a non-human subject are
the candidates: revoking an agent's token wrongly costs a restarted run.

**5 — Set the policy asymmetrically.** Auto-revoke agent credentials on
high-precision signals; keep a human in front of anything that affects a person's
access. State both halves so the policy survives review.

## Example

**Input** — the fixture committed at the top of [`scripts/machine_speed_containment.py`](scripts/machine_speed_containment.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
   agent rate   human 8min   auto 12s   ratio
----------------------------------------------
       30/min          240          6    40.0×
      120/min          960         24    40.0×
      300/min         2400         60    40.0×
     1200/min         9600        240    40.0×

At 300/min an 8-minute approval costs 2,400 further actions.
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
  "race": {"actions_per_min": 0, "approval_minutes": 0, "actions_during_approval": 0},
  "path": [{"step": "str", "seconds": 0}],
  "total_seconds": 0,
  "dominant_step": "str",
  "signals": [{"name": "str", "precision": 0.0, "subject": "agent|human",
               "auto_revoke": false, "false_revocation_cost": "str"}]
}
```

## Failure modes

- **Timing the revocation.** It is the fast part.
- **One policy for agents and people.** The costs differ by orders of
  magnitude.
- **Auto-revoking on a low-precision signal.** Precision is the entry
  requirement.
