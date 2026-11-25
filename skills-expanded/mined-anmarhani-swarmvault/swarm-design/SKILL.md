---
name: swarm-design
description: System design phase — architecture, tech-stack options, module boundaries, data model, and ADRs from a validated SRS. Use after requirements are validated, when choosing a tech stack, designing system structure/APIs/data models, or recording an architecture decision.
---

# swarm-design — system design phase

**Gate:** requires a validated SRS (else route back to swarm-spec). Read the SRS and
feature specs first; the design must answer them, not your habits.

**Lane:** this is the standard, agent-driven lane — you propose, the user validates. If the
user wants to *own* the system rather than receive it (deep design, pseudocode, algorithm-level
planning, "developer mode"), hand the phase to **swarm-design-deep** instead; the two replace
each other and never run together.

## Produce, in order

1. **Tech stack** — options with trade-offs *measured against the NFRs* (not fashion),
   recommendation first; the user decides. Significant picks become ADRs.
2. **Decomposition** — modules/services with single responsibilities, boundaries, and
   data flow. Prefer deep modules behind simple interfaces. Mermaid diagrams for the
   system view and any non-obvious flow.
3. **Data model & contracts** — entities, relationships, API contracts where relevant.
4. **Cross-cutting strategy** — error handling, logging, testing approach fit for the
   stack.
5. **Milestone boundaries** — group FRs into build milestones; these become
   swarm-implement's ticket batches.

## Rules

- **Traceability table required:** every Must-FR ↦ component; every NFR ↦ one line on how
  the design satisfies it. Nothing silently dropped.
- **Options with recommendation** for anything that meaningfully affects cost, lock-in,
  or complexity — never decide those silently (mode: in auto, only stack-level choices
  already delegated by the user proceed without asking; queue the rest).
- **Simplicity doctrine:** every moving part justifies itself; prefer known patterns
  (refactoring.guru names) over invention; when two designs both satisfy the NFRs, ship
  the smaller one.
- Each significant decision → `50 Decisions/<P>/ADR-NNN-<slug>.md` (template:
  `90 Templates/decision.md`): context, options, decision, consequences, FR/NFR links.

## Output & gate

`docs/design.md` (human lane) + ADRs, mirrored to the vault by sync. End with the user
validation gate (gated mode) or a self-check against the traceability table (auto mode);
update flow-state to `phase: design-ui` (if the SRS declares an interface) or
`phase: tickets`.

---
*Influences: Jeffallan's architecture-designer & api-designer; Pocock's codebase-design &
domain-modeling; refactoring.guru; Nygard ADRs — see CREDITS.md.*
