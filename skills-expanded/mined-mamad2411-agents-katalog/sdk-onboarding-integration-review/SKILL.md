---
name: sdk-onboarding-integration-review
description: Design and audit SDK, API, CLI, webhook, and developer-platform onboarding across quickstarts, auth keys, sandbox data, examples, docs IA, install friction, versioning, errors, observability, migration guides, sample apps, telemetry, and time-to-first-success. Use when developers need to integrate quickly and reliably.
---

# SDK Onboarding Integration Review

Use this skill to convert a SDK onboarding, integration success, quickstarts, auth keys, examples, errors, versioning, and developer telemetry question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify target developer, integration job, supported languages, auth model, first success event, sandbox needs, and common failure points.
2. Read `references/sdk-onboarding-integration-patterns.md`.
3. Map path from discovery to first successful API call/webhook/event and then production readiness.
4. Define docs IA, samples, environment setup, keys, mock/sandbox data, error taxonomy, observability, migration/versioning, and support handoff.
5. Produce integration journey, state machine, decision table, event schema, quickstart checklist, and failure-mode fixes.

## Guardrails

- Do not optimize docs volume instead of time-to-first-success.
- Do not require production credentials or real money/data to complete a safe quickstart.
- Do not ship SDK errors that hide request IDs, retryability, or misconfiguration cause.
- Do not break existing integrations without versioning, changelog, migration guide, and compatibility tests.

## Output format

```text
Developer context:
Integration job / language / first success event:

SDK onboarding plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Docs, samples, and errors:
- <item> -> <policy, metric, edge case, support note>

Versioning and migration policy:
- <trigger> -> <action, communication, owner>
```
