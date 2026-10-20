---
name: ai-agent-fundamentals
description: Design bounded AI agents with explicit authority, tools, state, and oversight. Use when planning or reviewing ai agent fundamentals; do not use as provider-specific implementation guidance.
---
# AI Agent Fundamentals

## Purpose

Design bounded AI agents with explicit authority, tools, state, and oversight.

## Problem Statement

Without a shared decision model, ai agent fundamentals is often driven by habit or defaults, producing inconsistent boundaries and hidden trade-offs.

## When to Use

Use when requirements, architecture, reviews, or change plans require decisions about ai agent fundamentals, before implementation choices become expensive to reverse.

## When NOT to Use

Do not substitute it for product requirements, provider documentation, implementation instructions, or accountable Agent decisions.

## Core Concepts

- Scope and accountable ownership.
- Inputs, outputs, invariants, and failure contracts.
- Evidence from requirements, measurements, risks, and consumers.
- Compatibility, migration, and rollback.
- Verification and review criteria.

## Engineering Principles

- Start from explicit outcomes and constraints.
- Keep boundaries visible.
- Prefer evidence over defaults.
- Make failure and change consequences reviewable.
- Choose the simplest adequate approach.

## Decision Tree

1. Clarify outcome and owner.
2. Record hard constraints and invariants.
3. Assess visibility and reversibility.
4. Match rigor to evidenced scale and risk.
5. Prefer the simplest adequate option.
6. Define verification before approval.

## Best Practices

- State outcomes, constraints, and trade-offs.
- Separate principles from providers.
- Cover normal, boundary, and failure cases.
- Record assumptions and invalidation evidence.
- Review dependencies and adjacent ownership.

## Common Mistakes

- Selecting patterns before understanding the problem.
- Treating defaults as requirements.
- Optimizing for hypothetical scale.
- Hiding failure or migration cost.
- Combining unrelated responsibilities.

## Anti-patterns

- Vendor-driven architecture without a portability decision.
- Unbounded best-practice checklists.
- Implicit ownership.
- Irreversible change without rollback planning.
- Unverifiable success criteria.

## Related Skills

- Review adjacent Wave 1 Official Skills in the same domain.

## Compatible Agents

- `ai`
- `architecture`
- `security`
- `testing`

## Compatible Sub-Agents

- `ai-agent-orchestration`

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
- `references.md` for research attribution only.

## Version History

- 1.0.0 — Initial Official OniRoute release.
