---
name: openspeq-record
description: Finalize an openspeq change by merging accepted staged specs into the permanent library and preserving durable decisions.
---

# openspeq-record

Use this skill after implementation and verification are complete.

## Goal

Promote accepted staged knowledge into permanent repo state and remove stale planning residue.

## Inputs

- target repository root
- completed plan folder under `specs/_plans/<plan-name>/`
- validated code and test results

## Steps

1. Confirm implementation passed the relevant validation commands.
2. Review staged deltas under `specs/_plans/<plan-name>/`.
3. Merge accepted deltas into permanent spec files.
4. Promote durable architectural decisions through `/adr` when they will matter beyond this change; mirror or link the ADR from `specs/decision-log.md` when appropriate.
5. Leave transient planning chatter in the plan folder or archive it according to repo policy.
6. Summarize what changed in code, specs, and decision history.

## Constraints

- Do not promote temporary noise into permanent docs.
- Preserve human readability.
- Keep decision records for constraints that will matter later, not every passing thought.
- Verify before recording; do not treat intent as completion.

## Outputs

- updated permanent specs
- updated permanent decision log if needed
- cleaned or archived plan staging area
- concise completion summary
