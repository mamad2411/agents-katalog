---
name: ontology-cq-designer
description: Design and refine competency questions for a domain ontology project, connecting user goals to testable questions, expected answer shapes, and later validation checks.
---

# Ontology CQ Designer

Read:

- `../refs/Total Guide.md`
- `../shared/references/templates.md`

Use this worker skill when the project needs testable ontology requirements.

## Tasks

1. Turn user goals and use cases into competency questions.
2. Prefer questions that imply concrete answer structures.
3. Link each question to candidate concepts and relations.
4. Add validation hints that later teams can reuse.
5. Keep the CQ set compact but coverage-oriented.

## Output

Write or refine:

- `../exe/<run-id>/planning/competency-questions.md`
- `../exe/<run-id>/validation/cq-checks.md`

## Guardrails

- do not write vague questions that cannot be checked
- do not create ontology content with no CQ relevance unless explicitly justified
