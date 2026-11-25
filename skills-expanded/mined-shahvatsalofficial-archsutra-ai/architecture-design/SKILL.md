---
name: architecture-design
description: Design the architecture of a new system or feature from requirements. Captures numeric non-functional targets, compares two or three options with weighted scoring, decides with an ADR, and produces C4 diagrams, data model, API boundaries, deployment view and a thin-slice roadmap. Use this skill whenever the user says design, architect, "how should we build", HLD or LLD, tech-stack choice, monolith versus microservices, or asks for diagrams or an ADR for something that does not exist yet, even if they only describe a product idea. Do not use it to review existing code (use architecture-audit) or to plan a migration (use architecture-modernization).
license: Apache-2.0
compatibility: Works with plain conversation and file tools. Diagrams are Mermaid text. The archsutra CLI is optional and not needed for design.
---
# Architecture Design

Turn requirements into a justified, buildable architecture that the team can start on this week.

## Why this skill is built the way it is

- Most bad architectures come from unstated numbers, not from bad technology choices. A design for "fast and scalable" cannot be checked; a design for "p95 under 300 ms at 50 requests per second, 99.9% availability" can.
- Teams over-build. Every extra moving part is operational cost forever, so the default is the simplest style that meets the stated targets, and each addition needs a reason.
- Decisions rot when their reasons are lost. So choices end in an ADR with the options that were rejected.

## Workflow

1. **Capture requirements as numbers.** Use [references/nfr-checklist.md](references/nfr-checklist.md). Record users, scale, data sensitivity, latency, availability, recovery targets (RTO, RPO), budget, team size, deadlines, compliance, existing systems. Any number the user did not give is `unknown`: ask once, then continue with a labeled assumption. Do not invent figures.
2. **Name the hard problem.** One or two sentences on what makes this design difficult (for example "strong consistency across two regions" or "bursty uploads"). Everything else should be boring.
3. **Generate two or three viable options** (for example modular monolith, event-driven services, serverless). Score them against weighted criteria with [references/options-scoring.md](references/options-scoring.md). Show how the winner changes if the two weakest assumptions are wrong.
4. **Decide with an ADR** using [references/adr-template.md](references/adr-template.md): context, options, decision, consequences, revisit triggers.
5. **Model it.** Produce only the views the audience needs: C4 level 1 and 2 (level 3 for the part that is hard), one sequence diagram for the critical flow, a data model with ownership and consistency, API boundaries, the auth model, and a deployment view. Use [references/design-doc-template.md](references/design-doc-template.md).
6. **Plan operations early.** Observability, SLOs, failure modes, backup and restore, cost envelope. State the pricing source and date for every cost figure; never quote live prices from memory.
7. **Roadmap as a thin vertical slice first**, then milestones, each with an acceptance test and its biggest risk.

## Rules that keep the design honest

- **Label claims** `observed`, `inferred`, `proposed` or `unknown`. In a design, most things are `proposed`; say so, and cite requirements by number.
- **Justify every added component.** If you cannot say what breaks without it, remove it.
- **Defer reversible choices, decide irreversible ones carefully.** Data models, public APIs and identity are hard to change; frameworks usually are not.
- **Diagrams must trace to requirements.** A box with no requirement behind it is decoration.
- **Do not claim certification** (security, privacy, compliance). Name frameworks as review references only.

## Files the reader gets

Write the design as both `docs/architecture/design.md` and `docs/architecture/design.html`. Save the Markdown, then run `archsutra html docs/architecture/design.md` so the HTML page is generated (headings, tables, diagrams). Do not hand-write HTML. Do not leave the design only in chat. ADRs in the same document follow the same pair.

## Hand-offs

Security-critical flows go to threat-modeling. Before sharing, run architecture-verification. When the design replaces an existing system, continue with architecture-modernization.
