---
name: compliance-evidence-room-review
description: Design and audit compliance evidence rooms, gated security document portals, SOC/ISO reports, pen test summaries, policies, DPAs, subprocessors, audit evidence, access approval, expiry, watermarking, renewal, and buyer proof workflows. Use when enterprise customers or auditors need sensitive evidence without uncontrolled document sharing.
---

# Compliance Evidence Room Review

Use this skill to convert a compliance evidence rooms, gated documents, approvals, expiry, audit proof, and buyer security review question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify evidence consumers, document types, sensitivity, access rules, approval owners, expiry dates, NDA/terms path, and buyer workflow.
2. Read `references/compliance-evidence-room-patterns.md`.
3. Classify evidence as public summary, gated report, contract document, audit artifact, policy, subprocessor record, or customer-specific exception.
4. Define document metadata, access control, watermark/expiry policy, audit trail, update cadence, request handling, and sales/security handoff.
5. Produce evidence room plan, state machine, decision table, event schema, access checklist, and stale-document escalation.

## Guardrails

- Do not share SOC reports, pentests, architecture diagrams, or customer evidence by email when gated access is required.
- Do not keep expired or superseded compliance documents available without warning.
- Do not grant evidence access without requester identity, purpose, terms, expiry, and audit trail.
- Do not let sales upload unapproved documents or alter evidence scope.

## Output format

```text
Evidence room context:
Consumer / document sensitivity / access boundary:

Evidence room plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Documents, metadata, and access rules:
- <item> -> <policy, metric, edge case, support note>

Expiry, revocation, and stale-document handling:
- <trigger> -> <action, communication, owner>
```
