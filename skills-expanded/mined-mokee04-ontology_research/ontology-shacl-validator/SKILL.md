---
name: ontology-shacl-validator
description: Validate ontology outputs through SHACL-oriented checks, structural issue reporting, and release-readiness notes tied to competency questions, evidence quality, and unresolved modeling risks.
---

# Ontology SHACL Validator

Read:

- `../refs/Total Guide.md`
- `../shared/references/templates.md`
- `../shared/references/ontology-codegen-spec.md` when shape generation is needed
- `../shared/references/shacl-spec.template.json` when initializing a new SHACL spec

Use this worker skill when the ontology must be checked for structural fitness and release readiness.

## Tasks

1. Translate required structural constraints into SHACL-oriented checks.
2. Check required properties, types, and cardinality expectations.
3. Report gaps between intended ontology behavior and current structure.
4. Separate blocking issues from advisory issues.
5. Feed unresolved items back to build when needed.
6. When requested, express the approved structural checks as a JSON spec and generate SHACL Turtle with `../shared/scripts/generate_shacl_ttl.py`.
7. Start from `../shared/references/shacl-spec.template.json` unless a run-specific spec already exists.

## Outputs

Write or refine:

- `../exe/<run-id>/validation/shacl-report.md`
- `../exe/<run-id>/validation/release-readiness.md`
- `../exe/<run-id>/validation/shacl-spec.json` when machine-generated shapes are requested

## Guardrails

- do not report validation as pass or fail without naming the checked scope
- do not hide unresolved issues that affect release confidence
- do not generate SHACL shapes for constraints that have not been agreed or scoped
