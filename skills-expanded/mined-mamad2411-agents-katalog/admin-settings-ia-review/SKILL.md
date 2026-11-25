---
name: admin-settings-ia-review
description: Design and audit admin settings information architecture, workspace controls, role and permission settings, billing/admin separation, security settings, defaults, auditability, dangerous actions, policy inheritance, team management, and enterprise admin UX. Use when building settings for SaaS, developer tools, marketplaces, desktop apps, or multi-user products.
---

# Admin Settings IA Review

Use this skill to convert a high-stakes product decision into a concrete, measurable, reviewable operating artifact.

## Workflow

1. Inventory settings by actor, scope, permission, risk, frequency, dependency, and audit need.
2. Read `references/admin-settings-ia-patterns.md`.
3. Group settings by user mental model: account, workspace, members, billing, security, integrations, data, notifications, support.
4. Map dangerous actions, defaults, role gates, confirmation, recovery, and audit logs.
5. Produce IA map, permission matrix, state flow, empty/error states, and instrumentation plan.

## Guardrails

- Do not bury destructive or security-critical controls behind ambiguous labels.
- Do not let billing admins silently become security or data admins unless intended.
- Avoid settings that depend on tribal knowledge, support-only changes, or hidden defaults.
- Every dangerous action needs confirmation, consequence copy, permission check, and recovery path where possible.

## Output format

```text
Settings context:
Actors / scopes / risk:

IA map:
- <section>
  - <setting> -> <owner, scope, permission, default, audit>

Permission matrix:
| Setting | Viewer | Editor | Approver | Audit event | Recovery |
| --- | --- | --- | --- | --- | --- |

Risk review:
- <dangerous action> -> <confirmation/recovery/support>
```
