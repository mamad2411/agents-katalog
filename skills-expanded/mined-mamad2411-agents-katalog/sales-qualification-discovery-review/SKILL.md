---
name: sales-qualification-discovery-review
description: Design and audit B2B sales qualification and discovery workflows covering ICP fit, buyer pain, urgency, authority, budget, decision process, procurement path, champion strength, technical fit, risk, no-fit disqualification, mutual action plans, CRM hygiene, and handoff to solution engineering or customer success. Use when agents need to decide whether an opportunity is real and what must be learned next.
---

# Sales Qualification Discovery Review

Use this skill to convert sales qualification, discovery, opportunity fit, decision-process, and mutual action plan questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify segment, ICP, source, buyer role, current trigger, business pain, current workaround, buying committee, timeline, budget, technical constraints, and next decision.
2. Read `references/sales-qualification-discovery-patterns.md`.
3. Classify the account as no-fit, nurture, discovery-needed, qualified opportunity, technical validation, procurement, stalled, or disqualified.
4. Define discovery questions, qualification evidence, red/yellow/green flags, mutual action plan, owner handoffs, CRM fields, and exit criteria.
5. Produce qualification plan, state machine, decision table, event schema, discovery checklist, and follow-up plan.

## Guardrails

- Do not qualify on enthusiasm alone; require problem, impact, decision path, and next commitment evidence.
- Do not force enterprise discovery on low-value self-serve users when product-led routing is better.
- Do not hide no-fit, missing authority, fake urgency, weak pain, or procurement blockers to protect pipeline optics.
- Do not promise product, security, legal, pricing, or implementation commitments outside approved owners.

## Output format

```text
Discovery context:
Audience / source of truth / risk boundary:

Qualification plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Discovery questions, flags, and next commitments:
- <trigger> -> <policy, metric, edge case, support note>
```
