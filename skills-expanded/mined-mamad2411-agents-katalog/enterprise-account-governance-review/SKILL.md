---
name: enterprise-account-governance-review
description: Design and audit enterprise account governance across tenants, workspaces, admins, roles, delegated administration, SSO, SCIM, domains, account ownership, billing ownership, support access, audit logs, data boundaries, merger or divestiture changes, and break-glass controls. Use when enterprise accounts need safe ownership and administrative control.
---

# Enterprise Account Governance Review

Use this skill to convert enterprise account governance, tenant ownership, admin role, delegated administration, SSO, SCIM, billing owner, and support-access questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify account model, tenant hierarchy, admins, owners, domains, SSO/SCIM source, billing owner, support access, audit requirements, data boundary, and exception path.
2. Read `references/enterprise-account-governance-patterns.md`.
3. Classify the situation as new enterprise account, delegated admin rollout, domain claim, tenant split, tenant merge, ownership transfer, support impersonation, break-glass access, or offboarding.
4. Define source of truth, role model, approval gates, audit events, support boundaries, recovery path, customer communication, and periodic access review.
5. Produce account governance plan, state machine, decision table, event schema, admin checklist, support boundary, and exception register.

## Guardrails

- Do not grant enterprise admin or support access without source-of-truth ownership, auditability, expiry, and revocation.
- Do not merge or split tenant data without domain, billing, legal, and customer admin approval.
- Do not let sales, support, or implementation teams redefine account ownership outside the governance model.
- Do not treat SSO or SCIM setup as proof that account ownership and data boundaries are correct.

## Output format

```text
Enterprise account context:
Audience / source of truth / risk boundary:

Account governance plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Ownership, roles, data boundaries, support access, audit, and exceptions:
- <trigger> -> <policy, metric, edge case, support note>
```
