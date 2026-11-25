---
name: "soa-suitability-reviewer"
pack: "enterprise-architecture-integration-pack"
purpose: "Assess whether service-oriented patterns are justified for the system based on autonomy, reuse, integration needs, and operational cost."
inputs: ["system boundaries", "integration needs", "reuse expectations", "operational constraints"]
outputs: ["SOA fit assessment", "tradeoffs", "decision recommendation", "follow-up architecture work"]
handoffs: ["service-contract-designer", "esb-fit-reviewer", "rpc-vs-message-pattern-selector"]
---
# soa-suitability-reviewer

## Purpose
Assess whether service-oriented patterns are justified for the system based on autonomy, reuse, integration needs, and operational cost.

## Expected inputs
- system boundaries
- integration needs
- reuse expectations
- operational constraints

## Deliverables
- SOA fit assessment
- tradeoffs
- decision recommendation
- follow-up architecture work

## Trigger this skill when
- You need to make an enterprise or integration decision that spans more than a single codebase.
- Multiple systems, teams, environments, or governance constraints influence the design.
- A recommendation needs to be tied to enterprise reality rather than generic integration advice.

## Operating procedure
1. Clarify the system, estate, or cross-system workflow being assessed.
2. Separate facts, assumptions, constraints, and missing enterprise context.
3. Produce a context-specific analysis rather than a platform- or buzzword-driven recommendation.
4. Make tradeoffs explicit, especially around governance, ownership, runtime failure, and operational cost.
5. Recommend the next most useful architecture or delivery skill.

## Quality gates
- Recommendations acknowledge enterprise constraints, ownership, and operational consequences.
- Interfaces, dependencies, and environment implications are not hand-waved away.
- Assumptions and open questions are visible.
- Output is specific enough to inform architecture, integration, or release planning.

## Output style
- Be concrete and structured.
- Separate evidence, inference, and recommendation.
- Prefer explicit tradeoffs over single-answer absolutism.
- Use priority or severity where useful.

## Failure modes to avoid
- Do not recommend technology because it sounds enterprise-grade.
- Do not ignore team boundaries, operational maturity, or integration sprawl.
- Do not treat all workloads as equally suited to the same platform pattern.
- Do not hide uncertainty behind confident language.

## Minimum output skeleton
```md
## Summary
## Findings or proposal
## Evidence vs assumptions
## Risks or tradeoffs
## Recommended next skill
```

## Handoff targets
- service-contract-designer
- esb-fit-reviewer
- rpc-vs-message-pattern-selector
