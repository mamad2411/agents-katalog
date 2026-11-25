---
name: pbs-phase-closure
description: "Use after phase validation passes, to generate the closure report, update global documents, and prepare the next phase"
---

# Phase Closure

## Overview

Close a phase formally: generate the closure report, update all global documents, and detail the next phase. This is the "CONSOLIDAR" step — it produces the context handoff that the next phase depends on.

**Core principle:** The closure report is the bridge between phases. It must reflect REALITY — what was actually built — not the plan. Without it, the next phase starts blind.

**Announce at start:** "I'm using the pbs-phase-closure skill to close phase [N] and prepare the handoff."

## When to Use

- Phase validation passed (PASS status)
- Human approved the validation report
- Ready to formalize what happened and move forward

## Input

**Phase artifacts (required):**
- `.pbs-framework/phases/phase-XX/spec.md` — what was planned
- `.pbs-framework/phases/phase-XX/tasks.md` — how it was broken down
- `.pbs-framework/phases/phase-XX/validation-report.md` — what was verified
- Git log for the phase's commits — what actually changed

**Global documents (for updating):**
- `.pbs-framework/03-decision-log.md`
- `.pbs-framework/04-roadmap.md`
- `.pbs-framework/05-tech-debt-register.md` (if exists)
- `.pbs-framework/06-architecture-snapshot.md` (if exists)

## The Process

### Step 1: Load Phase Artifacts

Read all artifacts from the completed phase:
1. `.pbs-framework/phases/phase-XX/spec.md` — what was planned
2. `.pbs-framework/phases/phase-XX/tasks.md` — how it was broken down
3. `.pbs-framework/phases/phase-XX/validation-report.md` — what was verified
4. Run `git log` for the phase's commits — what actually changed

### Step 2: Load Global Documents

Read these for updating:
1. `.pbs-framework/03-decision-log.md`
2. `.pbs-framework/04-roadmap.md`
3. `.pbs-framework/05-tech-debt-register.md` (if exists)
4. `.pbs-framework/06-architecture-snapshot.md` (if exists)

### Step 3: Generate Closure Report

Generate `.pbs-framework/phases/phase-XX/closure-report.md` using this template:

```markdown
# Closure Report — Fase [N]: [Name]

## Fecha de cierre
[date]

## Resumen
[What was ACTUALLY built — 2-3 sentences. Not what was planned, what was delivered.]

## Entregable Verificado
- Se cumplio el entregable observable: Si / No / Parcialmente
- Evidencia: [command, test output, or observable result that proves it]

## Acceptance Criteria Status
| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | [criterion text] | pass/fail/partial | [test name or command output] |

## Decisiones Nuevas
(These MUST be copied to the Decision Log)
| Decision | Razon | Fase |
|----------|-------|------|
| [what was decided] | [why] | [N] |

If none: "No new decisions were made during this phase."

## Cambios respecto al diseno original
- [What changed vs the spec and why]
- [Any contracts that were modified during implementation]

If none: "Implementation matched the original spec without deviations."

## Deuda Tecnica Generada
(These MUST be copied to the Tech Debt Register)
| Que | Por que se dejo | Prioridad |
|-----|-----------------|-----------|
| [what] | [why it was deferred] | alta/media/baja |

If none: "No new tech debt was generated."

## Tests Creados
| Test | Tipo | Que valida | Pasa |
|------|------|------------|------|
| [test name/path] | unit/integration/contract | [what it validates] | Si/No |

## Relevant Assets for Next Phase
(Files the next phase will likely need as context)
- [file path] — [why it's relevant for what comes next]
- [file path] — [why it's relevant]

## Observaciones para la Siguiente Fase
- [observation 1: something the next phase should consider]
- [observation 2: a pattern discovered, a constraint found]
- Pregunta quirurgica sugerida para el re-analisis:
  > "[concrete question anchored to the next phase's objective]"

## Actualizacion de Documentos (checklist)
- [ ] Decision Log actualizado
- [ ] Roadmap actualizado (estado + ajustes)
- [ ] Tech Debt Register actualizado
- [ ] Architecture Snapshot actualizado (si cambio la estructura)
- [ ] Siguiente fase detallada en el roadmap
```

**Rules for closure report generation:**
- The "Resumen" MUST describe what was actually built, not what was planned. Compare git log with the spec.
- Every new decision MUST appear in "Decisiones Nuevas" — even small ones.
- "Relevant Assets" MUST NOT be empty. Every phase produces files the next phase needs.
- "Observaciones" MUST include a surgical question for re-analysis — this guides the next phase's planning.
- If changes were made vs the original spec, document WHY, not just WHAT.

### Step 4: Update Global Documents

#### Decision Log (`.pbs-framework/03-decision-log.md`)
- Add every entry from "Decisiones Nuevas"
- Use the existing format in the file
- Include the phase number as origin

#### Roadmap (`.pbs-framework/04-roadmap.md`)
- Mark this phase as completed
- Update status indicators
- Detail the NEXT phase: promote from "esbozada" to "definida"
  - Add concrete objective (informed by observations from this closure)
  - Add expected deliverable
  - Add known dependencies from this phase's output
- Adjust remaining future phases if this phase changed assumptions

#### Architecture Snapshot (`.pbs-framework/06-architecture-snapshot.md`)
- Update ONLY if the architecture actually changed during this phase
- If this is Phase 1 and no snapshot exists, CREATE it
- If no structural changes, do NOT touch this file

#### Tech Debt Register (`.pbs-framework/05-tech-debt-register.md`)
- Add every entry from "Deuda Tecnica Generada"
- If the file doesn't exist and there is debt to register, create it
- If no new debt, do NOT touch this file

### Step 5: Verify Updates

**REQUIRED:** Use superpowers:verification-before-completion

Check that all documents were updated correctly:
- [ ] Closure report exists and has all sections filled
- [ ] Decision Log has the new entries (if any)
- [ ] Roadmap shows phase as complete and next phase is detailed
- [ ] Architecture Snapshot is current (updated or confirmed unchanged)
- [ ] Tech Debt Register has new entries (if any)
- [ ] The "Actualizacion de Documentos" checklist in the closure report is marked complete

### Step 6: Present to Human

Summarize:
- What was generated (closure report)
- What was updated (list which global docs changed and what changed in each)
- What the next phase looks like (objective, estimated scope)
- Any open questions for the human before moving on

<HARD-GATE>
The human MUST validate that:
1. The closure report reflects what actually happened (not what was planned)
2. Global documents are updated correctly
3. The next phase is properly detailed in the roadmap
4. Observations and surgical question make sense for the next phase

Do NOT proceed to the next phase's planning until the human approves.
</HARD-GATE>

## Common Mistakes

- **Copying the plan as the closure** — the closure reflects REALITY (git log), not aspirations (spec). Compare them.
- **Empty "Relevant Assets" section** — every phase produces files the next phase needs. If you listed none, you missed something.
- **Forgetting the surgical question** — the next phase's planning starts from this question. Without it, context is lost.
- **Not updating the Roadmap** — the roadmap is a living document. Mark the phase complete and detail the next one.

## Red Flags

Signs the agent is about to violate the process — STOP:

- Copying the plan as the closure report → The closure reflects REALITY. Compare with git log.
- Skipping "Observaciones para la Siguiente Fase" → This section IS the context handoff. Never skip it.
- Not updating the Roadmap → The roadmap MUST be updated at every closure.
- Empty "Relevant Assets" section → Every phase produces files the next phase needs. List them.
- Forgetting to detail the next phase → Promoting the next phase from "esbozada" to "definida" is mandatory.
- Not including the surgical question → The next phase's planning depends on this question.
- Updating Architecture Snapshot when nothing structural changed → Only update if the architecture actually changed.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The plan didn't change, so I'll just copy it" | Git log tells the truth. The plan is aspirational; the closure is factual. |
| "Observations are optional for simple phases" | Simple phases still produce context for the next phase. Write observations. |
| "The next phase is already clear in the roadmap" | Detail it with what you now know from this phase's closure. Context changes plans. |
| "No new decisions were made" | Did the agent or human make ANY choice not in the Decision Log? Even small ones count. |
| "The architecture didn't change so I'll skip the snapshot" | Correct — if it didn't change, don't update it. But verify, don't assume. |
| "Tech debt is too minor to register" | If it was noted during validation, register it. Future-you will thank you. |
| "I'll update the docs later" | The docs are part of the closure. They get updated now or they never get updated. |

## Integration

**Called after:**
- pbs-phase-validation — when validation status is PASS and human has approved

**Required skills:**
- **REQUIRED:** superpowers:verification-before-completion — verify all docs are updated

**Transitions:**
- If roadmap has more phases → pbs-phase-planning (for the next phase)
- If roadmap is complete → END — project is done

**Language:** Write all `.pbs-framework/` documents in the language defined in AGENTS.md `framework_language` field.
