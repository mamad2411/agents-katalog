---
name: ontology-source-scout
description: Find and triage primary sources, standards, ontologies, schemas, and domain documents for ontology projects, while checking whether usable data can actually be collected and logging the full research process in the exe folder.
---

# Ontology Source Scout

Read:

- `../refs/Total Guide.md`
- `../shared/references/exe-artifact-contract.md`
- `../shared/references/templates.md`

Use this worker skill when source discovery and triage are needed.

## Tasks

1. Start from competency questions and required standards.
2. Search official and primary sources first.
3. Identify reusable ontologies, vocabularies, and schemas before inventing new structure.
4. Record whether candidate data sources are actually obtainable in practice, including access method, license, stability, and likely collection burden.
5. Record both accepted and rejected sources with reasons.
6. Carry forward license, authority, freshness, and collection-feasibility notes.

## EXE Outputs

Always write:

- `../exe/<run-id>/research/queries.md`
- `../exe/<run-id>/research/source-inventory.md`

## Guardrails

- do not only save the final source list
- do not lose the actual queries or selection reasoning
- do not assume a source is usable just because it is conceptually relevant
- do not overvalue blog posts above primary standards when a primary source exists
