---
name: admin-delegation-boundary-review
description: Design and audit admin delegation boundaries for enterprise SaaS and marketplace products covering delegated admin roles, tenant hierarchy, scoped permissions, inherited access, approval chains, impersonation, break-glass, support handoff, audit logs, separation of duties, customer-visible controls, and privilege drift. Use when products need safe delegated administration without creating shadow superusers.
---

# Admin Delegation Boundary Review

Use this skill to convert admin delegation, delegated tenant admin, org hierarchy, scoped permissions, inherited access, support handoff, impersonation, break-glass, separation of duties, and customer-admin boundary questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify tenant hierarchy, admin personas, delegated scopes, inherited permissions, approval chains, source of truth, support override path, sensitive actions, audit evidence, recovery route, and customer-visible controls.
2. Read `references/admin-delegation-boundary-patterns.md`.
3. Classify the situation as new delegated admin model, enterprise tenant hierarchy, marketplace seller admin, reseller-managed account, support-assisted administration, break-glass path, merger/org split, or privilege-drift remediation.
4. Define delegation boundary, role/scope matrix, approval ladder, sensitive-action gates, inherited-access rules, support handoff, impersonation controls, audit events, drift review, and customer-admin UX.
5. Produce delegated admin boundary review, state machine, decision table, event schema, scope matrix, escalation path, and remediation plan.

## Guardrails

- Do not let delegated admin roles become hidden superuser roles without scope, expiry, or audit evidence.
- Do not mix customer-admin delegation, internal support access, reseller access, and break-glass access into one permission path.
- Do not expose internal policy details in customer UI, but do show what a delegated admin can affect and how to recover.
- Do not approve inherited access without drift detection, owner transfer, and revocation paths.

## Output format

```text
Admin delegation context:
Audience / source of truth / risk boundary:

Delegation boundary plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Scopes, approval chains, sensitive actions, support access, audit logs, and drift controls:
- <trigger> -> <policy, metric, edge case, support note>
```
