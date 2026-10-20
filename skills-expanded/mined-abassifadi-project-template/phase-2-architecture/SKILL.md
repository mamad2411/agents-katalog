---
name: phase-2-architecture
description: Phase 2 of the development cycle. Turns the approved product spec into an architecture — system design, technology decisions recorded as ADRs, C4 diagrams, data model, API contract, and threat model — then has the architecture-reviewer agent check it.
disable-model-invocation: true
---

# Phase 2 — Spec → Architecture

Input: `docs/spec/PRODUCT_SPEC.md`. If it's missing or not `Approved`, stop and tell the user to run `/phase-1-spec` first.

Goal: decide *how* to build it, and write the decisions down. Still no application code.

## Steps

```
Phase 2 progress:
- [ ] 1. System design            → docs/architecture/ARCHITECTURE.md
- [ ] 2. Key decisions            → docs/adr/NNNN-*.md
- [ ] 3. Diagrams                 → in ARCHITECTURE.md (Mermaid C4)
- [ ] 4. Data model               → docs/architecture/DATA_MODEL.md
- [ ] 5. API contract             → docs/api/ (openapi.yaml or equivalent)
- [ ] 6. Threat model             → docs/security/THREAT_MODEL.md
- [ ] 7. Review with the architecture-reviewer agent
- [ ] 8. User approval
```

**1. System design.** Follow the `designing-systems` skill. Turn the spec's NFRs into measurable targets, estimate capacity, and compare 2–3 options. **Default to the simplest architecture that meets the spec.** For a new product with a small team, that's usually a modular monolith with one relational database. Write the result to `docs/architecture/ARCHITECTURE.md`.

**2. Decisions.** Follow `writing-adrs`. Create `docs/adr/0001-…` onward, one ADR per decision, at minimum:
- language and framework (backend, and frontend if there is one)
- database
- hosting and deployment target
- authentication approach
- the architecture style itself

Present the stack options to the user with the trade-offs, and let the user choose. Record the user's choice.

**3. Diagrams.** Follow `modeling-c4-architecture`: add a System Context and a Container diagram to ARCHITECTURE.md.

**4. Data model.** Follow `designing-data-models`. List the entities, relationships, key constraints, and indexes, driven by the user stories. Write to `docs/architecture/DATA_MODEL.md`.

**5. API.** Follow `designing-apis`. Write the contract for the endpoints the Must-have stories need, for example `docs/api/openapi.yaml`.

**6. Threat model.** Follow `threat-modeling` for the flows that involve login, payments, personal data, or file uploads. Write to `docs/security/THREAT_MODEL.md`. Any mitigations become requirements for Phase 3.

**7. Review.** Use the **architecture-reviewer** agent on `docs/architecture/` and `docs/adr/`. Fix the High risks. List the rest under "Open risks" in ARCHITECTURE.md.

**8. Approve.** Summarize the architecture for the user in under 15 lines: the stack, the main components, and the top risks. Ask for approval. When approved, set `Status: Approved` in ARCHITECTURE.md and set each ADR to `accepted`.

Finish with: "Next: `/phase-3-plan`".
