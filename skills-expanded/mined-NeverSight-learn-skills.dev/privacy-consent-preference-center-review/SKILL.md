---
name: privacy-consent-preference-center-review
description: Design and audit privacy consent and preference centers covering consent categories, communication preferences, cookies, tracking, email, push, SMS, AI data use, regional rules, minors, opt-out signals, consent proof, synchronization, revocation, accessibility, localization, and audit evidence. Use when user privacy choices must be understandable, enforceable, and measurable.
---

# Privacy Consent Preference Center Review

Use this skill to convert privacy consent center, preference center, cookie category, communication opt-out, AI data-use preference, consent proof, and regional privacy choice questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify choice categories, legal basis, user segment, region, channel, downstream systems, consent proof, revocation path, sync latency, accessibility, and audit owner.
2. Read `references/privacy-consent-preference-center-patterns.md`.
3. Classify the situation as cookie consent, marketing preference, product notification preference, AI data-use choice, sale/share opt-out, consent withdrawal, minor consent, or enterprise admin policy.
4. Define choice taxonomy, UI copy, default state, proof event, downstream enforcement, sync SLA, exception handling, audit evidence, and user support path.
5. Produce preference center review, state machine, decision table, event schema, consent checklist, downstream sync map, and audit plan.

## Guardrails

- Do not collect consent that downstream systems cannot enforce or prove.
- Do not hide opt-outs behind confusing copy, dark patterns, inaccessible controls, or region-inconsistent defaults.
- Do not mix transactional, security, marketing, product, and AI data-use choices without clear semantics.
- Do not treat UI preference state as sufficient without event proof and downstream synchronization.

## Output format

```text
Preference center context:
Audience / source of truth / risk boundary:

Consent preference plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Choices, proof, enforcement, sync, support, accessibility, and audit:
- <trigger> -> <policy, metric, edge case, support note>
```
