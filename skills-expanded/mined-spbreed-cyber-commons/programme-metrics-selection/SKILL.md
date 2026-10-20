---
name: programme-metrics-selection
description: >-
  Pick programme metrics that degrade when the programme is neglected, and
  separate them from the comfortable ones that stay green regardless. Use when
  choosing what to report, or when every metric is green and the estate is not.
allowed-tools: Read, Grep, Glob
---

# A metric that cannot go red is a decoration

The test for a programme metric is simple and rarely applied: if the programme
were neglected for a quarter, would this number move? Counts of policies
published, training completed and tools deployed would not. Exposure,
containment effectiveness, evidence freshness and measured time-to-stop all
would.

## When to use this

Choosing what to report to an executive committee, and auditing an existing
dashboard that is entirely green.

## Procedure

**1 — List the candidate metrics** and, for each, what it is computed from.
Anything computed from a plan rather than from the estate is a decoration
already.

**2 — Apply the neglect test.** Simulate a quarter with nothing done: no
attestations refreshed, no evals run, no drift reviewed. Which numbers move?

**3 — Keep the ones that move and say what each one costs to compute.** A
metric nobody can produce monthly will be produced annually and stop being a
control.

**4 — Report the comfortable ones you are dropping,** with the reason. They have
constituencies, and removing them silently gets them reinstated.

**5 — Set a target and a direction per surviving metric.** A number with no
target is a chart; a number with a target is a commitment somebody is
accountable for.

## Example

**Input** — the fixture committed at the top of [`scripts/programme_metrics_selection.py`](scripts/programme_metrics_selection.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
exposure   fleet blast radius             46   units of unreviewed action
likelihood red-team ASR                  25%   measured, containment surface
assurance  controls evidenced            50%   4/8
coverage   agents in inventory           34%   41 of ~120 est.
speed      measured time-to-stop         12s   game day 41 days ago
metrics that look like governance and are not:
   findings closed this quarter      goes up with activity; says nothing about posture
   training completion %             reaches 98% and stays there forever
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
  "candidates": [{"name": "str", "computed_from": "estate|plan", "moves_under_neglect": false}],
  "kept": [{"name": "str", "value": 0.0, "target": 0.0, "cadence": "str", "cost": "str"}],
  "dropped": [{"name": "str", "why": "str"}],
  "neglect_simulation": {"quarter": "str", "moved": ["str"], "unmoved": ["str"]}
}
```

## Failure modes

- **Metrics computed from the plan.** They measure the plan.
- **Dropping comfortable metrics silently.** They come back.
- **No target.** Nobody is accountable for a direction.
