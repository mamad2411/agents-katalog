---
name: software-brd-prd
description: Use when starting, discovering, defining, reviewing, or revising a software product or project where a BRD, PRD, product requirements baseline, MVP scope, or requirements clarification is needed before design or implementation.
metadata:
  version: "1.0.0"
  domain: "software-product-requirements"
---

# Software BRD + PRD

## Core principle

Discover before documenting. Separate **business truth (BRD: why and outcomes)** from **product truth (PRD: users, behavior, capabilities, quality, and validation)**. Never invent missing project facts.

## Required behavior

1. Inspect all available project context first. Never ask for information already provided.
2. If the project is still vague, **do not jump to a final BRD/PRD**. Run a structured interview first.
3. Ask questions in small adaptive batches (normally 3–6). Ask only questions whose answers can change scope, requirements, priority, risk, or success criteria.
4. After each batch, maintain four buckets: **Confirmed**, **Assumptions**, **Open decisions**, **Unknowns**.
5. Resolve high-impact unknowns before labeling documents final. If the user chooses to proceed anyway, mark unresolved items explicitly as `TBD`—never fabricate them.
6. Build the BRD before the PRD so product requirements can trace to business outcomes.
7. Keep architecture, code structure, frameworks, database design, API design, and implementation plans out of the BRD/PRD unless they are genuine constraints. Those belong in technical/design documentation.
8. Keep project status, sprint progress, tickets, and temporary implementation notes out of these documents.

## Workflow

### 1. Select mode
Choose one: **Discover**, **Draft**, **Review**, or **Update**. For Discover/Draft, read [references/interview-guide.md](references/interview-guide.md).

### 2. Establish requirements ledger
Capture each statement as confirmed fact, assumption, open decision, or unknown. Identify conflicts immediately and ask the user to resolve material ones.

### 3. Produce BRD
Use [references/brd-template.md](references/brd-template.md). Focus on business need, objectives, stakeholders, value, boundaries, business rules, constraints, risks, success measures, and high-level business requirements.

### 4. Produce PRD
Use [references/prd-template.md](references/prd-template.md). Derive the product definition from the approved/confirmed BRD: users, use cases, journeys, features, functional requirements, non-functional requirements, data, integrations, permissions, edge cases, analytics, acceptance criteria, MVP, and future scope.

### 5. Preserve traceability
Use stable IDs and map downstream requirements upward:
- `BO-###` business objective
- `BR-###` business requirement
- `UR-###` user/stakeholder requirement
- `FR-###` functional requirement
- `NFR-###` non-functional requirement
- `DR-###` data requirement
- `IR-###` integration requirement
- `TR-###` transition requirement

Every material PRD requirement should trace to at least one user/stakeholder need or business objective.

### 6. Validate before finalizing
Read [references/quality-gates.md](references/quality-gates.md). A requirement must be necessary, singular, clear, unambiguous, feasible when known, measurable/verifiable, traceable, and implementation-neutral unless a constraint requires otherwise.

### 7. Deliver
Provide:
- `BRD.md`
- `PRD.md`
- a short **Open Questions / Decisions** section if anything remains unresolved
- a **Traceability Matrix** when the project is medium/large or when requested

Do not call the documents “final” while high-impact `TBD`s remain.

## Adaptation rule

Do not force identical questions on every product. Adapt discovery to the software domain (SaaS, marketplace, gaming, fintech, healthcare, AI, mobile, internal tool, developer platform, etc.) using [references/interview-guide.md](references/interview-guide.md). Domain-specific rules and regulations are requirements, not optional notes.

## Common failures

- Writing features before understanding the problem → return to business/user discovery.
- Mixing BRD and PRD → move “why/outcome” to BRD and “product behavior” to PRD.
- Vague requirements (“fast”, “secure”, “easy”) → define measurable targets or mark TBD.
- Treating assumptions as facts → label and validate them.
- Over-specifying implementation → restate as an outcome/capability or move to design docs.
- Asking a giant questionnaire → ask the highest-value questions first and iterate.
