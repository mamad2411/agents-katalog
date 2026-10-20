---
name: sector-overlay-assessment
description: >-
  Find the pre-existing sector clauses that already apply to an AI system
  without mentioning AI, and assess provider exit against them. Use when a team
  believes no regulation applies yet because the AI rules are not in force.
allowed-tools: Read, Grep, Glob
---

# The clauses that already apply and never say "AI"

Sector regulation was written before this and applies anyway. Outsourcing,
material change, operational resilience, exit strategy, data handling — none of
them mention AI, all of them bind an agent that processes claims or moves money.
The finding is usually that a system nobody thought was regulated attracts seven
clauses today.

## When to use this

Any AI system in a regulated sector, especially one whose team believes the
obligations arrive later.

## Procedure

**1 — Describe the system functionally.** What it processes, what it decides,
whose money or health or data it touches. Sector clauses trigger on function,
not on technology.

**2 — Search existing obligations for the functional triggers.** Outsourcing and
third-party dependency, material change notification, resilience and continuity,
record keeping, exit. Do not search for "AI" — that is why nobody found them.

**3 — Record each clause with what it requires,** in operational terms. "Notify
the regulator of material change to an outsourced arrangement" becomes a
question about whether a hosted model version change is a material change.

**4 — Assess provider exit specifically.** Could you move off this provider,
how long would it take, and is the alternative viable? A hosted frontier API
with no equivalent substitute usually fails an exit test that a database would
pass.

**5 — Make the case for each clause explicitly.** Clause, why it applies, what
it requires here. That framing survives a challenge from a team that would
rather it did not apply.

## Example

**Input** — the fixture committed at the top of [`scripts/sector_overlay_assessment.py`](scripts/sector_overlay_assessment.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
claims-triage-agent: autonomy L2.5, data ['customer', 'health'], external model True

DORA (financial)
   ICT third-party risk    your model provider is an ICT third party
   exit strategy           can you stop using this provider and keep operating?
   resilience testing      your stop mechanism is in scope for testing
   incident reporting      clocks measured in hours
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
  "system": {"function": "str", "decides": "str", "data": ["str"]},
  "clauses": [{"framework": "str", "clause": "str", "mentions_ai": false,
               "applies_because": "str", "requires": "str"}],
  "exit": [{"provider": "str", "substitutable": false, "days_to_exit": 0, "verdict": "str"}],
  "cases": [{"clause": "str", "argument": "str"}]
}
```

## Failure modes

- **Searching for AI.** The binding clauses do not use the word.
- **Waiting for the horizontal regime.** These apply now.
- **An exit assessment that assumes substitutability.** Test it.
