---
name: capture-refine
description: Use when a vague product request needs a testable agreement.
version: 1.0.0
---
# Capture and refine product intent

## Purpose and boundary
Produce an approved behavioural contract from incomplete intent. Do not choose architecture, write code, create technical tasks, or infer approval.

## Inputs
- Stable work-item ID, raw request, product boundary, product owner, engineer reviewer.
- Accessible requirements, design, behaviour tests, prior decisions, screenshots, or history.
- Source locators and access limitations.

## Steps
1. Create a source register. Label each claim `requested`, `observed`, `decided`, `conflicting`, or `unknown`; a missing source is not evidence of absence.
2. Write the actor, desired outcome, explicit exclusions, and domain terms.
3. Build a decision tree across permission, lifecycle state, validation, failure, retry, repeated action, concurrency, accessibility, and measurable qualities.
4. Ask only the current frontier. Each numbered question must be independently answerable. Include a product-level recommendation and trade-off, not a technical design.
5. Record each answer with decision owner and locator. Keep unanswered branches open; never manufacture an answer.
6. Draft functional requirements and Given/When/Then criteria. Give every material clause evidence or a decision reference.
7. Obtain engineer review, then explicit product decision (`approved`, `changes_requested`, or `pending`) bound to the exact revision.
8. Evaluate design readiness. Route to Design unless a version-aligned design covers all applicable states and is marked ready; otherwise route to Planner. Never route directly to Builder.

## Outputs
Source register, decision log, revisioned PRD, acceptance criteria, review records, design gate, and one bounded handoff or refusal.

## Stop gates
Stop for missing required input, inaccessible material evidence, open decisions, unsupported clauses, requested changes, absent exact-revision approval, or inconsistent design evidence.

## Example
Input: “Customers can cancel orders.” Question: “Which lifecycle states remain cancellable?” Product decision: `placed` and `confirmed`; once fulfilment starts, show `too_late`. Output criterion: “Given an owned confirmed order, when its owner cancels it, then status becomes cancelled and one cancellation event is recorded.”

## Quality check
A reader can distinguish facts, requests, decisions, and unknowns; every criterion is observable; status and owner are explicit; no implementation prescription is hidden in the PRD.
