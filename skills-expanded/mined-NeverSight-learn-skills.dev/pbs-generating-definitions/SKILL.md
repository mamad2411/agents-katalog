---
name: pbs-generating-definitions
description: "Use after both exploration syntheses are approved, to generate all project definition documents and prepare for construction"
---

# Generating Definitions

## Overview

Generate ALL project definition documents from the exploration syntheses. This bridges Etapa 0 (exploration) to Etapa 2 (construction) by producing the `.pbs-framework/` documents that guide the entire build.

**Core principle:** Documents are deliberately incomplete — they capture what is known TODAY. The detail comes phase by phase. Over-specifying upfront kills agility and invites hallucination.

**Announce at start:** "I'm using the pbs-generating-definitions skill to generate project definitions from the exploration syntheses."

## When to Use

- Both exploration syntheses (brainstorming + discovery) are approved by the human
- Re-generating definitions after the human found issues in a previous generation
- Generating definitions for a project that skipped formal exploration but has equivalent context

## The Process

### Step 1: Read Exploration Syntheses

1. Read the Brainstorming Synthesis (provided by the human or at `.pbs-framework/exploration/brainstorming-synthesis.md`)
2. Read the Discovery Synthesis (provided by the human or at `.pbs-framework/exploration/discovery-synthesis.md`)
3. Note: open questions, assumptions to validate, and decisions already taken

### Step 1b: Set Framework Language

Check if `AGENTS.md` already has a `framework_language` field.
- If yes → use that language for all `.pbs-framework/` documents
- If no → read the brainstorming synthesis Section 8 (Framework Language) and set it in the generated AGENTS.md

This applies ONLY to `.pbs-framework/` documents. Code, READMEs, and project docs follow whatever conventions the project uses.

### Step 1c: Read Code Conventions

Read the Discovery Synthesis Section 7 (Dev environment and tools) for code conventions:
- **Package manager** — which package manager the project uses (npm/pnpm/yarn/pip/poetry/etc.)
- **Naming convention** — which naming convention the project follows (camelCase/snake_case/PascalCase/etc.)

Include these in the generated AGENTS.md under the "Convenciones de Código" section, alongside any other project conventions.

### Step 2: Create Directory Structure

```
.pbs-framework/
├── 00-project-brief.md
├── 01-system-overview.md
├── 02-technical-design.md
├── 03-decision-log.md
├── 04-roadmap.md
└── phases/
    └── (empty — created during phase-planning)
```

### Step 3: Generate Documents

Generate each document in order. Be deliberate about what you KNOW vs what you DON'T KNOW YET.

#### `00-project-brief.md` — 1 page max

```markdown
# Project Brief

## Problema
[2-3 sentences: what concrete problem this project solves]

## Tipo de Proyecto
- [ ] POC (Proof of Concept): validate technical feasibility
- [ ] MVP (Minimum Viable Product): validate with real users

## Alcance
### Incluido
- [what IS in scope]

### Excluido
- [what is NOT in scope, even if related]

## Criterio de Exito
[Minimum proof that this works]

## Restricciones Tecnicas
- Lenguaje/stack:
- Dependencias externas:
- Restricciones de seguridad:

## Riesgos Conocidos
| Riesgo | Impacto | Mitigacion |
|--------|---------|------------|
```

#### `01-system-overview.md` — LIGHT, only what's known

```markdown
# System Overview

## Que hace este sistema
[2-3 paragraphs: what it does, for whom, main flow]

## Entidades Principales
| Entidad | Descripcion | Fuente de datos |
|---------|-------------|-----------------|

## Capacidades del Sistema
| ID | Capacidad | Prioridad | Fase estimada |
|----|-----------|-----------|---------------|
| CAP-1 | [verb-based description] | core/nice-to-have | Phase N |

## Integraciones Externas
| Servicio | Proposito | Autenticacion | Rate Limits |
|----------|-----------|---------------|-------------|
```

Do NOT include: edge cases, detailed contracts between modules, exhaustive actor lists. Those come per-phase in the spec.

#### `02-technical-design.md` — LIGHT, only big decisions

```markdown
# Technical Design

## Stack
- Lenguaje:
- Framework:
- Base de datos:
- Testing:

## Modulos Principales
| Modulo | Responsabilidad | Dependencias |
|--------|-----------------|-------------|

## Flujo de Datos Principal
[Description or simple diagram of how data flows through the system]

## Lo que se definira por fase
- Contratos detallados entre modulos → per-phase spec
- Edge cases y error handling → per-phase spec
- Performance optimizations → when relevant
```

#### `03-decision-log.md` — minimum 3-5 entries

```markdown
# Decision Log

| # | Fecha | Decision | Contexto | Alternativas | Fase |
|---|-------|----------|----------|-------------- |------|

## Detailed Entries

### DEC-001: [Title]
- **Contexto:** [what motivated this decision]
- **Decision:** [what was decided]
- **Razon:** [why this option]
- **Alternativas descartadas:** [what else was considered]
- **Consecuencias:** [implications for the project]
- **Reversible:** Si / No / Parcialmente
```

Populate with decisions from the Discovery Synthesis. Every technology choice, API selection, and architectural decision should be here.

#### `04-roadmap.md` — ALL phases, only Phase 1 detailed

```markdown
# Roadmap

## Objetivo Final
[What will be achieved when all phases are complete]

## Fases

### Fase 1: [Name] — DETALLADA
- **Objetivo:** [what this phase achieves]
- **Entregable:** [verifiable deliverable]
- **Estimacion:** [X days]
- **Estado:** pendiente
- **Dependencias:** ninguna
- **Tareas:** (high-level, will be detailed by phase-planning)
  - T-01: [description]
  - T-02: [description]
  - ...

### Fase 2: [Name] — DEFINIDA
- **Objetivo:** [what this phase achieves]
- **Entregable:** [verifiable deliverable]
- **Estimacion:** [X days]
- **Estado:** pendiente
- **Dependencias:** [what from Phase 1]
- → Se detallara al cerrar Fase 1

### Fase 3: [Name] — ESBOZADA
- **Objetivo:** [what this phase achieves]
- **Entregable:** [expected deliverable]
- **Estimacion:** [approximate range]
- **Estado:** pendiente
- **Dependencias:** [what from Phase 2]
- → Se definira al cerrar Fase 2

...
```

**Roadmap rules:**
- ALL phases exist from day 1 — at minimum: objective + deliverable
- Only Phase 1 has concrete tasks
- Each phase should be completable in 1-3 days
- Phases can be reordered, merged, or dropped as the project evolves
- 3-6 phases is the sweet spot. Under 3 → probably too coarse. Over 10 → probably too granular.

### Step 4: Verify

**REQUIRED:** Use superpowers:verification-before-completion

- [ ] All 5 documents exist in `.pbs-framework/`
- [ ] `phases/` directory exists
- [ ] Decision Log has at least 3 entries from the discovery
- [ ] Roadmap has ALL phases with at least objective + deliverable
- [ ] Phase 1 has concrete tasks with high-level descriptions
- [ ] No document tries to define detailed contracts or edge cases (those come per-phase)

### Step 5: Present Summary

Report to the human:
- Total documents created (should be 5)
- Estimated reading time for all documents combined (target: < 30 minutes)
- Ambiguities or open questions the human should resolve before starting Phase 1
- Any decisions that need human input (suggest adding to Decision Log)

<HARD-GATE>
## Definition of Ready

Before construction can begin, ALL of the following must be true:

1. Human can read ALL documents in under 30 minutes
2. Phase 1 in the roadmap has concrete tasks with high-level Definition of Done
3. No blocking ambiguities remain unanswered
4. Each phase in the roadmap is 1-3 days of work
5. The human has explicitly confirmed: "Definitions are ready"

If any condition fails → iterate with the human until all conditions are met.
Do NOT proceed to phase-planning until the human confirms readiness.
</HARD-GATE>

## Common Mistakes

- **Over-specifying upfront** — documents should capture what's known TODAY. Detailed contracts come per-phase.
- **Decision Log with zero entries** — the discovery produced decisions. If none are logged, you missed them.
- **Roadmap with only 1-2 phases** — likely too coarse. Split by deliverable boundary.
- **Phase 1 without concrete tasks** — the implementing agent needs explicit direction, not vague goals.

## Red Flags

- Documents are too detailed upfront → Over-specification kills agility. Capture only what's known TODAY.
- Missing "what we don't know yet" markers → Unknowns should be explicit, not hidden.
- Roadmap with only 1-2 phases → Probably too coarse. Break them down.
- Roadmap with 10+ phases → Probably too granular. Merge related phases.
- System overview defines edge cases → Edge cases belong in per-phase specs, not here.
- Technical design has full module contracts → Contracts are per-phase. Only list modules and responsibilities here.
- Decision Log is empty → The discovery produced decisions. If none are logged, something was missed.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Let me detail all contracts now to save time later" | Contracts change as you build. Detail them per-phase. |
| "Phase 1 is obvious, I don't need tasks" | Write them. The implementing agent needs explicit direction. |
| "The roadmap only has 2 phases" | You're probably bundling too much. Split by deliverable. |
| "This edge case is important to capture now" | Important for which phase? Put it there, not in the overview. |
| "30 minutes reading time is too strict" | If the human can't read it all, the documents are too long. Trim. |

## Integration

**Called after:**
- pbs-exploration-discovery — both syntheses approved by human

**Required skills:**
- **REQUIRED:** superpowers:verification-before-completion — verify all docs exist and are complete

**Calls next:**
- pbs-phase-planning — for Phase 1, after human confirms Definition of Ready
