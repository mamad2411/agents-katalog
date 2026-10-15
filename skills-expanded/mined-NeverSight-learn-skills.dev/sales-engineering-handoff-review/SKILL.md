---
name: sales-engineering-handoff-review
description: Design and audit sales engineering handoffs across discovery, demos, proof of concept, solution design, security answers, integration scope, success criteria, technical risks, mutual action plans, implementation notes, customer commitments, CRM fields, and post-sale ownership. Use when pre-sales technical work must become reliable delivery and customer success execution.
---

# Sales Engineering Handoff Review

Use this skill to convert sales engineering handoff, proof of concept, solution design, technical discovery, demo commitment, implementation handoff, and customer success transition questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify customer problem, stakeholders, technical environment, demo or POC scope, success criteria, constraints, commitments, open risks, owner teams, and post-sale timeline.
2. Read `references/sales-engineering-handoff-patterns.md`.
3. Classify the situation as technical discovery, demo follow-up, POC handoff, solution architecture, integration scoping, security/procurement handoff, implementation kickoff, or renewal expansion handoff.
4. Define handoff artifact, accepted commitments, unresolved risks, validation evidence, CRM fields, implementation owner, success metrics, and customer communication.
5. Produce SE handoff plan, state machine, decision table, event schema, technical checklist, commitment ledger, and post-sale owner map.

## Guardrails

- Do not let demo promises become delivery commitments without owner, evidence, and scope.
- Do not hand off a POC as successful unless success criteria and customer validation are explicit.
- Do not hide integration, data, security, or implementation risks in notes no delivery owner will read.
- Do not duplicate CRM, docs, and kickoff truth without a single handoff source of record.

## Output format

```text
Sales engineering context:
Audience / source of truth / risk boundary:

SE handoff plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Commitments, risks, validation, owner map, and post-sale execution:
- <trigger> -> <policy, metric, edge case, support note>
```
