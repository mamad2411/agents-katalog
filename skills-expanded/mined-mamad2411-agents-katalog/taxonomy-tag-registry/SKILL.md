---
name: taxonomy-tag-registry
description: Use when maintaining consistent Phase x Discipline x Lane tags across catalogs, plans, and workspace artifacts to prevent taxonomy drift.
---

# Taxonomy Tag Registry

## Specialization

Maintain consistent, authoritative Phase × Discipline × Lane taxonomy tags across catalogs, planning artifacts, skills, and documentation. Detect and correct tag drift before it creates routing inconsistencies or orphaned assets.

This skill owns tag consistency, not the underlying taxonomy definition. The PDL taxonomy is defined in the canonical matrix. This skill applies that taxonomy and surfaces deviations.

## Trigger Conditions

- A new skill, instruction, or agent references a Phase, Discipline, or Lane value and it must be verified against the canonical taxonomy.
- A catalog or index file has accumulated inconsistent tags from multiple contributors or sessions.
- A Discipline list change (per DEC-PDL-07) has occurred and all existing tags must be reviewed for alignment with the new taxonomy.
- A review or audit has flagged tag inconsistency across planning artifacts, ADRs, or skills.
- A new customisation is being created and needs a canonical routing coordinate assigned.

## Inputs

- Artifact set to tag-check: files, index rows, or skill frontmatter to evaluate.
- Canonical taxonomy reference: Phase × Discipline × Lane values from the PDL matrix.
- Discipline change record (if applicable): the DEC-PDL-07 revisit outcome that changed the Discipline list.
- Originating plan or workstream ID for traceability.

## Required Outputs

| Output | Description |
|---|---|
| Tag audit result | For each artifact checked: current tag values, canonical tag values, and verdict (Consistent / Drift / Missing). |
| Drift log | All artifacts where tag values deviate from canonical values. Each entry: artifact path, field, current value, correct value, and recommended action. |
| Correction set | The set of tag corrections to apply. Presented as discrete, reviewable changes before application. |
| Tag assignment record | For new artifacts: the assigned Phase, Discipline, and Lane coordinate with rationale and reference to the canonical matrix cell. |

## Workflow

1. Confirm the canonical taxonomy source: Phase values (ANALYSIS, DESIGN, IMPLEMENTATION, TEST, RELEASE), Discipline values (current approved list), Lane values (Plan, Execute, Review).
2. Collect artifacts to evaluate. For each artifact, identify where Phase, Discipline, and Lane values appear (frontmatter, table rows, index entries).
3. Compare each tag value against canonical. Record: consistent, drift, or missing.
4. Build the drift log: every non-canonical value with its correct counterpart.
5. Build the correction set: propose corrections as discrete changes. Do not apply automatically — present for review.
6. For new artifact assignments: identify the matrix cell that best matches the artifact's purpose and record the coordinate with rationale.
7. Confirm output references the originating plan or workstream ID.

## Canonical Taxonomy Reference

### Phases
`ANALYSIS` | `DESIGN` | `IMPLEMENTATION` | `TEST` | `RELEASE`

### Lanes
`Plan` | `Execute` | `Review`

### Discipline Change Protocol
- Any Discipline list change must be preceded by a DEC-PDL-07 revisit.
- After a Discipline change, run a full tag audit across all skills, instructions, agents, and index files before treating the change as adopted.

## Done Criteria

- Tag audit result covers every artifact in the input set.
- Drift log is present (may be empty if no drift found).
- Correction set is presented for review before any changes are applied.
- New artifact assignments include the matrix cell coordinate and rationale.
- Originating plan or workstream ID is on the output.

## Guardrails

- Do not apply tag corrections silently — always present the correction set for review before applying.
- Do not invent new Phase, Discipline, or Lane values; flag unknown values as taxonomy drift and escalate for DEC-PDL-07 revisit.
- Do not run a full workspace tag audit in the same pass as a Discipline list change — complete the matrix revisit first, then audit tags.

## References

- Canonical matrix: [phase-discipline-lane-agentic-delivery-matrix.md](../matrix-skill-mapping/references/phase-discipline-lane-agentic-delivery-matrix.md)
- Related skills: `matrix-skill-mapping`, `sync-customizations`, `asset-naming-taxonomy`, `governance-audit`

