---
name: handoff-delivery-check
description: >-
  Trace each joint runbook from the function that owns it to the function that
  consumes it, and find the handoffs that were agreed and never actually
  delivered. Use when two teams both believe the other has something.
allowed-tools: Read, Grep, Glob
---

# Agreed, documented, never delivered

A joint runbook has an owner and a consumer, and closing the seam between two
functions means the consumer actually receives the artefact. The common failure
is that everyone agrees the handoff exists, the runbook says so, and nothing has
ever been sent — which is invisible until somebody asks the consumer.

## When to use this

After designing cross-functional runbooks, and periodically — this decays.

## Procedure

**1 — List the joint runbooks.** For each: the owning function, the consuming
function, the artefact, and the trigger that should produce it.

**2 — Ask the consumer, not the owner.** "Have you received this, and when?"
Owners report intent accurately and delivery optimistically. The consumer's
answer is the measurement.

**3 — Record the consequence of each undelivered handoff.** Model risk never
receiving the privacy assessment means the tier is computed without a data
input. Name the specific consequence, not "reduced coverage".

**4 — Check the trigger, not the document.** A handoff triggered by a person
remembering is not a handoff. Look for the mechanism: a ticket transition, a
pipeline step, a scheduled export.

**5 — Close by making the trigger automatic or naming a date.** Anything else
recreates the same state, and the check will find it again next time.

## Example

**Input** — the fixture committed at the top of [`scripts/handoff_delivery_check.py`](scripts/handoff_delivery_check.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
MRM validation -> security evidence
   artefact  : validation report with tool surface and autonomy
   owner     : model_risk
   consumers : cyber, compliance, internal_audit

legal position -> system prompt
   artefact  : approved language and refusal set
   owner     : legal
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
  "runbooks": [{"name": "str", "owner": "str", "consumer": "str", "artefact": "str",
                "trigger": "str", "trigger_automatic": false}],
  "delivery": [{"runbook": "str", "consumer_confirms": false, "last_received": "str|null"}],
  "undelivered": [{"runbook": "str", "consequence": "str"}],
  "closure": [{"runbook": "str", "action": "automate|scheduled", "due": "str"}]
}
```

## Failure modes

- **Asking the owner.** They will describe the design.
- **Accepting the runbook as evidence.** It is the agreement, not the delivery.
- **A human-memory trigger.** It works until the person changes role.
