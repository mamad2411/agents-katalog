---
name: trace-personal-data-audit
description: >-
  Find personal data that nobody deliberately placed in an agent trace, and run
  an erasure request through every system that holds a copy. Use when agent
  telemetry meets data protection, or before a subject access request arrives.
allowed-tools: Read, Grep, Glob
---

# Nobody put it there, and it is there

An agent trace accumulates personal data as a side effect: a name in a ticket, an
email in a tool result, an account number in a document it read, a card number
in a file it was asked to fix. None of it was placed deliberately, all of it is
personal data, and it is copied into every system the trace is shipped to.

## When to use this

Before agent telemetry is retained or exported, and before the first erasure
request rather than during it.

## Procedure

**1 — Run detectors over the whole trace.** Every field, every step. Names,
emails, account and card numbers, health terms. Record which step introduced
each, because that tells you whether it is preventable.

**2 — Map every system that holds a copy.** The trace store, the SIEM, the
warehouse, backups, and any vendor it is exported to. This list is the erasure
surface and it is longer than the trace store.

**3 — Run a real erasure request end to end.** Locate every copy for one
subject, delete, and verify. Systems that cannot delete a single subject's
records — append-only stores, immutable backups, aggregate indexes — are the
finding.

**4 — Say what is legitimately retained and why.** Some copies survive erasure
lawfully. Naming the basis, per system, is the difference between a defensible
position and a gap.

**5 — Reduce at source.** Redaction at write time is cheaper than erasure across
six systems. Say which detector should run before the trace is stored.

## Example

**Input** — the fixture committed at the top of [`scripts/trace_personal_data_audit.py`](scripts/trace_personal_data_audit.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
personal data present in the agent trace:
   step 1  email           dana.okonkwo@example.com
   step 1  payment card    4111111111111111
   step 1  account number  acct 8812
   step 1  name            J. Okonkwo

4 items. Nobody put them there deliberately — the agent read
a support ticket, which is exactly what it was asked to do.
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
  "trace": {"steps": 0},
  "detections": [{"kind": "str", "field": "str", "step": 0, "deliberate": false}],
  "systems": [{"name": "str", "holds_copy": true, "can_delete_subject": false}],
  "erasure": {"subject": "str", "located": 0, "deleted": 0, "failed_in": ["str"]},
  "retained_lawfully": [{"system": "str", "basis": "str"}],
  "redaction_at_source": ["str"]
}
```

## Failure modes

- **Auditing the trace store only.** The copies are the problem.
- **Assuming erasure works.** Run one and find out.
- **Reporting failures without the lawful retentions.** Half the list is fine
  and the report loses credibility without saying so.
