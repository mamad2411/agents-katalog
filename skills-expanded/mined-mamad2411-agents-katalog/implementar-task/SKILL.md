---
name: implementar-task
description: Use when implementing a Track task or writing production code for assigned delivery work — hard gate requires get_agent_execution_context (or equivalent MCP scope) before any code edit
---

# Implementar Task

## Visão geral

Executar uma task do Track com **escopo travado** pelo MCP. Combina hard gate de cloud agents + disciplina do Superpowers `executing-plans` (review do plano, stop when blocked, verifications) adaptada à entrega Track.

**Anuncie:** "Usando implementar-task para [taskId / título]."

## Lei de ferro

```
NENHUMA EDIÇÃO DE CÓDIGO SEM CONTEXTO MCP VÁLIDO NESTA CONVERSA
```

Colar escopo no chat **não** substitui o MCP.  
"Eu já sei o que fazer" **não** substitui o MCP.  
Violar a letra é violar o espírito.

## Fase 0 — ESCOPO (obrigatória)

1. Resolver `taskId` + `projectId` (`list_my_tasks` se o humano não passou)
2. Chamar **`get_agent_execution_context`** com esses ids
3. Ler: requirements, acceptance, feature, etContext, instructionBlocks do projeto
4. Escrever bullets curtos:
   - **No escopo:** RFs / comportamento desta task
   - **Fora de escopo:** o que NÃO vai fazer
5. Se a tool falhar com **401 / 403 / token expirado** → **PARE**. Não edite. Invoque **`setup`**. Se for “task não encontrada” / ids ambíguos (sem erro de auth) → confirme `taskId`/`projectId` com o humano. **Nunca** peça, aceite, cole ou ecoe credenciais no chat.

Se `get_agent_execution_context` não existir no perfil MCP autenticado, use o melhor equivalente de leitura (`get_release_planning_context` + detalhe da task) e declare a limitação — ainda assim **sem chute**.

## Fase 1 — PLANO (curto, sem placeholders)

Máx ~15 linhas. Deve ser executável por alguém sem contexto da conversa.

Inclua:
- **Arquivos:** paths exatos a criar/modificar/testar (não “alguns arquivos do módulo”)
- **Abordagem:** 2–5 passos concretos (bite-sized)
- **Verificações:** comandos exatos que vai rodar (lint/test/build relevantes)
- **Branch:** confirmar que **não** está em `main`/`master`/`staging` sem consentimento explícito do humano; preferir `feat/**` (e worktree se o checkout principal estiver ocupado)

**Proibido no plano:** `TBD`, `TODO`, “valido depois”, “add appropriate error handling”, “similar to X” sem detalhar.

### Review crítico do plano (antes de codar)

Antes da Fase 2, releia o plano contra o MCP:

- Acceptance/RF cobertos?
- Risco, gap ou contradição com ET/código?
- Dependência faltando?

**Se houver concern:** levante com o humano **antes** de editar.  
**Se limpo:** crie todos pelos passos do plano e siga — **não** pergunte “posso continuar?” se o humano já pediu implementar.

## Fase 2 — IMPLEMENTAR

Para cada passo/todo:

1. Marque `in_progress`
2. Execute o passo (siga o plano; não invente escopo)
3. Rode a verificação daquele passo quando o plano especificar
4. Marque `completed` no todo

Regras:
- Siga rules/skills do repo (`.cursor/rules`, padrões existentes)
- Não expanda além do escopo listado na Fase 0
- **Não** modifique `.cursor/` de agente em PR de task (se o projeto sincroniza skills)
- Feature/bug fix comportamental → invoque `tdd-antes-de-codigo`
- Falha misteriosa → invoque `debugar-com-metodo` **antes** de patch aleatório
- Task grande / plano multi-arquivo independente → pode usar subagents; task típica Track = execute na sessão

### Pare e pergunte (não chute)

**STOP imediato quando:**
- Blocker (deps, permissão, infra)
- Instrução/acceptance ambígua demais para escolher comportamento
- Plano tem gap crítico
- Você não entendeu um requisito
- Verificação falha de forma repetida sem hipótese clara → `debugar-com-metodo`; se continuar bloqueado, escale ao humano

**Não force** passando por cima do blocker. Pergunte.

## Fase 3 — Self-review de acceptance + verificar

1. Checklist **item a item** do `acceptance` / RFs cobertos no MCP — gaps = não está pronto
2. Declare status interno:
   - **DONE** — acceptance coberta, verificações locais ok
   - **DONE_WITH_CONCERNS** — entregável, mas liste dúvidas (arquivo grande, dívida, edge)
   - **NEEDS_CONTEXT** — falta info; não finja
   - **BLOCKED** — não dá para fechar sem humano/plano
3. Só com **DONE** ou **DONE_WITH_CONCERNS** (concerns não bloqueantes): obrigatório `verificar-antes-de-enviar` com evidência fresca antes de qualquer claim de sucesso / push
4. **BLOCKED** / **NEEDS_CONTEXT** → não chame `fechar-task`

## Fase 4 — Entregar

Só depois da verificação verde: `fechar-task` (commit + push + `in_review` + reviewer; **sem** abrir PR).

**Nunca** chame `complete_dev_task`. **Nunca** abra PR no fechar — a menos que o humano peça explicitamente.

Após `fechar-task`, se a feature ficou sem tasks de entrega pendentes → **ofereça** `gerar-plano-qa` (não gere sozinho).

## Sinais vermelhos

| Pensamento | Realidade |
|------------|-----------|
| "O usuário colou a descrição" | Ainda assim: MCP |
| "É um fix de uma linha" | Ainda assim: MCP |
| "MCP está lento, sigo sem" | Pare |
| "Vou só explorar arquivos" | Depois do MCP; exploração sem escopo gasta token |
| "Plano vago, começo e vejo" | Fase 1 com paths/comandos; senão pergunte |
| "Estou em staging, vai dar" | Branch `feat/**` ou consentimento explícito |
| "Verificação falhou, mas acho que é flaky" | Não chute — debug / evidência |
| "Completo a task no Track" | Só `in_review` via `fechar-task` |
| "Self-review mental basta" | Acceptance checklist + `verificar-antes-de-enviar` |
| "Devo continuar?" (humano já pediu implementar) | Só pare em blocker real |

## Relação com outras skills

```
usando-contexto-certo → implementar-task
  → (opcional) tdd-antes-de-codigo / debugar-com-metodo
  → verificar-antes-de-enviar
  → fechar-task
  → (se feature pronta) oferecer gerar-plano-qa
```

**Não substitui** `planejar-no-track` / plano multi-RF longo — aqui o plano é curto e por **uma** task.
