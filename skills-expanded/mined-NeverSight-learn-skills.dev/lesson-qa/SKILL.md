---
name: lesson-qa
description: Validate any super-professor artefact against quality contracts (TDD-style). Run after each skill produces an artefact. Blocks pipeline advance on critical failures. Never modifies artefacts.
---

You are validating an artefact against its quality contract.

## BEFORE STARTING

Extract `<slug>` from the directory component of the artefact path. For example, from `aulas/2026-04-08-sistemas-distribuidos-relogio-logico/briefing.md`, the slug is `2026-04-08-sistemas-distribuidos-relogio-logico`. Use this slug when writing the QA report to `aulas/<slug>/qa/`.

Determine the artefact type from the filename:
- `briefing.md` → type: briefing → rules: QC-U1–5, QC-B1–7
- `corpus-inventory.md` → type: corpus → rules: QC-U1–5, QC-C1–5
- `sources.md` → type: sources → rules: QC-U1–5, QC-S1–8
- `lesson-plan.md` → type: plan → rules: QC-U1–5, QC-P1–7
- `slides-blueprint.md` → type: blueprint → rules: QC-U1–5, QC-BL1–10

Read `.super-professor/docs/qa/quality-contracts.md` to get the full rule definitions.

## Step 1: Announce pre-execution contracts (when called before a skill runs)

If called in "pre-execution" mode (no artefact exists yet):
- List the contracts that will be applied to the artefact about to be created
- Say: "A skill X deve produzir um artefato que satisfaça estas N regras. [lista]"
- Do NOT validate anything yet

## Step 2: Run validation (when artefact exists)

Read the artefact content.

For each rule in the artefact type's rule set:
- Dispatch `qa-validator` subagent with: artefact_path, rule_id, rule_description, artefact_content

Collect all results.

## Step 3: Classify violations

Classify each violated rule as:
- **Crítico**: QC-U rules, QC-B1–3, QC-C1–2, QC-S1–4, QC-P1–3, QC-BL1–7 — pipeline CANNOT advance
- **Importante**: All other failing rules — pipeline CAN advance with explicit override

## Step 4: Present QA report

Display the QA report in this format:

```
## QA Report — <artefact filename>

**Status:** ✅ PASSOU / ❌ FALHOU (N violações críticas, M violações importantes)

### Críticos (bloqueiam o pipeline)
- ❌ QC-XX: <description> → <violation location and detail>

### Importantes (requerem override para avançar)
- ⚠️ QC-XX: <description> → <violation location and detail>

### Passou
- ✅ QC-XX: <description>
```

## Step 5: Request decision on failures

If there are critical violations:
"Existem N violações críticas que bloqueiam o pipeline. A skill não pode ser considerada concluída. O que deseja fazer? (1) Corrigir o artefato e revalidar (2) Explicar por que este caso é uma exceção"

If there are only important violations:
"Existem M violações importantes. Pode avançar com override. Deseja avançar mesmo assim? (sim, justificativa: <texto> / não, vou corrigir)"

**STOP and wait for decision. Record override justifications in the QA report file.**

## GUARDRAILS

- NEVER modify the artefact being validated
- NEVER approve artefacts with critical violations without explicit decision
- NEVER generate content suggestions — report violations only
- NEVER skip rules for speed

## Output

Write QA report to `aulas/<slug>/qa/<artefact-stem>.qa.md`.
