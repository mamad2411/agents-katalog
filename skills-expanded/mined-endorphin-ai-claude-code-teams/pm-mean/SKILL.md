---
name: pm-mean
description: "Product management for MEAN stack apps. Use when writing PRDs, defining features, acceptance criteria, or reviewing deliverables for MongoDB + Express + React + Node.js projects."
---

# PM Mean

## Purpose

Write PRDs (Product Requirements Documents) for MEAN stack web applications and validate deliverables against acceptance criteria. This skill bridges user requests and developer execution.

## Key Patterns

### PRD Structure
Every PRD must include:
1. **Overview** — What the app does, who it's for, core value proposition
2. **Features** — Numbered list (F1, F2...), each with: description, user story, acceptance criteria
3. **Data Model Summary** — Key entities and relationships (high-level, not full schema)
4. **API Summary** — Key endpoints grouped by resource (high-level, not full contracts)
5. **UI Summary** — Key pages/views and user flows (high-level, not full component tree)
6. **Technical Constraints** — Auth method (JWT for MEAN), deployment target, performance requirements
7. **Priorities** — MoSCoW (Must/Should/Could/Won't) for features

### User Story Format
As a [role], I want to [action] so that [benefit].
Acceptance Criteria:
- Given [context], when [action], then [result]

### Acceptance Review Pattern
When reviewing deliverables (final pipeline phase):
1. Read the original PRD
2. For each feature: check if acceptance criteria are met
3. Produce a pass/fail verdict per feature
4. Flag missing features, partial implementations, and deviations

## Conventions

- Write for developers, not stakeholders — be specific, not vague
- Every feature MUST have testable acceptance criteria (Given/When/Then)
- Use REST resource naming: plural nouns, lowercase (/api/users, /api/posts)
- Specify auth requirements per feature (public, authenticated, admin)
- Include error scenarios in acceptance criteria
- Number features for easy reference (F1, F2, F3...)

## Knowledge Strategy

- **Patterns to capture:** Successful PRD structures, common MEAN features (auth, CRUD, real-time), good acceptance criteria examples
- **Examples to collect:** Completed PRDs that led to successful implementations
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
