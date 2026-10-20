---
name: audit-answerability-check
description: >-
  Put an investigation's three questions to an existing agent log — which human,
  what motivated the action, which hop originated it — and record which of them
  the record cannot answer. Use when reviewing agent telemetry before an
  incident rather than during one.
allowed-tools: Read, Grep, Glob
---

# A complete log that answers nothing

Agent logs are usually complete in the sense that every tool call is present.
They are useless in the sense that the three questions an investigation opens
with have no fields behind them. The check is not "are we logging" — it is
"which question dies here".

## When to use this

Before an incident. Run it against a real log line from production, not against
the logging design.

## Procedure

**1 — Take one real record.** A single tool-call row, with every field it
actually carries. Not the schema — the row.

**2 — Ask: which human?** Is there a field naming the principal on whose behalf
this ran? An agent identity is not an answer; it is the thing that ran.

**3 — Ask: what motivated it?** Which input caused this call — the user's
request, a retrieved document, a tool result, a memory record. Without it you
cannot tell an instructed action from an injected one, and that is the
distinction the whole investigation turns on.

**4 — Ask: which hop originated it?** In any multi-agent or delegated flow,
which agent started the chain. A chain reconstructed by correlating timestamps
across four services is a chain you will not reconstruct at 2am.

**5 — Report per question, with the field that would answer it.** Three rows.
Each says: answerable yes/no, and the field to add. Anything vaguer produces a
logging project rather than a fix.

## Example

**Input** — the fixture committed at the top of [`scripts/audit_answerability_check.py`](scripts/audit_answerability_check.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
the log you have:
   09:14:02  agent-svc search      {'q': 'invoice 8812'}
   09:14:07  agent-svc fetch_doc   {'id': 'wiki/473'}
   09:14:11  agent-svc run_query   {'sql': 'DELETE FROM invoices WHERE id=8812'}
   09:14:12  agent-svc send_email  {'to': 'ops@corp.example'}

question                                    field needed        present?
which user caused the deletion?             principal           NO
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
  "record": {"fields": ["str"]},
  "questions": [{"question": "which human|what motivated|which hop", "answerable": false, "missing_field": "str"}],
  "answerable_count": 0,
  "reconstruction": {"possible": false, "requires_correlating": ["str"]}
}
```

## Failure modes

- **Checking the schema.** Fields exist in schemas and are null in rows.
- **Accepting the agent identity as the principal.** It answers "what", never
  "who".
- **Recording "add more logging".** Name the three fields or nothing changes.
