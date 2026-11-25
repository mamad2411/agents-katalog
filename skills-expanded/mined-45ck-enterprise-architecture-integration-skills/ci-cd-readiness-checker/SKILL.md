---
name: "ci-cd-readiness-checker"
pack: "enterprise-architecture-integration-pack"
purpose: "Check whether architecture, environments, governance, and testing are ready for reliable CI/CD and controlled releases."
inputs: ["repo/build setup", "test coverage", "environment model", "release governance"]
outputs: ["CI/CD readiness report", "blocking issues", "improvement backlog", "readiness verdict"]
handoffs: ["environment-topology-planner", "container-vs-vm-advisor", "public-private-hybrid-cloud-selector"]
---
# ci-cd-readiness-checker

## Purpose
Check whether architecture, environments, governance, and testing are ready for reliable CI/CD and controlled releases.

## Expected inputs
- repo/build setup
- test coverage
- environment model
- release governance

## Deliverables
- CI/CD readiness report
- blocking issues
- improvement backlog
- readiness verdict

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
- environment-topology-planner
- container-vs-vm-advisor
- public-private-hybrid-cloud-selector
