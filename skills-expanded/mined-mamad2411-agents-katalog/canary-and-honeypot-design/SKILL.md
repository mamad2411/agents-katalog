---
name: canary-and-honeypot-design
description: >-
  Place credential canaries and honeypot tasks in an agent's environment so that
  an alert has no structurally possible false positive, and measure how fast the
  signal decays as agents learn. Use when deception is being added, or when a
  detection needs to be one nobody has to triage.
allowed-tools: Read, Grep, Glob
---

# An alert with no possible false positive

A canary credential that nothing legitimate uses produces an alert that needs no
triage: the only way it authenticates is that somebody read it and tried it.
That property is structural, not statistical, and it is why deception belongs in
an agent environment where every other signal is ambiguous.

## When to use this

Designing detection for agent environments, and whenever an existing detection's
false-positive rate is the reason it is ignored.

## Procedure

**1 — Place canaries where only reading them is unusual.** Environment
variables, config files, the fixtures a code agent walks. They must be
indistinguishable from real ones — a canary named `canary_key` is a filter, not
a trap.

**2 — Ensure nothing legitimate uses them.** This is the whole property. Check
the code, the tests and the deployment. One legitimate reference and the alert
becomes triage.

**3 — Instrument the authentication path** to capture source address and user
agent on use. A canary alert with no context tells you that it happened and
nothing about who.

**4 — Add honeypot tasks for behaviour rather than credentials.** A task with an
available shortcut that nothing legitimate would take. Log the attempt and score
it; this measures inclination, which no credential can.

**5 — Measure decay.** Agents and operators learn. Model the hit rate over days
since placement, with and without rotation, and set the rotation interval from
the curve rather than from a calendar.

## Example

**Input** — the fixture committed at the top of [`scripts/canary_and_honeypot_design.py`](scripts/canary_and_honeypot_design.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
token                     source        agent                 verdict
hf_liveTokenNotShown      10.2.0.11     ci-runner             normal use
hf_CANARY7Fq2mXvLpR8s     203.0.113.9   python-requests/2.31  CONFIRMED COMPROMISE
ghp_alsoLive              10.2.0.11     ci-runner             normal use
sk-CANARYd3Vn8yHc2Uae     203.0.113.9   python-requests/2.31  CONFIRMED COMPROMISE

canary hits: 2  false positives possible: 0
Not zero because the detector is good - zero because nothing legitimate
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
  "canaries": [{"id": "str", "placed_in": "str", "indistinguishable": true, "legitimate_refs": 0}],
  "alerts": [{"canary": "str", "source_ip": "str", "user_agent": "str", "false_positive_possible": false}],
  "honeypot_tasks": [{"task": "str", "shortcut": "str", "attempts": 0}],
  "decay": {"days": [0], "hit_rate": [0.0], "rotation_days": 0}
}
```

## Failure modes

- **A canary anything legitimate touches.** The property is gone and the alert
  becomes noise.
- **Naming it as a canary.** It becomes a filter for the competent attacker.
- **Never rotating.** The signal decays and the absence of alerts reads as
  safety.
