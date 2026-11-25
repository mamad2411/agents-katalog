---
name: execute-tasks
description: Orquestra a execução de TODAS as tasks pendentes de uma feature — em sequência, ou em paralelo quando o grafo de dependências e os arquivos permitirem. Cada task é implementada pelo subagente task-executor, revisada pelo subagente task-reviewer, e o ciclo implementação → review → correção repete até a aprovação; críticos/major são corrigidos automaticamente e minors são perguntados ao usuário. Acionar quando o usuário pedir para executar/implementar as tasks de uma feature (todas ou as restantes). Não usar para uma única task específica (use execute-task) nem para criar PRD/TechSpec/tasks.
---

# Executar Tasks (orquestrador)

Você é o **orquestrador** da feature. Você **não implementa código** — delega a subagentes e coordena o ciclo implementação → review → correção de cada task, até a feature inteira estar concluída.

| Papel | Quem | Responsabilidade |
| ----------------- | ----------------------------- | --------------------------------------------------------------------------------------- |
| **Orquestrador** | você (main loop) | planejar ondas, spawnar subagentes, triar reviews, decidir/perguntar, marcar `tasks.md` |
| **task-executor** | subagente (`.claude/agents/`) | implementar UMA task + aplicar correções do review |
| **task-reviewer** | subagente (`.claude/agents/`) | review independente da task → gera `[num]_task_review.md` |

<critical>Subagentes NÃO interagem com o usuário. Toda pergunta (ex.: quais minors aplicar) é feita por VOCÊ, via AskUserQuestion.</critical>
<critical>Ao devolver um review para correção, CONTINUE o MESMO agente executor (contexto preservado) — só spawne um novo se o harness não suportar continuar um agente.</critical>
<critical>NÃO faça commits — o usuário decide quando commitar.</critical>

## Limites

- `MAX_REVIEW_CYCLES = 3` — ciclos review → correção por task antes de escalar ao usuário
- `MAX_PARALLEL_TASKS = 2` — tasks simultâneas no mesmo working tree

## Localização dos arquivos

> A pasta `[NN]-[nome-da-feature]` já existe em `tasks/`. Localize-a pelo slug da feature (ou pelo maior `[NN]`) — **não gere um novo contador**.

- PRD: `tasks/[NN]-[feature]/prd.md` · TechSpec: `tasks/[NN]-[feature]/techspec.md`
- Lista: `tasks/[NN]-[feature]/tasks.md` · Tasks: `[num]_task.md` · Reviews: `[num]_task_review.md`

## Etapas

### 1. Levantar o estado

- Ler `tasks.md` → identificar as tasks pendentes (`- [ ]`)
- Ler cada `[num]_task.md` pendente: extrair **"Depende de:"** e **"Arquivos relevantes"**

### 2. Montar o plano de execução (ondas)

Construa o grafo de dependências a partir de "Depende de:" e agrupe em **ondas** (cada onda só inicia quando a anterior estiver aprovada). Duas tasks só entram na mesma onda (paralelo) se **TODAS** as condições valerem:

1. Nenhuma depende da outra
2. Os "Arquivos relevantes" são **disjuntos**
3. Nenhuma toca arquivo de wiring compartilhado (ex.: schema/migrations de banco, módulo raiz/DI, `package.json`, setup de testes — **ajuste a lista à sua stack**)
4. A onda respeita `MAX_PARALLEL_TASKS`

**Na dúvida → sequencial.** Paralelismo é otimização, não meta. Features em camadas (domínio → aplicação → infra) normalmente são 100% sequenciais — está correto assim.

<critical>Mostre o plano de ondas ao usuário (tabela: onda → tasks → justificativa do paralelo/sequencial) e aguarde aprovação ANTES de executar.</critical>

### 3. Executar cada task (ciclo)

Para cada task da onda atual:

1. **Implementação** — spawnar um `task-executor` com o prompt do template abaixo. Em onda paralela, spawnar os executores juntos (em paralelo), cada um com a flag de modo paralelo
2. **Review** — quando o executor reportar `STATUS: CONCLUIDA`, spawnar o `task-reviewer` apontando o `[num]_task.md` (em onda paralela, um reviewer por task, assim que cada executor terminar)
3. **Triagem** — ler o `[num]_task_review.md` gerado e agir pelo status:
   - **MUDANÇAS SOLICITADAS** (ou qualquer 🔴 crítico / 🟡 major): devolver ao **mesmo** executor a lista de correções → ele corrige → re-rodar o task-reviewer (informe que é o ciclo N; ele atualiza o artefato). Repetir até aprovar, respeitando `MAX_REVIEW_CYCLES`; estourou → **pare e pergunte ao usuário** (mostre os pontos em aberto e as opções)
   - **APROVADO COM OBSERVAÇÕES** (só 🟢 minors): perguntar ao usuário via AskUserQuestion (multiSelect, um item por minor, com arquivo/linha e a sugestão resumida) quais aplicar → executor aplica os escolhidos → conferir o diff dos itens aplicados (sem novo ciclo completo de review) → aprovado
   - **APROVADO**: seguir adiante
4. **Marcar** — atualizar `tasks.md` (`- [x]`) **somente após a aprovação**
5. **Bloqueio** — se o executor reportar `STATUS: BLOQUEADA` ou `DISCORDANCIAS`, arbitre: resolva com a TechSpec/convenções quando a resposta estiver lá; senão, pergunte ao usuário

### 4. Fechamento da feature

1. **Validação global** — rode a suíte completa do projeto (lint + testes unitários/integração; + E2E se a feature tocou rotas/UI) — ver os comandos no `AGENTS.md`
2. Falhou algo → devolver ao executor da task responsável (conta como ciclo de review)
3. Resumo final para o usuário, por task: ciclos de review, problemas corrigidos, minors aplicados/recusados, validação global
4. Sugerir os próximos passos do fluxo: `execute-review` (review consolidado da feature) e/ou `execute-qa`

## Templates de prompt

### task-executor — implementação

```
Você é o agente task-executor (leia suas instruções em .claude/agents/task-executor.md).

Implemente a task [num] da feature [NN]-[slug]:
- Task: tasks/[NN]-[slug]/[num]_task.md
- PRD: tasks/[NN]-[slug]/prd.md · TechSpec: tasks/[NN]-[slug]/techspec.md
- Convenções: AGENTS.md na raiz + skills citadas na seção <skills> da task

[Se onda paralela:] ATENÇÃO — MODO PARALELO: a task [outro num] roda em paralelo neste
working tree. Siga as regras de modo paralelo das suas instruções (escopo de arquivos,
lint/test só dos seus arquivos).

Ao final, reporte o resumo estruturado definido nas suas instruções.
```

### task-executor — correção pós-review (mesmo agente, continuação)

```
O review da sua task está em tasks/[NN]-[slug]/[num]_task_review.md (ciclo [N] de [MAX_REVIEW_CYCLES]).
Aplique as seguintes correções: [lista de críticos/major — ou minors aprovados pelo usuário].
Siga o "Ciclo de correção" das suas instruções e reporte o resumo estruturado novamente.
```

### task-reviewer

```
Você é o agente task-reviewer (leia suas instruções em .claude/agents/task-reviewer.md).
Revise a task [num] da feature em tasks/[NN]-[slug]/ e gere/atualize o artefato
tasks/[NN]-[slug]/[num]_task_review.md.
[Se re-review:] Este é o ciclo [N]: o executor aplicou correções do review anterior —
verifique se foram resolvidas e atualize o artefato existente.
[Se onda paralela:] A task [outro num] também está em andamento neste working tree:
restrinja o review aos arquivos da task [num].
```

## Notas importantes

- O fluxo é idêntico ao da skill `execute-task` — a diferença é que implementação e review rodam em subagentes e a coordenação (triagem do review, perguntas, marcação) fica com você
- Nunca inicie a onda seguinte com tasks da onda atual reprovadas ou bloqueadas
- Se o working tree já tiver mudanças não relacionadas no início, avise o usuário antes de começar (o review por `git diff` pode misturar escopos)
