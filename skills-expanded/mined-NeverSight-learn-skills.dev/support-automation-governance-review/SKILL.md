---
name: support-automation-governance-review
description: Design and audit support automation governance for chatbots, macros, AI copilots, routing, triage, deflection, knowledge retrieval, human escalation, confidence thresholds, source freshness, refund or account actions, QA, privacy, analytics, and customer trust. Use when automating support without trapping users or creating unsafe actions.
---

# Support Automation Governance Review

Use this skill to convert support automation, chatbot, macro, AI copilot, deflection, routing, human escalation, support QA, and automation policy questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify contact drivers, automation surface, source content, action authority, confidence threshold, escalation path, privacy risk, QA owner, and success metric.
2. Read `references/support-automation-governance-patterns.md`.
3. Classify the situation as routing automation, macro suggestion, self-serve deflection, AI answer, account action, refund action, incident triage, abuse triage, or agent-assist workflow.
4. Define allowed actions, source grounding, escalation triggers, confidence thresholds, QA sampling, rollback, analytics, customer messaging, and product feedback loop.
5. Produce support automation governance plan, state machine, decision table, event schema, QA checklist, escalation ladder, and rollback plan.

## Guardrails

- Do not optimize deflection while hiding unresolved contacts, churn, refunds, or safety issues.
- Do not allow automation to perform account, billing, refund, deletion, or security actions without authority and audit controls.
- Do not answer from stale, uncited, or conflicting knowledge sources when stakes are high.
- Do not remove human escalation for confused, angry, vulnerable, high-value, or policy-sensitive users.

## Output format

```text
Support automation context:
Audience / source of truth / risk boundary:

Automation governance plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Allowed actions, confidence, sources, escalation, QA, analytics, and rollback:
- <trigger> -> <policy, metric, edge case, support note>
```
