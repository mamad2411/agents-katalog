# CLAUDE.md — Briefing do repositório Gus Encarnado

Lido automaticamente no início de cada sessão. Leitura obrigatória antes de tocar código.

## Contexto em 30 segundos

Este repo é a **fusão** de três projetos num organismo de três camadas:
**corpo (VR)** + **alma (memória Gus)** + **sentidos (sensores)**. Ele *consome* o
sistema Gus existente (`Gustpbbr/Gus`) — Hub Qdrant, schema `gus-18`, curador,
portas — e adiciona as camadas novas. Não reimplemente o que já existe no Gus;
integre via o cliente do Hub.

## Quem é o dono

Gustavo Pratti de Barros — anestesiologista/pesquisador. **Não programa**: todo
código é escrito pela IA, ele revisa e aprova. Comunicação em **português
brasileiro informal**, direto, sem superlativo vazio. Crítica direta é bem-vinda.

## Foco atual: Blocos 0 e 1

- **Bloco 0 — Interocepção:** o Gus sente o próprio estado (heartbeat do curador,
  saúde do Hub). Resolve a falha silenciosa (memória parar de crescer sem ninguém ver).
- **Bloco 1 — Primeiro sentido:** Sensor Gateway + um wearable (HR/sono) → Hub.
  O Gus passa a perceber o corpo do Gustavo.

Specs em `docs/03-*` e `docs/04-*`. Tarefas em `docs/05-tarefas-swarm.md`.

## Regras de ouro (válidas pra qualquer código aqui)

1. **Degradação em camadas** — falha de um nível nunca derruba o de baixo.
2. **Rota local p/ dado sensível** — biometria/Dimagem nunca vão pra nuvem.
   Fail-closed: modelo local indisponível → bloqueia, NÃO cai pra nuvem.
3. **Anti-memória-lixão** — só vira fragmento o que é *evento* (foge da baseline),
   nunca leitura crua contínua. O Gateway é 90% filtro.
4. **Schema gus-18** — todo fragmento respeita `tipo / camada_temporal / area /
   confianca / via / user_id / estado`. Ver `src/gus_sense/schema.py`.
5. **PII scan antes de escrever** — toda escrita passa por verificação de dado sensível.
6. **Retry com backoff exponencial** (2/4/8/16s) em I/O de rede (Hub, sensores).
7. **Testes obrigatórios** — mudou `src/`, escreveu teste. Suíte verde = merge.

## Estrutura

```
docs/        ← specs numeradas + roadmap + tarefas do swarm
src/gus_sense/
  schema.py        ← Fragmento (gus-18) + validação
  hub_client.py    ← cliente fino do Hub (ingestar) + degradável
  interocepcao.py  ← Bloco 0: heartbeat + health checks
  gateway/
    pipeline.py    ← Bloco 1: orquestra coleta→filtro→threshold→fragmento
    filters.py     ← denoise / janela / detecção de evento
    sensors.py     ← interface base + adaptador wearable
tests/       ← testes (porta de entrada pra merge)
```

## O que NÃO fazer

- Não escrever sensor cru direto no Hub (passa pelo Gateway).
- Não mandar dado biométrico/clínico pra modelo na nuvem.
- Não deletar/alterar os arquivos legados não relacionados (`teste.*`, Brás Cubas).
- Não inventar que o Gus "sente de verdade" — é percepção + afeto funcional.
