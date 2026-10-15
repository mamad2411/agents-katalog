---
name: risk-register-governance-review
description: Design and audit product risk registers, decision governance, mitigation ownership, severity/likelihood scoring, control evidence, review cadence, triggers, assumptions, dependencies, AI/safety risk, commercial risk, operational risk, privacy/security risk, and acceptance decisions. Use when a product team needs to track and reduce material risk instead of relying on scattered notes.
---

# Risk Register Governance Review

Use this skill to convert a risk register governance, mitigations, control evidence, owners, triggers, review cadence, and acceptance decisions question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify product decision, risk domains, stakeholders, owner, customer impact, regulatory/security sensitivity, and time horizon.
2. Read `references/risk-register-governance-patterns.md`.
3. Classify risks across product, market, technical, operational, security/privacy, legal/compliance, trust/safety, AI, revenue, and support.
4. Define severity, likelihood, detectability, controls, mitigations, owner, trigger, review cadence, residual risk, and acceptance authority.
5. Produce risk register, state machine, decision table, event schema, governance cadence, and escalation checklist.

## Guardrails

- Do not label risk “accepted” without owner, rationale, expiry/review date, and residual impact.
- Do not mix assumptions, issues, incidents, decisions, and risks without clear states.
- Do not bury security, privacy, billing, or safety risks in generic product notes.
- Do not use risk scoring that cannot change a concrete decision or mitigation.

## Output format

```text
Risk context:
Decision / domain / customer impact / time horizon:

Risk register:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Controls and mitigations:
- <item> -> <policy, metric, edge case, support note>

Governance and escalation:
- <trigger> -> <action, communication, owner>
```
