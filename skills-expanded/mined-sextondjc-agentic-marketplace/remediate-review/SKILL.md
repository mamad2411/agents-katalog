---
name: remediate-review
description: Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation
---

# Code Review Reception

## Core Principle

## Trigger Conditions

Invoke this skill when any of the following is true:

- Code review feedback has been received and needs evaluation before implementation.
- Review suggestions appear unclear or technically questionable.
- Implementation of review feedback is about to begin and verification is needed first.

## Core Principle

Validate review feedback against codebase reality before implementation.

## Response Sequence

1. Read full feedback without implementing.
2. Restate understanding or ask clarifying questions.
3. Verify findings against current code and constraints.
4. Decide: accept, partially accept, or push back with technical evidence.
5. Implement accepted items one at a time with verification.

## Mandatory Rules

- No performative agreement language.
- No implementation before understanding and verification.
- If any feedback item is unclear, pause and clarify before starting changes.
- For external feedback, verify compatibility with existing architecture and prior decisions.

## Priority Order for Implementation

1. Blocking correctness, reliability, or security issues.
2. Simple mechanical fixes.
3. Complex refactors.

Run validation after each item or tightly scoped batch.

## Pushback Conditions

Push back when feedback:

- Breaks existing behavior.
- Conflicts with workspace standards or explicit user decisions.
- Adds unused complexity (YAGNI).
- Depends on assumptions not supported by repository evidence.

For edge-case triage patterns and pushback templates, use [remediation-edge-cases.md](./references/remediation-edge-cases.md).

## Required Inputs

- Review comments or findings.
- Relevant code paths and constraints.
- Applicable standards and prior decisions.

## Required Outputs

- Clear disposition per comment: accept, reject, or needs clarification.
- Implemented remediations for accepted items.
- Technical rationale for rejected or deferred items.

## Workflow

1. Build a disposition list for all review items.
2. Resolve ambiguities first.
3. Implement accepted items in priority order.
4. Validate each change and confirm no regressions.
5. Report completion and unresolved items explicitly.

## References

- [README.md](./references/README.md)
- [review-response-examples.md](./references/review-response-examples.md)
- [remediation-edge-cases.md](./references/remediation-edge-cases.md)
