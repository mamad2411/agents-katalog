---
name: reasoning-strategies
description: Select reasoning structure and verification depth according to task risk and ambiguity. Use for planning, evaluation, governance, or review of reasoning strategies; do not use as framework-specific or provider-specific implementation guidance.
---
# Reasoning Strategies

## Purpose

Select reasoning structure and verification depth according to task risk and ambiguity.

## Problem Statement

Reasoning Strategies decisions often fail when teams optimize one visible concern while leaving ownership, evidence, dependencies, failure behavior, or change cost implicit.

## Core Concepts

- Outcome: the decision or behavior this capability must support.
- Boundary: what is inside scope, outside scope, and owned elsewhere.
- Evidence: requirements, measurements, risks, and uncertainty.
- Contract: inputs, outputs, invariants, and failure conditions.
- Evolution: compatibility, migration, reversibility, and review triggers.

## Engineering Principles

- Begin with explicit outcomes and accountable ownership.
- Match controls and rigor to evidenced impact and risk.
- Keep provider and framework choices outside the universal contract.
- Prefer observable, reversible decisions with clear failure handling.
- Record assumptions, alternatives, and conditions for reconsideration.

## Decision Framework

Evaluate the capability across outcome fit, ownership, risk, evidence quality, dependencies, compatibility, operability, security, reversibility, and verification. Reject options that satisfy local convenience while violating system constraints.

## Decision Tree

1. Is the outcome and primary owner explicit? If not, clarify first.
2. Are mandatory constraints, obligations, or invariants known? Record them.
3. Which options satisfy the contract without expanding ownership?
4. What failures, abuse cases, or operational limits matter?
5. Which option is simplest to verify, operate, and reverse?
6. What evidence and review trigger will confirm or revisit the decision?

## Best Practices

- Use authoritative inputs and traceable evidence.
- Define boundaries before selecting patterns.
- Separate required controls from optional improvements.
- Include degraded, exceptional, and recovery behavior.
- Make approval, escalation, and review criteria explicit.

## Common Mistakes

- Choosing a solution before defining the decision.
- Treating popularity or defaults as evidence.
- Hiding dependencies, exceptions, or ownership gaps.
- Confusing documentation with verification.
- Ignoring migration, rollback, or retirement.

## Anti-patterns

- Provider-driven design presented as a universal rule.
- Controls without a stated threat, risk, or outcome.
- Metrics without definitions or decision use.
- Review checklists that cannot change the decision.
- Shared ownership with no accountable primary owner.

## Review Checklist

- Is the outcome, scope, and primary owner explicit?
- Are assumptions, alternatives, and evidence recorded?
- Are dependencies and compatibility constraints resolved?
- Are failure, recovery, and escalation paths defined?
- Is the decision provider-independent and reviewable?

## Quality Checklist

- Clear and internally consistent terminology.
- Traceable inputs and conclusions.
- Proportionate risk and verification depth.
- No hidden implementation or provider assumptions.
- Defined expected outcomes and reconsideration triggers.

## Related Skills

- `official.ai.prompt-evaluation`
- `official.ai.model-evaluation`
- `official.ai.context-optimization`
- `official.ai.agent-collaboration`

## Compatible Agents

- `ai`
- `architecture`
- `security`
- `testing`
- `documentation`

## Compatible Sub-Agents

- `ai-reasoning-strategy`

## Primary Owner Agent

- `ai`

## Primary Owner Sub-Agent

- `ai-reasoning-strategy`

## Secondary Owners

- `architecture`
- `security`
- `testing`
- `documentation`

## Consumer Agents

- `ai`
- `architecture`
- `security`
- `testing`
- `documentation`

## Prerequisites

- Approved goals and decision authority.
- Relevant architecture, policy, and domain constraints.
- Evidence proportionate to expected impact.

## Expected Outcomes

- A bounded decision with one accountable owner.
- Explicit trade-offs, risks, dependencies, and compatibility.
- Review and quality criteria suitable for later verification.
- Clear escalation and reconsideration conditions.

## Learning Resources

- OniRoute architecture, Skill Specification, and Official Skill Guide.
- Relevant open standards and primary technical documentation.
- `references.md` for research attribution; source wording is not reproduced.

## Version History

- 1.0.0 — Initial Official OniRoute release.
