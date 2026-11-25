---
name: ontology-evidence-curator
description: Curate ontology-ready evidence from collected sources by capturing concept definitions, relation clues, constraints, reuse notes, data collection feasibility, and source-grounded synthesis in the exe folder.
---

# Ontology Evidence Curator

Read:

- `../refs/Total Guide.md`
- `../shared/references/exe-artifact-contract.md`
- `../shared/references/templates.md`

Use this worker skill after sources have been identified.

## Tasks

1. Extract candidate concepts, definitions, relations, constraints, and examples.
2. Tie every claim back to a source entry.
3. Distinguish direct evidence from interpretation.
4. Flag where ontology scope depends on data that is hard to collect, unstable, restricted, or not actually available.
5. Flag reuse opportunities and conflicts across sources.
6. Produce a concise synthesis for ontology design that separates feasible data-backed scope from speculative extensions.

## EXE Outputs

Always write:

- `../exe/<run-id>/research/evidence-log.md`
- `../exe/<run-id>/research/synthesis.md`
- `../exe/<run-id>/research/reuse-candidates.md`

## Guardrails

- do not create unsupported claims
- do not merge conflicting definitions without noting the conflict
- do not recommend ontology scope that depends on unavailable or access-blocked data without marking it as a risk
- do not strip away source location hints
