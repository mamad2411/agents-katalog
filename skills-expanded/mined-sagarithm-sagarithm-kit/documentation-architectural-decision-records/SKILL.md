<!-- SAGARITHM:START - DO NOT EDIT DIRECTLY -->
---
id: "documentation.architectural-decision-records"
name: "Architectural Decision Records (ADRs)"
version: "1.2.0"
domain: "documentation"
description: "Author, update, and manage Architectural Decision Records (ADRs) using MADR 3.0 and quantitative decision matrices to record trade-offs."
triggers:
  - "Introducing a major technology or framework"
  - "Establishing a new architectural pattern or structural boundary"
  - "Making a significant trade-off affecting maintenance or performance"
  - "Evaluating competing technical alternatives"
prerequisites:
  - "architecture.system-design"
risk_profile: "medium"
---

# Architectural Decision Records (ADRs)

## Overview
This skill guides AI agents and engineers in capturing consequential architectural decisions as living, version-controlled records. ADRs preserve institutional memory, explain the *why* behind complex designs, and prevent recurring circular debates.

## Core Directives
1. **Identify Consequential Decisions**: Not every bug fix requires an ADR; write an ADR whenever a structural choice has long-term implications or accepts explicit trade-offs.
2. **Follow MADR Standards**: Structure ADRs with clear Context, Decision Drivers, Options, Outcome, and Trade-offs.
3. **Use Quantitative Matrices for Contested Choices**: When evaluating multiple competing technologies, employ a weighted decision matrix to anchor choices objectively.
4. **Record Both Pros and Cons**: A balanced decision record explicitly documents accepted downsides and operational costs.
5. **Immutable History**: Once an ADR is accepted, do not edit its historical decision text; create a new ADR that supersedes the prior one.

## 🛑 Anti-Rationalization Matrix

| Agent Excuse / Shortcut | Documentation Reality | Mandatory Action |
|---|---|---|
| *"We can document this technology choice later."* | Rationale is forgotten within weeks; future engineers will question why it was built this way. | Commit the ADR alongside the implementation PR. |
| *"The choice was obvious, no need to write options considered."* | Without documenting rejected alternatives, teams repeat the same debates repeatedly. | Document at least two viable alternatives and why they were rejected. |
| *"This architectural decision only affects this one file."* | If it introduces a new external dependency or state model, it affects the entire system. | Record any external dependency or protocol choice in `docs/adr/`. |

## Detailed Guidance
- [ADR Lifecycle & Structural Guidelines](references/adr-lifecycle-and-structure.md)
- [MADR 3.0 & Quantitative Decision Matrices](references/madr-and-decision-matrices.md)
- [Canonical ADR Sample](examples/canonical-adr-sample.md)
- [Quantitative Decision Matrix Sample](examples/quantitative-decision-matrix-sample.md)
- [ADR Authoring Checklist](checklists/adr-authoring-checklist.md)
<!-- SAGARITHM:END -->
