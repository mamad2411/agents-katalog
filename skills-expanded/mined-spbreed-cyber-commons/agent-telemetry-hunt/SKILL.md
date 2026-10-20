---
name: agent-telemetry-hunt
description: >-
  Run a hypothesis-first hunt over agent traces and score what it catches
  against what it misses. Use when looking for agent behaviour no rule was
  written for, when deciding whether a hunt finding should become a detection,
  or when a clean detection surface needs testing from the other direction.
allowed-tools: Read, Grep, Glob
---

# Hunting is the pass that finds what nobody wrote a rule for

A detection encodes a behaviour somebody already understood. A hunt goes the
other way: you state a hypothesis about behaviour that *would* be suspicious,
run it over stored traces, and find out whether it happens.

Over agent telemetry the hypothesis is not the endpoint one. It is not "has
something malicious executed". It is **"has an agent done something its stated
purpose does not explain"** — a tool it never needs, an hour it never runs, a
volume no task requires.

## When to use this

After detection coverage is written, not before. A hunt over a surface with no
rules just re-finds what a rule would have caught cheaply. Run one when the
alert queue has gone quiet and you do not believe it, when an agent's scope
changed, and on a standing cadence for the agents that hold the most authority.

## Step-by-step

**1 — State the hypothesis as a sentence with a subject.** "A workflow agent
called a payments tool outside a booking flow." Not "look for anomalies" —
that is a wish, and it cannot be falsified.

**2 — Name the population before you run it.** Which agents, which window.
Without it, a hit rate has no denominator and you cannot tell a rare event from
a common one you sampled badly.

**3 — Run it and count both sides.** What matched, and what should have matched
and did not. A hunt with only hits is a demo.

**4 — Decide the outcome explicitly: promote, tune, or discard.** A hypothesis
that fires on normal work is not a finding, it is a description of the job.

**5 — Promote to a detection only with a false-positive number attached.**
That is the handover to `detection-rule-synthesis`.

## Example

**Input** — a labelled trace corpus committed in
[`scripts/agent_telemetry_hunt.py`](scripts/agent_telemetry_hunt.py), with
three hypotheses.

**Output** — the opening lines of a real run:

```
corpus: 40 agent runs, 6 of them labelled anomalous

hypothesis                       matched  tp  fp  precision  recall
tool outside declared scope            3   3   0       1.00    0.50
run outside working hours             14   2  12       0.14    0.33
volume above task ceiling              2   2   0       1.00    0.33
```

The middle row is the lesson. Twelve of its fourteen matches are the overnight
batch doing its job, so it is a description of normal work wearing a
hypothesis' clothes. Tune it or discard it — do not ship it.

## Output contract

```json
{
  "corpus": {"runs": 0, "anomalous": 0},
  "hypotheses": [{"name": "str", "matched": 0, "true_positives": 0,
                  "false_positives": 0, "precision": 0.0, "recall": 0.0,
                  "outcome": "promote|tune|discard"}]
}
```

## Common edge cases

- **The hypothesis describes the job.** "Agent called a tool" matches
  everything. If precision is near the base rate, you have described normal.
- **The window excludes the behaviour.** Hunting 24 hours for something that
  happens monthly returns nothing and proves nothing.
- **Labels are the hunt's own output.** Scoring a hunt against findings the
  same hunt produced measures nothing.

## Failure modes

- **Hunting without a denominator.** Five hits is not a result until you know
  five out of how many.
- **Promoting on precision alone.** A rule that fires on one known case and
  nothing else has perfect precision and no value.
- **Never discarding.** A hunt library where nothing is ever retired becomes a
  second alert queue with worse rules.
