---
name: research-durability-check
description: >-
  Separate a folklore claim from a research result, and score a finding backlog
  on whether each finding became a control, a detection, or nothing. Use when
  justifying a research function, or when last year's findings cannot be traced
  to anything that changed.
allowed-tools: Read, Grep, Glob
---

# Research is what survives the person who did it

A finding that closed a ticket is a fix. A finding that became a control or a
detection is institutional capital, and the difference is measurable — which
means a research programme can be defended with a number rather than with
enthusiasm.

## When to use this

Reviewing a research backlog, defending the function's budget, or deciding what
"done" means for a finding.

## Procedure

**1 — Test each claim for actionability.** Three gaps disqualify it: no
reproduction, no affected-version statement, no stated condition under which it
does not hold. A card failing any of them is folklore, however true it is.

**2 — Classify each closed finding by outcome.** A control, a detection, an eval
case, or nothing — a patch with no accompanying control counts as nothing for
this purpose, because the class recurs.

**3 — Compute durability.** The share of findings that produced a control or a
detection. It is usually about half, and the half that produced nothing is
usually the more interesting work.

**4 — Look at what the lost half had in common.** Typically: no owner outside
the research team, or a finding whose class had no control to attach to. Both
are addressable and neither is about effort.

**5 — Define closure to require an outcome.** A finding is closed when it has a
control, a detection or an explicit accepted-risk record with an owner. Anything
else reopens as the same finding next year.

## Example

**Input** — the fixture committed at the top of [`scripts/research_durability_check.py`](scripts/research_durability_check.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
=== folklore — actionable: False ===
CLAIM     our review agent can be tricked by comments in diffs
SETUP     the review agent
TRIGGER   a comment
OBSERVED  it approved something it shouldn't
RATE      not measured
HOLDS WHEN
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
  "claims": [{"name": "str", "actionable": false, "gaps": ["reproduction", "versions", "conditions"]}],
  "backlog": [{"finding": "str", "outcome": "control|detection|eval|none", "owner": "str|null"}],
  "durability": 0.0,
  "lost": {"count": 0, "common_cause": "str"},
  "closure_definition": "str"
}
```

## Failure modes

- **Counting patched as closed.** The class recurs and the count flatters.
- **Scoring effort.** Durability is about outcome, not about difficulty.
- **No owner outside research.** That is the mechanism by which findings are
  lost.
