---
name: versioning-fundamentals
description: Manage change through explicit compatibility and evolution rules. Use when planning or reviewing versioning fundamentals; do not use as provider-specific implementation guidance.
---
# Versioning Fundamentals

## Purpose

Manage change through explicit compatibility and evolution rules.

## Problem Statement

Without a shared decision model, versioning fundamentals is often driven by habit, defaults, or isolated rules. That produces inconsistent boundaries, hidden trade-offs, and weak reviewability.

## When to Use

Use this Skill when requirements, architecture, reviews, or change plans require decisions about versioning fundamentals. Apply it before implementation choices become expensive to reverse.

## When NOT to Use

Do not use it as a substitute for product requirements, authoritative provider documentation, implementation instructions, or accountable Agent decisions. Do not apply every practice mechanically.

## Core Concepts

- Scope: define the decision boundary and accountable owner.
- Contract: state inputs, outputs, invariants, and failure behavior.
- Evidence: use requirements, measurements, risks, and consumer needs.
- Evolution: plan compatibility, migration, and rollback.
- Assurance: define how correctness and quality will be reviewed.

## Engineering Principles

- Start from explicit outcomes and constraints.
- Keep ownership and boundaries visible.
- Prefer evidence over convention or vendor defaults.
- Make failure, change, and operational consequences reviewable.
- Choose the simplest approach that satisfies required qualities.

## Decision Tree

1. Is the desired outcome and owner explicit? If not, clarify first.
2. Are there hard constraints or invariants? Reject options that violate them.
3. Is the decision externally visible or difficult to reverse? Strengthen contracts and migration planning.
4. Is there evidence of scale, risk, or complexity? Match rigor to evidence.
5. Can a simpler option satisfy the requirements? Prefer it and document why.
6. Define verification and review criteria before approval.

## Best Practices

- Express decisions through outcomes, constraints, and trade-offs.
- Separate universal principles from provider choices.
- Define normal, boundary, and failure cases.
- Record assumptions and invalidation evidence.
- Review dependencies and adjacent ownership.

## Common Mistakes

- Choosing a pattern before understanding the problem.
- Treating defaults as requirements.
- Optimizing for hypothetical scale without measurements.
- Hiding failure behavior or migration cost.
- Combining unrelated responsibilities.

## Anti-patterns

- Vendor-driven architecture without a portability decision.
- Unbounded best-practice checklists.
- Implicit ownership or undocumented exceptions.
- Irreversible change without rollback planning.
- Success criteria that cannot be verified.

## Related Skills

- `official.foundation.rest-fundamentals`
- `official.foundation.api-design-fundamentals`
- `official.foundation.authentication-fundamentals`
- `official.foundation.authorization-fundamentals`

## Compatible Agents

- `architecture`
- `backend`
- `frontend`
- `database`
- `security`
- `testing`

## Compatible Sub-Agents

- `architecture-technical-standards`

## Prerequisites

- Approved requirements and decision authority.
- Relevant architecture, risk, and quality constraints.
- Evidence appropriate to expected impact.

## Expected Outcomes

- A bounded, provider-independent decision.
- Explicit alternatives, trade-offs, assumptions, and risks.
- Defined compatibility, failure, and verification expectations.
- Clear ownership and follow-up actions.

## Learning Resources

- OniRoute architecture and Skill Specification.
- Relevant open standards and primary technical documentation.
- `references.md` for community research attribution only.

## Version History

- 1.0.0 — Initial Official OniRoute release.
