---
name: capability-build-order
description: >-
  Compare a build order that produces control coverage against one that produces
  demos, quarter by quarter, and state what each has at the end of every period.
  Use when planning what to build first with a fixed team.
allowed-tools: Read, Grep, Glob
---

# Nothing demoable until Q3, and 100% coverage at Q4

Two orders, the same work. One builds the controls in dependency order and
produces coverage; the other builds the visible things first and produces
capabilities. The second looks better for three quarters and finishes lower, and
the only way to survive the first is to say in advance that it will look like
that.

## When to use this

Planning a multi-quarter build with a fixed team, and defending a plan whose
early quarters have nothing to show.

## Procedure

**1 — List the required controls and what each depends on.** Coverage is
measured against this list, so it has to exist before either order can be
scored.

**2 — Mark which controls are demoable.** Some produce something a stakeholder
can see; most do not. This is the honest input to the tension rather than a
complaint about it.

**3 — Simulate the dependency-respecting order.** Coverage per quarter and what
is demoable per quarter. Expect a flat, invisible start.

**4 — Simulate the demo-first order.** It will lead for several quarters on
capability and trail on coverage, and it will end lower because later controls
block on earlier ones.

**5 — Publish both, with the Q1 and Q2 warning explicit.** A plan that predicts
its own quiet period survives it; one that does not gets re-planned in month
four into the other order.

## Example

**Input** — the fixture committed at the top of [`scripts/capability_build_order.py`](scripts/capability_build_order.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
quarter                         coverage   demoable
------------------------------------------------------
Q1 · inventory + identity            25%          0
Q2 · containment                     50%          0
Q3 · evidence + evaluation           75%          1
Q4 · continuous + stop              100%          3

Q1 and Q2 produce nothing demoable. That is the political problem, and
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
  "required": ["str"],
  "demoable": {"str": false},
  "orders": [{"name": "str",
              "quarters": [{"q": "str", "built": ["str"], "coverage": 0.0, "demoable": 0}],
              "final_coverage": 0.0, "final_capabilities": 0}],
  "warning": "str"
}
```

## Failure modes

- **Building demoable things first.** It finishes lower.
- **Not warning about the quiet quarters.** The plan gets replaced in month
  four.
- **Coverage against a list that does not exist yet.** Write the required set
  first.
