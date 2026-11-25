---
name: risk-translation-upward
description: >-
  Compute a fleet's exposure, containment effectiveness and control coverage,
  then translate the three numbers into a statement a board can act on rather
  than a list of findings. Use when preparing an executive update on agentic
  risk.
allowed-tools: Read, Grep, Glob
---

# A findings list is not a position

An executive update made of findings asks the reader to do the synthesis, and
they will do it wrong or not at all. Three computed numbers — how much the fleet
can reach, how much of an attack it stops, how much of the control set is
evidenced — support a position, a decision and a request.

## When to use this

Preparing a board or executive committee update, and whenever the current one is
a list of incidents.

## Procedure

**1 — Compute exposure.** Sum the blast radius across the fleet, weighted by
scope, with gated actions discounted. One number, and say what it is a sum of.

**2 — Compute containment effectiveness.** Attack success rate against the
controls as they run today, from the eval suite rather than from design intent.

**3 — Compute control coverage in three states.** Evidenced, stale, unevidenced.
The stale count is the one that moves an executive conversation, because it is
the one nobody expected.

**4 — Write the findings-shaped version and mark what is wrong with it.**
Usually: no trend, no comparison, no decision requested, no cost, and no
statement of what happens if nothing changes. Showing that is how the format
changes.

**5 — Write the position.** Where the exposure is concentrated, what would
reduce it most per unit of friction, what you are asking for, and what you will
report next time. Same numbers, different artefact.

## Example

**Input** — the fixture committed at the top of [`scripts/risk_translation_upward.py`](scripts/risk_translation_upward.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
agent                     blast radius
----------------------------------------
pr-remediation-agent                44
claims-triage-agent                  1
doc-summariser                       1
FLEET TOTAL                         46

red-team attack success rate (containment surface): 25%
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
  "exposure": {"total": 0, "by_agent": [{"name": "str", "blast": 0, "gated": ["str"]}]},
  "containment": {"asr": 0.0, "from": "eval suite"},
  "coverage": {"evidenced": 0, "stale": 0, "unevidenced": 0, "of": 0},
  "findings_version": {"problems": ["str"]},
  "position": {"concentration": "str", "best_reduction": "str", "ask": "str", "next_report": "str"}
}
```

## Failure modes

- **Reporting incidents.** They are anecdotes at this altitude.
- **One coverage number.** The stale bucket is the story.
- **No ask.** An update with no decision requested gets noted.
