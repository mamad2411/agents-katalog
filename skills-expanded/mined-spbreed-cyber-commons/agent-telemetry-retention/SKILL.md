---
name: agent-telemetry-retention
description: >-
  Scan an agent's run record for sensitive content it read legitimately, then
  set retention per field rather than per record so the investigable parts
  survive and the prompts do not. Use when agent telemetry is being kept,
  discarded, or argued about with privacy.
allowed-tools: Read, Grep, Glob
---

# The agent read a card number because you asked it to

An agent run record is the richest telemetry in the estate and the most
dangerous to keep whole. The content it read — source files, tickets, documents
— lands in the record, so the record inherits every classification the source
had. Per-record retention forces a choice between losing the investigation and
keeping the data; per-field does not.

## When to use this

Before agent telemetry is retained at scale, and whenever a retention policy is
being written by someone who has not read a run record.

## Procedure

**1 — Read one full record.** Every step, every field. This is the step people
skip, and it is where the payment-card pattern in a legitimately-read source
file turns up.

**2 — Scan for sensitive patterns across all fields.** Card numbers, keys,
personal data, health terms. Record which field carried each hit — prompts and
tool results are the usual answer.

**3 — Classify fields by investigative value.** Timestamps, tool name, target
and verifier verdict answer most investigation questions. Prompts and raw tool
output answer few and carry most of the risk.

**4 — Set retention per field.** Long for the structural fields, short for the
content ones. Then age a record and check what an investigation could still do
with it — that check is what makes the policy defensible.

**5 — State what is lost.** A short prompt retention means you cannot re-derive
motivation after that window. Say so, rather than discovering it in an incident.

## Example

**Input** — the fixture committed at the top of [`scripts/agent_telemetry_retention.py`](scripts/agent_telemetry_retention.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
full record (everything the harness saw):
    {'n': 1, 'tool': 'read_file', 'target': '/work/repo/billing.py', 'verifier': 'n/a', 'ok': True, 'prompt': 'Investigate finding SEC-4471 in billing.py', 'result': 'def charge(card_number, amount):  # card_number = 4111111111111111'}
    {'n': 2, 'tool': 'search_code', 'target': 'charge(', 'verifier': 'n/a', 'ok': True, 'prompt': 'find callers of charge()', 'result': 'api/checkout.py:88 charge(user.card, total)'}
    {'n': 3, 'tool': 'write_file', 'target': '/work/repo/billing.py', 'verifier': 'tests pass', 'ok': True, 'prompt': 'apply the fix', 'result': 'patch applied'}
sensitive content found in the trace:
   step 1  result   payment card

Nobody put a card number in the trace deliberately. The agent read a
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
  "record": {"steps": 0, "fields": ["str"]},
  "scan": [{"pattern": "str", "field": "str", "legitimate_source": "str"}],
  "retention": [{"field": "str", "days": 0, "investigative_value": "high|low"}],
  "aged_record": {"age_days": 0, "questions_still_answerable": ["str"], "lost": ["str"]}
}
```

## Failure modes

- **Retaining or discarding whole records.** Both answers are wrong.
- **Scanning prompts only.** Tool results carry the same content.
- **Not stating what the short windows lose.** That is the trade being made.
