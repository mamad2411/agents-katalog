---
name: ontology-build-team
description: Turn research outputs into a domain ontology draft using layered modeling, SKOS-first conceptualization, selective OWL formalization, and explicit modeling decisions tied back to evidence.
---

# Ontology Build Team

Read:

- `../refs/Total Guide.md`
- `../shared/references/skill-family-architecture.md`
- `../shared/references/templates.md`

Use this skill after research artifacts exist.

## Build Segments

| Segment | Goal | Required user feedback |
| --- | --- | --- |
| B1 Concept backbone | settle core entities and boundaries | yes |
| B2 Relation and constraint draft | connect concepts and note unresolved choices | yes |
| B3 Machine-readable spec | express stable structure in ontology spec files | yes |
| B4 Review packaging | prepare outline, mapping notes, and modeling decisions | yes |

## Team Composition

Route build work through:

- `ontology-ontology-architect`

## Tasks

1. Start from evidence and competency questions, not from guesswork.
2. Separate `Core`, `Domain`, and `Application` concerns when possible.
3. Build a stable glossary or SKOS concept layer first.
4. Pause and confirm the conceptual backbone with the user before adding more detail.
5. Add OWL constructs only where richer semantics are justified.
6. Record every important modeling choice and unresolved ambiguity.
7. Prepare a validation-ready ontology outline and mapping notes.
8. Pause after the outline/spec draft and ask the user what feels wrong, missing, or over-modeled.

## Outputs

Write or update:

- `../exe/<run-id>/build/glossary.md`
- `../exe/<run-id>/build/modeling-decisions.md`
- `../exe/<run-id>/build/ontology-outline.md`
- `../exe/<run-id>/build/mapping-notes.md`

## Exit Criteria

Do not hand off to validation until:

- the glossary or concept layer exists
- key relations are modeled
- mapping assumptions are explicit
- unresolved issues are clearly listed
- a build checkpoint has been reviewed with the user
