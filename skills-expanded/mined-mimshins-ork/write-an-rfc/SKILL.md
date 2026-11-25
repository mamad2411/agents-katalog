---
name: write-an-rfc
description: Use when a change to Ork is architectural, structural, cross-cutting, or has real alternatives. Decides whether an RFC, an ADR, or only a plan is needed, and carries an RFC from draft to ADR to archive.
---

# write-an-rfc

## Prerequisites

- [`rfcs/README.md`](../../../rfcs/README.md) (lifecycle) and
  [`decisions/README.md`](../../../decisions/README.md) (ADR conventions).
- The affected specs in [`specs/`](../../../specs/README.md).

## Workflow

1. **Route the change:**
   - real alternatives to weigh (a new node type, a change to the workflow
     format, a new driver, a new integration, a change to how Ork touches
     credentials or publishes) → an **RFC** in `rfcs/active/`;
   - a hard-to-reverse choice with no alternative worth an RFC (a new runtime
     dependency, a layer-rule change) → an **ADR** directly;
   - otherwise → a **plan** in `.ai/plans/` (local, gitignored) from
     [`.ai/templates/plan.md`](../../templates/plan.md) is enough.
2. **Draft** `rfcs/active/RFC-NNN-<kebab>.md` from
   [`.ai/templates/rfc.md`](../../templates/rfc.md) with the next free number.
   Ground the Context in file references, issues, and measurements, not
   assertions. Add a row to the index in `rfcs/README.md`.
3. **One decision per RFC.** Split independent decisions.
4. **Status** `Draft` → `Proposed` when ready; the maintainer moves it to
   `Accepted`. Do not implement before `Accepted`.
5. **On ship:**
   - fold the current behavior into the affected specs;
   - write `decisions/ADR-NNN-<kebab>.md` from
     [`.ai/templates/adr.md`](../../templates/adr.md) and cross-link RFC ↔ ADR;
   - run `pnpm rfc:close RFC-NNN`, which sets the RFC to `Implemented`, moves
     it to `rfcs/archived/` and updates its index and every link to it, and add the ADR's row to
     `decisions/README.md`;
   - run `pnpm docs:check`.

## Constraints

- Never fabricate numbers, benchmarks, or sources; unknowns become open
  questions.
- An RFC that is not `Accepted` never overrides `specs/` or an ADR.
- Accepted ADRs are not rewritten; a new ADR supersedes them, and the old one
  only gains `Status: Superseded by ADR-NNN`.
- When the maintainer decides directly (for example in a design review), the ADR
  records "RFC: waived" and the options that were considered.

## Expected output

The RFC (or ADR), the updated indexes, and a list of open questions for the
maintainer.

## References

- [ADR-001](../../../decisions/ADR-001-spec-driven-development.md)
- [knowledge-drift-sync](../knowledge-drift-sync/SKILL.md)
