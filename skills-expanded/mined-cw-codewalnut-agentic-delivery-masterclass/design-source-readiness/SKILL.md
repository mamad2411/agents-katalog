---
name: design-source-readiness
description: Use when composing an interaction artifact, auditing its coverage and drift, and preparing the exact Design handoff.
---

# Compose and review Design evidence

## Inputs
Input-gate record, interaction contract, project component guidance, exact source identity or specification-only mode, and named review owners.

## Procedure
1. Confirm capability and authority separately. Tool availability does not authorise source mutation.
2. Map states to project components and tokens; record deviations and conflicting guidance rather than inventing a parallel system.
3. In specification-only mode, write traceable frame/component changes and state that no design workspace changed.
4. In editable mode, mutate only the pinned source, then save and read back the exact resulting revision.
5. Compare every requirement, criterion, and state with the produced artifact; compare editable-source revisions to separate intended changes from accidental drift.
6. Classify findings as omission, design conflict, product-policy question, stale source, or evidence gap. Repair Design-owned omissions and rerun coverage.
7. Record exact-revision Design review and Product review for policy changes as pending, approved, changes requested, or not supplied.

## Output
A specification or exact editable revision plus component/deviation log and `ready|design_not_required|incomplete|conflicting|blocked` handoff bound to exact inputs.

## Stop condition
Stop mutation on absent authority, missing target, integration/read-back failure, or conflicting guidance. A screenshot, save event, or tool success cannot prove editable identity or human approval.
