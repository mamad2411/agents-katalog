---
name: investigation-admission-rules
description: >-
  Decide and enforce which sources, fields and volumes an investigating agent
  may reach, before the investigation starts, and record every refusal. Use when
  granting an agent read access for incident response, when investigation
  queries touch personal data, or when an investigation's own access needs to be
  auditable.
allowed-tools: Read, Grep, Glob
---

# The investigation is the second-largest access grant in the incident

An investigating agent is handed broad read across the estate so it can find
the problem. Broad read across the estate is frequently what the problem *was*.

Admission rules decide, per investigation class and before anything runs, which
sources it may reach, which fields it may never see, and how much it may pull.

## When to use this

Before an agent-driven investigation touches production data, and whenever an
investigation class is defined. Also after the fact: the refusal log is the
evidence that the response did not become its own incident.

## Step-by-step

**1 — Classify the investigation first.** "Agent misuse" and "data exfiltration"
need different sources. One admission set for everything is no admission set.

**2 — Name the sources positively.** An allowlist. A denylist of sources is a
list of the ones somebody thought of.

**3 — Deny fields, not just sources.** The trace table is admissible; the
message body inside it usually is not.

**4 — Cap the volume.** The same query over the same fields is an investigation
at 400 rows and a copy at 90,000.

**5 — Record refusals as evidence, not errors.** A refusal carries the exact
query, so a human can grant it deliberately.

## Example

**Input** — one admission set and six queries, in
[`scripts/investigation_admission_rules.py`](scripts/investigation_admission_rules.py).

**Output** — the refusals from a real run:

```
bookings.db     owner_id,payment_card                8000  REFUSE — source not admitted for this class
agent.traces    agent,message_body                    900  REFUSE — denied field: message_body
gateway.logs    src,route                           90000  REFUSE — 90000 rows exceeds the 5000 cap
```

The third is refused on volume alone — same source, same fields as an allowed
query.

## Output contract

```json
{
  "allowed": [{"source": "str", "fields": ["str"], "rows": 0, "why": null}],
  "refused": [{"source": "str", "fields": ["str"], "rows": 0, "why": "str"}]
}
```

## Common edge cases

- **The agent needs the denied field to answer.** Then a human grants it, on
  the record — which is the outcome, not a failure of the rule.
- **Volume caps break a legitimate sweep.** Raise the cap for that class
  explicitly rather than removing it.
- **A source is admitted but joins to one that is not.** Enforce at the tool
  boundary, not on the query text.

## Failure modes

- **Granting once, broadly, "for the duration".** The duration is when the
  access is least supervised.
- **Silent drops.** A refusal nobody sees is indistinguishable from no data.
- **Rules written after the first investigation.** They will be written to
  permit whatever that one did.
