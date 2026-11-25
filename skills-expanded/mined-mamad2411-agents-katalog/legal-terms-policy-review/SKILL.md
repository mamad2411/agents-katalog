---
name: legal-terms-policy-review
description: Review product legal terms and policy surfaces covering Terms of Service, privacy policy links, acceptable use, refunds, trials, renewals, cancellation, billing disclosures, AI disclaimers, marketplace rules, store policies, consent, regional notices, versioning, change notice, and support/legal escalation. Use when product flows or public copy create legal commitments or user obligations.
---

# Legal Terms Policy Review

Use this skill to convert legal terms, policy surface, user obligation, billing disclosure, acceptable use, and change-notice questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify product surface, user action, promise/obligation, geography, customer type, policy owner, current terms, and risk of mismatch between UI, sales, support, and contracts.
2. Read `references/legal-terms-policy-patterns.md`.
3. Classify the term as ToS, privacy notice, acceptable use, refund, trial, renewal, cancellation, AI disclosure, marketplace policy, regional notice, or contract exception.
4. Define required disclosure, consent/acknowledgement, versioning, change notice, evidence capture, support macro, owner approval, and escalation path.
5. Produce legal-terms review, state machine, decision table, event schema, policy checklist, and launch/readiness gates.

## Guardrails

- Do not invent legal language or treat the skill output as legal advice; route final wording to legal counsel or approved policy owners.
- Do not bury material billing, renewal, cancellation, AI, data, or marketplace obligations where users cannot discover them.
- Do not let support macros, sales decks, pricing pages, store listings, and product UI contradict approved terms.
- Do not change user obligations without versioning, notice, evidence, and rollback/exception handling.

## Output format

```text
Terms context:
Audience / source of truth / risk boundary:

Policy surface plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Notices, consent, versioning, and support/legal escalation:
- <trigger> -> <policy, metric, edge case, support note>
```
