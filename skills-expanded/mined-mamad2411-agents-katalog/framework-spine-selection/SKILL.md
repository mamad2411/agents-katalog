---
name: framework-spine-selection
description: >-
  Choose the framework that covers the most of your controls as a spine, supply
  the remainder from the others, and compare that against building a programme
  per framework. Use when several frameworks apply and each is proposing its own
  programme.
allowed-tools: Read, Grep, Glob
---

# One spine, and the rest as supplements

Voluntary frameworks overlap heavily. Building a programme per framework
multiplies the same work by the number of logos, and the artefacts are nearly
identical. Choosing the one with the widest coverage as a spine and supplying
the gaps from the others produces the same coverage for a fraction of the
effort — and the comparison is arithmetic, so it survives a meeting.

## When to use this

When more than one framework is in scope, and when a second framework is
proposed as a separate workstream.

## Procedure

**1 — Take your control catalogue as the fixed thing.** Frameworks are mapped to
it, not the other way round. If you do not have one, build it first; there is
nothing to compare otherwise.

**2 — Compute coverage per framework.** How many of your controls each one
addresses. Report the counts, not impressions of comprehensiveness.

**3 — Select the widest as the spine,** and name the controls it leaves
uncovered. Those are the gaps, and they are usually few.

**4 — Assign each gap to whichever framework covers it best.** One control, one
source. The result is a single programme with a few supplements rather than
several programmes.

**5 — Cost both plans.** Spine-plus-supplements against per-framework. Include
the duplicated evidence collection, which is where the difference actually sits.

## Example

**Input** — the fixture committed at the top of [`scripts/framework_spine_selection.py`](scripts/framework_spine_selection.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
framework           covers  controls
--------------------------------------------------------------
NIST AI RMF              5  ['AC-1', 'AC-2', 'DR-1', 'EV-2', 'SB-1']
ISO 42001                4  ['AC-1', 'AC-2', 'DR-1', 'EV-1']
EU AI Act                4  ['AC-1', 'EV-1', 'SB-2', 'ST-1']
ISO 27001                1  ['SB-1']
DORA                     1  ['ST-1']
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
  "catalogue": ["str"],
  "coverage": [{"framework": "str", "covers": ["str"], "count": 0}],
  "spine": {"framework": "str", "count": 0, "gaps": ["str"]},
  "supplements": [{"control": "str", "from": "str"}],
  "cost": {"spine_plan": 0, "per_framework_plan": 0, "duplicated_evidence": 0}
}
```

## Failure modes

- **Choosing the spine by reputation.** Choose it by coverage of your controls.
- **Building per framework.** The evidence is duplicated, not the assurance.
- **No control catalogue.** There is nothing to map against.
