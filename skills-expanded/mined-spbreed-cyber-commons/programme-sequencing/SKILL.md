---
name: programme-sequencing
description: >-
  Simulate a programme's build order against its prerequisites and find the
  steps that block on something not yet done. Use when planning an AI security
  programme, or when a plan starts with evaluation.
allowed-tools: Read, Grep, Glob
---

# Only one step is doable from a standing start

Programme plans are usually ordered by what is interesting or visible.
Simulating the order against prerequisites shows which steps block: the popular
evaluation-first sequence completes four of six on the first pass and stalls
twice, because you cannot evaluate what you have not inventoried or tier what
you cannot list.

## When to use this

Planning a programme, reviewing somebody else's plan, and when a quarter ended
with several things "in progress".

## Procedure

**1 — Write the steps and their prerequisites.** Explicitly, as a dependency
list. Most disagreements about order dissolve here, because the dependency is
not a matter of opinion.

**2 — Identify what is doable from a standing start.** Steps with no
prerequisites. There is usually exactly one, and it is the inventory.

**3 — Simulate the proposed order.** Walk it, marking each step done or blocked.
Report completions on the first pass and the steps that blocked, with what they
were waiting on.

**4 — Simulate the dependency-respecting order** and compare. Same steps, same
effort, different completion — that comparison is the argument, and it does not
require anybody to concede a preference.

**5 — Say what each order produces at the end of each period.** The correct
order usually produces nothing demoable for two quarters, and saying so in
advance is what stops it being abandoned in the second.

## Example

**Input** — the fixture committed at the top of [`scripts/programme_sequencing.py`](scripts/programme_sequencing.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
 step  name          needs     unlocks
------------------------------------------------------------------------------------
    1  inventory     []        you can now tier and assign owners
    2  identity      [1]       per-agent revocation; attribution in logs
    3  containment   [1]       bounded blast radius; a red team has something to test
    4  evidence      [2]       act chains; replayable runs; a drift baseline
    5  evaluation    [4]       accuracy you can defend; regression cases
    6  continuous    [4, 5]    freshness windows; drift alerts; live posture
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
  "steps": [{"id": 0, "name": "str", "requires": [0]}],
  "doable_from_start": [0],
  "orders": [{"name": "str", "sequence": [0], "completed_first_pass": 0,
              "blocked": [{"step": 0, "waiting_on": [0]}]}],
  "per_period_output": [{"order": "str", "period": "str", "demoable": false}]
}
```

## Failure modes

- **Starting with evaluation.** It depends on nearly everything else.
- **Arguing about order without the dependency list.** It becomes preference.
- **Not warning about the quiet quarters.** The plan gets abandoned mid-way.
