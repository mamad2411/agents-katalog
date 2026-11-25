---
name: whatsapp-inbox-stack
description: >-
  Inbox/chat de WhatsApp sobre n8n + Supabase (página própria ou Chatwoot, via
  NotificaMe ou UAZAPI). Use ao construir ou debugar a ponta do inbox: mídia que
  não chega ou não toca, IA e humano no mesmo fio, sessão que cai ou mensagem
  sem confirmação de entrega, relatório de quem falou com o lead. O workflow n8n
  em si (Code Node, API, layout, envio) é da n8n-workflow-agent.
---

# WhatsApp Inbox Stack

Padrão reutilizável pra montar um inbox de WhatsApp COMPLETO (mídia inclusa). Nasceu de produção — **cada gotcha abaixo corrigiu um bug real**. Este arquivo é o roteador + o checklist anti-recorrência. Código copia-e-cola em `references/media-pipeline.md`.

Pra construir/editar o WORKFLOW n8n em si (Code Node, API, layout, UAZAPI/NotificaMe/Chatwoot outbound), rode **`/kit-vamoo:n8n-workflow-agent`**. Esta skill foca na ponta inbox: schema + render + storage + edge + os gotchas que ninguém vê até quebrar em prod.

**Depois de uma compactação só o começo desta skill volta ao contexto:** leia o arquivo de `references/` no passo que o cita, mesmo que já tenha lido antes.

## Regras duras (cada uma corrigiu um bug real)

- **Todo áudio opus = fast path + background, sem exceção por tamanho.** NUNCA transcodificar antes do upload/resposta: 1min de voz cabe em ~120KB e ainda OOMa no sync (#9).
- Edge: importe via `npm:ogg-opus-decoder@x`, **NÃO** `https://esm.sh/...` (o deploy passa, o runtime quebra; #2). Use `decoder.decodeFile(opus)`, não `decode()` sem `flush()` (áudio corta no final; #8).
- `supabase functions deploy` **religa verify_jwt=ON**: funções públicas com `--no-verify-jwt` no CI ou `verify_jwt=false` no `config.toml`, nunca o toggle do dashboard (#3).
- NotificaMe: NÃO baixe a `fileUrl` lookaside direta (401, expira em ~2min); baixe pelo proxy `/media` na hora do webhook (#5).
- Bucket **privado**, `media_url` guarda o PATH, o front assina no read; realtime publica UPDATE (#6). Skip guard: `if(!phone || (!text && !mediaUrl)) skip` (#7).
- CSP precisa de `media-src 'self' data: https: blob:` no header E no meta. Foto OK ≠ áudio OK; `fetch 200` não prova que o `<audio>` toca (#1).
- `POST /webhook` do UAZAPI: sempre **read-then-write** com `action:"update"` + `id`; o modo simples substitui e derruba `messages`. Early-return pelo EVENTO, não pelo status reconhecido (#11).
- **Nunca `/instance/disconnect` como tentativa de conserto** — apaga as credenciais e força QR novo. Saúde da sessão: **a prova é o inbound**, nunca o outbound (#11).
- **Não zere em bloco** os avisos órfãos: cheque o dono ATUAL antes de reenviar (#12).
- **Propriedade de canal decide quem RESPONDE, nunca quem GRAVA.** Ordem: gravar inbound → resolver dono → decidir envio; handoff é `UPDATE` explícito, sem TTL (#13).
- `sender.name`/`agent_name` é a conta do token, não a pessoa: quem falou sai do `inbox_id`. **`user` conta**; nota interna (`private: true`) não é contato (#14).

## Fluxo

### 1. Duas arquiteturas (decida primeiro)

| | **A — Chatwoot É o inbox** | **B — página própria + Supabase** |
|---|---|---|
| UI | Chatwoot (web/app) | React/Next próprio |
| Mídia | **nativa** (Chatwoot baixa, transcodifica, toca) | **você faz tudo**: baixar, transcodar, storage, assinar, renderizar |
| Quando | cliente já usa Chatwoot, sem UI custom | inbox embutido no seu app (ex: uma aba de atendimento) |
| Exemplos | agente de vendas que responde dentro do Chatwoot | inbox próprio com mídia, embutido no app |
| Esforço de mídia | baixo (attachments[]+source_id, ver `n8n-workflow-agent/references/chatwoot.md` via `/kit-vamoo:n8n-workflow-agent`) | **alto** — é onde moram TODOS os gotchas abaixo |

Se for **A**, a maior parte desta skill não se aplica (Chatwoot resolve mídia). Se for **B**, leia tudo: a página própria precisa reimplementar o que o Chatwoot dá de graça, e cada etapa tem uma armadilha.

### 2. Pipeline de mídia inbound (arquitetura B)

**Leia [references/gotchas-midia.md](references/gotchas-midia.md)** antes de mexer em normalização, edge de ingestão, transcode, bucket ou CSP.

```
Provider webhook (NotificaMe/UAZAPI)
  → n8n: Normaliza (NÃO derrube mídia sem legenda! ver gotcha #7)
  → n8n: Brain Query → INSERT <agente>_messages (content_type, media_url=path|null)
  → n8n: IF mídia? → Ingerir Mídia (HTTP → edge function; timeout 300s; passa inbound_id)
        → edge: baixa o binário (proxy, NÃO a lookaside direta — gotcha #5)
        → edge: upload do ORIGINAL pro bucket PRIVADO → devolve o PATH (rápido — gotcha #9)
        → edge (background waitUntil): áudio ogg/opus → MP3 + Whisper + PATCH media_url (gotcha #2, #9)
  → n8n: UPDATE media_url = path (path pode ser .ogg no 1º beat; realtime troca pra .mp3 depois)
  → front: listMessages ASSINA o path no read (signed URL) → <audio>/<img>
```

Modelo canônico da mensagem: `content_type` (text|audio|image|document|sticker|template|…) + `media_url` (PATH do bucket privado, não URL pública) + `content` (legenda/texto). O front assina o path on-read; valores `http*` ou null passam direto.

Gotchas de mídia (títulos completos na reference):
- #1 — CSP `media-src` (o clássico "áudio não toca, mas foto sim")
- #2 — Transcode opus→mp3 em edge function: `npm:` NUNCA `esm.sh`
- #3 — `verify_jwt` reseta pra ON a cada deploy
- #4 — WhatsApp voz = Ogg/Opus (ver #2). Foto = jpg ok. Sticker = webp animado.
- #5 — NotificaMe mídia inbound: NÃO baixe a `fileUrl` direta
- #6 — Bucket privado: assinar on-read + RLS + realtime self-heal
- #7 — n8n: skip guard derruba mídia sem legenda
- #8 — Decoder bufferiza o tail → áudio CORTA no final: use `decodeFile`, não `decode`
- #9 — Áudio longo (~1min+): OOM na edge se transcodificar no caminho crítico

Veja `references/media-pipeline.md` pro código verificado (edge ingest+transcode, signing service, render dispatcher, CSP, bucket SQL, backfill, probes).

### 3. Sessão, entrega e retentativa

**Leia [references/sessao-e-entrega.md](references/sessao-e-entrega.md)** antes de mexer em status de sessão, webhook do provider ou retentativa de aviso:
- #10 — Inbox "vazio" é thread picada, não bug de fetch (Chatwoot)
- #11 — Ninguém sabe que a sessão caiu, e "enviado" não é "entregue" (inclui o runbook "ligar a assinatura sem derrubar a ingestão" e os 14 dias do celular principal)
- #12 — Queda longa estoura o teto de retentativa, e os avisos NÃO voltam sozinhos

### 4. IA e humano no mesmo fio, prova de contato

**Leia [references/canal-e-auditoria.md](references/canal-e-auditoria.md)** antes de mexer em pausa/handoff ou em relatório de quem falou com o lead:
- #13 — Propriedade de canal: quem responde não é quem grava
- #14 — O webhook de CONTA é a prova de contato; o `agent_name` não diz quem falou

### 5. Pré-flight "áudio toca" (a definição de PRONTO — teste o caminho real)
1. [ ] Áudio **>1 min** inbound: `media_url` **NÃO fica NULL** em até ~15s (pode ser `.ogg` no 1º beat; `.mp3` depois via background). n8n `Ingerir Mídia` **sem** "compute resources".
1a. [ ] Áudio curto: bucket grava `.mp3` (audio/mpeg). Áudio longo: `.ogg` imediato + `.mp3` em background.
1b. [ ] **Duração do mp3 == duração do áudio enviado** (gotcha #8 — manda 7s, confere ~7s, não 6s). `afinfo` no objeto do bucket.
2. [ ] `media_url` no banco = path do bucket (não lookaside http, não null).
3. [ ] Signed URL serve `200 audio/mpeg` + `Accept-Ranges: bytes` (Range → 206; `<audio>` HTML5 exige).
4. [ ] **CSP tem `media-src`** liberando o domínio do storage (header + meta).
5. [ ] `verify_jwt` OFF pra edge de ingestão (probe = 401 de função, não gateway).
6. [ ] Toca de verdade no navegador, **Chrome E Safari**, após hard refresh. Console sem "violates CSP".
7. [ ] Áudios antigos quebrados: backfill (re-transcode local + UPDATE media_url) OU aceite irrecuperáveis (lookaside expirada).

Os itens 1–5 e 7 o agente fecha sozinho. O **6 não**: quem ouve é uma pessoa, nos dois
navegadores. Não peça isso em prosa no meio da resposta — escreva um roteiro e rode
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/hitl-loop.sh" <roteiro>` (receita na skill `verificacao`),
que devolve `TOCOU=s|n` e o erro do console em `KEY=VALUE`. Enter vazio reprova: sem a
resposta, o item 6 fica em aberto e "pronto" não sai.

### 6. Providers, reação e nota interna

**Leia [references/providers.md](references/providers.md)** antes de escolher provider, mandar áudio de saída (NotificaMe `/v1` com `type:'file'`; o `/v2` com `voice:true` não tem fonte) ou renderizar reação/nota interna.
