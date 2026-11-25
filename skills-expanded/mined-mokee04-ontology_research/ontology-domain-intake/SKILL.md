---
name: ontology-domain-intake
description: Clarify the target domain for ontology work by defining scope, users, constraints, out-of-scope areas, and approval points before modeling starts.
---

# Ontology Domain Intake

Read:

- `../refs/Total Guide.md`
- `../shared/references/templates.md`

Use this worker skill to produce a clean scope and constraint statement.

## Tasks

1. Begin with discovery questions if the user has not yet specified intended use, users, available data, and constraints.
2. Ask the domain intake question set below before drafting scope.
3. Name the domain and intended use.
4. Separate in-scope from out-of-scope.
5. Identify intended users, downstream systems, and data sensitivity.
6. Note required standards, regulations, or internal constraints.
7. Mark where human approval is required.

## Domain Intake Question Set

Ask explicitly about:

1. The operational use case or service to support
2. The core entities or axes that define the domain
3. The data currently collected for each core entity
4. The most important decisions or workflows to improve
5. The boundaries of the first version
6. Sensitive or regulated data elements
7. Any required internal terminology or external standards

## Output

Write or refine:

- `../exe/<run-id>/planning/scope.md`
- `../exe/<run-id>/planning/risks.md`

## Guardrails

- do not let scope remain open-ended
- do not draft scope from the domain label alone when the intended use is still unclear
- do not hide unresolved ambiguity
- do not treat approval-sensitive constraints as optional
