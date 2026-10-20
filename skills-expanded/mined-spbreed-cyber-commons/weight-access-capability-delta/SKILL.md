---
name: weight-access-capability-delta
description: >-
  Enumerate the capabilities local weights grant that a hosted API does not, and
  convert a rate limit into an attempt budget to show what removing it does to a
  low-probability technique. Use when assessing open-weight release risk or
  arguing about hosted safeguards.
allowed-tools: Read, Grep, Glob
---

# The rate limit was the control

Hosted access and local weights differ in two ways that matter and one that gets
all the attention. The capability delta — fine-tuning away refusals, reading
activations, sampling without a filter — is real. The larger one is arithmetic:
a hosted rate limit caps attempts, and removing it turns a technique with a
0.5% success rate into tens of thousands of successes in a day.

## When to use this

Assessing the risk of an open-weight release, comparing hosted and local
deployment, or evaluating a safeguard that exists only in the serving layer.

## Procedure

**1 — List the capabilities local access grants.** Weight modification,
activation access, unfiltered sampling, arbitrary system prompts, no logging.
For each, say whether a hosted API offers it.

**2 — Turn the rate limit into an attempt budget.** Requests per minute × the
window. Do the same for local inference from its throughput. Report the ratio;
it is usually two or three orders of magnitude and it is the headline.

**3 — Apply a per-attempt success rate.** A technique that works 0.5% of the
time produces a handful of successes hosted and tens of thousands locally. The
technique did not change.

**4 — Assess readiness for each safeguard.** Which safeguards survive weight
access at all — the ones in the serving layer do not. Say so plainly rather than
listing them as mitigations.

**5 — Weight the blast radius by scope.** A capability that reaches a team's
resources is not the same as one that reaches a run's own. Score tools by scope
and mark which are gated.

## Example

**Input** — the fixture committed at the top of [`scripts/weight_access_capability_delta.py`](scripts/weight_access_capability_delta.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
setting                              attempts in 24h
------------------------------------------------------
hosted API, 20 req/min                        28,800
hosted API, 20 req/min, 5 keys               144,000
local open weights, 1 GPU                    691,200
local open weights, 8 GPUs                 5,529,600

ratio: 192× more attempts, with no abuse signal reaching anyone.
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
  "capabilities": [{"name": "str", "hosted": false, "local": true}],
  "attempts": {"hosted_per_day": 0, "local_per_day": 0, "ratio": 0},
  "technique": {"per_attempt_rate": 0.0, "hosted_successes": 0, "local_successes": 0},
  "safeguards": [{"name": "str", "layer": "serving|weights", "survives_local": false}],
  "blast": {"tools": [{"name": "str", "scope": "self|project|team", "gated": false}], "score": 0}
}
```

## Failure modes

- **Listing serving-layer safeguards as mitigations** for a weight release.
- **Comparing capability and ignoring throughput.** Throughput is the bigger
  term.
- **Assuming a low success rate is a control.** It is, until the attempt budget
  changes.
