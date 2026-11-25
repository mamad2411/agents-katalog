---
name: data-subject-request-ops-review
description: Design and audit data subject request operations for access, export, correction, deletion, restriction, objection, consent withdrawal, identity verification, authorized agents, minors, workspace data, legal holds, retention exceptions, subprocessors, SLAs, proof packages, and audit trails. Use when privacy requests need reliable operational handling across product systems.
---

# Data Subject Request Ops Review

Use this skill to convert DSAR, access, export, correction, deletion, consent withdrawal, identity verification, legal hold, subprocessor, and privacy SLA questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify request type, jurisdiction, data subject, account/workspace scope, identity proof, authorized agent status, systems touched, retention/legal exceptions, SLA deadline, and communication owner.
2. Read `references/data-subject-request-ops-patterns.md`.
3. Classify the situation as access/export, correction, deletion, restriction, objection, consent withdrawal, portability, authorized-agent request, minor request, or escalated/legal-hold request.
4. Define verification, scope resolution, system inventory, execution order, exception handling, subprocessor workflow, response package, audit evidence, and SLA monitoring.
5. Produce DSAR operating plan, state machine, decision table, event schema, request checklist, evidence package, and escalation map.

## Guardrails

- Do not fulfill irreversible requests without identity, authority, scope, and legal-hold checks.
- Do not promise deletion or export coverage for unmapped backups, logs, analytics, support tools, or subprocessors.
- Do not disclose workspace, admin, billing, security, or third-party data to the wrong subject.
- Do not let privacy request status live only in tickets without auditable events and deadlines.

## Output format

```text
Data subject request context:
Audience / source of truth / risk boundary:

DSAR operations plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Verification, scope, systems, exceptions, response, and audit proof:
- <trigger> -> <policy, metric, edge case, support note>
```
