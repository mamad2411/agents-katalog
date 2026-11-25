---
name: constitution-reference
description: Instructions for reading and referencing the project constitution during validation
user-invocable: false
---

# Constitution Reference

## Location

The project constitution lives at `.specify/memory/constitution.md`.

## How to Read

Always use the Read tool to load the FULL constitution before any validation. Never validate from memory or assumptions.

## What to Extract

When reading the constitution, identify:

1. **Stack Principles** — What technologies are mandated and their usage patterns
2. **Engineering Principles** — How code should be written (TDD, type safety, simplicity)
3. **AI Collaboration Principles** — How human and AI work together (gates, approval flow)
4. **Quality Gates** — What must pass before a phase is considered complete

## If Constitution Doesn't Exist

If `.specify/memory/constitution.md` does not exist or is empty:

1. Report that no constitution has been established
2. Recommend editing `.specify/memory/constitution.md` directly
3. Do NOT proceed with validation — there is nothing to validate against
