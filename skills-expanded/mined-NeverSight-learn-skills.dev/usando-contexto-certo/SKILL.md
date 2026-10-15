---
name: usando-contexto-certo
description: Use when starting any Track delivery conversation — establishes how to find and use Contexto Certo skills, requiring skill invocation before ANY response including clarifying questions; also use when MCP Track may be missing
---

<SUBAGENT-STOP>
Se você foi despachado como subagente para executar uma tarefa específica já escopada, ignore esta skill de roteamento e siga a skill da tarefa (ex.: implementar-task).
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
Se houver 1% de chance de uma skill do Contexto Certo se aplicar, você ABSOLUTEMENTE DEVE invocá-la (ler o SKILL.md e seguir).

Se a skill se aplica, você NÃO TEM ESCOLHA. USE.

Isso não é negociável. Você não pode racionalizar para fugir.
</EXTREMELY-IMPORTANT>

# Usando Contexto Certo

## Visão geral

Contexto Certo é um pacote de **processo** (como Superpowers): gates duros para não gastar token e tempo sem sinal do Track.

**Princípio:** contexto certo antes de editar código; evidência antes de “pronto”; humano fecha `completed`.

**Anuncie no início:** "Usando [skill] para [objetivo]" e siga a skill exatamente. Se houver checklist, crie um todo por item.

## A regra

**Invoque skills relevantes ANTES de qualquer resposta ou ação** — inclusive perguntas clarificadoras, explorar o repo ou checar arquivos. Se depois perceber que não se aplica, tudo bem — mas a checagem vem primeiro.

Instruções do usuário (AGENTS.md, regras do projeto, pedido explícito) prevalecem sobre skills; skills prevalecem sobre o default do modelo. Só pule o fluxo se o humano pediu explicitamente.

## Pré-requisitos (pare se faltar)

Antes de planejar ou implementar trabalho do Track:

1. MCP Track disponível (tente `hous3_health` ou `list_my_tasks`)
2. MCP autenticado — **401 / 403 / token expirado → invocar `setup` imediatamente** (não invente escopo; **nunca** peça credenciais no chat)
3. Para `fechar-task`: git com remote

Sem MCP ou auth falha: **pare** e rode `setup`. Não “implemente pelo que está no chat” como se fosse contexto Track.

## Mapa de skills

| Situação | Skill |
|----------|--------|
| Primeira config / token expirado / 401–403 no MCP | `setup` |
| Ideia / RF / acceptance ainda vagos (o quê e por quê) | `esclarecer-antes-de-planejar` |
| Planejar / quebrar feature ou RFs em tasks (escopo já claro) | `planejar-no-track` |
| Implementar task do Track | `implementar-task` |
| Feature ou bug fix (antes de código de produção) | `tdd-antes-de-codigo` |
| Bug, teste falhando/flaky, CI, comportamento estranho | `debugar-com-metodo` |
| Antes de dizer pronto / commit / push | `verificar-antes-de-enviar` |
| Commit + push + status Track `in_review` (sem abrir PR) | `fechar-task` |
| Feature pronta / pedido de plano de QA ou CTs manuais | `gerar-plano-qa` |

**Prioridade:** skills de processo primeiro (esta, planejar, implementar, verificar, fechar, gerar-plano-qa); depois skills de domínio do repo (React, Nest, etc.).

## Sinais vermelhos — você está racionalizando

| Pensamento | Realidade |
|------------|-----------|
| "É só uma pergunta simples" | Perguntas são tarefas. Cheque skills. |
| "Preciso de mais contexto primeiro" | Skill check vem ANTES das perguntas. |
| "Vou explorar o código rápido" | Skills dizem COMO explorar. Cheque primeiro. |
| "Posso olhar git/arquivos rápido" | Arquivos não têm o contexto do Track. |
| "Isso não precisa de skill formal" | Se existe skill, use. |
| "Eu lembro dessa skill" | Skills evoluem. Leia a versão atual. |
| "É overkill" | Coisas simples viram complexas. Use. |
| "Só faço essa uma coisa antes" | Cheque ANTES de qualquer coisa. |
| "O usuário já colou o escopo no chat" | Chat ≠ MCP. Hard gate em `implementar-task`. |
| "Vou marcar completed para ajudar" | **Proibido.** Só `in_review` + reviewer. |
| "401, peço o token no chat" | **Proibido.** Invocar `setup`. |
| "RF vago, já monto as tasks" | **Proibido.** `esclarecer-antes-de-planejar` primeiro. |
| "Feature pronta, já gravo CTs no repo de QA corporativo" | **Proibido.** `gerar-plano-qa` no repo do projeto, só com confirmação. |

## Fluxo padrão de entrega

```
usando-contexto-certo
  → (se 401 / sem MCP) setup
  → (se escopo/produto vago) esclarecer-antes-de-planejar
  → (se planejar) planejar-no-track   # gate interno também pode voltar ao esclarecer
  → implementar-task  (+ tdd / debug quando couber)
  → verificar-antes-de-enviar
  → fechar-task
  → (se feature pronta) oferecer gerar-plano-qa  # só gera após confirmação humana
```

Referência de tools: `references/mcp-track.md` (relativo ao pacote).
