---
name: support-deflection-knowledge-base-review
description: Design and audit support deflection, knowledge bases, help-center search, article quality, macros, chatbots, in-product help, diagnostics, escalation paths, unresolved-user recovery, support analytics, and product feedback loops. Use when reducing tickets while preserving customer trust and fast human help for high-stakes issues.
---

# Support Deflection Knowledge Base Review

Use this skill to convert a support deflection, knowledge base quality, help search, chatbot/macros, escalation, and unresolved-user recovery question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify top contact drivers, user stakes, self-service surfaces, article owners, search quality, escalation promise, and risk of trapping users.
2. Read `references/support-deflection-knowledge-base-patterns.md`.
3. Classify deflection target: how-to, troubleshooting, billing/refund, account access, bug/incident, policy, integration, or product education.
4. Define content IA, search terms, article quality, diagnostics, macro/chatbot boundaries, escalation triggers, measurement, and product feedback loop.
5. Produce support deflection plan, state machine, decision table, event schema, article QA checklist, and escalation policy.

## Guardrails

- Do not celebrate deflection rate if unresolved users churn, complain, refund, or recontact.
- Do not block human escalation for billing, account access, safety, privacy, payment, or incident issues.
- Do not let AI/chatbot answers outrank verified policy or current incident status.
- Do not create duplicate stale help articles without ownership and refresh cadence.

## Output format

```text
Support context:
Contact driver / user stakes / escalation promise:

Deflection plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Articles, search, and automation:
- <item> -> <policy, metric, edge case, support note>

Escalation and feedback loop:
- <trigger> -> <action, communication, owner>
```
