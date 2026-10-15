---
name: security-questionnaire-response-review
description: Prepare and review security questionnaire responses, trust center answers, vendor risk evidence, enterprise buyer security packets, control mappings, gaps, remediation notes, and truthful sales handoffs. Use when responding to customer security reviews, procurement questionnaires, SSO/audit/data questions, privacy evidence requests, or enterprise trust due diligence.
---

# Security Questionnaire Response Review

Use this skill to convert a high-stakes product decision into a concrete, measurable, reviewable operating artifact.

## Workflow

1. Identify buyer, questionnaire source, requested controls, data sensitivity, product scope, answer owner, and evidence source.
2. Read `references/security-questionnaire-patterns.md`.
3. Classify each question: implemented control, partially implemented, not applicable, roadmap, unknown, or requires legal/security review.
4. Attach evidence, caveats, commitments, reviewer, expiry, and follow-up owner for every material answer.
5. Produce response table, evidence pack, gap register, sales-safe summary, and escalation list.

## Guardrails

- Do not invent certifications, penetration tests, controls, SLAs, data residency, subprocessors, or compliance status.
- Do not answer legal, regulatory, or contractual commitments without the accountable owner.
- Separate current fact, compensating control, roadmap intent, and open gap.
- Redact secrets, internal vulnerabilities, customer data, and sensitive architecture details.

## Output format

```text
Questionnaire context:
Buyer / scope / sensitivity:

Response table:
| Question | Classification | Answer | Evidence | Caveat | Owner |
| --- | --- | --- | --- | --- | --- |

Gap register:
- <gap> -> <risk, compensating control, owner, target>

Sales-safe summary:
- <what can be said now / what needs follow-up>
```
