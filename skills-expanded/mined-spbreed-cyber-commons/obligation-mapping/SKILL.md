---
name: obligation-mapping
description: >-
  Resolve which regulatory layers apply to an AI system — horizontal, sectoral
  and data protection — and register the shortest clock among the obligations
  they impose. Use when a system attracts obligations from more than one regime.
allowed-tools: Read, Grep, Glob
---

# Three layers, and the shortest clock is the one you plan against

Regulation arrives in layers that apply simultaneously: horizontal AI rules
triggered by what the system does, sector rules triggered by the industry, and
data protection triggered by the data. A single agent commonly attracts all
three, and the operational consequence is one number — the shortest reporting
clock among them.

## When to use this

At intake for any AI system, and again when it changes what it does, who it
serves, or what data it reads.

## Procedure

**1 — Describe the system in the terms the regimes use.** Purpose, sector,
decision effect on individuals, data categories, deployment geography. These are
the trigger inputs, and vague answers here produce vague obligations.

**2 — Resolve each layer independently.** Horizontal by risk category, sector by
industry and function, data protection by category and territory. Do not let one
layer's conclusion suppress another's — they are cumulative.

**3 — List the obligations each produces,** with its clock. Reporting windows,
assessment requirements, record-keeping durations, human-oversight duties.

**4 — Register the shortest clock.** That is the one the incident runbook has to
meet. Publish it with the obligation it comes from, so nobody relaxes it by
citing a longer one.

**5 — Record what changes the answer.** Adding a decision effect, a new
territory, a new data category. Obligations are re-derived on those events, not
annually.

## Example

**Input** — the fixture committed at the top of [`scripts/obligation_mapping.py`](scripts/obligation_mapping.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
claims-triage-agent — autonomy L2.5, data ['customer', 'health', 'regulated']

instrument             layer  obligation
--------------------------------------------------------------------------------------------
EU AI Act                  1  automated decision affecting individuals; human oversight and record-keeping obligations
DORA                       2  ICT third-party risk, incident reporting, resilience testing, exit strategy
HIPAA-equivalent           2  minimum necessary; audit controls
GDPR                       3  lawful basis, erasure, automated decision-making
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
  "system": {"purpose": "str", "sector": "str", "decision_effect": true,
             "data_categories": ["str"], "territories": ["str"]},
  "layers": [{"layer": "horizontal|sector|data_protection", "regime": "str", "applies": true, "why": "str"}],
  "obligations": [{"regime": "str", "obligation": "str", "clock_hours": 0}],
  "shortest_clock": {"hours": 0, "from": "str"},
  "re_derive_on": ["str"]
}
```

## Failure modes

- **Stopping at the first regime that applies.** They are cumulative.
- **Planning against the longest clock.** The shortest is the one you miss.
- **Annual re-derivation.** The triggers are changes, not dates.
