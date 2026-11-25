---
name: ontology-ontology-architect
description: Design a domain ontology from evidence using layered modeling, stable concept definitions, explicit relations, SKOS-first structure, and selective OWL formalization with recorded modeling decisions.
---

# Ontology Ontology Architect

Read:

- `../refs/Total Guide.md`
- `../shared/references/skill-family-architecture.md`
- `../shared/references/templates.md`
- `../shared/references/ontology-codegen-spec.md` when code generation is needed
- `../shared/references/ontology-spec.template.json` when initializing a new machine-readable ontology spec

Use this worker skill to turn research outputs into a coherent ontology design.

## Tasks

1. Identify the conceptual backbone of the domain.
2. Separate core concepts, domain concepts, and application-specific extensions.
3. Start with a glossary or SKOS concept scheme.
4. Add relations and formal constraints only where justified by CQ and evidence.
5. Record modeling decisions, alternatives, and unresolved ambiguity.
6. When requested, turn the stable ontology outline into a JSON spec that can be rendered into RDF/OWL Turtle with `../shared/scripts/generate_ontology_ttl.py`.
7. Start from `../shared/references/ontology-spec.template.json` unless a run-specific spec already exists.

## Outputs

Write or refine:

- `../exe/<run-id>/build/glossary.md`
- `../exe/<run-id>/build/modeling-decisions.md`
- `../exe/<run-id>/build/ontology-outline.md`
- `../exe/<run-id>/build/mapping-notes.md`
- `../exe/<run-id>/build/ontology-spec.json` when machine-generated Turtle is requested

## Guardrails

- do not confuse taxonomy with every kind of relation
- do not add OWL complexity without a concrete payoff
- do not finalize equivalence or inheritance decisions without evidence
- do not generate RDF/OWL code from unstable modeling decisions
