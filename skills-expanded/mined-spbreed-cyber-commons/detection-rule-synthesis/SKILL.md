---
name: detection-rule-synthesis
description: >-
  Generate a detection rule from an incident trace and score it against benign
  traffic before it ships. Use after an incident is reconstructed, when turning
  a hunt finding into a standing detection, or when a proposed rule has no
  measured false-positive rate.
allowed-tools: Read, Grep, Glob
---

# The incident tells you what to write; the benign corpus tells you whether to ship it

The fastest source of a good detection is an incident you have just had. The
trap is that **every candidate rule catches the incident** — that is how it was
generated — so catching it cannot be the property you select on.

What separates a rule worth deploying is what it does to traffic that is *not*
the incident.

## When to use this

Immediately after reconstruction, while the trace is still loaded, and again
whenever a hunt hypothesis is promoted. Do not use it to write coverage from
scratch: a rule generated from no incident has nothing to generalise from.

## Step-by-step

**1 — Take the reconstructed trace, not the alert.** The alert is one event;
the rule needs the sequence around it.

**2 — Write more than one candidate, deliberately including a bad one.** The
naive generalisation ("the tool that appeared") and the over-fitted one ("this
booking id") are both worth writing, because seeing them scored is the lesson.

**3 — Assemble a benign corpus that contains the hard cases.** Legitimate
refunds, not just unrelated traffic. A corpus with no near-misses proves
nothing.

**4 — Score every candidate on the benign corpus and record the rate.** Not a
verdict, a number.

**5 — Ship the one that generalises and stays quiet, and say why the others
were rejected.** The rejected candidates are the evidence that the shipped one
was chosen rather than assumed.

## Example

**Input** — a three-step incident and an 84-run benign corpus, in
[`scripts/detection_rule_synthesis.py`](scripts/detection_rule_synthesis.py).

**Output** — a real run:

```
candidate rule                          fires on   FP  FP rate  verdict
any refund                                  True   18     21%  REJECT — buries the queue
refund with no approval in the run          True    0      0%  ship
refund on BK-772                            True    0      0%  REJECT — matches this incident only
```

All three catch the incident. Only one is a detection.

## Output contract

```json
{
  "benign_runs": 0,
  "candidates": [{"rule": "str", "catches_incident": true,
                  "false_positives": 0, "fp_rate": 0.0,
                  "verdict": "ship|REJECT"}]
}
```

## Common edge cases

- **The over-fitted rule scores perfectly.** Zero false positives and zero
  future value. Test for a literal identifier in the rule body.
- **The benign corpus is too easy.** If it contains no legitimate refunds, the
  naive rule looks shippable.
- **The incident is the only positive.** One true positive cannot establish
  recall; the rule's recall is unknown until it runs.

## Failure modes

- **Selecting on "does it catch the incident".** Every candidate does.
- **Shipping without a false-positive number.** That is a guess with syntax.
- **Never writing the bad candidates.** Then nothing shows the good one is good.
