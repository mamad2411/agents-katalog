---
name: detection-triage
description: >-
  Triage security alerts with the context needed to reach a defensible verdict,
  and sample what is auto-closed so the closing rule stays honest. Use when
  working an alert queue, deciding whether an alert is a true positive, tuning
  a noisy detection, or designing automated alert handling.
allowed-tools: Read, Grep, Bash
---

# Alert triage with context

An analyst reading an alert in isolation is guessing. The verdict comes from
the alert **plus** the context that makes it normal or abnormal, and most
triage automation fails because it automated the guess instead of the context.

## When to use this

Working an alert queue, building an auto-close rule, or reviewing why a
detection produces verdicts nobody trusts.

## Procedure

**1 — Gather the context before judging.** For every alert, assemble:

- **asset** — what it is, who owns it, how exposed it is
- **identity** — human or workload, and its normal behaviour
- **history** — has this fired before on this asset, and how was it resolved
- **change** — was there a deploy, a migration, a new agent, in the window
- **peers** — did the same thing fire elsewhere at the same time

A verdict issued without `history` will re-litigate a decision the team already
made, which is the most common way triage automation loses trust.

**2 — Reach a verdict, with the reason.** One of `true_positive`,
`false_positive`, `benign_true_positive` (it really happened and it is fine),
or `needs_human`. Record which context field decided it. "Benign true positive"
is a distinct category and collapsing it into false-positive corrupts every
tuning decision made from the data afterwards.

**3 — Attach confidence, and let it gate automation.** Only high-confidence
verdicts may auto-close. Everything else queues.

**4 — Sample the auto-closed.** Automation that closes alerts must be audited
by re-opening a fraction of them for human review. This is the control that
catches a closing rule that has quietly started closing real incidents.

Seed the sampler from something **stable** — a checksum of the alert id, never
`hash()`, which Python randomises per process. A sampling rule that picks a
different subset every run cannot be audited, because you cannot tell whether a
change in findings came from the rule or from the dice.

**5 — Feed tuning from verdicts, not volume.** A detection is noisy if its
false-positive rate is high, not if it fires often. Rank tuning candidates by
`false_positive_rate × volume`, with a full tiebreak so the list is stable
between runs.

## Example

**Input** — the fixture committed at the top of [`scripts/detection_triage.py`](scripts/detection_triage.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
BARE ALERT (what most SOCs receive):
   patch-agent read /vault/.env
   rotator-agent read /vault/.env
   → identical. An analyst cannot tell these apart.

ENRICHED ALERT:
   actor        patch-agent
   on behalf of dana@corp
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
  "triaged": [
    {"alert_id": "str", "verdict": "true_positive|false_positive|benign_true_positive|needs_human",
     "deciding_context": "asset|identity|history|change|peers",
     "reason": "str", "confidence": 0.0,
     "auto_closed": false, "sampled_for_review": false}
  ],
  "sampling": {"rate": 0.0, "seed_source": "str", "reviewed": 0, "disagreements": 0},
  "tuning": [{"rule": "str", "fp_rate": 0.0, "volume": 0, "priority": 0.0}]
}
```

`disagreements` is the number that matters: it is the measured error rate of
the automation, and it belongs in every report about it.

## Failure modes

- **Auto-closing without sampling.** The rule then has no error bar and no way
  to acquire one.
- **Seeding the sampler from `hash()`.** Non-reproducible sampling is not a
  control.
- **Folding benign-true-positive into false-positive.** It teaches the tuner to
  suppress a working detection.
- **Removing `needs_human`.** Forced verdicts under uncertainty are how a queue
  becomes an incident.
