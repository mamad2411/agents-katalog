---
name: fluxline-plan
description: Quebra a spec em tasks ordenadas e grava plan+todo em docs/fluxline/plan. Use com spec-fase aprovada. Não use sem spec (mande pra fluxline-spec), nem typo/1 arquivo óbvio, nem para escrever código. Terceira porta da cadeia fluxline-*.
---

# Fluxline Plan

Decomponha a **spec** em tasks pequenas, verificáveis, com aceite explícito. Toda task cabe em **uma sessão focada** (implementar + testar + verificar).

| | |
|---|---|
| **Começa** | Spec em disco (`spec-fase-…`) lida e suficiente para fatiar |
| **Termina** | Plan+todo **aprovados (sim)** + **salvos** + handoff **`fluxline-build`** |

**Não faz:** interview, spec, código, review.  
Cadeia: `interview → spec → **plan** → build → review`.

**Discovery:** esta cadeia é `fluxline-*` do começo ao fim — não substituir porta por skill de outro pack.

DoD (barra de “pronto” em cima do aceite): fonte canônica `../fluxline-build/references/definition-of-done.md` (a partir desta skill) ou `skills/fluxline-build/references/definition-of-done.md` (raiz do pack) (pointer local em `references/definition-of-done.md`).

---

## 0 — Gate

1. Localize `docs/fluxline/spec/spec-fase-N-<slug>-<nome-curto>.md` (path dado pelo humano ou o mais recente da ideia **já aprovada**).
2. **Sem spec** → **para**. Recomende `fluxline-spec` (1–2 linhas). Não invente plan a partir de chat solto.
3. Spec existe mas intenção/sucesso/fora ainda frouxos → **não complete o plan no chute**:
   - buraco de **intenção** → devolve `fluxline-interview` / `fluxline-spec`
   - buraco pontual de desenho → **Q + RECOMENDO** no chat; fecha antes de gravar

```
Q: <decisão que trava o fatiamento>
RECOMENDO: <opção> — <1 linha>
(ok / outra?)
```

Proibido seção Open Questions no plan. Typo / uma linha óbvia → nem plan; só faça.

---

## 1 — Plan mode (só leitura)

Antes de gravar artefatos:

- Ler a **spec** (fonte) e trechos do codebase que ela toca
- Padrões existentes, dependências, riscos
- **Não escrever código**

---

## 2 — Grafo de dependências

O que depende do quê; ordem **bottom-up** (fundação primeiro):

```
schema / tipos base
    └── API / serviços
            └── client / UI
```

---

## 3 — Fatia vertical

Um caminho completo de valor por vez — não “todo DB, depois toda API, depois toda UI”.

**Ruim (horizontal):** schema inteiro → endpoints inteiros → UI inteira → “ligar”.  
**Bom (vertical):** “usuário cria conta” (schema+API+UI do registro) → “usuário faz login” → …

Cada task deixa o sistema **em estado usável/testável** naquele pedaço.

---

## 4 — Escrever tasks

Alvo: **S ou M**. L ou XL → quebrar.

| Size | Files | Exemplo |
|------|-------|---------|
| XS | 1 | Uma regra de validação |
| S | 1–2 | Um endpoint ou componente |
| M | 3–5 | Uma fatia de feature |
| L | 5–8 | Quebrar |
| XL | 8+ | Quebrar já |

Quebre se: >1 sessão focada; aceite não cabe em ≤3 bullets; 2+ subsistemas independentes; “e” no título.

### Estrutura de cada task

```markdown
## Task [N]: [título curto — verbo + outcome]

**O quê:** 1–3 frases do resultado.

**Aceite:**
- [ ] [condição testável]
- [ ] …

**Verificação:**
- [ ] Testes: [comando focado do repo]
- [ ] Build: [comando do repo]   # se aplicável
- [ ] Manual: [o que olhar]

**Deps:** Task … | nenhuma
**Arquivos prováveis:** `path/…` (módulo/área; não romance)
**Size:** XS | S | M
```

Aceite = “é a coisa certa?” (por task). Em cima disso vale a **Definition of Done** canônica.

---

## 5 — Ordem e checkpoints

1. Deps satisfeitas  
2. Cada task deixa sistema coerente  
3. Checkpoint a cada **2–3** tasks  
4. Alto risco **cedo** (fail fast)

```markdown
## Checkpoint: após Tasks 1–3
- [ ] Testes da fatia passam
- [ ] Build ok
- [ ] Fluxo central da fatia ok
- [ ] Review humano se a fatia for arriscada
```

---

## 6 — Dois artefatos (rascunho no chat; ainda **não** gravar)

| Arquivo | Papel |
|---|---|
| `plan-fase-N-<slug>-<nome-curto>.md` | Contexto: overview, decisões de ordem, grafo/fases, riscos, **índice** das tasks + checkpoints |
| `todo-fase-N-<slug>-<nome-curto>.md` | **Corpo** das tasks (estrutura do passo 4), na ordem de execução — o que o build consome task a task |

O plan **não** recopia o texto completo de cada task. O todo **não** reexplica a spec. Spec continua a fonte do “o quê”; plan/todo só fatiam.

### Template do plan

```markdown
# Plan: [nome curto]

## Overview
[1 parágrafo — o que esta entrega realiza, apontando a spec]

## Spec
`docs/fluxline/spec/spec-fase-N-<slug>-<nome-curto>.md`

## Ordem / fases
### Fase 1: …
- Tasks 1–2 (ver todo)
### Checkpoint: …
### Fase 2: …
…

## Riscos
| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| … | Alto/Méd/Baixo | … |

## Paralelização (se houver)
- Paralelo ok: …
- Sequencial: …
- Contrato primeiro, depois paralelo: …
```

### Template do todo

```markdown
# Todo: [nome curto]
# Spec/Plan id: N-<slug>-<nome-curto>

## Task 1: …
…
## Checkpoint: …
## Task 2: …
…
```

Apresente plan+todo (ou resumo + paths previstos) e peça:

```
Fecha assim ordem e escopo das tasks? (sim / não / ajustar)
```

**Não grave** `plan-fase-…` / `todo-fase-…` sem sim. Disco = aprovado.

---

## 7 — Aprovar → só então salvar

1. **Sim** no plan+todo (ordem e escopo).
2. Garantir pasta na **raiz do workspace**:
   - Preferir: `bash <pack>/skills/fluxline-build/scripts/fluxline-run.sh plan` — cria a pasta e devolve `next_n`
   - Sem bash: criar `docs/fluxline/plan/` na mão
3. Grave **os dois** arquivos com o **mesmo id da spec**
4. Paths + id na resposta

| | |
|---|---|
| Plan | `docs/fluxline/plan/plan-fase-N-<slug>-<nome-curto>.md` |
| Todo | `docs/fluxline/plan/todo-fase-N-<slug>-<nome-curto>.md` |
| Id | **igual** ao da `spec-fase-…` |
| Sem spec numerada | só se o humano mandar planejar avulso: `N` = `next_n` do script — preferível ter spec |

Salvar **sem perguntar** “posso salvar?” — o gate é o **sim no conteúdo**.

---

## 8 — Handoff e parar

1. Paths + id  
2. Próximo = **`fluxline-build`** (lê todo/plan/spec; mesmo id)  
3. **PARE** — zero implementação, zero “já faço a task 1”

---

## Paralelização (resumo)

- **Paralelo:** fatias independentes; testes de coisa já estável; docs  
- **Sequencial:** migrations, estado compartilhado, cadeia de deps  
- **Coordenar:** contrato de API primeiro, depois lados em paralelo  

---

## Anti-skip

| Racionalização | Realidade |
|---|---|
| "Sem spec, planejo do chat" | Gate: `fluxline-spec` primeiro. |
| "Open Questions no plan" | Q + rec agora, ou devolve spec. |
| "Task = implementar a feature" | Aceite + verificação ou não é task. |
| "Tudo XL, depois quebra" | Quebra **agora**. |
| "Descubro codando" | Por isso existe plan. |
| "Já implemento a 1ª" | Handoff `fluxline-build`. |
| "Gravo e peço sim depois" | Sim **antes** de gravar. |
| "Pergunto se salva" | Após sim, salva os dois. |

**Red flags:** plan sem spec; tasks sem aceite/verificação; só horizontal; sem checkpoint; Open Questions no `.md`; código nesta run; um arquivo só (falta plan ou todo); gravar sem sim; handoff sem `fluxline-build`.

---

## Verificação

- [ ] Spec lida; id reutilizado
- [ ] Buracos fechados no chat (ou devolvidos à spec/interview)
- [ ] Fatias verticais; deps ordenadas; size ≤ M (L+ quebrado)
- [ ] Toda task: aceite + verificação
- [ ] Checkpoints a cada 2–3 tasks
- [ ] **Sim do humano** em ordem/escopo
- [ ] `plan-fase-…` + `todo-fase-…` salvos **só depois** do sim
- [ ] Próximo = `fluxline-build`; **PARE**
