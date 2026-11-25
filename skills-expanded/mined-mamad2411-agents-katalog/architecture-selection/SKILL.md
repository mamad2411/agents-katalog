---
name: architecture-selection
description: Architecture style selection, design documentation, and cost-aware design. Use when starting a new system or major component, deciding between monolith vs microservices vs serverless, choosing between layered/hexagonal/event-driven/pipeline styles, writing a design doc or RFC, or evaluating the cost implications of an architectural choice. Covers style trade-offs (fits-when / does-not-fit-when), a context-based decision rubric, ADR and RFC templates, and cost as an architectural constraint (build-vs-buy, sync-vs-async, dedicated-vs-shared). Does not cover cloud-provider-specific services.
---

# Architecture Selection

Architecture decisions are hard to reverse. The cost of a wrong choice compounds over time — not because the choice itself was wrong, but because the system grows in a direction that the choice made hard to change.

The goal of this skill is not to recommend an architecture. It is to surface the trade-offs so the right choice can be made with the actual context in mind.

For architecture style trade-offs see [styles.md](styles.md).
For the context-based decision rubric see [decision-rubric.md](decision-rubric.md).
For Architecture Decision Records see [adrs.md](adrs.md).
For design documents (RFCs) see [design-docs.md](design-docs.md).
For cost as an architectural constraint see [cost-awareness.md](cost-awareness.md).

## The most dangerous question

"What architecture should we use?" is the wrong question. The right questions are:

- What are the actual constraints on this system (team size, release cadence, consistency requirements, operational maturity)?
- What does the system need to do in 12 months that it does not do today, and how much of that can we anticipate?
- What is the cost of being wrong, and how reversible is the decision?

Architecture is not a technical preference. It is a response to constraints.

## Distributed systems are a choice, not a default

A distributed system trades away simplicity, consistency, and debuggability in exchange for independent deployability, team autonomy, and the ability to scale components independently.

None of these benefits are free, and not all systems need them.

Before choosing a distributed architecture, ask: **what problem would a monolith not solve?** If the answer is not clear, start with the monolith.

## The fallacies of distributed computing

Commonly assumed and consistently wrong in distributed systems:
1. The network is reliable
2. Latency is zero
3. Bandwidth is infinite
4. The network is secure
5. Topology does not change
6. There is one administrator
7. Transport cost is zero
8. The network is homogeneous

These are design constraints, not theoretical concerns. Every distributed architecture must account for them.
