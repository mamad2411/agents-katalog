---
name: structural-investigating
description: Use when debugging defects, running spikes, reducing unknowns, diagnosing flaky behavior, investigating incidents, testing hypotheses, or de-risking an approach.
---

# Structural Investigating

Spend inquiry, not luck. Close when the unknown is reduced enough to act.

Core rule:

> Name one question, make the failure reproducible or measured, falsify hypotheses, and hand off a diagnosis plus a failing test.

## Default output

```md
## Question
- Single unknown:
- Time box:
- Decision if unresolved:

## Reproduction / measurement
- Controlled inputs:
- Remaining randomness:
- Failure rate or deterministic repro:

## Hypotheses
- Current theory:
- What would disprove it:
- Next bisection step:

## Output
- Diagnosis:
- Red test / spike finding:
- Ruled out:
- Follow-up:
```

## Investigation checks

- Name the one question and time-box the answer. Decide what happens if the box expires.
- Reproduce deterministically first; if impossible, pin variables and measure a failure rate.
- Form a falsifiable hypothesis before looking. Design probes to halve the search space.
- Cash in existing observability before adding probes. A blind spot is a finding.
- Distrust narratives and wall-clock ordering; use artifacts, traces, commit/config diffs, causal ids.
- Spike forward, then throw spike code away unless you are ready to harden and own it.
- End with diagnosis and failing test or decision record, not an unproven fix.
- Record what you ruled out so the next person does not rerun the dig.

## Red flags

- “Look into it” with no question or clock.
- Testing fixes against a flaky repro and treating silence as proof.
- Changing three layers at once.
- Adding broad debug logging without removing/scoping it later.
- Shipping spike-grade code because the demo worked.
