---
name: runbook-tier-assignment
description: >-
  Run one incident's response at fully automated, human-in-the-loop and manual
  tiers, and compare time to contain against wrong actions. Use when choosing a
  runbook's tier, when justifying automation to a risk function, or when
  "automate everything" and "keep a human in it" are both being asserted.
allowed-tools: Read, Grep, Glob
---

# Three tiers, three ways of being wrong

The tiers are not levels of ambition. They are three different trades between
**time to contain** and **the cost of acting on a bad signal** — and which trade
is right depends on the detection's false-positive rate, not on taste.

There is no single score that ranks them. Seconds of exposure and wrongly
contained agents are in different units; any number that ranks them has an
exchange rate hidden inside it. Choose that rate openly, per incident class, or
do not choose it.

## When to use this

When assigning a tier to a new runbook, and when reviewing an existing one after
its detection's false-positive rate has been measured. The tier should move when
the rate moves.

## Step-by-step

**1 — Take the tier from `remediation-policy-check` as the ceiling.** This skill
chooses within what policy permits, never above it.

**2 — Time each step at each tier honestly.** The decide step is where the tiers
actually differ; the mechanical steps barely move.

**3 — Bring the detection's measured false-positive rate.** Without it this is
an argument about feelings.

**4 — Report both costs side by side, unranked.** Resist the composite score.

**5 — Choose, and write down the exchange rate you used.** The next person needs
to know what you traded, not just what you picked.

## Example

**Input** — one incident, five steps, three tiers, in
[`scripts/runbook_tier_assignment.py`](scripts/runbook_tier_assignment.py).

**Output** — a real run:

```
tier                   contain   reaches the estate wrongly / 100
automated                  14s                                8.0
human-in-the-loop         253s                                1.2
manual                   2072s                                0.2
```

Manual contains after 34 minutes, against a 29-minute breakout time.

## Output contract

```json
{
  "tiers": [{"tier": "str", "seconds_to_contain": 0, "wrong_actions_per_100": 0.0}]
}
```

## Common edge cases

- **The detection has no measured rate.** Then no tier can be justified; measure
  first.
- **The human is not actually available.** A human-in-the-loop tier with a
  four-hour on-call response is a manual tier wearing a badge.
- **The confirmation dialog.** A HITL step nobody can meaningfully refuse is an
  automated step with extra latency.

## Failure modes

- **Composite scores.** They always favour whichever axis the author weighted.
- **Automating on an unmeasured detection.** The fastest possible way to break
  production on a false positive.
- **Manual as the safe default.** On a 29-minute breakout time, slow is a risk
  decision too — just an unstated one.
