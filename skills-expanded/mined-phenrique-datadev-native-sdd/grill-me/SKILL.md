---
name: grill-me
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
argument-hint: "<o plano, decisão ou ideia a ser interrogado>"
metadata:
  maintained_by: vendored (third-party) — upstream mattpocock/skills, MIT
  upstream: https://github.com/mattpocock/skills
  upstream_path: skills/productivity/grilling/SKILL.md
  upstream_sha: 6654f6b60cd9d5be8b54c6fafe44346dabeb3b76
  license: MIT (ver LICENSE nesta pasta)
  vendored_at: "2026-08-28"
  version: "1.0.0"
---

<!--
  Procedimento VENDORIZADO, texto literal do upstream (skill `grilling`, MIT © 2026 Matt Pocock).
  Não reescreva o corpo: mudança de método sobe para o upstream ou vira fork declarado aqui.
  O frontmatter é NOSSO e difere do upstream em dois pontos, ambos deliberados:
    1. `name: grill-me` — upstream separa o wrapper `grill-me` do corpo `grilling`; aqui o alias
       explícito do usuário é o próprio `/grill-me` que esta skill cria (skill vence command
       homônimo — por isso não há `commands/grill-me.md`), então uma skill só.
    2. SEM `disable-model-invocation` — medido em 2026-08-28 (CLI 2.1.251, projeto isolado, com
       controle positivo): com o campo, o harness RECUSA `Skill(skill: "...")` feito pelo modelo.
       Como `/setup`, `/brainstorm`, `/define` e `/train-kb` chamam esta skill, o campo a tornaria
       inalcançável exatamente nos quatro pontos que a justificam.
-->

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

---

## Onde este projeto chama esta skill

Quatro pontos a chamam por **predicado**, não por lembrança (ver cada command):

| Ponto | Dispara quando |
|-------|----------------|
| [`/setup`](../../commands/setup.md) | o `project-context.md` está `status: template` — o insumo de todo o resto ainda não existe |
| [`/brainstorm`](../../commands/brainstorm.md) | sempre: é o passo de perguntas da fase 0 |
| [`/define`](../../commands/define.md) | o **Clarity Score** fica abaixo de 12/15 |
| [`/train-kb`](../../commands/train-kb.md) | antes do Passo 1, quando o plano de ondas sairia de inferência sobre o contexto |

## Fato do ambiente: subagente só para busca ampla

O corpo upstream manda despachar um sub-agente para todo fato do ambiente. Aqui, fato que sai de
uma leitura ou de um grep (um campo do `project-context.md`, uma flag no `-Help`, um arquivo citado)
você lê direto: o subagente parte sem o contexto da conversa e custa mais que a resposta. Despache
quando a busca varrer muitos arquivos, e aí sem bloquear a rodada, como o corpo diz.

## Chamada direta

`/grill-me <plano, decisão ou ideia>` roda **esta skill** (skill vence command homônimo). Sem
argumento, entreviste sobre **o que estiver em pauta na conversa**; se não houver nada em pauta,
pergunte o que interrogar antes de abrir a primeira rodada.

Não use para:
- Decisão **já tomada** que só precisa ser explicada ou revisada → `/decision-preview` (comparar
  variantes ainda abertas) ou revisão normal.
- Pergunta cuja resposta está **no repositório** — descubra em vez de interrogar o usuário.
- Tarefa pequena e reversível → [`/dev`](../../commands/dev.md). Interrogatório cobra tempo do
  usuário; gaste onde errar dói.
