---
name: contract-obligation-renewal-audit-review
description: Design and audit contract obligation renewal reviews covering order forms, MSAs, DPAs, SLAs, security addenda, pricing exceptions, usage minimums, notice windows, auto-renewal, deliverables, support commitments, product promises, evidence owners, remediation, and renewal negotiation handoff. Use when commercial teams need obligation truth before renewal or expansion.
---

# Contract Obligation Renewal Audit Review

Use this skill to convert contract obligation, renewal audit, auto-renewal, notice window, SLA, DPA, security addendum, pricing exception, usage minimum, support commitment, product promise, and renewal negotiation questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify signed contract sources, renewal dates, notice windows, obligations, exception clauses, pricing commitments, SLA/support terms, security/privacy commitments, product promises, evidence owners, and unresolved remediation.
2. Read `references/contract-obligation-renewal-audit-patterns.md`.
3. Classify the situation as routine renewal, high-risk renewal, expansion negotiation, price increase, security/privacy obligation review, service-credit risk, product-commitment review, or termination/exit prep.
4. Define obligation register, evidence mapping, owner assignments, renewal calendar, remediation backlog, customer communication, exception expiry, and negotiation handoff.
5. Produce contract obligation audit, state machine, decision table, event schema, renewal checklist, evidence matrix, and remediation/negotiation plan.

## Guardrails

- Do not provide legal advice or rewrite contract terms; route legal interpretation to qualified counsel.
- Do not let obligations hide in PDFs, sales notes, or old emails without an owner and evidence source.
- Do not enter renewal negotiations without notice-window, SLA, pricing, security, and product-commitment truth.
- Do not treat an expired exception as harmless if billing, support, or product behavior still depends on it.

## Output format

```text
Contract renewal context:
Audience / source of truth / risk boundary:

Obligation audit plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Obligations, evidence, owners, remediation, renewal windows, and negotiation handoff:
- <trigger> -> <policy, metric, edge case, support note>
```
