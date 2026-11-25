---
name: resilience-readiness-check
description: >-
  Check the three properties a programme needs for the day a control fails —
  drift is detected, the stop mechanism is tested, and the run is replayable —
  and report which are not ready. Use as a standing readiness check rather than
  after an incident.
allowed-tools: Read, Grep, Glob
---

# Perfection is not available; these three are

A programme cannot prevent every failure and does not need to. What it needs is
that when a control fails, somebody notices, somebody can stop it, and somebody
can reconstruct what happened. Each of the three is testable today, and each
fails quietly if nobody tests it.

## When to use this

As a standing quarterly check, before granting unattended autonomy, and as the
closing item of a programme review.

## Procedure

**1 — Detection: compare today against the signed-off baseline.** Not "do we
have monitoring" — run the comparison and report the drift and any new tool. A
monitor that has never been compared against a baseline is untested.

**2 — Stop: check the mechanism, the measurement and the date.** A named
mechanism, a measured time-to-stop in seconds, and when it was last exercised. A
test older than a quarter is a claim.

**3 — Replay: check the run record has the five inputs** — prompts, tool
results, model version, seed, retrieved context — and confirm the delegation
chain and the resources reached are recorded.

**4 — Report each as ready or not, with the missing item named.** Three
booleans and three sentences. A single readiness score hides which of the three
is missing, and they have different owners.

**5 — Re-run after every change to any of the three.** A model upgrade
invalidates the drift baseline; a platform change invalidates the stop test.

## Example

**Input** — the fixture committed at the top of [`scripts/resilience_readiness_check.py`](scripts/resilience_readiness_check.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
NOTICE   drift 0.500  new tools ['run_shell']  → detected
STOP     12s, tested 41d ago, survives restart True  → ready
RECOVER  replayable True, scope from the chain ['queue', 'repo-core', 'repo-payments']  → ready
programme                 containment ASR  outcome when containment fails
------------------------------------------------------------------------------------------------
prevention only                        0%  undetected — found by a third party, weeks later
                                         elapsed to resolution: 720h
prevention + notice                    0%  detected, cannot halt it — damage continues while you improvise
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
  "detection": {"baseline_at": "str", "drift": 0.0, "new_tools": ["str"], "ready": true},
  "stop": {"mechanism": "str", "measured_seconds": 0, "last_tested": "str", "ready": true},
  "replay": {"inputs_present": ["str"], "missing": ["str"], "chain_recorded": true,
             "resources_recorded": true, "ready": true},
  "verdict": {"ready": false, "missing": ["str"]}
}
```

## Failure modes

- **Checking that monitoring exists.** Run the comparison.
- **An estimated time-to-stop.** Measure it.
- **A single readiness score.** Three properties, three owners.
