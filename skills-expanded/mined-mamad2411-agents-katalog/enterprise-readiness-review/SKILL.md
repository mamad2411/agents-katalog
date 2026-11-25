---
name: enterprise-readiness-review
description: Audit and design enterprise readiness across security review, SSO, SCIM, RBAC, audit logs, admin controls, procurement, legal, privacy, compliance evidence, SLA/support, implementation, pilot, rollout, and expansion. Use when selling SaaS, developer tools, marketplaces, or platforms to larger organizations or preparing an enterprise plan.
---

# Enterprise Readiness Review

Use this skill to turn a recurring product-operations problem into a concrete, reviewable artifact instead of generic advice.

## Workflow

1. Identify buyer, champion, economic owner, IT/security reviewer, deployment model, data sensitivity, and contract motion.
2. Read `references/enterprise-readiness-patterns.md`.
3. Map enterprise asks into security/trust, identity/admin, legal/procurement, support/SLA, implementation, and product gaps.
4. Separate launch blockers from sales-enablement evidence and premium-plan polish.
5. Produce readiness matrix, risk register, sales proof pack, and rollout plan.

## Guardrails

- Do not promise certifications, compliance, SLAs, or data residency that do not exist.
- Do not build enterprise features without a buyer/problem/use-case map.
- Separate security evidence from marketing claims.
- Escalate legal, regulatory, and contractual obligations to qualified owners.

## Output format

```text
Enterprise context:
Buyer / reviewer / data sensitivity:

Readiness matrix:
| Area | Current proof | Gap | Buyer impact | Priority | Owner |
| --- | --- | --- | --- | --- | --- |

Blockers vs polish:
- Blocker:
- Sales enablement:
- Future plan:

Pilot / rollout plan:
- <step, proof, gate>
```
