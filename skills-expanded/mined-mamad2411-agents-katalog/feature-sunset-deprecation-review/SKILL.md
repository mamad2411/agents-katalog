---
name: feature-sunset-deprecation-review
description: Design and audit feature sunsets, API deprecations, plan removals, integration shutdowns, legacy workflow retirement, game event closure, migration alternatives, usage analysis, customer communication, contract exceptions, support readiness, kill dates, and post-sunset cleanup. Use when removing or materially changing a product capability without breaking trust.
---

# Feature Sunset Deprecation Review

Use this skill to convert a feature sunset, deprecation, migration alternatives, customer communication, support readiness, and cleanup question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify feature owner, dependency map, active usage, customer segments, contractual commitments, replacement path, and shutdown reason.
2. Read `references/feature-sunset-deprecation-patterns.md`.
3. Classify sunset type: UI feature, API version, pricing plan, integration, platform support, data format, workflow, or time-limited game/live feature.
4. Define usage thresholds, notice timeline, migration tooling, exceptions, support playbook, kill switch, and cleanup verification.
5. Produce deprecation plan, state machine, customer decision table, event schema, comms checklist, and rollback/extension criteria.

## Guardrails

- Do not remove a used capability without usage readback, impacted account list, migration path, and support owner.
- Do not rely on one generic changelog entry for high-impact or contract-bound customers.
- Do not keep deprecated features alive indefinitely without explicit owner, cost, risk, and exception expiry.
- Do not delete customer data, integrations, exports, or audit evidence before retention and legal obligations are checked.

## Output format

```text
Sunset context:
Capability / users impacted / commitments:

Deprecation plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Migration and communication:
- <item> -> <policy, metric, edge case, support note>

Extension and cleanup criteria:
- <trigger> -> <action, communication, owner>
```
