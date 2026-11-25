---
name: fluxline-interview
description: Use sempre que o usuário for explicar uma implementação nova ou pedir para ser entrevistado (me entrevista, grill me, stress-test, ideate). Também quando o pedido de feature/mudança estiver vago ou convencional. Não use em typo/rename, pergunta de informação, pedido explícito de velocidade, ou contexto sem usuário (CI/loop). Primeira porta da cadeia fluxline-*.
---

# Fluxline Interview

Extrai a **intenção real** (uma pergunta por vez) e grava artefato em disco para a spec. Duas fases: Interview (F1) e Refine (F2).

| | |
|---|---|
| **Começa** | Pedido vago/convencional, falta quem/por quê/sucesso/restrição, ou invocação (“me entrevista”, “ideate”, …) |
| **Termina** | Restate (F1) ou one-pager (F2) **salvo** após sim + handoff **`fluxline-spec`** — zero spec/plan/código |

**Não faz:** spec, plan, todo, tasks, código, review.  
Cadeia: `**interview** → spec → plan → build → review`.

**Discovery:** esta cadeia é `fluxline-*` do começo ao fim — não substituir porta por skill de outro pack.

---

## 0 — Gate

| | Ação |
|---|---|
| Typo / rename / inequívoco auto-contido / velocidade pedida / pergunta de info | **Não** usar esta skill |
| Já ≥~95% e restate fechável sem chute | Restate → sim → salvar (pode pular perguntas) |
| Falta quem, por quê, sucesso ou restrição; ou convenção no lugar de outcome | **Fase 1** |
| Intenção ok, forma da solução não (“quero X, não sei como escopar”) | **Fase 2** (após F1 ou conceito grosso) |
| CI / loop / agendado sem usuário vivo e pedido subespecificado | **Bloquear** — não chute |

```
HIPÓTESE: …
CONFIDENCE: ~N% — falta: …
```

Abaixo de ~70%: motivo breve na mesma linha. Número alto sem prever as próximas 3 reações do usuário = número errado.

---

## Por que existe

O que se pede e o que se quer divergem: "dashboard" costuma ser convenção, não solução; "mais rápido" sem número. O momento mais barato de fechar esse gap é **antes** de spec, plan ou código.

- **Fase 1 — Interview:** intenção real, uma pergunta por vez, confiança explícita.
- **Fase 2 — Refine:** intenção confirmada mas sem forma → variações → uma direção.

Maioria dos pedidos: só Fase 1. Fase 2 quando o destino existe e a rota não.

---

## Fase 1: Interview

### Passo 1 — Hipótese + confiança

Antes de perguntar, uma frase + número honesto (0–100%):

```
HIPÓTESE: Você quer um jeito de responder "como estamos?" no standup; "dashboard" foi a convenção que veio à mente.
CONFIDENCE: ~30% — falta: para quem, o que "métricas" significa aqui, o que sucesso parece ser
```

### Passo 2 — Uma pergunta por vez, com GUESS

```
Q: <uma pergunta focada>
GUESS: <hipótese da resposta + raciocínio que a produziu>
```

Espere a reação antes da próxima.

- **Uma por vez (não lote):** a 3ª pergunta quase sempre depende da 1ª.
- **GUESS anexado:** reagir a um chute errado é mais fácil que inventar do zero. Fique **visivelmente** disposto a estar errado (mitiga concordância educada).

### Passo 3 — "Quer" vs "deveria querer"

Best-practice theater, deferência à convenção, buzzword como meta:

> *Se você não tivesse que justificar isso para ninguém, o que você realmente queria?*

### Passo 4 — Restate (curto, legível, humano)

Quando ≥~95% (ou quando for fechar), **não escreva relatório**. Alguém precisa ler em ~10 segundos.

- **Só o bloco abaixo** — sem preâmbulo
- **1 frase curta por linha** (máx. ~15 palavras)
- **Fora** é inegociável
- Tom de conversa, não de PRD

```
Entendi assim:

- O quê:     <resultado, não a feature>
- Pra quem:  <quem se beneficia>
- Por quê:   <o que mudou / por que agora>
- Sucesso:   <como sabemos que funcionou — observável>
- Limite:    <restrição que manda>
- Fora:      <o que explicitamente não entra>

Fecha assim? (sim / não / ajustar)
```

### Passo 5 — Sim explícito

Gate = "sim" claro. Não enrole pedindo confirmação campo a campo.

| Resposta | O que é | O que fazer |
|---|---|---|
| "o que você achar melhor" | delegação | **2 opções concretas**, uma linha cada |
| "parece bom" | ambíguo | "O que mudaria?" |
| "beleza, bora" | saída educada frequente | "Sim no recap acima, ou quer ajustar algo?" |
| silêncio + "ok, pode começar" | desistência, não convergência | não tratar como sim |

### Parada ~95%

Feito quando: *Consigo prever a reação do usuário às próximas três perguntas?* → **restate curto e para**.  
Várias rodadas e ainda imprevisível = diga em uma linha e pergunte se recua.

### Saída da Fase 1

**Intenção confirmada** = restate + sim explícito + **arquivo em disco**.

Chat sozinho **não conta**. Depois do sim, **salve na hora** — não pergunte:

1. Garantir pasta (ver **Artefato em disco**)
2. Grave o restate em `docs/fluxline/interview/interview-fase-N-<slug>-<nome-curto>.md` (só o bloco do Passo 4)
3. Path + id `N-<slug>-<nome-curto>`

- Concreto → handoff `fluxline-spec`
- Direção sem forma → Fase 2 (mesmo id; arquivo pode ser substituído pelo one-pager)

---

## Fase 2: Refine

Intenção confirmada (F1) ou conceito grosseiro entregue direto → abrir → convergir.

### Passo 1 — Expandir (divergente)

1. Restate como **How Might We** nítido (problema, não solução embutida).
2. **3–5** perguntas de afiar (máx.): quem, sucesso, restrições, o que já tentou, por que agora. Use ferramenta de pergunta estruturada do host se houver. Não avance sem quem + sucesso.
3. **5–8 variações** (qualidade > quantidade), lentes: inversão, remoção de restrição, mudança de público, combinação, simplificação 10×, versão 10×, lente de especialista.

Em codebase: ancorar variações no que existe. Travado → `references/frameworks.md` (seletivo).

### Passo 2 — Avaliar e convergir

1. Agrupar o que ressoou em **2–3 direções distintas**.
2. Stress-test (`references/refinement-criteria.md`): valor, viabilidade, diferenciação.
3. **Assunções escondidas** por direção (o que aposta, o que mata se falso, o que ignora agora e por quê).

Opinião com recomendação — não menu neutro. Direção fraca: diga com gentileza.

### Passo 3 — One-pager (ainda legível)

**Só o decidido.** Bloqueio real fecha no chat com Q + RECOMENDO **antes** de salvar.  
**Proibido** seção “Em aberto” / Open Questions / lista de pendências no `.md`.

```markdown
# [Nome curto]

## Problema
[HMW em 1 frase]

## Direção
[2–4 frases: o que e por quê. Sem ensaio.]

## Apostas a validar
- [ ] [assunção] — [como testar em 1 linha]

## MVP
- Entra: [lista curta]
- Fica de fora: [aponta pro Not Doing]

## Not Doing
- [coisa tentadora] — [motivo em 1 frase]
```

**Not Doing é a parte mais valiosa** — específica, justificada. Máx. ~5 itens.

Apresente o one-pager no chat e peça o mesmo gate da F1:

```
Fecha assim? (sim / não / ajustar)
```

**Não grave** enquanto não houver sim no one-pager. Ajuste no chat até fechar.

### Saída da Fase 2

One-pager com direção, assunções e Not Doing + **sim explícito** → **salve na hora** no mesmo path `interview-fase-N-<slug>-<nome-curto>.md` (substitui o restate da F1 se existir). Sem perguntar “posso salvar?”.  
`fluxline-spec` lê **o arquivo**, não o chat.

Calibração: `references/examples.md` (só na F2, sob demanda).

---

## Artefato em disco (obrigatório)

A interview **termina em arquivo**. Chat sem `.md` = incompleta. **Salve sempre após o sim; nunca pergunte se quer salvar.**

### Garantir pasta

Na **raiz do workspace do app** (onde moram o código e `docs/` — não o pacote da skill):

1. **Preferir (tem bash):** `bash <pack>/skills/fluxline-build/scripts/fluxline-run.sh interview`  
   Script único do pack (canônico junto da DoD). Cria a pasta **e** devolve `next_n` — use esse `N` no id, em vez de contar arquivo a olho.
2. **Sem bash:** criar `docs/fluxline/interview/` na mão (`mkdir` / `New-Item -ItemType Directory -Force`) e calcular `N` pela tabela abaixo.

O script resolve o workspace pelo git root de `$PWD` — nunca o path de install da skill.

| | |
|---|---|
| Path | `docs/fluxline/interview/interview-fase-N-<slug>-<nome-curto>.md` |
| Prefixo | `interview-fase-` (cadeia: `spec-fase-`, `plan-fase-`/`todo-fase-`, `review-fase-`) |
| Id da run | `N-<slug>-<nome-curto>` — reutilizado na cadeia inteira |
| `N` | `next_n` do script; sem bash, próximo após o maior `N` em `docs/fluxline/{interview,spec,plan,review}/` (ou 1) |
| `<slug>` | tema/escopo em kebab-case |
| `<nome-curto>` | rótulo da peça em kebab-case |
| Quando | logo após o **sim** (F1 restate **ou** F2 one-pager) |
| Conteúdo F1 | só o restate curto |
| Conteúdo F2 | one-pager no mesmo id — **sem** Em aberto / Open Questions |

Ex.: `docs/fluxline/interview/interview-fase-3-restaurantes-motor-regulares.md`

---

## Handoff — próximo = `fluxline-spec`

Cadeia fixa: **interview → spec → plan → build → review**. Esta skill **não** planeja, implementa nem revisa.

Depois de salvar (F1 ou F2), na **mesma mensagem de fechamento**:

1. Path do artefato + id `N-<slug>-<nome-curto>`
2. Próximo = **`fluxline-spec`**, lendo esse arquivo e reusando o id
3. **PARE** — zero rascunho de spec, plan, tasks ou código

| Skill | Quando |
|---|---|
| `fluxline-spec` | **Imediatamente depois** — lê `interview-fase-…` |
| `fluxline-plan` | Só depois da spec aprovada e salva |
| `fluxline-build` | Só depois do plan |
| `fluxline-review` | Pedido de revisão ou handoff pós-build |

---

## Anti-skip

| Racionalização | Realidade |
|---|---|
| "Já está claro o suficiente" | Sem outcome em uma frase agora → F1 Passo 1 |
| "Perguntar demais gasta tempo" | 4–6 perguntas focadas ≪ construir a coisa errada |
| "Descubro construindo" | Custo de mudança com código é ~10× o de agora |
| "'O que você achar' = eu decido" | Delegação. Duas opções concretas. |
| "Várias opções pra ele escolher" | Ainda não sabe → **estreite**, não alargue |
| "Já conversamos, entendi" | Prevê as próximas 3 reações? Se não, não entendeu |
| "Já sei a direção, pulo pro one-pager" | Sem assunções expostas = preferência, não direção |
| "Quanto mais ideias melhor" | 5–8 consideradas > 20 rasas |
| "Só falei no chat, não preciso de arquivo" | Spec/plan leem disco. Sem `.md` a interview não terminou. |
| "Pergunto se quer salvar" | Não. Salva após sim. Informa o path. |
| "F2 one-pager sem Fecha assim?" | Mesmo gate da F1. Sim **antes** de gravar. |
| "Em aberto no one-pager" | Fecha no chat; artefato só decidido. |

**Red flags:** ≥3 perguntas numa mensagem; pergunta sem GUESS; aceitar "o que achar" como terminal; spec/plan/tasks antes do sim; pular Fora / Not Doing; 20+ variações rasas; zero assunções antes de cravar direção; restate/one-pager longo demais; **fechar só no chat**; **perguntar se pode salvar**; **Open Questions / Em aberto no `.md`**.

---

## Verificação

- [ ] Gate §0 respeitado (não usou skill à toa; não pulou com pedido vago)
- [ ] CONFIDENCE honesta; F1 com 1Q+GUESS por vez até ~95%
- [ ] Restate curto + **sim explícito** (F1) **ou** one-pager F2 + **sim explícito** (Not Doing e assunções)
- [ ] Artefato **sem** Em aberto / Open Questions
- [ ] `docs/fluxline/interview/interview-fase-N-<slug>-<nome-curto>.md` na raiz do workspace
- [ ] Path + id na resposta; próximo = `fluxline-spec`; **PARE**
