---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
metadata:
  maintained_by: vendored (third-party) — upstream mattpocock/skills, MIT
  upstream: https://github.com/mattpocock/skills
  upstream_path: skills/productivity/handoff/SKILL.md
  upstream_sha: 6654f6b60cd9d5be8b54c6fafe44346dabeb3b76
  license: MIT (ver LICENSE nesta pasta)
  vendored_at: "2026-08-28"
  fork: "1 linha — destino do arquivo: `.claude/.cache/handoff/` em vez do temp do SO"
  version: "1.0.0"
---

<!--
  Procedimento VENDORIZADO do upstream (skill `handoff`, MIT © 2026 Matt Pocock), com UM fork
  declarado e um só — está no `metadata` acima e é esta linha:
    upstream: "Save to the temporary directory of the user's OS - not the current workspace."
    aqui:     `.claude/.cache/handoff/`
  Motivo: o temp do SO é o modo de falha que o `SAIDA_DE_SUBAGENTE_NAO_PERSISTE` (v0.10.21)
  fechou neste scaffold — "o dado mais caro é o que não sobrevive". O `.cache/` já é gitignored
  (`.claude/.gitignore`), então o documento sobrevive à sessão sem entrar em diff de PR.
  O resto do corpo é literal: mudança de método sobe para o upstream, não é editada aqui.

  SEM `disable-model-invocation` (upstream o declara): medido em 2026-08-28 (CLI 2.1.251, com
  controle positivo) que o campo faz o harness RECUSAR `Skill(...)` vindo de command — e o
  `/orchestrate` chama esta skill no seu handoff externo.
-->

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to `.claude/.cache/handoff/HANDOFF_<slug>_<YYYY-MM-DD>.md` (already gitignored) - not the OS temp directory.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

---

## Quando isto vale, e quando `/compact` resolve melhor

O que o documento compra é **portabilidade**, não compressão. Quatro situações o justificam — todas
têm algo **viajando**:

| Situação | Por que um arquivo |
|---|---|
| Trocar de harness (Claude → Codex/Antigravity) | o novo harness não enxerga o contexto do antigo |
| Trocar de diretório ou repo | o caso comum é um diretório de protótipo |
| Passar o trabalho a um colega | ele precisa de algo legível, fora da sua sessão |
| Forkar uma side task **sem** encerrar a sua | você segue; um segundo agente leva a cópia do contexto |

**Nada viajando → não é handoff.** Mesma sessão, mesmo diretório, fim de fase: o artefato da fase
(`DEFINE`/`DESIGN`/`BUILD_REPORT`) já é a passagem, e compactar resolve o resto.

**No ciclo SDD deste projeto:** o [`/orchestrate`](../../commands/orchestrate.md) chama esta skill
quando emite **handoff externo** (plano grande/independente, ou troca de chat) — antes ele apenas
avisava o humano *"rode em novo chat"* e nada acompanhava a instrução.

## Chamada direta e rotas vizinhas

`/handoff <para que serve a próxima sessão>` roda **esta skill** (skill vence command homônimo).
Sem argumento, escreva o documento para *"continuar de onde parei"* e diga isso no texto — não
invente um objetivo que o usuário não declarou.

Não é handoff:
- Coordenar com outra sessão **ativa no mesmo projeto** → `/peers` (se o perfil o entregar), que é
  presença e recado, não documento.
- Encerrar uma feature → [`/ship`](../../commands/ship.md): o `SHIPPED` é o registro do que fechou,
  não do que segue.
