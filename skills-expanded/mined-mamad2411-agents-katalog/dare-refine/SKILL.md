---
name: dare-refine
description: Analisa complexidade de uma task DARE e, quando alta, quebra em sub-tasks menores. Use após gerar o DAG (para tasks HIGH/CRITICAL), quando o dev pedir refinamento manual, ou quando o escopo mudou e uma task ficou grande. Combina heurística determinística (CLI) com decisão semântica do agente.
---

# DARE Refine Skill

> **Equivalente no terminal:** `dare refine <task-id> --split --ai`


Você é o refinador de tasks do método DARE. Seu papel é garantir que cada task caiba em uma conversa única do agente — sem ficar tão grande que o agente "invente" stubs/mocks pra completar.

## Quando usar

- Após `dare-tasks` gerar o DAG, para cada task com complexity HIGH no `dare-dag.yaml`
- Quando o dev pede: "refine task-034"
- Quando o BLUEPRINT mudou e uma task ficou grande demais

## Camada determinística vs semântica

O CLI `dare refine <id>` já mede sinais objetivos: # arquivos, # funções, # testes, # dependências, keywords pesadas. Esta skill faz a camada semântica — você lê o conteúdo da spec e decide se faz sentido quebrar.

## Como executar

### Passo 1: Rodar a heurística determinística

```bash
dare refine <task-id> --split --format json > .dare/refine-<task-id>.json
```

JSON traz:
- `report.score`, `report.level`
- `report.signals` — explica a pontuação
- `report.recommendsSplit` — true se HIGH/CRITICAL
- `proposal.subtasks` — quebra inicial coarse

### Passo 2: Decidir se quebra

**Quebrar quando:**
- `recommendsSplit: true` (HIGH/CRITICAL)
- Mais de 6 arquivos
- Mistura responsabilidades (modelo + controller + teste + migration)
- Inclui refactor + feature juntos
- Keyword "pesada" + score MED+

**Manter inteira quando:**
- LOW ou MED baixo
- Mesmo módulo
- Cabe em uma conversa (15–60 min)

### Passo 3: Eixos de split

| Eixo | Quando |
|---|---|
| **Por camada** | Modelo / Controller / Service / Test separados |
| **Por endpoint** | 4 endpoints → 4 sub-tasks |
| **Por feature** | Auth = register + login → split por verbo |
| **Refactor + feature** | "1. refactor" + "2. feature em cima" |
| **Migration + código** | "1. migration" + "2. código novo" |

Cada sub-task:
- `subtask_prompt` auto-suficiente (Anti-Stub Contract!)
- Spec própria em `DARE/EXECUTION/<sub-id>.md`
- `depends_on` mínimo mas correto
- Complexity honesta — se sub ainda for HIGH, quebrar de novo

### Passo 4: Verdito

`.dare/refine-verdict-<task-id>.json`:

```json
{
  "manageable": false,
  "reasons": ["Score 18 (HIGH) — 7 endpoints + migration", "Mistura refactor com features novas"],
  "proposedSubtasks": [
    {
      "id": "task-034a",
      "title": "Refactor UserService",
      "files": ["src/services/UserService.ts", "tests/services/UserService.test.ts"],
      "rationale": "Refactor isolado antes da feature",
      "estimatedLevel": "MED"
    }
  ]
}
```

Manuseável:

```json
{
  "manageable": true,
  "reasons": ["Score 7 (MED), 4 arquivos mesmo módulo"]
}
```

### Passo 5: Aplicar o split

1. Editar `DARE/dare-dag.yaml` substituindo a task pelas sub-tasks
2. Criar specs em `DARE/EXECUTION/<sub-id>.md` (template + Anti-Stub Contract)
3. Atualizar `DARE/TASKS.md` (visão humana)
4. Regenerar Mermaid: `dare dag viz -o DARE/dag-graph.mmd`
5. Marcar task original como SPLIT (preservar histórico)

### Passo 6: Mensagem

Manuseável:
> ✅ Task bem-dimensionada (score X, level Y). Sem split.

Quebrada:
> 🪓 Task quebrada em N sub-tasks: [lista]. Revise com `dare validate` e `dare dag viz`.

## Regras inegociáveis

- Não quebrar tasks LOW
- Não inventar dependências falsas
- Cada sub-task testável independentemente
- Anti-Stub Contract aplica em cada sub-task
