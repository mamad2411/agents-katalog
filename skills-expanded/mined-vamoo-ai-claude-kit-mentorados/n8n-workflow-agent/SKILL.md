---
name: n8n-workflow-agent
description: >-
  Construir, editar, depurar ou publicar workflow n8n, com ou sem agente de WhatsApp:
  layout sem cruzamento, baseline + diff antes de PUT, Code Node, e referências de
  UAZAPI, NotificaMe, Chatwoot, Pipedrive, Postgres, disparo, pausa Redis e QA simulada
  de agente. A ponta do inbox no app é da whatsapp-inbox-stack.
---

# n8n Workflow Agent

Skill de referência pra construir e manter workflows n8n — agentes de IA no WhatsApp incluídos.
Nasceu de produção — cada regra preveniu ou corrigiu um bug real.

Este arquivo é o **roteador**: traz a regra dura de layout, a arquitetura típica
e a ordem de decisão. O conhecimento por domínio está em `references/` — **leia
só a referência do tema da tarefa**, não todas.

Se o projeto tem `.context/docs/n8n.md` (host, versão, modo de deploy, nomes das
credenciais e o que já foi medido naquela instância), leia antes de tocar o workflow: o
comportamento de PUT, ativação e webhook varia por versão e deploy, e o que vale para a
instância do projeto está lá.

## Qual referência ler (ordem de decisão)

| Tarefa envolve... | Leia |
|---|---|
| Criar/editar workflow via API, PUT, ativação, build a partir de source files | [references/n8n-api.md](references/n8n-api.md) |
| Code Node (JS), HTTP node com `jsonBody` | [references/code-node.md](references/code-node.md) |
| Query Postgres/Supabase, `queryReplacement`, schema `dispatch_tracking` | [references/postgres.md](references/postgres.md) |
| Enviar N mensagens/balões, fan-out, debounce, pausa Redis, anti-loop, dedup, keep-alive 24h | [references/messaging-patterns.md](references/messaging-patterns.md) |
| UAZAPI (alertas internos, mídia, uptime watcher) | [references/uazapi.md](references/uazapi.md) |
| NotificaMe (templates client-facing, status callbacks) | [references/notificame.md](references/notificame.md) |
| Chatwoot (espelho, labels, transferência, webhooks) | [references/chatwoot.md](references/chatwoot.md) |
| Pipedrive (deals, stages via n8n) | [references/pipedrive.md](references/pipedrive.md) |
| Pipeline de dispatch, estágios do cliente, resumo diário, follow-up | [references/pipelines.md](references/pipelines.md) |
| ElevenLabs TTS, transcrição Whisper, auth de webhook (inclui token no corpo via `.hash`), API route Next.js, Supabase Storage | [references/integrations-misc.md](references/integrations-misc.md) |
| IA que fala com cliente: onde cada guard-rail entra no workflow (allowlist, opt-out, escalar pra humano, pausa) | [references/guardrails-ia.md](references/guardrails-ia.md) — o porquê está em `guardrails-ia/SKILL.md` (leia o arquivo; a pessoa chama por `/kit-vamoo:guardrails-ia`) |
| **Qualquer bug, erro estranho, teste de agente** | [references/troubleshooting.md](references/troubleshooting.md) — comece pela tabela Common Mistakes |
| Regressão de agente em conversa longa ou com lead imprevisível (lead simulado + juiz + checagens) | [references/qa-simulada.md](references/qa-simulada.md) — `scripts/simular-conversa.mjs` |
| Inbox próprio (React+Storage), mídia inbound NULL, áudio >1min, CSP, transcode edge | **`/kit-vamoo:whatsapp-inbox-stack`** (gotcha #9 OOM + fast path) — complementa esta skill na ponta UI/storage |

## Layout visual — linhas retas

Workflows são lidos no canvas por humanos, e conexão que cruza outra deixa o fluxo
ilegível — em produção, canvas cruzado é rejeitado. Ao posicionar nodes via API
(`node.position = [x, y]`), calcule as coordenadas dos nodes que você cria ou move para
que nenhuma conexão cruze outra. Workflow linear, sem branches: todos na mesma Y, X
crescente.

### Regras

1. **Chain linear horizontal:** mesma coordenada Y. Se A→B→C, mantém Y constante, varia só X. Espaçamento mínimo 220px em X.
2. **Branches paralelas em Y separados:** quando um Switch/IF cria N branches, distribui em Y crescente (ex: branch[0] Y=400, branch[1] Y=600, branch[2] Y=800). Cada branch corre horizontal nessa Y dela.
3. **Branches que convergem:** quando 2+ branches voltam pro mesmo node downstream, escolhe a Y do branch principal e roteia visualmente em "L" (canto reto), nunca em diagonal.
4. **Não puxa linha pra trás:** se um node referencia outro upstream via `$('Foo').first()`, mantém a conexão visual fluindo pra direita. Pra trás é só pra Wait/Loop com retorno explícito.
5. **Sub-fluxos verticais quando branches são muitas:** se Switch tem 4+ branches, considera empilhar verticalmente em colunas alinhadas (canvas vira grid).
6. **Hierarquia Y por tipo de operação:** Y baixo = caminho feliz; Y alto = error handling, skip branches, alerts. Mantém consistente no workflow inteiro.

### Anti-pattern (causa cruzamento)

- Mover um node "pra cima" geometricamente quando o anterior está embaixo → cria diagonal que cruza outras chains
- Mesma Y pra branches paralelas (todas em 400) → ramais sobrepostos
- Posicionar Set/Code "auxiliar" longe do node que consome → linha longa atravessa outras

### Ao editar via API

`node.position = [x, y]` é onde o n8n renderiza. Quando script adiciona um node novo no meio de uma chain, **calcula a posição assim**:

```python
# Insere node entre A e B
new_x = nodeA["position"][0] + 220
new_y = nodeA["position"][1]   # mesma Y de A
# Depois shifta B (e tudo a partir dele) +220 em X pra abrir espaço
```

Sem isso, fica empilhado em cima ou cruzando. Após PUT, drag+save no UI **preserva** as coordenadas (não auto-relayouta) — então responsabilidade do script colocar certo já.

## Antes de aplicar JSON preparado: puxe o baseline e olhe o diff

PUT de workflow **substitui o workflow inteiro**. Não faz merge, não avisa que o
live mudou, não deixa rastro do que apagou. Um JSON gerado ontem sobrescreve, em
silêncio, quem editou hoje pelo editor.

**A regra:** logo antes de qualquer PUT em lote, puxe o estado ao vivo para o
mesmo diretório versionado que gerou o JSON e confira o diff.

- diff vazio → pode aplicar;
- diff → **alguém mexeu**: regenere a partir do baseline novo e revise o que
  mudou antes de seguir. Nunca aplique por cima.

Vale o mesmo para o rollback: o snapshot só serve se for do estado imediatamente
anterior. Baseline velho é rollback que restaura um passado errado.

## Workflow Architecture (Fluxo Típico N8N)

```
Webhook UAZAPI
  → Normalizar Entrada (Code Node)
  → IF skip? (grupo, fromMe)
  → IF audio? (sim → transcrever → set texto)
  → Dedup (lock file)
  → Log Entrada (grava o inbound)
  → IF dono ≠ ia ou pausa Redis (anti-loop)? (sim → para; já gravou — `/kit-vamoo:whatsapp-inbox-stack` #13)
  → Debounce Save → Wait 3s → Debounce Verify
  → AI Agent (LangChain + o LLM que o projeto usa + Postgres Memory)
  → Validar JSON resposta
  → IF transferir? (sim → notificar admin + dono do canal = humano + Chatwoot labels)
  → IF audio response? (TTS ElevenLabs)
  → Split Out Mensagens → Loop → Enviar UAZAPI/NotificaMe
  → Registrar Chatwoot (ver chatwoot.md § Mirror de OUTGOING)
```

## Stack coberta

- **n8n**: API, Code Nodes, workflow patterns
- **UAZAPI**: WhatsApp provider (alertas internos, mídia)
- **NotificaMe**: WhatsApp provider (templates client-facing)
- **Chatwoot**: CRM omnichannel (espelho, labels, transferência, atividade)
- **Dispatch Pipeline**: dispatch backend (ou o próprio n8n) → N8N → NotificaMe → webhook callbacks
- **Client Pipeline**: avanço de estágio (contatado → visualizado → interagiu → qualificado → transferido)
- **Daily Summary**: relatório diário agregado via UAZAPI
- **ElevenLabs**: TTS pra respostas em áudio
- **Redis**: pausa IA, debounce
