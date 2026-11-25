---
name: product-governance
description: Use when creating or maintaining docs/PRD.md, product requirements, product scope, user stories, success metrics, or product source-of-truth documents for OpenArc repositories.
---

# Product Governance

Use this skill when creating or updating `docs/PRD.md`.

## Goal

Build a product source of truth that is clear enough for agents to implement against without inventing product intent.

Use Clarification Gate output when available. If the goal, audience, non-goals, constraints, or success criteria are still unclear, run `clarification-gate` before creating or rewriting `docs/PRD.md`.

## Fixed Clarification Flow

If the user has not clearly specified the product direction, follow this flow before writing:

1. Discover existing signals: README, docs, specs, routes, UI copy, package metadata, tests, issues, and assets.
2. Extract knowns, unknowns, contradictions, and risky assumptions.
3. Ask focused questions for material gaps only.
4. Draft PRD sections from confirmed information.
5. Cross-check with `docs/DESIGN.md`, `docs/BRAND.md`, and latest `docs/specs/*` when present.
6. Confirm unresolved product decisions with the user.
7. Create or patch `docs/PRD.md`.

## PRD Owns

- Product background
- Problem statement
- Audience
- Goals and non-goals
- User stories
- Functional requirements
- UX requirements
- Data requirements
- AI / prompt requirements
- Performance and security requirements
- Success metrics
- Risks and open questions

## Rules

- Do not fill core product strategy with generic guesses.
- Do not write PRD requirements from ambiguous goals; clarify first or record unresolved questions explicitly.
- Preserve existing product language when it is coherent.
- Keep requirements testable.
- Link features to specs instead of duplicating detailed implementation plans.
- Use `templates/PRD.template.md` for new documents.
