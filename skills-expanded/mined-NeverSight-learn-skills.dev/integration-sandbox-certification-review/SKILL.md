---
name: integration-sandbox-certification-review
description: Design and audit integration sandbox certification for APIs, SDKs, apps, plugins, marketplace integrations, OAuth scopes, webhooks, test tenants, synthetic data, rate limits, error handling, security review, privacy boundaries, version compatibility, support readiness, and certification badges. Use when partners or developers need a safe path from sandbox to production integration.
---

# Integration Sandbox Certification Review

Use this skill to convert integration sandbox, developer certification, partner integration test, OAuth scope, webhook test, sandbox data, and production-readiness questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify integration type, developer/partner, sandbox environment, test data, required scopes, API surfaces, webhook events, certification criteria, support owner, and production gate.
2. Read `references/integration-sandbox-certification-patterns.md`.
3. Classify the situation as self-serve sandbox, partner sandbox, certification test suite, OAuth review, webhook certification, SDK compatibility, marketplace app review, or production promotion gate.
4. Define sandbox setup, test cases, data boundaries, security checks, rate-limit behavior, error cases, support docs, badge criteria, and recertification cadence.
5. Produce sandbox certification plan, state machine, decision table, event schema, test checklist, evidence package, and recertification policy.

## Guardrails

- Do not certify integrations that only pass happy-path API calls.
- Do not use real customer data in sandboxes without explicit policy and isolation.
- Do not grant broad OAuth scopes or production credentials before certification evidence exists.
- Do not let certified integrations drift after API, webhook, SDK, policy, or security changes.

## Output format

```text
Integration sandbox context:
Audience / source of truth / risk boundary:

Sandbox certification plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Environment, scopes, tests, evidence, production gate, support, and recertification:
- <trigger> -> <policy, metric, edge case, support note>
```
