---
name: design
description: Use when approved behaviour needs complete interaction states.
version: 1.0.0
---
# Design a state-complete interaction

## Purpose and boundary
Turn an approved PRD into a state-complete, accessible interaction specification. Do not alter product policy or create engineering tasks.

## Inputs
Approved PRD revision, evidence register, domain context, design standards, supported platforms, and named design/product owners.

## Steps
1. Verify approval and revision identity. Reject a stale or unsigned PRD.
2. Map entry, confirmation, pending, success, empty, invalid, refusal, failure, retry, offline, and permission-denied states; mark non-applicable states with reasons.
3. For each state, define visible copy, enabled actions, focus destination, keyboard behaviour, screen-reader announcement, and recovery route.
4. Identify destructive or irreversible actions and specify confirmation proportional to consequence.
5. Link each state to requirements and acceptance criteria. Return policy gaps to Capture & Refine rather than choosing them.
6. Review edge transitions: double activation, navigation during pending work, delayed response, and a result that arrives after the view changes.
7. Record review owner, covered states, gaps, decision, timestamp, and exact PRD/design revision.

## Outputs
Journey/state model, interaction and content specification, accessibility notes, coverage matrix, decision log, and `ready`, `incomplete`, `conflicting`, or `blocked` status.

## Stop gates
Stop when approval is missing, product policy is unresolved, a relevant failure or accessibility state lacks treatment, or the design conflicts with the PRD.

## Example
For cancellation, the primary action opens a confirmation naming the cutoff. Submission disables repeat activation and announces progress. `cancelled` moves focus to a status heading; `too_late` preserves the order and offers help; an unknown result says it is safe to retry using the same request.

## Quality check
Every applicable state has content, action, focus, announcement, and recovery; design decisions cite requirements; readiness is revision-bound and has an owner.
