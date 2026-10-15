---
name: customer-feedback-intake-review
description: Design and audit customer feedback intake across support tickets, sales calls, app reviews, surveys, NPS, communities, cancellation reasons, feature requests, bug reports, and product analytics. Use when teams need to turn noisy feedback into evidence, prioritization input, roadmap decisions, and customer follow-up without overreacting to anecdotes.
---

# Customer Feedback Intake Review

Use this skill to convert a customer feedback intake, dedupe, routing, prioritization evidence, roadmap loops, and close-the-loop communication question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify feedback sources, customer segments, revenue/user impact, product area, owner, decision cadence, and follow-up promise.
2. Read `references/customer-feedback-intake-patterns.md`.
3. Classify feedback as bug, usability friction, feature request, pricing objection, churn reason, praise, risk signal, or research lead.
4. Define intake fields, taxonomy, dedupe, severity, evidence score, routing, prioritization handoff, and close-the-loop workflow.
5. Produce feedback state machine, signal decision table, event schema, triage checklist, and anti-anecdote guardrails.

## Guardrails

- Do not let loudness, logo size, or recency become the only priority signal.
- Do not promise delivery dates from intake unless roadmap owners explicitly commit.
- Do not merge bugs, support confusion, feature requests, and churn reasons into one undifferentiated backlog.
- Do not store sensitive customer comments without redaction, consent, and access control.

## Output format

```text
Feedback context:
Source / segment / product area / promise:

Feedback system:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Taxonomy and evidence:
- <item> -> <policy, metric, edge case, support note>

Close-the-loop and governance:
- <trigger> -> <action, communication, owner>
```
