---
name: regulatory-clock-check
description: >-
  Run a disclosure deadline from each candidate awareness point and find which
  scoping delays cause it to be missed, then name the owner of each step in the
  runbook. Use when an incident has a reporting obligation and scoping is slow.
allowed-tools: Read, Grep, Glob
---

# The clock started before you knew what happened

Disclosure deadlines run from awareness, and awareness is a defensible judgement
rather than a timestamp. The same incident is met or missed depending on which
point you treat as the start — and the delay that misses it is almost never
containment. It is scoping, and broken attribution is what makes scoping slow.

## When to use this

Any incident with a reporting obligation, and in advance as a tabletop, which is
the only time the answer can still be changed.

## Procedure

**1 — List the candidate awareness points.** First alert, first triage, first
confirmation, first executive notification. Each is arguable, and the earliest
defensible one is the one to plan against.

**2 — Run the clock from each.** Containment, scoping, report drafted, report
submitted. Record met or missed per obligation, per starting point.

**3 — Find the term that misses the deadline.** Containment in an hour and
scoping in three days still misses a 72-hour obligation. Attribution that cannot
say which principal acted turns scoping from hours into days.

**4 — Map obligations to jurisdictions and their clocks.** Different regimes,
different windows, different definitions of a reportable event. One incident can
be inside one and outside another.

**5 — Name an owner per step in the runbook.** Containment, scoping, disclosure
drafting, submission. A runbook with an unowned step is where the hours go.

## Example

**Input** — the fixture committed at the top of [`scripts/regulatory_clock_check.py`](scripts/regulatory_clock_check.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
scenario                            contain   report   met   margin
--------------------------------------------------------------------
fast containment, slow scoping          1.0     80.0 False     -8.0
slow containment, fast reporting       40.0     60.0  True     12.0
both fast                               2.0     20.0  True     52.0
attribution broken (E3.5)               6.0     92.0 False    -20.0

The first row contained in ONE HOUR and still missed the deadline.
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
  "awareness_points": [{"name": "str", "at": "str", "defensible": true}],
  "obligations": [{"regime": "str", "hours": 0}],
  "runs": [{"from": "str", "containment_h": 0, "scoping_h": 0, "report_h": 0,
            "met": [{"regime": "str", "met": false, "by_hours": 0}]}],
  "dominant_delay": "str",
  "runbook": [{"step": "str", "owner": "str|null"}]
}
```

## Failure modes

- **Starting the clock at confirmation.** A regulator may start it earlier.
- **Optimising containment.** Scoping is the term that misses the deadline.
- **An unowned runbook step.** It is the one that takes a day.
