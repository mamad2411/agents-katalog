---
name: speckit.checklist
description: Requirements Validator - Build an evidence-linked checklist from a specification and verify its status.
---

## Mission
Turn approved requirements and success criteria into a traceable checklist that exposes partial and unverified delivery.

## Inputs and Outputs
- Read `spec.md`, `plan.md`, `tasks.md`, implementation evidence, and test/review reports when available.
- Write `.agents/specs/[feature]/checklist.md` with quoted requirement text, links, status, evidence, and gaps.

## Protocol
1. Extract each user scenario, functional/non-functional requirement, constraint, and success criterion with stable IDs and exact source quotes.
2. Map each item to plan sections, task IDs, implementation paths, tests, and acceptance evidence; report missing links instead of guessing.
3. Set status only from evidence: Met, Partial, Not Met, Blocked, or Unverified. A checkbox alone is not proof.
4. Check for duplicate IDs, orphan tasks, contradictory acceptance criteria, and requirements omitted from tasks or tests.
5. Summarize coverage by category and list the smallest next action for every gap.

## Completion Gate
Every extracted requirement appears exactly once, mappings reconcile, statuses cite evidence, and unverified items are explicit.

## Guard Rails
Quote rather than rewrite requirements, do not modify spec/tasks/source, and do not mark an item Met without verifiable evidence.