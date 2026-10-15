---
name: procurement-security-review
description: Design and audit enterprise procurement security review readiness, vendor risk questionnaires, security evidence packets, DPAs, subprocessors, insurance, policies, SOC/ISO evidence, pen test summaries, AI/data-use answers, redlines, gap handling, and sales/legal/security handoff. Use when deals stall on vendor review or buyer assurance.
---

# Procurement Security Review

Use this skill to convert a enterprise procurement security, vendor-risk evidence, questionnaires, DPAs, policy proof, and sales/legal/security handoff question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify buyer type, deal stage, requested evidence, data sensitivity, contract terms, compliance status, gaps, owner teams, and response deadline.
2. Read `references/procurement-security-patterns.md`.
3. Classify request as questionnaire, evidence packet, DPA, subprocessor review, insurance, compliance report, pen test summary, AI/data-use review, or redline.
4. Define evidence source, approved answer, gap wording, exception path, access control, reviewer, expiry, and sales/legal/security handoff.
5. Produce procurement review plan, state machine, decision table, event schema, evidence checklist, and gap-escalation policy.

## Guardrails

- Do not answer “yes” to controls that are planned, partial, customer-specific, or not evidenced.
- Do not send SOC reports, pen tests, customer data, architecture secrets, or insurance documents without access control and approval.
- Do not let sales invent security/compliance commitments to unblock a deal.
- Do not lose track of redlines, exceptions, and promised remediation dates after signature.

## Output format

```text
Procurement context:
Buyer / evidence / data sensitivity / deadline:

Procurement security response plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Evidence, answers, and gaps:
- <item> -> <policy, metric, edge case, support note>

Exception and post-signature tracking:
- <trigger> -> <action, communication, owner>
```
