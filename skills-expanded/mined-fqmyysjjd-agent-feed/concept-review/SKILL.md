---
name: concept-review
description: Use when reviewing naming, vocabulary drift, invented concepts, misleading abstractions, or unclear domain language.
source: agent-feed
trust: core
---

# Concept Review Skill

Use this skill to keep AI-assisted work from introducing unnecessary concepts, misleading names, or vocabulary drift.

## Required Use

Use this skill when:

1. A review includes naming, terminology, abstraction, module boundaries, or user-facing concept changes.
2. A diff introduces new nouns, categories, layers, services, records, statuses, protocols, or workflow names.
3. The user questions whether wording, naming, or abstraction is necessary.
4. A task imports, creates, or modifies external/custom skills whose terminology could override project language.

## Required Reading

1. `.agents/rules/outcome-boundary.md`
2. `.agents/skills/README.md`
3. `.agents/project/README.md`
4. `.agents/domain/README.md`
5. The files, diff, plan, or skill being reviewed.

## Evidence Priority

Resolve terminology against evidence in this order:

1. Current user request and Task Brief language.
2. Project/domain source-of-truth files and indexed read triggers.
3. Existing public contracts, CLI/API names, generated file names, schemas, and module owners.
4. Established naming patterns in the same repository.
5. External or custom skill terminology, only as a lower-priority method vocabulary.

If existing terminology is already inconsistent, do not use the inconsistency as permission to add another term. Prefer convergence toward the clearest existing source of truth, or apply `.agents/rules/decision-gates.md` when renaming a stable contract would affect future development.

## Concept Noise Categories

Flag these four types of concept noise:

1. `Vocabulary drift`: a new word competes with an existing word for the same concept.
2. `Pseudo-concept`: a new class, layer, workflow name, status, or category wraps an existing action without adding durable meaning.
3. `Semantic misdirection`: a name implies a lifecycle, orchestration, state machine, authority, or guarantee that the implementation does not provide.
4. `Concept pollution`: a lower-level module, reusable rule, public contract, or generic skill imports terms that belong to a different layer, one repository, or one product domain.

## Review Procedure

1. Identify the baseline vocabulary from project/domain source-of-truth files.
2. List new or changed terms in the current work.
3. For each term, check whether it maps to an existing project concept, contract, or user-visible behavior.
4. Classify any problem as vocabulary drift, pseudo-concept, semantic misdirection, or concept pollution.
5. Flag invented concepts that hide a simpler action, duplicate existing language, imply unsupported behavior, or move project-specific meaning into reusable rules.
6. Prefer the plainest accurate name that a future maintainer can understand without translating it back to the implementation.

## Guardrails

1. Do not rename stable public, persistence, API, CLI, or domain contracts without applying `.agents/rules/decision-gates.md`.
2. Do not block useful domain terms just because they are new; require evidence that the term owns a durable behavior or boundary.
3. Do not treat style preference as a finding unless it creates ambiguity, drift, or maintenance cost.

## Output

Return concept findings with the affected term, why it is risky, the source-of-truth it conflicts with or lacks, and the smallest safer wording or boundary.
