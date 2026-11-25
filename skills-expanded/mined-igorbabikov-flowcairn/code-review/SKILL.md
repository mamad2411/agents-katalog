---
name: code-review
description: Independently assess actual changes and current evidence for each requirement in ai-review.
---

# Review the result against the contract

- Read the full supplied bundle, including deletions, relevant callers, implementation receipts and prior repairs. Judge artifacts and original criteria, not the implementer's narrative. Incomplete evidence prevents pass for the affected criterion; reviewEvidenceHash binds input but does not prove review quality.
- Trace each changed boundary: input, state transition, consumer, error path and recovery. Check compatibility, access/privacy and regressions according to risk. Verify tests exercise the claimed behavior and meaningful failures. Broad rewrites, style preferences and unrelated dependencies are not completion criteria.
- Return requirementAssessments for mandatory requirements: exact requirementId, criterion, verdict, checkIds, citations and reason. Global pass cannot replace separate assessments; failed requirements need concrete blocking findings.
- Compare successful facts in priorEvidence.verificationChecks to the actual scenario/criterion. Source-review covers directly observable properties only; human acceptance remains the user's decision. Successful check/source-review assessments require nonempty citations with path, startLine and exact quote from a current file within verification.paths and readPaths. Runtime checks bytes; invented quotes or unrelated checks are not evidence.
- Findings identify trigger, actual/expected behavior, location, user impact and suitable reverification. Calibrate severity to impact. Separate reproduced defects, plausible unverified risks, missing evidence and optional improvements. State out-of-contract risks explicitly without inventing requirement IDs or expanding the contract.

## TypeScript boundaries, only when touched

Follow project compiler settings and public types. Inspect unsafe casts, any and non-null assertions at changed external-data/state boundaries. Types do not validate JSON/persisted data: inspect actual guards/schema checks, including malformed input. For discriminated state unions, verify reachable transitions and exhaustive handling; never checks are compile-time support, not runtime validation. Prefer simple existing types to unrelated advanced-type refactors.

Review is read-only: no edits, extra reviewer dispatch, commit or merge. Do not declare PROVEN; Executor owns final completion and evidence freshness. Repairs require fresh assessment of affected criteria.

Adapted from obra/superpowers requesting-code-review/code-reviewer and narrow wshobson/agents typescript-advanced-types guidance. Copyright (c) 2025 Jesse Vincent; Copyright (c) 2024 Seth Hobson. [Obra MIT](../licenses/obra-superpowers-MIT.txt), [wshobson MIT](../licenses/wshobson-agents-MIT.txt); official TypeScript docs and modifications: [PROVENANCE](../PROVENANCE.json).
