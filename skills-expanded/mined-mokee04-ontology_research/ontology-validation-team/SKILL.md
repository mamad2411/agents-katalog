---
name: ontology-validation-team
description: Validate a domain ontology draft using competency-question checks, SHACL-oriented structural validation, review gates, and release-readiness criteria before the ontology is treated as stable.
---

# Ontology Validation Team

Read:

- `../refs/Total Guide.md`
- `../shared/references/exe-artifact-contract.md`
- `../shared/references/templates.md`

Use this skill after build artifacts exist.

## Validation Segments

| Segment | Goal | Required user feedback |
| --- | --- | --- |
| V1 CQ coverage check | test whether the ontology answers the intended questions | yes |
| V2 Structural validation | draft SHACL-oriented checks and identify blockers | yes |
| V3 Release decision framing | separate hold items from nice-to-haves | yes |

## Team Composition

Route validation work through:

- `ontology-cq-designer`
- `ontology-shacl-validator`

## Tasks

1. Re-check the ontology against the competency questions.
2. Check whether required constraints can be expressed and tested.
3. Produce a SHACL-oriented validation report.
4. Flag missing evidence, unresolved mappings, and governance gaps.
5. Recommend release, revision, or hold.
6. Pause after CQ coverage and after the release recommendation so the user can redirect before finalizing the judgment.

## Outputs

Write or update:

- `../exe/<run-id>/validation/cq-checks.md`
- `../exe/<run-id>/validation/shacl-report.md`
- `../exe/<run-id>/validation/release-readiness.md`

## Exit Criteria

A release recommendation requires:

- CQ coverage status
- SHACL status
- unresolved issue summary
- explicit human review note for high-risk decisions
- a validation checkpoint reviewed with the user
