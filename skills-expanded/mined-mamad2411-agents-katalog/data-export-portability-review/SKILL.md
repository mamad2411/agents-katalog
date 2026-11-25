---
name: data-export-portability-review
description: Design and audit data export, portability, backup handoff, account deletion, workspace offboarding, migration, machine-readable formats, admin exports, and user trust flows for SaaS, apps, marketplaces, games, and desktop software. Use when users need to export, move, delete, restore, or leave with their data safely.
---

# Data Export Portability Review

Use this skill to turn a recurring product-operations problem into a concrete, reviewable artifact instead of generic advice.

## Workflow

1. Identify requester, data owner, scope, authority, sensitivity, size, format, retention, and destination.
2. Read `references/data-portability-patterns.md`.
3. Map request, authorization, export generation, delivery, expiration, deletion/retention exceptions, and support review.
4. Separate user export, admin export, backup restore, migration, account deletion, and legal/privacy requests.
5. Produce a portability flow, schema plan, support copy, risk controls, and event schema.

## Guardrails

- Do not export secrets, third-party private data, or other users’ data without authority.
- Do not make deletion promises that backups, legal holds, billing records, or fraud evidence cannot satisfy.
- Prefer machine-readable stable formats plus human-readable summaries where useful.
- Escalate jurisdiction-specific privacy/legal requests to qualified owners.

## Output format

```text
Portability context:
Requester / scope / sensitivity:

Flow:
- <request state> -> <authorization/export/delivery/support action>

Data package plan:
| Data class | Format | Included | Excluded | Retention/deletion note |
| --- | --- | --- | --- | --- |

Risks and support copy:
- <risk/control/message>
```
