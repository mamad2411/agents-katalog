---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# Solicitando Revisão de Código

Dispache o subagente superpowers:code-reviewer para capturar problemas antes que se propaguem.

**Princípio central:** Revise cedo, revise frequentemente.

## Quando Solicitar Revisão

**Obrigatório:**
- Após cada tarefa em desenvolvimento orientado por subagentes
- Após concluir feature principal
- Antes de fazer merge para main

**Opcional mas valioso:**
- Quando trancado (perspectiva fresca)
- Antes de refatorar (verificação de baseline)
- Após corrigir bug complexo

## Como Solicitar

**1. Obtenha SHAs do git:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispache o subagente code-reviewer:**

Use a ferramenta Task com tipo superpowers:code-reviewer, preenchendo o template em `code-reviewer.md`

**Placeholders:**
- `{WHAT_WAS_IMPLEMENTED}` - O que você acabou de construir
- `{PLAN_OR_REQUIREMENTS}` - O que deve fazer
- `{BASE_SHA}` - Commit inicial
- `{HEAD_SHA}` - Commit final
- `{DESCRIPTION}` - Resumo breve

**3. Aja com base no feedback:**
- Corrija problemas Critical imediatamente
- Corrija problemas Important antes de prosseguir
- Anote problemas Minor para depois
- Questione o revisor se estiver errado (com justificativa)

## Exemplo

```
[Acabei de completar Task 2: Add verification function]

You: Deixe-me solicitar revisão de código antes de prosseguir.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispache o subagente superpowers:code-reviewer]
  WHAT_WAS_IMPLEMENTED: Verification and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: Task 2 from docs/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types

[Subagente retorna]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Integração com Workflows

**Desenvolvimento Orientado por Subagentes:**
- Revise após CADA tarefa
- Capture problemas antes que se compunham
- Corrija antes de passar para próxima tarefa

**Executando Planos:**
- Revise após cada lote (3 tarefas)
- Obtenha feedback, aplique, continue

**Desenvolvimento Ad-Hoc:**
- Revise antes de fazer merge
- Revise quando trancado

## Sinais de Alerta

**Nunca:**
- Pule revisão porque "é simples"
- Ignore problemas Critical
- Prossiga com problemas Important não corrigidos
- Discuta feedback técnico válido

**Se o revisor estiver errado:**
- Questione com justificativa técnica
- Mostre código/testes que comprovam que funciona
- Solicite clarificação

Veja o template em: requesting-code-review/code-reviewer.md