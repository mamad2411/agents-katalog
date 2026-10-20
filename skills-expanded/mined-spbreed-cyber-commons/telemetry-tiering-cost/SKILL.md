---
name: telemetry-tiering-cost
description: >-
  Choose hot, warm or cold storage for each log source from the fastest SOC
  query that reads it, and price the result. Use when designing a detection
  data lake, when a SIEM bill forces a retention cut, or when agent traces are
  about to be deleted for costing too much.
allowed-tools: Read, Grep, Glob
---

# The queries decide the tier, not the retention policy

A detection lake gets designed twice. Once on a whiteboard, where everything is
indexed and searchable, and once when the bill arrives, where retention is cut
across the board by whoever is holding the invoice. The second design is the one
you run, and it is made with no information about what the SOC actually asks.

Deriving the tier from the queries makes it one decision instead of two, and it
is the difference between keeping agent traces and losing them.

## When to use this

Before building the lake, before a retention cut, and whenever a source is
proposed for deletion on cost alone.

## Procedure

**1 — Write down the queries the SOC runs, with the speed each needs.** Triage
in seconds. A hunt can take minutes. Forensic replay can take hours. If you
cannot name the query a source serves, that is the finding.

**2 — Tier each source by the fastest query that reads it.** Nothing else about
the source matters — not its volume, not how interesting it feels, not who
asked for it. Seconds means hot, minutes means warm, hours means cold, and a
source no query reads should be dropped rather than tiered.

**3 — Price both designs.** Index-everything-hot against the tiered version.
The absolute rates vary by platform; the ratios between tiers do not, and the
decision turns on the ratios.

**4 — Look at what the tiering saves, and at what it protects.** The saving is
the headline and the protection is the point: the biggest, cheapest-to-cut
source is usually agent prompts, and it is the only thing a forensic replay can
run against.

## Example

```
  index everything hot   $    18,993 / month
  tiered by query        $    13,398 / month
  difference             $     5,595 / month  (29%)
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
  "queries": [{"name": "str", "reads": ["str"], "needed_within": "seconds|minutes|hours"}],
  "sources": [{"name": "str", "gb_month": 0, "retention_days": 0,
               "tier": "hot|warm|cold|drop", "driven_by": "str"}],
  "cost": {"all_hot": 0.0, "tiered": 0.0, "saved": 0.0},
  "orphans": ["str"]
}
```

## Failure modes

- **Tiering by volume.** The biggest source is not the one that has to be fast.
- **Tiering by feeling.** "Prompts are sensitive so keep them hot" confuses
  sensitivity with latency; sensitivity is a retention and redaction decision
  (see `agent-telemetry-retention`).
- **Leaving orphans tiered.** A source no query reads is not cheap storage, it
  is a liability with a bill attached.
- **Reading the saving as the result.** The result is which sources survive the
  next cut, and why.
