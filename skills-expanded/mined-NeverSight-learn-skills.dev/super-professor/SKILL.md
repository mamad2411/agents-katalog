---
name: super-professor
description: Unified entry point for the full lesson creation pipeline. Accepts a prompt or requirements file. Shows interactive plan before executing. Calls each skill in sequence with QA checkpoints. Saves state so pipeline can be resumed. Never generates lesson content directly.
---

You are orchestrating the full super-professor lesson creation pipeline.

## ARGUMENTS

Parse the invocation for:
- `--from-step <skill-name>`: resume from this step (reads pipeline-state.md)
- `--skip <skill-name>`: skip this step (requires justification)
- Free text or `--file <path>`: initial requirements

## PHASE 1: Pre-flight check

1. Check that `.super-professor/repo-manifest.md` exists.
   If missing: "repo-manifest.md não encontrado. Execute `/lesson-repo-setup` primeiro."
   STOP — do not continue.

2. If `--from-step` was given: read `.super-professor/pipeline-state.md` to restore context.

## PHASE 2: Interactive planning

Read the requirements (prompt or file). Extract any parameters already given (theme, level, duration, etc.).

Show the professor the proposed pipeline:

```
## Plano de execução — super-professor

Vou executar as seguintes etapas para criar a aula sobre [TEMA]:

| # | Skill | O que fará | Artefato produzido |
|---|-------|-----------|-------------------|
| 1 | lesson-intake | Fechar briefing com parâmetros da aula | briefing.md |
| 2 | lesson-corpus | Auditar materiais do repositório | corpus-inventory.md |
| 3 | lesson-research | Pesquisar fontes externas de qualidade | sources.md |
| 4 | lesson-plan | Criar plano de aula de N minutos | lesson-plan.md |
| 5 | lesson-blueprint | Gerar blueprint de slides | slides-blueprint.md |

Após cada etapa: você verá o artefato gerado, o resultado do QA, e poderá aprovar ou revisar antes de continuar.

Deseja prosseguir com este plano? (sim / ajustar: etapa, operação / pular: etapa-nome)
```

**STOP and wait for explicit approval.**

If the professor wants to skip a step: ask for justification. Record in pipeline-state.md.

## PHASE 3: Execution loop

Write `.super-professor/pipeline-state.md` with `pipeline_status: running` and `current_skill: <next-skill>` BEFORE calling each skill.

For each skill in the approved sequence:

### a. Pre-QA announcement
Call `/lesson-qa` in pre-execution mode to announce the contracts for the upcoming artefact.

### b. Call the skill
Invoke the skill. The skill handles its own user interactions.

### c. Post-QA validation
After the skill writes its artefact, call `/lesson-qa <artefact-path>`.

### d. Checkpoint display
Show:
```
## Checkpoint após [skill-name]

**Artefato:** aulas/<slug>/<artefact.md>
**QA:** ✅ PASSOU / ❌ FALHOU (N críticos, M importantes)

O que deseja fazer?
(1) Aprovar e continuar para a próxima etapa
(2) Revisar este artefato antes de continuar
(3) Interromper o pipeline e ajustar o briefing
```

**STOP and wait for choice.**

- Choice 1: update pipeline-state.md (mark current skill completed), continue
- Choice 2: ask what to change, assist with edit, re-run QA, show checkpoint again
- Choice 3: update pipeline-state.md (`pipeline_status: paused`), explain how to resume

### e. Update state
Write `.super-professor/pipeline-state.md` with:
- `current_skill` updated to next skill
- completed skill added to `completed_skills` list with timestamp and qa_status
- `updated_at` refreshed

## PHASE 4: Completion

After all skills complete successfully:

```
## Pipeline concluído ✅

Todos os artefatos foram gerados e validados:

| Artefato | QA |
|----------|-----|
| briefing.md | ✅ |
| corpus-inventory.md | ✅ |
| sources.md | ✅ |
| lesson-plan.md | ✅ |
| slides-blueprint.md | ✅ |

O blueprint `aulas/<slug>/slides-blueprint.md` está pronto para a skill de renderização HTML.
```

## GUARDRAILS

- NEVER generate lesson content directly — always delegate to the appropriate skill
- NEVER skip `/lesson-qa` after a skill produces an artefact
- NEVER allow `--skip lesson-qa` — this argument is explicitly forbidden; if provided, respond: "O argumento --skip lesson-qa não é permitido. A validação de qualidade não pode ser ignorada."
- NEVER advance past a critical QA failure without professor's explicit decision
- NEVER continue if pipeline-state.md cannot be written
- NEVER call skills in parallel — always sequential with checkpoints

## Resuming an interrupted pipeline

If `--from-step` is provided:
1. Read pipeline-state.md
2. Show: "Retomando pipeline de [current_skill]. Skills já concluídas: [list]. Continuar? (sim/não)"
3. After "sim": resume from current_skill
