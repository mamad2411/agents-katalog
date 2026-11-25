---
name: incident-control-mapping
description: >-
  Map each control failure in a published incident to the control that would
  have closed it, count preventive against detective, and find the shared
  surface that turns several findings into one chain. Use when reading an
  incident report you did not write.
allowed-tools: Read, Grep, Glob
---

# The report is a list; the value is the chain

A published incident gives you a sequence of control failures for free. Two
things turn it into something you can act on: pairing each failure with the
control that would have closed it, and noticing where one shared surface appears
in several rows — because filed as separate findings, three teams each fix their
third and the surface stays.

## When to use this

Reading any incident report — yours or somebody else's — and when building a
control register from real events rather than from a framework.

## Procedure

**1 — Extract the failures in order.** One row per control that did not hold,
with the precondition that made the next one reachable.

**2 — Pair each with a mitigating control.** Name it, classify it as preventive,
detective or corrective, and map it to whatever catalogue you already report
against.

**3 — Count preventive against detective.** A register that is overwhelmingly
preventive is a register that will not tell you when a control is off, and that
ratio is worth stating explicitly.

**4 — Find the shared surfaces.** Which surface appears in three or more rows.
That is one chain, not three findings, and the remediation is a single
workstream with one owner.

**5 — Assign each control an owning lesson or team.** A control with no owner is
a sentence in a report. This is the column that makes the mapping a register
rather than an analysis.

## Example

**Input** — the fixture committed at the top of [`scripts/incident_control_mapping.py`](scripts/incident_control_mapping.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
shared surface        rows        reading
agent container       [1]         single row
artifact repository   [1, 2, 5]   one chain, not separate findings
benchmark scoring     [10]        single row
eval configuration    [6]         single row
harness tooling       [9]         single row
peer channel          [7, 8]      linked
public internet       [4]         single row
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
  "failures": [{"id": "str", "what": "str", "precondition": "str"}],
  "controls": [{"id": "str", "name": "str", "type": "P|D|C|P/D|D/C", "catalogue_ref": "str", "owner": "str"}],
  "mix": {"preventive": 0, "detective": 0},
  "surfaces": [{"surface": "str", "rows": [0], "reading": "single row|linked|one chain"}]
}
```

## Failure modes

- **One finding per row.** The shared surface survives every fix.
- **An all-preventive register.** Nothing tells you when a control is disabled.
- **Controls with no owner.** They do not get built.
