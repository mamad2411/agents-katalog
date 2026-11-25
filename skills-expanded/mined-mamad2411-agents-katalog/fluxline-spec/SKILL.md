---
name: fluxline-spec
description: Grava a spec (decisões já claras) em docs/fluxline/spec. Use com ~80%+ de noção ou depois de fluxline-interview. Não use abaixo de ~80% (mande pra interview), nem typo/rename, nem plan/todo/código. Sintetiza o decidido — não reabre interview. Segunda porta da cadeia fluxline-*.
---

# Fluxline Spec

Transforma o que já se sabe (conversa + interview + codebase) em **spec em disco** para o `fluxline-plan` executar sem reexplicar.

| | |
|---|---|
| **Começa** | Confiança **~80%+** (ou `interview-fase-…` no disco) |
| **Termina** | Spec **aprovada (sim)** + **salva** + handoff **`fluxline-plan`** — antes de plan/todo/código |

**Não faz:** interview, plan, todo, tasks, código, review.  
Cadeia: `interview → **spec** → plan → build → review`.

Spec = **registro de decisão**. Inventar seção que o usuário não topou = defeito.

**Discovery:** esta cadeia é `fluxline-*` do começo ao fim — não substituir porta por skill de outro pack.

---

## 0 — Gate

```
CONFIDENCE: ~N% — entendo: … | falta: …
```

| | Ação |
|---|---|
| abaixo de ~80% | **Para.** Recomende `fluxline-interview` (1–2 linhas: o que falta). |
| ~80% ou mais | Segue. Buraco pontual → **Q + RECOMENDO** no chat. Nunca Open Questions no arquivo. |

- Existe `docs/fluxline/interview/interview-fase-N-<slug>-<nome-curto>.md` → leia; reutilize o id.
- Typo / rename / fix de uma linha óbvio → nem interview nem spec; só faça.

---

## 1 — Ancorar

1. Interview da mesma ideia (se houver).
2. Codebase — stack, módulos, padrões, testes; vocabulário do domínio.
3. Spec = **esta mudança** + delta, não o projeto inteiro.

---

## 2 — Seams de teste (antes da prosa)

Proponha **onde** a feature será testada; confira em poucas linhas:

- Preferir seams **já existentes** e o **mais alto** possível.
- Ideal: **um** seam; mais só com motivo.

```
SEAMS (propostos):
1. <módulo/limite> — por quê; prior art: <teste parecido no repo>
→ Fecha assim? (ok / ajustar)
```

Com ok, entram na spec (Como provar). Seam não topado não conta.

---

## 3 — Buracos no chat

```
ASSUNÇÕES (me corrija ou sigo):
1. … — recomendo … porque …
```

```
Q: <decisão>
RECOMENDO: <opção> — <1 linha>
(ok / outra?)
```

- “Tanto faz” → cravar a rec.
- Dúvida de intenção (quem/por quê/sucesso) → confiança caiu → `fluxline-interview`.

Vago → sucesso testável:

```
Pedido: "dashboard mais rápido"
Sucesso (rec): LCP < 2.5s 4G · dados < 500ms · CLS < 0.1
→ Esses alvos?
```

---

## 4 — Escrever (mostrar no chat; ainda **não** gravar disco)

| Faça | Não faça |
|---|---|
| Só o **decidido** | Encher template |
| Legível em poucos minutos | Mural de user stories |
| Fora **real** (o que se recusou) | Fora genérico |
| Módulo / contrato estável | Lista de paths que vão stale |
| Teste de comportamento externo | Teste de miolo |
| Delta no repo | Boilerplate greenfield |

Ordem: Problema → Solução → Entra/**Fora** → Aceite → Sucesso → Decisões de implementação → Seams/como provar → Boundaries.

### Template

Omita o que não se aplica. Não invente.

```markdown
# Spec: [nome curto]

## Problema
[2–4 frases — quem sofre a dor]

## Solução
[2–4 frases — o que passa a existir]

## Escopo
- Entra: …
- Fora: …

## Aceite
- [ ] …    # observável; poucos e afiados

## Sucesso
- …        # “pronto” testável, não adjetivo

## Decisões de implementação
- Módulos / limites: …
- Contratos (API, schema, eventos): …
- Arquitetura fechada: …
# Sem diff. Snippet só se carregar decisão acordada (tipo, state machine).

## Como provar
- Seams acordados: …
- Comportamento externo; prior art no repo: …
- Manual: …

## Boundaries (desta entrega)
- Always: …
- Ask first: …
- Never: …
```

Apresente o rascunho no chat e peça **sim no conteúdo**:

```
Fecha assim a spec? (sim / não / ajustar)
```

**Não grave** `spec-fase-…` enquanto não houver sim. Disco com spec rejeitada = defeito de processo.

---

## 5 — Aprovar → só então salvar

1. **Sim** no conteúdo da spec (ajuste no chat até fechar).
2. Garantir pasta na **raiz do workspace**:
   - Preferir: `bash <pack>/skills/fluxline-build/scripts/fluxline-run.sh spec` — cria a pasta e devolve `next_n`
   - Sem bash: criar `docs/fluxline/spec/` na mão
3. Grave `docs/fluxline/spec/spec-fase-N-<slug>-<nome-curto>.md`
4. Path + id na resposta

| | |
|---|---|
| Id | `N-<slug>-<nome-curto>` |
| Com interview | mesmo id |
| Sem interview | `N` = `next_n` do script (ou próximo em `docs/fluxline/{interview,spec,plan,review}/`) |

Salvar **sem perguntar** “posso salvar?” — o gate é o **sim no conteúdo**, não permissão de I/O.

---

## 6 — Handoff e parar

1. Path + id  
2. Próximo = **`fluxline-plan`** (`plan-fase-…` + `todo-fase-…`, mesmo id)  
3. **PARE** — zero grafo, todo, task, código  

---

## Anti-skip

| Racionalização | Realidade |
|---|---|
| "50% mas escrevo" | Interview. |
| "Open Questions no final" | Q + rec agora. |
| "Inventei o módulo pra completar" | Defeito. Só o decidido. |
| "Pulo seams" | Seams antes da prosa. |
| "Já deixo o plan" | Spec termina **antes** do plan. |
| "Gravo e peço sim depois" | Sim **antes** de gravar. Disco = aprovado. |
| "Pergunto se salva" | Após sim, salva. |

**Red flags:** confiança baixa; inventar seção; Open Questions; plan/todo/código nesta run; seams sem ok; Fora vazio; gravar sem sim; handoff sem `fluxline-plan`.

---

## Verificação

- [ ] CONFIDENCE; se baixo → interview
- [ ] Seams topados
- [ ] Só decisões reais; rascunho no chat
- [ ] **Sim do humano no conteúdo**
- [ ] `docs/fluxline/spec/spec-fase-N-<slug>-<nome-curto>.md` salvo **só depois** do sim
- [ ] Sem plan/todo/código
- [ ] Próximo = `fluxline-plan`; **PARE**
