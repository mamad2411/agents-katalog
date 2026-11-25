---
name: "message-bus-selector"
pack: "enterprise-architecture-integration-pack"
purpose: "Choose an appropriate message bus or event backbone pattern based on integration scale, latency, delivery guarantees, and governance."
inputs: ["integration scale", "eventing needs", "delivery requirements", "tooling/governance constraints"]
outputs: ["message bus recommendation", "selection rationale", "delivery/ops caveats", "next design steps"]
handoffs: ["publish-subscribe-designer", "environment-topology-planner", "ci-cd-readiness-checker"]
---
# message-bus-selector

## Purpose
Choose an appropriate message bus or event backbone pattern based on integration scale, latency, delivery guarantees, and governance.

## Expected inputs
- integration scale
- eventing needs
- delivery requirements
- tooling/governance constraints

## Deliverables
- message bus recommendation
- selection rationale
- delivery/ops caveats
- next design steps

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
- publish-subscribe-designer
- environment-topology-planner
- ci-cd-readiness-checker
