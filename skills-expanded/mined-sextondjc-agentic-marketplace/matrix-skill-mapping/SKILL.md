---
name: matrix-skill-mapping
description: Use when maintaining the Phase / Discipline / Lane matrix and its mapping to skill assets, including bundle ownership, discipline change checks, and catalog alignment.
---

# Matrix Skill Mapping

## Specialization

Own the mapping layer between the Phase / Discipline / Lane coverage map and workspace skills.

This skill centralizes bundle-to-skill associations so individual skills remain self-contained and focused on their own behavior.

## Trigger Conditions

- A skill description or frontmatter starts embedding matrix bundle or cell metadata.
- A new skill must be associated with a matrix bundle code (X-code, N-code, or O-code).
- A Discipline, Phase, or Lane value changes and matrix mapping must be recalibrated.
- The matrix legend and skill-discovery catalog drift out of sync.

## Inputs

- Canonical matrix path: `.github/skills/matrix-skill-mapping/references/phase-discipline-lane-agentic-delivery-matrix.md`
- Posterity copy path: `.docs/plans/governance/taxonomy-tag-registry/phase-discipline-lane-agentic-delivery-matrix.md`
- Skills discovery index path: `.github/catalogs/skills-discovery-index.md`
- Target skill names and proposed mapping changes
- Relevant ADR or decision-log reference

## Required Outputs

| Output | Description |
|---|---|
| Mapping registry update | Updated mapping table in `references/mapping-registry.md` linking bundle codes to owning skills and lane intent. |
| Drift assessment | Findings for legend/index mismatch, stale mappings, or unsupported discipline changes. |
| Mapping decision note | A concise record of what mapping changed, why, and what downstream files were updated. |
| Scope check result | Confirmation that individual SKILL.md files remain self-contained (no embedded bundle/cell metadata in frontmatter). |

## Workflow

1. Read the matrix legend and identify bundle codes in scope.
2. Read the skill discovery index and list candidate owner skills.
3. Update `references/mapping-registry.md` with bundle code to skill mappings and lane intent.
4. Check for drift between matrix legend and skill catalog entries.
5. If a discipline changed, verify DEC-PDL-07 revisit evidence exists before adopting mapping updates.
6. Keep per-skill metadata clean: remove matrix bundle/cell mapping from individual skill frontmatter.
7. Publish a concise mapping decision note in the output.

## Guardrails

- Keep bundle ownership metadata in the mapping registry, not in individual skill frontmatter.
- Do not change matrix discipline lists without DEC-PDL-07 revisit evidence.
- Do not create new skills for sparse matrix cells unless adoption protocol criteria are met.

## References

- Canonical matrix: `./references/phase-discipline-lane-agentic-delivery-matrix.md`
- Skill index: `../../catalogs/skills-discovery-index.md`
- Mapping registry: `./references/mapping-registry.md`

