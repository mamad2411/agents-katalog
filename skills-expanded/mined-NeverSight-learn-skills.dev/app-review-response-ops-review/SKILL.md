---
name: app-review-response-ops-review
description: Design and audit app review response operations for App Store, Google Play, Steam, Microsoft Store, and marketplace review notices covering policy classification, evidence packages, reviewer communication, metadata fixes, screenshots, privacy labels, IAP/subscription issues, appeals, expedited review, release sequencing, user communication, and recurrence prevention. Use when a store review rejection or warning threatens launch or revenue.
---

# App Review Response Ops Review

Use this skill to convert app review rejection, store policy notice, reviewer response, appeal, expedited review, metadata fix, privacy label, IAP subscription review, and launch-risk questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify store, policy citation, rejected build, affected release, reviewer message, product behavior, metadata, screenshots, privacy labels, commerce setup, deadline, and owner.
2. Read `references/app-review-response-ops-patterns.md`.
3. Classify the situation as metadata issue, binary behavior issue, privacy disclosure issue, IAP/subscription issue, content/moderation issue, policy misunderstanding, legal/compliance issue, or appeal/escalation.
4. Define evidence package, reproduction steps, reviewer response, build or metadata fix, appeal path, release plan, customer communication, recurrence prevention, and monitoring.
5. Produce app review response plan, state machine, decision table, event schema, policy checklist, reviewer-message draft, and recurrence-prevention log.

## Guardrails

- Do not argue with reviewers without mapping the cited policy to product behavior and evidence.
- Do not submit speculative builds or metadata changes that create new policy, privacy, subscription, or screenshot mismatches.
- Do not hide user-impacting launch delays from support, marketing, customer success, or revenue owners.
- Do not treat each rejection as a one-off if the root cause is release process, entitlement, privacy, or policy drift.

## Output format

```text
App review context:
Audience / source of truth / risk boundary:

Review response plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Policy, evidence, fix, appeal, release sequencing, and prevention:
- <trigger> -> <policy, metric, edge case, support note>
```
