---
name: api-versioning-deprecation-review
description: Design and audit API versioning and deprecation programs covering breaking-change policy, semantic versions, compatibility, SDKs, docs, changelogs, migration guides, sunset timelines, usage analytics, customer notifications, exceptions, webhooks, schema changes, test fixtures, and support readiness. Use when public APIs or integrations need safe evolution.
---

# API Versioning Deprecation Review

Use this skill to convert API versioning, deprecation, breaking change, SDK, migration, changelog, and customer-notification questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify API surface, consumers, current versions, change type, compatibility impact, SDK/docs impact, usage analytics, contractual promises, and migration deadline.
2. Read `references/api-versioning-deprecation-patterns.md`.
3. Classify change as additive, behavior change, breaking schema, auth/permission, rate limit, webhook, SDK-only, deprecated field, endpoint sunset, or emergency security change.
4. Define versioning policy, compatibility tests, docs/changelog, migration guide, usage segmentation, notification plan, exception path, and support runbook.
5. Produce API change plan, state machine, decision table, event schema, deprecation checklist, and rollout timeline.

## Guardrails

- Do not call a breaking behavior change additive because the schema still validates.
- Do not sunset endpoints without usage analytics, customer notification, migration path, and support readiness.
- Do not update SDKs, docs, OpenAPI, examples, and changelog inconsistently.
- Do not make exceptions permanent without owner, expiry, and customer migration plan.

## Output format

```text
API change context:
Audience / source of truth / risk boundary:

Versioning and deprecation plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Compatibility, migration, notifications, and support:
- <trigger> -> <policy, metric, edge case, support note>
```
