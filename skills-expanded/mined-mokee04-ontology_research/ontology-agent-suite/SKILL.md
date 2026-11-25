---
name: ontology-agent-suite
description: Orchestrate a hierarchical ontology engineering skill family for a specific domain. Use when the user wants end-to-end planning, team composition, research, ontology construction, validation, and release guidance grounded in competency questions, evidence, reuse-first modeling, and human review gates.
---

# Ontology Agent Suite

Use this skill when the request is to run the full ontology workflow, not just one stage.

Before acting, read:

- `../refs/Total Guide.md`
- `../shared/references/skill-family-architecture.md`
- `../shared/references/exe-artifact-contract.md`
- `../shared/references/templates.md`

## Workflow

1. Start with an intent-clarification pass before writing substantive artifacts.
2. Ask targeted questions until the user's actual goal, target decisions, available data, constraints, and desired output shape are concrete enough to proceed.
3. Use the mandatory discovery question set below unless the user has already answered the items explicitly.
4. Do not create planning, research, build, or validation artifacts until the user has answered enough of those questions to bound the engagement.
5. Summarize the clarified intent back to the user in a compact table and pause for confirmation or correction.
6. Start `ontology-planning-team` only after the intent is concrete enough.
7. Pause for user feedback after planning before moving to research.
8. Move to `ontology-research-team` and separate feasible scope from aspirational scope.
9. Pause for user feedback after research before moving to build.
10. Move to `ontology-build-team` only after evidence and reuse candidates exist.
11. Pause for user feedback after build before moving to validation.
12. Move to `ontology-validation-team` only after build artifacts exist.
13. Pause at required human review gates before irreversible decisions.

## Mandatory Discovery Question Set

Before any artifact drafting, explicitly ask about the following and wait for enough answers to narrow scope:

1. What is the primary objective of the ontology right now: search, integration, analytics, prediction, workflow management, recommendation, or something else?
2. What are the top 3 to 5 decisions or questions this ontology must support?
3. Who will directly use the ontology outputs: analysts, operators, trainers, customers, product systems, or executives?
4. What entities or axes are believed to be central, and how are they expected to interact?
5. What data is already available today for each axis, and what is only aspirational?
6. What outcome variables or predictions are desired?
7. What is explicitly out of scope for the first version?
8. What sensitivity, privacy, licensing, or regulatory constraints apply?
9. What final artifact shape is desired for this engagement: concept model, glossary, ontology outline, RDF/OWL draft, SHACL draft, or data collection schema?

If the user gives a high-level domain statement only, start by asking these questions rather than opening a run folder or drafting the ontology.

## Required Principles

- clarify user intent before artifact generation
- reuse first
- competency questions first
- evidence before claims
- SKOS before OWL unless richer semantics are needed
- validation is mandatory
- feedback checkpoints are mandatory between major stages
- prefer table-first markdown outputs for readability
- human review for high-risk modeling decisions

## Minimum Outputs

Create or update one run folder under `../exe/<run-id>/` with:

- `planning/intent-clarification.md`
- `planning/scope.md`
- `planning/competency-questions.md`
- `research/source-inventory.md`
- `research/evidence-log.md`
- `research/synthesis.md`
- `build/modeling-decisions.md`
- `validation/shacl-report.md`
- `validation/release-readiness.md`

## Do Not Do

- do not start writing the ontology plan before checking what the user actually wants
- do not open with ontology structure proposals when the user's operational goal is still underspecified
- do not draft artifacts before the mandatory discovery question set has been asked or the equivalent answers are already present
- do not push through all stages in one burst without checkpointing with the user
- do not jump straight to OWL without a stable conceptual layer
- do not treat secondary commentary as stronger than primary standards
- do not finalize mappings or release decisions without review when risk is meaningful
